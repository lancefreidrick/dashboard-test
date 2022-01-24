""" tests.api.test_project_controller.py """
# pylint: disable=global-statement,redefined-outer-name,unused-argument
import json
from tests.utils.token_storage import token_storage

base_url = '/xqwapi/merchants'
m_rome_id = 90000
p_colosseum_id = 100000
p_artemis_id = 100006
p_neptune_id = 100014
p_pluto_id = 100015
p_deleted_bridge_id = 100016

## GET PROJECTS

def test_get_projects_as_admin_successfully(a_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = a_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['totalCount'] == 38
    assert data['projects'] is not None

def test_get_projects_as_client_successfully(s_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = s_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['totalCount'] == 38
    assert data['projects'] is not None

def test_get_projects_as_merchant_admin_successfully(ma_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = ma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['totalCount'] == 38
    assert data['projects'] is not None
    assert 'id' in data['projects'][0]
    assert 'code' in data['projects'][0]
    assert 'key' in data['projects'][0]
    assert 'name' in data['projects'][0]
    assert 'category' in data['projects'][0]
    assert 'description' in data['projects'][0]
    assert 'isActive' in data['projects'][0]
    assert 'isEnabled' in data['projects'][0]
    assert 'projectFields' in data['projects'][0]
    assert 'modifiedAt' in data['projects'][0]

def test_get_projects_as_merchant_staff_successfully(ms_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = ms_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['totalCount'] == 38
    assert data['projects'] is not None

def test_get_projects_as_merchant_agent_successfully(mag_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = mag_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['totalCount'] == 38
    assert data['projects'] is not None

def test_get_projects_as_another_merchant_admin(ama_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = ama_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to get projects'

def test_get_projects_as_multiple_merchant_admin_successfully(mma_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = mma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['totalCount'] == 38
    assert data['projects'] is not None

def test_get_projects_with_no_token(client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = client.get(get_url, headers={
        'Content-Type': 'application/json'
    })
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_get_projects_as_merchant_admin_merchant_does_not_exist(ma_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(80000000)
    res = ma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_get_projects_as_merchant_admin_on_page_2(ma_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects?size={1}&page={2}'.format(m_rome_id, 10, 2)
    res = ma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['projects']) == 10
    assert data['totalCount'] == 38

def test_get_projects_as_merchant_admin_on_page_8_size_500(ma_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects?size={1}&page={2}'.format(m_rome_id, 500, 8)
    res = ma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert len(data['projects']) == 0
    assert data['totalCount'] == 0

## FIND PROJECT

def test_find_project_as_admin_successfully(a_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_colosseum_id)
    res = a_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert 'category' in data
    assert 'code' in data
    assert 'description' in data
    assert 'id' in data
    assert 'isActive' in data
    assert 'isEnabled' in data
    assert 'key' in data
    assert 'modifiedAt' in data
    assert 'name' in data
    assert 'projectFields' in data

def test_find_project_as_staff_successfully(s_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_colosseum_id)
    res = s_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None

def test_find_project_as_merchant_admin_successfully(ma_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_colosseum_id)
    res = ma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None

def test_find_project_as_merchant_staff_successfully(ms_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_colosseum_id)
    res = ms_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None

def test_find_project_as_merchant_agent_successfully(mag_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_colosseum_id)
    res = mag_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None

def test_find_project_as_another_merchant_admin(ama_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_colosseum_id)
    res = ama_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to get this project'

def test_find_project_as_multiple_merchant_admin_successfully(mma_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_colosseum_id)
    res = mma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 200
    assert data is not None

def test_find_project_with_no_token(client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_colosseum_id)
    res = client.get(get_url, headers={
        'Content-Type': 'application/json'
    })
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_find_project_not_found(ma_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, 100222)
    res = ma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Project does not exist'

def test_find_project_merchant_does_not_exist(ma_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(80000, p_colosseum_id)
    res = ma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Merchant does not exist'

def test_find_project_from_another_merchant(ma_client, test_data):
    """
    GET /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_artemis_id)
    res = ma_client.get(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    })
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Project does not exist'

## CREATE PROJECT

def test_create_project_as_admin_successfully(a_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = a_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Test project 1',
        'category': 'Batch One',
        'description': None
    }))
    data = res.json
    assert res.status_code == 201
    assert data is not None
    assert data['message'] == 'Project has been created'
    assert data['key'] is not None
    assert data['projectId'] is not None

def test_create_project_as_staff_successfully(s_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = s_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Test project 2',
        'category': 'Batch One',
        'description': None
    }))
    data = res.json
    assert res.status_code == 201
    assert data is not None
    assert data['message'] == 'Project has been created'
    assert data['key'] is not None
    assert data['projectId'] is not None

def test_create_project_as_merchant_admin_successfully(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Test project 3',
        'category': 'Batch One',
        'description': None
    }))
    data = res.json
    assert res.status_code == 201
    assert data is not None
    assert data['message'] == 'Project has been created'
    assert data['key'] is not None
    assert data['projectId'] is not None

def test_create_project_as_merchant_staff_successfully(ms_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = ms_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Test project 4',
        'category': 'Batch One',
        'description': None
    }))
    data = res.json
    assert res.status_code == 201
    assert data is not None
    assert data['message'] == 'Project has been created'
    assert data['key'] is not None
    assert data['projectId'] is not None

def test_create_project_as_merchant_agent(mag_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = mag_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Test project 5',
        'category': 'Batch One',
        'description': None
    }))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_create_project_as_another_merchant_admin(ama_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = ama_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Test project 6',
        'category': 'Batch One',
        'description': None
    }))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to create a project'

def test_create_project_as_multiple_merchant_admin_successfully(mma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = mma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Test project 7',
        'category': 'Batch One',
        'description': None
    }))
    data = res.json
    assert res.status_code == 201
    assert data is not None
    assert data['message'] == 'Project has been created'
    assert data['key'] is not None
    assert data['projectId'] is not None

def test_create_project_with_no_token(client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = client.post(get_url, headers={
        'Content-Type': 'application/json',
    }, data=json.dumps({
        'name': 'Test project 8',
        'category': 'Batch One',
        'description': None
    }))
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_create_project_with_empty_request_body(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Submitted project has form validation errors'
    assert data['fields']['name'] is not None
    assert data['fields']['name'][0] == 'Missing data for required field.'

def test_create_project_with_empty_category(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Test project 9',
        'category': None
    }))
    data = res.json
    assert res.status_code == 201
    assert data is not None
    assert data['message'] == 'Project has been created'
    assert data['projectId'] is not None
    assert data['key'] is not None

def test_create_project_with_unknown_field(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects'.format(m_rome_id)
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Test project 9',
        'testField': None
    }))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Submitted project has form validation errors'
    assert data['fields']['testField'] is not None
    assert data['fields']['testField'][0] == 'Unknown field.'

## UPDATE PROJECT

def test_update_project_as_admin_successfully(a_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_neptune_id)
    res = a_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Temple of Neptune',
        'category': 'temple',
        'description': 'For Neptune''s glory!'
    }))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Project has been updated'
    assert data['key'] is not None

def test_update_project_as_staff_successfully(s_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_neptune_id)
    res = s_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Temple of Neptune',
        'category': 'temple',
        'description': 'For Neptune''s glory!'
    }))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Project has been updated'
    assert data['key'] is not None

def test_update_project_as_merchant_admin_successfully(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_neptune_id)
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Temple of Neptune',
        'category': 'temple',
        'description': 'For Neptune''s glory!'
    }))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Project has been updated'
    assert data['key'] is not None

def test_update_project_as_merchant_staff_successfully(ms_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_neptune_id)
    res = ms_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Temple of Neptune',
        'category': 'temple',
        'description': 'For Neptune''s glory!'
    }))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_project_as_another_merchant_admin(ama_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_neptune_id)
    res = ama_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Temple of Neptune',
        'category': 'temple',
        'description': 'For Neptune''s glory!'
    }))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to update the project'

def test_update_project_as_multiple_merchant_admin_successfully(mma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_neptune_id)
    res = mma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Temple of Neptune',
        'category': 'temple',
        'description': 'For Neptune''s glory!'
    }))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Project has been updated'
    assert data['key'] is not None

def test_update_project_without_token(client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_neptune_id)
    res = client.post(get_url, headers={
        'Content-Type': 'application/json',
    }, data=json.dumps({
        'name': 'Temple of Neptune',
        'category': 'temple',
        'description': 'For Neptune''s glory!'
    }))
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_update_project_with_empty_request_body(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_neptune_id)
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
    }))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Submitted project has form validation errors'
    assert data['fields'] == {'name': ['Missing data for required field.']}

def test_update_project_on_name_more_than_100_characters(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_neptune_id)
    name = 'Temple of Neptune Temple of Neptune Temple of Neptune Temple of Neptune Temple of Neptune Temple of Neptun'
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': name,
    }))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Submitted project has form validation errors'
    assert data['fields'] == {'name': ['Length must be between 1 and 100.']}

def test_update_project_on_empty_name(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_neptune_id)
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': None,
        'category': None,
        'description': None,
    }))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Submitted project has form validation errors'
    assert data['fields'] == {'name': ['Field may not be null.']}

def test_update_project_on_project_does_not_exist(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, 100222)
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Temple of Neptune',
        'category': 'temple',
        'description': None,
    }))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Project does not exist'

def test_update_project_on_deleted_project(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_deleted_bridge_id)
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Temple of Neptune',
        'category': 'temple',
        'description': None,
    }))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Project does not exist'

def test_update_project_on_category_more_than_100_characters(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_pluto_id)
    category = 'This is a very long category which will cause problems.'
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Temple of Pluto',
        'category': category,
        'description': None,
    }))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Submitted project has form validation errors'
    assert data['fields'] == {'category': ['Length must be between 0 and 50.']}

def test_update_project_on_description_more_than_250_characters(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_pluto_id)
    description = '''
    Wojtek (1942 – 2 December 1963; Polish pronunciation: [ˈvɔjtɛk]; in English,
    sometimes spelled Voytek and pronounced as such) was a Syrian brown bear (Ursus arctos syriacus)
    bought, as a young cub, at a railway station in Hamadan, Iran, by Polish II Corps
    soldiers who had been evacuated from the Soviet Union. In order to provide for
    his rations and transportation, he was eventually enlisted officially as a soldier
    with the rank of private, and was subsequently promoted to corporal.
    '''
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': 'Temple of Pluto',
        'category': 'temple',
        'description': description,
    }))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Submitted project has form validation errors'
    assert data['fields'] == {'description': ['Length must be between 0 and 250.']}

## UPDATE PROJECT METADATA

def test_update_project_metadata_as_admin_successfully(a_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/metadata
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}/metadata'.format(m_rome_id, p_neptune_id)
    res = a_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps([
        {'text': 'Company code', 'name': 'companyCode', 'value': '2000'},
        {'text': 'Built On', 'name': 'builtOn', 'value': '04 Oct'},
        {'text': 'Status', 'name': 'status', 'value': 1}
    ]))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Project metadata has been updated'

def test_update_project_metadata_as_staff_successfully(s_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/metadata
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}/metadata'.format(m_rome_id, p_neptune_id)
    res = s_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps([
        {'text': 'Company code', 'name': 'companyCode', 'value': '2000'},
        {'text': 'Built On', 'name': 'builtOn', 'value': '04 Oct'},
        {'text': 'Status', 'name': 'status', 'value': 1}
    ]))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Project metadata has been updated'

def test_update_project_metadata_as_merchant_admin_successfully(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/metadata
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}/metadata'.format(m_rome_id, p_neptune_id)
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps([
        {'text': 'Company code', 'name': 'companyCode', 'value': '2000'},
        {'text': 'Built On', 'name': 'builtOn', 'value': '04 Oct'},
        {'text': 'Status', 'name': 'status', 'value': 1}
    ]))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Project metadata has been updated'

def test_update_project_metadata_as_merchant_staff_successfully(ms_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/metadata
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}/metadata'.format(m_rome_id, p_neptune_id)
    res = ms_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps([
        {'text': 'Company code', 'name': 'companyCode', 'value': '2000'},
        {'text': 'Built On', 'name': 'builtOn', 'value': '04 Oct'},
        {'text': 'Status', 'name': 'status', 'value': 1}
    ]))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_update_project_metadata_as_another_merchant_admin(ama_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/metadata
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}/metadata'.format(m_rome_id, p_neptune_id)
    res = ama_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps([
        {'text': 'Company code', 'name': 'companyCode', 'value': '2000'},
        {'text': 'Built On', 'name': 'builtOn', 'value': '04 Oct'},
        {'text': 'Status', 'name': 'status', 'value': 1}
    ]))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to update the project metadata'

def test_update_project_metadata_as_multiple_merchant_admin_successfully(mma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/metadata
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}/metadata'.format(m_rome_id, p_neptune_id)
    res = mma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps([
        {'text': 'Company code', 'name': 'companyCode', 'value': '2000'},
        {'text': 'Built On', 'name': 'builtOn', 'value': '04 Oct'},
        {'text': 'Status', 'name': 'status', 'value': 1}
    ]))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Project metadata has been updated'

def test_update_project_metadata_without_token(client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/metadata
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}/metadata'.format(m_rome_id, p_neptune_id)
    res = client.post(get_url, headers={
        'Content-Type': 'application/json',
    }, data=json.dumps([
        {'text': 'Company code', 'name': 'companyCode', 'value': '2000'},
        {'text': 'Built On', 'name': 'builtOn', 'value': '04 Oct'},
        {'text': 'Status', 'name': 'status', 'value': 1}
    ]))
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_update_project_metadata_with_empty_request_body(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/metadata
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}/metadata'.format(m_rome_id, p_neptune_id)
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps([
    ]))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Project metadata has been updated'

def test_update_project_metadata_on_missing_custom_fields(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/metadata
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}/metadata'.format(m_rome_id, p_neptune_id)
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps([
        {'key': 'Company code'},
    ]))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Submitted project has form validation errors'
    assert data['fields'] == {
        'name': ['Missing data for required field.'],
        'text': ['Missing data for required field.'],
        'value': ['Missing data for required field.'],
        'key': ['Unknown field.']
    }

def test_update_project_metadata_on_invalid_schema(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>/metadata
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}/metadata'.format(m_rome_id, p_neptune_id)
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
        'name': None,
        'category': None,
        'description': None,
    }))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Submitted project has form validation errors'
    assert data['fields'] == {
        '_schema': ['Invalid input type.']
    }

def test_update_project_metadata_on_project_does_not_exist(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>/metadata
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}/metadata'.format(m_rome_id, 100222)
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps([
        {'text': 'Company code', 'name': 'companyCode', 'value': '2000'},
        {'text': 'Built On', 'name': 'builtOn', 'value': '04 Oct'},
        {'text': 'Status', 'name': 'status', 'value': 1}
    ]))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Project does not exist'

def test_update_project_metadata_on_deleted_project(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>/metadata
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}/metadata'.format(m_rome_id, p_deleted_bridge_id)
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps([
        {'text': 'Company code', 'name': 'companyCode', 'value': '2000'},
        {'text': 'Built On', 'name': 'builtOn', 'value': '04 Oct'},
        {'text': 'Status', 'name': 'status', 'value': 1}
    ]))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Project does not exist'

def test_update_project_metadata_on_long_text_name(ma_client, test_data):
    """
    POST /xqapi/merchants/<merchant_code>/project/<project_id>
    """
    get_url = '/xqwapi/merchants/{0}/projects/{1}/metadata'.format(m_rome_id, p_pluto_id)
    name = 'This is a very long name which will cause problems in the future'
    res = ma_client.post(get_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps([
        {'text': name, 'name': 'companyCode', 'value': '2000'},
    ]))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Submitted project has form validation errors'
    assert data['fields'] == {'text': ['Length must be between 1 and 50.']}

## DISABLE PROJECT

def test_disable_project_as_admin_successfully(a_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/disable
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/disable'.format(m_rome_id, 100017)
    res = a_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    assert res.status_code == 204
    assert res.data == b''

def test_disable_project_as_staff_successfully(s_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/disable
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/disable'.format(m_rome_id, 100018)
    res = s_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    assert res.status_code == 204
    assert res.data == b''

def test_disable_project_as_merchant_admin_successfully(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/disable
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/disable'.format(m_rome_id, 100019)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    assert res.status_code == 204
    assert res.data == b''

def test_disable_project_as_merchant_staff(ms_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/disable
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/disable'.format(m_rome_id, 100020)
    res = ms_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_disable_project_as_another_merchant_admin(ama_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/disable
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/disable'.format(m_rome_id, 100021)
    res = ama_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to disable the project'

def test_disable_project_as_multiple_merchant_admin_successfully(mma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/disable
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/disable'.format(m_rome_id, 100022)
    res = mma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    assert res.status_code == 204
    assert res.data == b''

def test_disable_project_without_token(client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/disable
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/disable'.format(m_rome_id, 100023)
    res = client.post(post_url, headers={
        'Content-Type': 'application/json',
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_disable_project_does_not_exist(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/disable
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/disable'.format(m_rome_id, 100999)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Project does not exist'

def test_disable_project_already_disabled_project(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/disable
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/disable'.format(m_rome_id, 100024)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Project has already been disabled'

def test_disable_project_already_deleted_project(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/disable
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/disable'.format(m_rome_id, p_deleted_bridge_id)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Project does not exist'

## PUBLISH PROJECT

def test_publish_project_as_admin_successfully(a_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/publish
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/publish'.format(m_rome_id, 100025)
    res = a_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({
    }))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Project has been published'

def test_publish_project_as_staff_successfully(s_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/publish
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/publish'.format(m_rome_id, 100026)
    res = s_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Project has been published'

def test_publish_project_as_merchant_admin_successfully(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/publish
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/publish'.format(m_rome_id, 100027)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Project has been published'

def test_publish_project_as_merchant_staff(ms_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/publish
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/publish'.format(m_rome_id, 100028)
    res = ms_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_publish_project_as_another_merchant_admin(ama_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/publish
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/publish'.format(m_rome_id, 100029)
    res = ama_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to publish the project'

def test_publish_project_as_multiple_merchant_admin_successfully(mma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/publish
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/publish'.format(m_rome_id, 100030)
    res = mma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 200
    assert data is not None
    assert data['message'] == 'Project has been published'

def test_publish_project_without_token(client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/publish
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/publish'.format(m_rome_id, 100031)
    res = client.post(post_url, headers={
        'Content-Type': 'application/json',
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_publish_project_does_not_exist(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/publish
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/publish'.format(m_rome_id, 100999)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Project does not exist'

def test_publish_project_already_publish_project(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/publish
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/publish'.format(m_rome_id, 100032)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 400
    assert data is not None
    assert data['message'] == 'Project has already been published'

def test_publish_project_already_deleted_project(ma_client, test_data):
    """
    POST /xqwapi/merchants/<merchant_id>/project/<project_id>/publish
    """
    post_url = '/xqwapi/merchants/{0}/projects/{1}/publish'.format(m_rome_id, p_deleted_bridge_id)
    res = ma_client.post(post_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Project does not exist'

## DELETE PROJECT

def test_delete_project_as_admin_successfully(a_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/project/<project_id>
    """
    delete_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, 100033)
    res = a_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    assert res.status_code == 204
    assert res.data == b''

def test_delete_project_as_staff_successfully(s_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/project/<project_id>
    """
    delete_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, 100034)
    res = s_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    assert res.status_code == 204
    assert res.data == b''

def test_delete_project_as_merchant_admin_successfully(ma_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/project/<project_id>
    """
    delete_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, 100035)
    res = ma_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    assert res.status_code == 204
    assert res.data == b''

def test_delete_project_as_merchant_staff(ms_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/project/<project_id>
    """
    delete_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, 100036)
    res = ms_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed here'

def test_delete_project_as_another_merchant_admin(ama_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/project/<project_id>
    """
    delete_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, 100037)
    res = ama_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 403
    assert data is not None
    assert data['message'] == 'You are not allowed to delete the project'

def test_delete_project_as_multiple_merchant_admin_successfully(mma_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/project/<project_id>
    """
    delete_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, 100038)
    res = mma_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    assert res.status_code == 204
    assert res.data == b''

def test_delete_project_without_token(client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/project/<project_id>
    """
    delete_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, 100039)
    res = client.delete(delete_url, headers={
        'Content-Type': 'application/json',
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 401
    assert data is not None
    assert data['message'] == 'Unauthorized access'

def test_delete_project_does_not_exist(ma_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/project/<project_id>
    """
    delete_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, 100999)
    res = ma_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Project does not exist'

def test_delete_project_already_disabled_project(ma_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/project/<project_id>
    """
    delete_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, 100040)
    res = ma_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    assert res.status_code == 204
    assert res.data == b''

def test_delete_project_already_deleted_project(ma_client, test_data):
    """
    DELETE /xqwapi/merchants/<merchant_id>/project/<project_id>
    """
    delete_url = '/xqwapi/merchants/{0}/projects/{1}'.format(m_rome_id, p_deleted_bridge_id)
    res = ma_client.delete(delete_url, headers={
        'Content-Type': 'application/json',
        'Authorization': token_storage.bearer_token,
        'X-Client-Id': token_storage.client_id,
        'X-Refresh-Token': token_storage.refresh_token
    }, data=json.dumps({}))
    data = res.json
    assert res.status_code == 404
    assert data is not None
    assert data['message'] == 'Project does not exist'
