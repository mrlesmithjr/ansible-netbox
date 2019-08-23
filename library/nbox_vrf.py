#!/usr/bin/env python
# (c) 2019, Larry Smith Jr. <mrlesmithjr@gmail.com>
#
# This file is a module for managing NetBox vrfs

from ansible.module_utils.basic import *
import json
import requests


def main():
    '''
    Main module execution
    '''
    argument_spec = dict(
        custom_fields=dict(type='dict', default=dict()),
        description=dict(type='str', default=''),
        enforce_unique=dict(type='bool', default=False),
        name=dict(type='str', required=True),
        netbox_token=dict(type='str', required=True, no_log=True),
        netbox_url=dict(type='str', required=True),
        rd=dict(type='str', default=None),
        state=dict(type='str', default='present',
                   choices=['absent', 'present']),
        tags=dict(type='list', default=[]),
        tenant=dict(type='str', default=None),
    )
    module = AnsibleModule(argument_spec=argument_spec)
    data = {
        'custom_fields': module.params['custom_fields'],
        'description': module.params['description'],
        'enforce_unique': module.params['enforce_unique'],
        'name': module.params['name'],
        'rd': module.params['rd'],
        'tags': module.params['tags'],
        'tenant': module.params['tenant'],
    }
    results = dict(changed=False)

    token = module.params['netbox_token']
    url = module.params['netbox_url']

    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
    }

    existing_tenants = get_tenants(url, headers)
    existing_vrfs = get_vrfs(url, headers)

    vrf_name = module.params['name']
    state = module.params['state']

    vrf = dict()
    vrf['data'] = data

    vrf_tenant = data.get('tenant')
    if vrf_tenant is not None:
        vrf_tenant_id = existing_tenants[vrf_tenant]['id']
        vrf['data']['tenant'] = vrf_tenant_id

    if state == 'present':
        if vrf_name not in existing_vrfs:
            add_vrf(url, headers, vrf['data'], results, module)
        else:
            vrf_lookup = existing_vrfs.get(vrf_name)
            vrf_lookup_data = vrf_lookup['data']
            vrf_lookup_id = vrf_lookup['id']
            if vrf_lookup_data != vrf['data']:
                vrf['id'] = vrf_lookup_id
                update_vrf(url, headers, vrf, results, module)
    else:
        if vrf_name in existing_vrfs:
            vrf_lookup = existing_vrfs.get(vrf_name)
            vrf_lookup_id = vrf_lookup['id']
            vrf['id'] = vrf_lookup_id
            delete_vrf(url, headers, vrf, results, module)

    module.exit_json(**results)


def get_tenants(url, headers):
    '''
    Get dictionary of existing tenants
    '''
    api_url = f'{url}/api/tenancy/tenants/'
    tenants = dict()
    response = requests.request('GET', api_url, headers=headers)
    all_tenants = response.json()['results']
    for tenant in all_tenants:
        tenants[tenant['name']] = {
            'id': tenant['id'],
            'slug': tenant['slug'],
            'group': tenant['group'],
            'description': tenant['description'],
            'comments': tenant['comments'],
            'tags': tenant['tags']
        }
    return tenants


def get_vrfs(url, headers):
    '''
    Get dictionary of existing VRFs
    '''
    vrfs = dict()
    api_url = f'{url}/api/ipam/vrfs/'
    response = requests.request('GET', api_url, headers=headers)
    all_vrfs = response.json()['results']
    for vrf in all_vrfs:
        vrfs[vrf['name']] = {
            'id': vrf['id'],
            'data': {
                'name': vrf['name'],
                'rd': vrf['rd'],
                'enforce_unique': bool(vrf['enforce_unique']),
                'description': vrf['description'],
                'tags': vrf['tags'],
                'custom_fields': vrf['custom_fields']
            }
        }
        if vrf['tenant'] is not None:
            vrfs[vrf['name']]['data']['tenant'] = vrf['tenant']['id']
        else:
            vrfs[vrf['name']]['data']['tenant'] = None

    return vrfs


def add_vrf(url, headers, data, results, module):
    '''
    Add new vrf
    '''
    api_url = f'{url}/api/ipam/vrfs/'
    payload = data
    response = requests.request(
        'POST', api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 201:
        vrf_name = data['name']
        results.update(changed=True,
                       msg=f'{vrf_name} successfully created!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


def update_vrf(url, headers, vrf, results, module):
    '''
    Update existing vrf
    '''
    vrf_id = vrf['id']
    api_url = f'{url}/api/ipam/vrfs/{vrf_id}/'
    payload = vrf['data']
    response = requests.request(
        'PATCH', api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        vrf_name = vrf['data']['name']
        results.update(changed=True,
                       msg=f'{vrf_name} successfully updated!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


def delete_vrf(url, headers, vrf, results, module):
    '''
    Delete existing vrf
    '''
    vrf_id = vrf['id']
    api_url = f'{url}/api/ipam/vrfs/{vrf_id}/'
    response = requests.request('DELETE', api_url, headers=headers)
    if response.status_code == 204:
        vrf_name = vrf['data']['name']
        results.update(changed=True,
                       msg=f'{vrf_name} successfully deleted!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


if __name__ == '__main__':
    main()
