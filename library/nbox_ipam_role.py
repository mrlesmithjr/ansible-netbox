#!/usr/bin/env python
# (c) 2019, Larry Smith Jr. <mrlesmithjr@gmail.com>
#
# This file is a module for managing NetBox IPAM roles

from ansible.module_utils.basic import *
import json
import requests


def main():
    '''
    Main module execution
    '''
    argument_spec = dict(
        name=dict(type='str', required=True),
        netbox_token=dict(type='str', required=True, no_log=True),
        netbox_url=dict(type='str', required=True),
        state=dict(type='str', default='present',
                   choices=['absent', 'present']),
        weight=dict(type='int', default=1000),
    )
    module = AnsibleModule(argument_spec=argument_spec)
    data = {
        'name': module.params['name'],
        'weight': module.params['weight'],
    }
    results = dict(changed=False)

    token = module.params['netbox_token']
    url = module.params['netbox_url']

    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
    }

    ipam_role_name = module.params['name']
    ipam_role = dict()
    ipam_role['data'] = data

    state = module.params['state']

    existing_ipam_roles = get_ipam_roles(url, headers)

    if state == 'present':
        if ipam_role_name not in existing_ipam_roles:
            slug = get_slug(ipam_role_name)
            ipam_role['data']['slug'] = slug
            add_ipam_role(url, headers, ipam_role['data'], results, module)
        else:
            ipam_role_lookup = existing_ipam_roles.get(ipam_role_name)
            ipam_role_lookup_data = ipam_role_lookup['data']
            ipam_role_lookup_id = ipam_role_lookup['id']
            if ipam_role_lookup_data != ipam_role['data']:
                ipam_role['id'] = ipam_role_lookup_id
                update_ipam_role(url, headers, ipam_role, results, module)
    else:
        if ipam_role_name in existing_ipam_roles:
            ipam_role_lookup = existing_ipam_roles.get(ipam_role_name)
            ipam_role_lookup_data = ipam_role_lookup['data']
            ipam_role_lookup_id = ipam_role_lookup['id']
            ipam_role['id'] = ipam_role_lookup_id
            delete_ipam_role(url, headers, ipam_role, results, module)

    module.exit_json(**results)


def get_ipam_roles(url, headers):
    '''
    Get dictionary of existing ipam roles
    '''
    roles = dict()
    api_url = f'{url}/api/ipam/roles/'
    response = requests.request('GET', api_url, headers=headers)
    json_response = response.json()
    results = json_response.get('results')
    for ipam_role in results:
        roles[ipam_role['name']] = {
            'id': ipam_role['id'],
            'data': {
                'name': ipam_role['name'],
                # 'slug': ipam_role['slug'],
                'weight': ipam_role['weight']
            }
        }

    return roles


def get_slug(name):
    '''
    Convert ipam role name to slug
    '''
    if '-' in name:
        slug = name.replace(' ', '').lower()
    elif ' ' in name:
        slug = name.replace(' ', '-').lower()
    else:
        slug = name.lower()

    return slug


def add_ipam_role(url, headers, data, results, module):
    '''
    Add new ipam role
    '''
    api_url = f'{url}/api/ipam/roles/'
    payload = data
    response = requests.request(
        'POST', api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 201:
        ipam_role_name = data['name']
        results.update(changed=True,
                       msg=f'{ipam_role_name} successfully created!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


def update_ipam_role(url, headers, ipam_role, results, module):
    '''
    Update existing ipam role
    '''
    ipam_role_id = ipam_role['id']
    api_url = f'{url}/api/ipam/roles/{ipam_role_id}/'
    payload = ipam_role['data']
    response = requests.request(
        'PATCH', api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        ipam_role_name = ipam_role['data']['name']
        results.update(changed=True,
                       msg=f'{ipam_role_name} successfully updated!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


def delete_ipam_role(url, headers, ipam_role, results, module):
    '''
    Delete existing ipam role
    '''
    ipam_role_id = ipam_role['id']
    api_url = f'{url}/api/ipam/roles/{ipam_role_id}/'
    response = requests.request('DELETE', api_url, headers=headers)
    if response.status_code == 204:
        ipam_role_name = ipam_role['data']['name']
        results.update(changed=True,
                       msg=f'{ipam_role_name} successfully deleted!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


if __name__ == '__main__':
    main()
