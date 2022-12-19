"""Copyright 2022 Cado Security Ltd. All rights reserved.
"""
import json
import logging
import os

from requests.exceptions import ConnectionError, HTTPError, Timeout

from utils.api_utils import import_ec2_disks, import_ec2_memory, new_project
from utils.consts import SYSTEMS_LIMIT

def lambda_handler(event, context):
    """
    """
    project_id = new_project()
    logging.info(f'Created a new project (id: {project_id})')

    for i in range(1, SYSTEMS_LIMIT):  # Acquire up to a limit
        try:
            system = json.loads(os.environ[f'SYSTEM{i}'])
        except KeyError:
            logging.info('Last system that was found')
            break

        logging.info(f'About to try and import system: {system}')
        try:
            import_ec2_disks(instance_id=system['instanceid'], region=system['region'], project_id=project_id)

        except (ConnectionError, Timeout):
            logging.error('Cannot access Cado Response')

        except HTTPError as e:
            if e.response.status_code >= 400 and e.response.status_code <= 499:
                logging.info('The request that was made was incorrect')
            elif e.response.status_code > 500:
                logging.error('A problem with Cado Response platform')
            else:
                logging.error()
            logging.exception(e)

        except Exception as e:
            logging.info('Unknown exception while importing instance')
            logging.exception(e)

    return {'statusCode': 200, 'body': 'Scan complete'}
