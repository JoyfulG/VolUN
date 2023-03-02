"""
Everything that employs database connection on the server is stored in this module.
"""

import time
import datetime  # Required in the for-loop of the show_errors definition.
from collections import defaultdict

import pymysql

import collector
import server_config


def connection_info():
    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user=server_config.db_server_user,
        password=server_config.db_server_pwd,
        database=server_config.db_name,
        cursorclass=pymysql.cursors.DictCursor)

    return connection


def database_filler(identifiers_list):
    """
    Primary function to interact with the database in terms of information gathering. Connects to the database and
    inserts collected information into the tables.
    :param identifiers_list: A list of identifiers of assignments that will be recorded into the database.
    :type identifiers_list: list
    :return: Number of assignments successfully recorded into the database.
    :rtype: int
    """
    connection = connection_info()
    with connection:
        successfully_added = 0
        insert_query_1 = 'REPLACE INTO assignments SET title=%s, doarequestno=%s, isonsite=%s, host_entity=%s, ' \
                         'territory=%s, duration=%s, extension=%s, publish_date=%s, assgn_expires=%s, ' \
                         'start_date=%s, vol_category=%s, min_age=%s, max_age=%s, ' \
                         'ed_lvl=%s, ed_specs=%s, years_of_xp=%s, field_of_xp=%s'
        insert_query_2_1 = 'INSERT INTO dutystations SET station=%s ON DUPLICATE KEY UPDATE station=station'
        insert_query_2_2 = 'INSERT INTO assignments_dutystations SET ' \
                           'assgn_id=(SELECT assgn_id FROM assignments WHERE doarequestno=%s), ' \
                           'ds_id=(SELECT ds_id FROM dutystations WHERE station=%s), ' \
                           'assgns_per_station=%s ON DUPLICATE KEY UPDATE assgns_per_station=assgns_per_station'
        insert_query_3_1 = 'INSERT INTO languages SET lang=%s ON DUPLICATE KEY UPDATE lang=lang'
        insert_query_3_2 = 'INSERT INTO assignments_languages SET ' \
                           'assgn_id=(SELECT assgn_id FROM assignments WHERE doarequestno=%s), ' \
                           'lang_id=(SELECT lang_id FROM languages WHERE lang=%s), ' \
                           'level=%s, ' \
                           'isrequired=%s ON DUPLICATE KEY UPDATE level=level'
        for identifier in identifiers_list:
            time.sleep(3)
            try:
                ai = collector.assignment_info(identifier)
                values_1 = (ai['title'], ai['doarequestno'], ai['isonsite'], ai['host_entity'], ai['territory'],
                            ai['duration'], ai['extension'], ai['publish_date'], ai['assgn_expires'], ai['start_date'],
                            ai['vol_category'], ai['min_age'], ai['max_age'], ai['ed_lvl'], ai['ed_specs'],
                            ai['years_of_xp'], ai['field_of_xp'])
                with connection.cursor() as cursor:
                    cursor.execute(insert_query_1, values_1)
                    for station, assgns_per_station in ai['dutystations'].items():
                        values_2_1 = (station,)
                        values_2_2 = (ai['doarequestno'], station, assgns_per_station)
                        cursor.execute(insert_query_2_1, values_2_1)
                        cursor.execute(insert_query_2_2, values_2_2)
                    for lang, properties in ai['languages'].items():
                        values_3_1 = (lang,)
                        values_3_2 = (ai['doarequestno'], lang, properties['level'], properties['isrequired'])
                        cursor.execute(insert_query_3_1, values_3_1)
                        cursor.execute(insert_query_3_2, values_3_2)
                    connection.commit()
            except Exception as inner_ex:
                err_type = type(inner_ex).__name__
                err_body = inner_ex
                errs_log_insert_query = 'INSERT INTO errors_log SET err_type=%s, err_body=%s, ' \
                                        'failed_doarequestno=%s, current_datetime=NOW()'
                err_values = (err_type, err_body, identifier)
                with connection.cursor() as cursor:
                    cursor.execute(errs_log_insert_query, err_values)
                    connection.commit()
                continue

            successfully_added += 1

    return successfully_added


def last_inner_error():
    """Returns the last record from the errors_log database table."""
    connection = connection_info()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM errors_log ORDER BY err_id DESC LIMIT 1')
            last_err = cursor.fetchone()

    return last_err


def failed_records_identifiers(period):
    """
    Collects all records from the failed_doarequestno column of the errors_log database table over a time interval.
    :param period: A period of time back from the current date.
    :type period: int
    :return: A dictionary with date keys and values in a form of a list that contains all assignment identifiers that
    were not recorded into the database on a particular date.
    :rtype: dict
    """
    interval_query = f'SELECT failed_doarequestno, current_datetime FROM errors_log ' \
                     f'WHERE current_datetime BETWEEN DATE_SUB(NOW(), INTERVAL %s DAY) AND NOW()'
    connection = connection_info()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(interval_query, period)
            errors_per_day = defaultdict(list)
            for record in cursor:
                errors_per_day[record['current_datetime'].date()].append(record['failed_doarequestno'])
            errors_per_day['Total'] = [sum(map(len, errors_per_day.values()))]

    return errors_per_day


def show_details(all_queries_params):
    """
    Carries out a search of specific records in the errors_log database table.
    :param all_queries_params: A list with values each containing parameters for one search request. The parameters are
    separated by a space and include an assignment identifier and optional date.
    :type all_queries_params: list
    :return: Full records of sought errors.
    :rtype: list
    """
    detailed_response = []
    connection = connection_info()
    with connection:
        with connection.cursor() as cursor:
            for query_params in all_queries_params:
                query_params_split = query_params.split(' ')
                identifier = query_params_split[0]
                if len(query_params_split) == 2:
                    error_date = query_params_split[1] + ' 00:00:00'
                    dated_values = (identifier, error_date, error_date)
                    dated_query = 'SELECT * FROM errors_log WHERE failed_doarequestno=%s AND current_datetime>=%s ' \
                                  'AND current_datetime<%s + INTERVAL 1 DAY'
                    cursor.execute(dated_query, dated_values)
                    for record in cursor:
                        detailed_response.append(record)
                else:
                    no_date_query = 'SELECT * FROM errors_log WHERE failed_doarequestno=%s ORDER BY ' \
                                    'current_datetime DESC LIMIT 1'
                    no_date_values = (identifier,)
                    cursor.execute(no_date_query, no_date_values)
                    no_date_result = cursor.fetchone()
                    detailed_response.append(no_date_result)

    return detailed_response
