#!/usr/bin/env python
# (c) 2019, Larry Smith Jr. <mrlesmithjr@gmail.com>
#
# This file is a module for managing NetBox tenant groups

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
                   choices=['absent', 'present'])
    )
    module = AnsibleModule(argument_spec=argument_spec)
    results = dict(changed=False)

    token = module.params['netbox_token']
    url = module.params['netbox_url']

    group = module.params['name']
    state = module.params['state']
    data = {'group': group, 'state': state}

    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
    }

    existing_tenant_groups = get_tenant_groups(url, headers)

    if state == 'present':
        if group not in existing_tenant_groups:
            add_tenant_group(url, headers, data, results, module)
    else:
        if group in existing_tenant_groups:
            group_id = existing_tenant_groups[group].get('id')
            data.update({'group_id': group_id})
            delete_tenant_group(url, headers, data, results, module)

    module.exit_json(**results)


def get_tenant_groups(url, headers):
    '''
    Get dictionary of existing tenant groups
    '''
    api_url = f'{url}/api/tenancy/tenant-groups/'
    tenant_groups = dict()
    response = requests.request('GET', api_url, headers=headers)
    json_response = response.json()
    for group in json_response['results']:
        tenant_groups[group['name']] = {
            'id': group['id'],
            'slug': group['slug'],
            'tenant_count': group['tenant_count']
        }
    return tenant_groups


def get_slug(name):
    '''
    Convert tenant group name to slug
    '''
    if '-' in name:
        slug = name.replace(' ', '').lower()
    elif ' ' in name:
        slug = name.replace(' ', '-').lower()
    else:
        slug = name.lower()

    return slug


def add_tenant_group(url, headers, data, results, module):
    '''
    Add new tenant group
    '''
    api_url = f'{url}/api/tenancy/tenant-groups/'
    group = data.get('group')
    slug = get_slug(group)

    payload = {'name': group, 'slug': slug}
    response = requests.request(
        'POST', api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 201:
        results.update(changed=True, msg=f'{group} successfully created!')
    else:
        module.fail_json(msg=response.text)


def delete_tenant_group(url, headers, data, results, module):
    '''
    Delete existing tenant group
    '''
    group = data.get('group')
    group_id = data.get('group_id')
    api_url = f'{url}/api/tenancy/tenant-groups/{group_id}'
    response = requests.request(
        'DELETE', api_url, headers=headers)
    if response.status_code == 204:
        results.update(changed=True, msg=f'{group} successfully deleted!')
    else:
        module.fail_json(msg=response.text)


if __name__ == '__main__':
    main()
