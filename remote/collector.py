"""
The module contains functions that collect data from app.unv.org.
"""

import json
import math
import time

import requests

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0 (Edition Yx 05)'
           }
all_assgns_url = 'https://app.unv.org/api/doa/doa/SearchDoaAsyncByAzureCognitive'


def number_of_assignments():
    """
    Sends a mini-request to see how many assignments are currently posted.
    :return: A total number of assignments available at the moment at app.unv.org.
    :rtype: int
    """
    payload_all = {'take': 1, 'skip': 0}
    response_all = requests.post(all_assgns_url, headers=headers, json=payload_all)
    total_number = json.loads(response_all.text)['value']['total']

    return total_number


def collect_all_identifiers(total_number):
    """
    Collects all unique identifiers of available assignments.
    :param total_number: A total number of available assignments.
    :type total_number: int
    :return: A list of strings that contain assignments identifiers.
    :rtype: list
    """
    all_identifiers = []
    payload_id_collection = {'take': 50, 'skip': 0}
    num_of_search_requests = math.ceil(total_number / 50)

    for _ in range(num_of_search_requests):
        response_id_collection = requests.post(all_assgns_url, headers=headers, json=payload_id_collection)
        search_result = json.loads(response_id_collection.text)['value']['result']

        for assignment in search_result:
            identifier = assignment['doaRequestNo']
            all_identifiers.append(identifier)

        payload_id_collection['skip'] += 50
        time.sleep(3)

    # It seems the same "phantom" identifier is always appended last. I want to address exactly that behavior.
    if all_identifiers[-1] == '1212082':
        del all_identifiers[-1]

    return all_identifiers


def assignment_info(identifier):
    """
    Collects all information of interest on a specified assignment into one dictionary to use
    when populating database tables.
    :param identifier: A unique 16-digit assignment identifier.
    :type identifier: str
    :return: All essential information on one assignment.
    :rtype: dict
    """
    assgn_info_request_url = 'https://app.unv.org/api/doa/doa/' + identifier
    response_assgn_info = requests.get(assgn_info_request_url, headers=headers)
    assgn_info = json.loads(response_assgn_info.text)['value']

    collected_info = {
        'title': assgn_info['name'],
        'doarequestno': identifier,
        'isonsite': assgn_info['isOnsite'],
        'host_entity': assgn_info['hostEntity']['name'],
        'territory': assgn_info['country']['label'],
        'duration': assgn_info['duration'],
        'extension': assgn_info['possibilityOfExtension'],
        'publish_date': assgn_info['publishDate'],
        'assgn_expires': assgn_info['sourcingEndDate'],
        'start_date': assgn_info['startDate'],
        'vol_category': assgn_info['volunteersCategory']['label'],
        'min_age': None,
        'max_age': None,
        'ed_lvl': assgn_info['requiredEducation']['label'],
        'ed_specs': assgn_info['specializationArea'],
        'years_of_xp': assgn_info['requiredExperience'],
        'field_of_xp': assgn_info['requiredSkillExperience'],
        'dutystations': {},
        'languages': {}
    }

    # The age range is not specified for every assignment and is retrieved from another source.
    vol_category_code = assgn_info['volunteersCategory']['value']['code']
    if vol_category_code is not None:
        age_range_url = f'https://app.unv.org/api/mastertables/masterTables/Category/values/{vol_category_code}/' \
                        f'children/ElegibilityCriteria/languages/EN'
        response_age_range = requests.get(age_range_url, headers=headers)
        age_range_info = json.loads(response_age_range.text)['values'][0]['props']
        collected_info['min_age'] = age_range_info['minValue']
        collected_info['max_age'] = age_range_info['maxValue']

    """Even if it is an online assignment and no duty station is listed, my database structure still requires a duty 
    station name and a number of assignments at this station. I also want to make sure I won't miss any station name."""
    for station in assgn_info['assignmentsList']:
        station_name = station['dutyStation']['label']
        if station_name is None:
            collected_info['dutystations']['Not specified'] = collected_info['dutystations'].get('Not specified', 0) + 1
        else:
            collected_info['dutystations'][station_name] = collected_info['dutystations'].get(station_name, 0) + 1

    for lang in assgn_info['languages']:
        lang_name = lang['language']['label']
        collected_info['languages'][lang_name] = {'level': lang['level']['label'], 'isrequired': lang['isRequired']}

    """Since I am unaware what are the limitations on the length of some values, I implement the following checks for 
    data to be compatible with my database. The number of checks is subject to change."""
    if len(collected_info['title']) > 255:
        collected_info['title'] = collected_info['title'][:252] + '...'

    """I am not sure whether collected_info['dutystations'] and collected_info['languages'] can be empty, 
    so I am going to assume it is a possible scenario. Will see later and remove the following code if necessary."""
    if len(collected_info['dutystations']) == 0:
        collected_info['dutystations'] = {'Not specified': 0}

    if len(collected_info['languages']) == 0:
        collected_info['languages'] = {'Not specified': {'level': 'Not specified', 'isrequired': False}}

    return collected_info
