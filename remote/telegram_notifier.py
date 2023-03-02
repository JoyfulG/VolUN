"""
A telegram bot that helps to monitor the process of data collection on the server.
"""

from functools import wraps

import telebot

import database
import server_config as sc

bot = telebot.TeleBot(sc.tg_bot_token)

approved_users = [sc.tg_bot_creator]


def private_access(function):
    """A decorator that verifies if a user is authorized to use a command. Must be put after message_handler."""
    @wraps(function)
    def wrapper(message, *args, **kwargs):
        if message.chat.id not in approved_users:
            bot.send_message(message.chat.id, "Not allowed.")
        else:
            return function(message, *args, **kwargs)

    return wrapper


def send_notification(msg_text):
    """Sends a message to the bot creator."""
    msg_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    bot.send_message(sc.tg_bot_creator, msg_text, parse_mode='HTML')


@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = 'Hi!\nThis bot is a part of an educational project. Most of the bot commands are available to ' \
                   'approved users only. If you are a random stranger, pass by. If you are supposed to have access ' \
                   'but encounter issues, contact the bot owner.\nText /help to see the list of commands.'
    bot.send_message(message.chat.id, welcome_text)


@bot.message_handler(commands=['help'])
def show_commands(message):
    commands_text = '<b>Public commands:</b>\n' \
                    '/mytgid - Returns your Telegram User ID\n' \
                    '\n<b>Private commands:</b>\n' \
                    '/last - Shows the last error recorded into the database that occurred while ' \
                    'treating an assignment\n' \
                    '/day - Lists the identifiers of assignments that were not saved into the database ' \
                    'over the last 24 hours\n' \
                    '/week - Does the same but the period is 7 days\n' \
                    '/month - Does the same but the period is 30 days\n' \
                    '/detail - Allows to search for certain errors in the errors log by assignment identifiers'
    bot.send_message(message.chat.id, commands_text, parse_mode='HTML')


@bot.message_handler(commands=['mytgid'])
def my_tg_id(message):
    """Replies with the sender's telegram user ID."""
    bot.send_message(message.chat.id, message.chat.id)


@bot.message_handler(commands=['last'])
@private_access
def last_recorded_error(message):
    """Sends the last record from the errors_log database table."""
    last_error = database.last_inner_error()
    err_type = last_error['err_type'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    err_body = last_error['err_body'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    last_error_text = f'<b>Error DB ID:</b> {last_error["err_id"]}\n' \
                      f'<b>Date:</b> {last_error["current_datetime"]}\n' \
                      f'<b>Assignment:</b> https://app.unv.org/opportunities/{last_error["failed_doarequestno"]}\n' \
                      f'<b>{err_type}:</b> {err_body}\n'
    bot.send_message(message.chat.id, last_error_text, parse_mode='HTML')


@bot.message_handler(commands=['day', 'week', 'month'])
@private_access
def show_failed_records_identifiers(message):
    """Sends a list of the identifiers of assignments that were not recorded into the database due to an error.
    Sent information is sorted by day of an error occurrence. Based on the passed command, selects among three
    time intervals."""
    period = 1
    if message.text == '/week':
        period = 7
    elif message.text == '/month':
        period = 30
    errors_period = database.failed_records_identifiers(period)
    errors_total = errors_period.pop('Total')[0]
    errors_period_text = ''
    for date, identifiers in errors_period.items():
        identifiers_unpacked = '\n'.join(identifiers)
        temp_text = f'\n<b><u>{date}:</u></b>\n{identifiers_unpacked}\n'
        errors_period_text += temp_text

    errors_period_text += f'\n<b>Total:</b> {errors_total}'
    if len(errors_period_text) < 4000:
        bot.send_message(message.chat.id, errors_period_text, parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "Too many results. Can't send. Please choose a shorter time interval.")


@bot.message_handler(commands=['detail'])
@private_access
def start_show_details(message):
    """Starts the search of specific records in the errors log. Prompts an input in a particular format and passes
    it to the show_details function."""
    start_detailing_text = "Specify the errors you'd like to retrieve in the following format:\n" \
                           "<i>XXXXXXXXXXXXXXXX YYYY-MM-DD</i>\n" \
                           "where <i>XXXXXXXXXXXXXXXX</i> - a 16-digit assignment identifier,\n" \
                           "<i>YYYY-MM-DD</i> - optional date parameter; if omitted, the last error with the " \
                           "passed identifier is returned.\nIf you are retrieving several records, group each " \
                           "request on a new line. No more than 8 requests can be passed at a time.\n" \
                           "Example:\n1234567898765432 2011-06-23\n5678912345678912\n9876543212345678 2009-11-01\n" \
                           "Text /cancel to abort the command execution."
    bot.send_message(message.chat.id, start_detailing_text, parse_mode='HTML')
    bot.register_next_step_handler(message, show_details)


def show_details(message):
    """Passes the received search parameters to the search function and replies with the result."""
    queries_split = message.text.split('\n')
    if message.text == '/cancel':
        bot.send_message(message.chat.id, 'Canceled.')
    elif len(queries_split) > 8:
        too_many_records_text = 'Cannot request more than 8 records at a time. Try again. Text /cancel to abort ' \
                                'the command execution.'
        bot.send_message(message.chat.id, too_many_records_text)
        bot.register_next_step_handler(message, show_details)
    else:
        results = database.show_details(queries_split)
        details_text = ''
        for record in results:
            err_type = record['err_type'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            err_body = record['err_body'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            details_text += f'\n<b>Error DB ID:</b> {record["err_id"]}\n' \
                            f'<b>Date:</b> {record["current_datetime"]}\n' \
                            f'<b>Assignment:</b> https://app.unv.org/opportunities/{record["failed_doarequestno"]}\n' \
                            f'<b>{err_type}:</b> {err_body}\n'
        if len(details_text) < 4000:
            bot.send_message(message.chat.id, details_text, parse_mode='HTML')
        else:
            result_too_long_text = 'The resulting message is too long and cannot be sent. Please request less ' \
                                   'records. Text /cancel to abort the command execution.'
            bot.send_message(message.chat.id, result_too_long_text)
            bot.register_next_step_handler(message, show_details)


if __name__ == '__main__':
    bot.infinity_polling()
