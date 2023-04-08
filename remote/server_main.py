"""
This is the main server module. Intended to be permanently executed.
"""

import time

import schedule
from requests.exceptions import ConnectionError

import collector
import database
import telegram_notifier as tgn


def daily_collector():
    """
    Main function designed to be called once a day on the server. Calls other functions related to the information
    collection and saving. Intercepts major errors and sends a notification via Telegram.
    """
    try:
        assgns_number = collector.number_of_assignments()
        time.sleep(2)
        list_of_identifiers = collector.collect_all_identifiers(assgns_number)
        idntfs_num = len(list_of_identifiers)  # Unlike assgns_number, list_of_identifiers has the "phantom" excluded
        recorded_assgns = database.database_filler(list_of_identifiers)
        if idntfs_num != recorded_assgns:
            inner_error_message = f'Some assignments were not saved into the database.\n' \
                                  f'Total number of assignments: <b>{idntfs_num}</b>\n' \
                                  f'Successfully saved: <b>{recorded_assgns}</b>\n' \
                                  f'Failed: <b>{idntfs_num - recorded_assgns}</b>'
            tgn.send_notification(inner_error_message)
    except ConnectionError:
        conn_message = "Connection error occurred. The database hasn't been updated today."
        tgn.send_notification(conn_message)
    except Exception as outer_ex:
        unexp_err_type = type(outer_ex).__name__
        unexp_err_body = outer_ex
        unexp_error_message = "Unexpected error occurred. The database hasn't been updated today.\n" \
                              f"<b>{unexp_err_type}</b>:\n{unexp_err_body}"
        tgn.send_notification(unexp_error_message)


if __name__ == '__main__':
    schedule.every().day.at('19:30:00').do(daily_collector)
    while True:
        schedule.run_pending()
        time.sleep(1)
