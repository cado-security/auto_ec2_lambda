"""Copyright 2022 Cado Security Ltd. All rights reserved.
Utils functions to interact with Cado API
"""

import logging
from datetime import date
from typing import Dict
import random
import string

import requests

from utils.consts import API_KEY, API_URL, BUCKET

def new_project() -> int:
    """Create a new project

    :return: New project id
    :rtype: int
    """
    S = 4
    proj_rdm = "".join(random.choices(string.ascii_lowercase + string.digits, k = S))
    project_name = f'weekly_scan_{date.today()}_{proj_rdm}'
    logging.info(f'Creating a new project: {project_name}')

    response = requests.post(
        f'{API_URL}/projects',
        json={'caseName': project_name},
        headers={'Authorization': f'Bearer {API_KEY}'},
        verify=False
    )
    response.raise_for_status()
    return response.json()['id']

def import_ec2_disks(instance_id: str, region: str, project_id: int) -> Dict:
    """Import disks of an ec2 into a cado project

    :param str instance_id: AWS instance id 
    :param str region: AWS region of the instance 
    :param str project_id: Cado project id where the memory will be imported to
    """
    logging.info(f"About to import disks of the instance: {instance_id}")

    body_params = {"bucket":BUCKET,"instance_id": instance_id,"include_screenshot": True,"include_logs": True,"compress":True,"include_disks": True, "region": region}
    response = requests.post(
        f'{API_URL}/projects/{project_id}/imports/ec2',
        json=body_params,
        headers={'Authorization': f'Bearer {API_KEY}'},
        verify=False
    )
    response.raise_for_status()
    return response.json()