""" server.repositories.project_repository """
from json import dumps
from typing import Tuple, List, Optional

from server.config import database
from server.models.search_option_model import SearchOption
from server.models.merchant_model import Merchant
from server.models.project_model import Project


def get_merchant_projects(
        merchant: Merchant,
        search_option: SearchOption) -> Tuple[List[Project], int]:
    params = [
        merchant.merchant_id,
        search_option.search_term,
        search_option.size,
        search_option.skip()
    ]
    rows = database.func('directory.get_merchant_projects', params)
    if not rows:
        return [], 0

    merchant_projects = [Project.map(row) for row in rows]
    total_count = rows[0]['total_count']
    return merchant_projects, total_count


def find_merchant_project_by_project_id(
        merchant: Merchant,
        project_id: int) -> Optional[Project]:
    params = [
        merchant.merchant_id,
        project_id]
    rows = database.func('directory.find_merchant_project_by_id', params)

    if not rows:
        return None

    return Project.map(rows[0])


def update_merchant_project(
        merchant: Merchant,
        project: Project) -> Tuple[bool, str]:
    params = [
        merchant.merchant_id,
        project.project_id,
        project.name,
        project.category,
        project.description,
        project.project_key
    ]
    rows = database.func('directory.update_merchant_project_by_project_id', params)
    if not rows:
        return False, 'We are not able to update this project'

    return rows[0]['status'] == 'success', rows[0]['message']


def disable_merchant_project(
        merchant: Merchant,
        project: Project) -> Tuple[bool, str]:
    params = [
        merchant.merchant_id,
        project.project_id,
    ]
    rows = database.func('directory.disable_merchant_project', params)
    if not rows:
        return False, 'We are not able to disable this project'

    return rows[0]['status'] == 'success', rows[0]['message']


def delete_merchant_project(
        merchant: Merchant,
        project: Project) -> Tuple[bool, str]:
    params = [
        merchant.merchant_id,
        project.project_id,
    ]
    rows = database.func('directory.delete_merchant_project', params)
    if not rows:
        return False, 'We are not able to remove this project'

    return rows[0]['status'] == 'success', rows[0]['message']


def publish_merchant_project(
        merchant: Merchant,
        project: Project) -> Tuple[bool, str]:
    params = [
        merchant.merchant_id,
        project.project_id,
    ]
    rows = database.func('directory.publish_merchant_project', params)
    if not rows:
        return False, 'We are not able to publish this project'

    return rows[0]['status'] == 'success', rows[0]['message']


def create_merchant_project(
        merchant: Merchant,
        project: Project) -> Tuple[int, bool, str]:
    params = [
        merchant.merchant_id,
        project.name,
        project.category,
        project.description,
        project.project_key
    ]
    rows = database.func('directory.create_merchant_project', params)
    if not rows:
        return 0, False, 'We are not able to create this project'

    return rows[0]['created_project_id'], rows[0]['status'] == 'success', rows[0]['message']


def update_merchant_project_metadata(project: Project) -> Tuple[bool, str]:
    params = [
        project.project_id,
        dumps(project.project_fields)
    ]

    result = database.func('directory.update_merchant_project_metadata', params)

    if not result:
        return False, 'Unable to update merchant project metadata'

    return result[0]['status'] == 'success', result[0]['message']
