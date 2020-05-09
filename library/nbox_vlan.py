#!/usr/bin/env python

"""library/nbox_vlan.py"""

# (c) 2020, Larry Smith Jr. <mrlesmithjr@gmail.com>
#
# This file is a module for managing NetBox vlans

# pylint: disable=unused-wildcard-import,redefined-builtin,wildcard-import,too-many-arguments # noqa E501

import json
import requests
from ansible.module_utils.basic import *  # noqa F403

SITE_STATUS_CODES = {
    'Active': 1,
    'Planned': 2,
    'Retired': 4
}


def main():
    """Main module execution"""

    argument_spec = dict(
        description=dict(type='str', default=None),
        group=dict(type='str', default=None),
        name=dict(type='str', required=True),
        netbox_token=dict(type='str', required=True, no_log=True),
        netbox_url=dict(type='str', required=True),
        role=dict(type='str', default=None),
        site=dict(type='str', default=None),
        state=dict(type='str', default='present',
                   choices=['absent', 'present']),
        status=dict(type='str', required=True,
                    choices=['Active', 'Planned', 'Retired']),
        tags=dict(type='list', default=[]),
        tenant=dict(type='str', default=None),
        vid=dict(type='int', required=True)
    )

    module = AnsibleModule(argument_spec=argument_spec)  # noqa F405

    data = {
        'description': module.params['description'],
        'group': module.params['group'],
        'name': module.params['name'],
        'role': module.params['role'],
        'site': module.params['site'],
        'status': module.params['status'],
        'tags': module.params['tags'],
        'tenant': module.params['tenant'],
        'vid': module.params['vid'],
    }

    results = dict(changed=False)

    token = module.params['netbox_token']
    url = module.params['netbox_url']
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
    }

    state = module.params['state']
    existing_vlans, vlan = normalize(url, headers, data)

    if state == 'present':
        if vlan['data']['name'] not in existing_vlans:
            add_vlan(url, headers, vlan['data'], results, module)
        else:
            existing_vlan = existing_vlans.get(vlan['data']['name'])
            if vlan['data']['vid'] != existing_vlan['data']['vid']:
                add_vlan(url, headers, vlan['data'], results, module)

            else:
                update_vlan(
                    url, headers, vlan['data'], existing_vlan, results, module)
    else:
        if vlan['data']['name'] in existing_vlans:
            existing_vlan = existing_vlans.get(vlan['data']['name'])
            delete_vlan(url, headers, existing_vlan, results, module)

    module.exit_json(**results)


def normalize(url, headers, data):
    """Normalize data"""

    existing_ipam_roles = get_ipam_roles(url, headers)
    existing_sites = get_sites(url, headers)
    existing_tenants = get_tenants(url, headers)
    existing_vlan_groups = get_vlan_groups(url, headers)
    existing_vlans = get_vlans(url, headers)

    vlan = dict()
    vlan['data'] = data
    vlan['data']['status'] = SITE_STATUS_CODES.get(data['status'])

    if data['group'] is not None:
        vlan['data']['group'] = existing_vlan_groups[data['group']]['id']
    if data['role'] is not None:
        vlan['data']['role'] = existing_ipam_roles[data['role']]['id']
    if data['site'] is not None:
        vlan['data']['site'] = existing_sites[data['site']]['id']
    if data['tenant'] is not None:
        vlan['data']['tenant'] = existing_tenants[data['tenant']]['id']

    return existing_vlans, vlan


def get_sites(url, headers):
    """Get dictionary of existing sites"""

    api_url = f'{url}/api/dcim/sites/'
    response = requests.request('GET', api_url, headers=headers)
    json_results = response.json().get('results')

    sites = dict()
    for site in json_results:
        sites[site['name']] = {'id': site['id']}
        if site['tenant'] is not None:
            sites[site['name']]['tenant'] = site['tenant'].get('id')

    return sites


def get_ipam_roles(url, headers):
    """Get dictionary of existing ipam roles"""

    api_url = f'{url}/api/ipam/roles/'
    response = requests.request('GET', api_url, headers=headers)
    json_results = response.json().get('results')

    roles = dict()
    for ipam_role in json_results:
        roles[ipam_role['name']] = {'id': ipam_role['id']}

    return roles


def get_tenants(url, headers):
    """Get dictionary of existing tenants"""

    api_url = f'{url}/api/tenancy/tenants/'
    response = requests.request('GET', api_url, headers=headers)
    json_results = response.json().get('results')

    tenants = dict()
    for tenant in json_results:
        tenants[tenant['name']] = {'id': tenant['id']}

    return tenants


def get_vlan_groups(url, headers):
    """Get dictionary of existing vlan groups"""

    api_url = f'{url}/api/ipam/vlan-groups/'
    response = requests.request('GET', api_url, headers=headers)
    json_results = response.json().get('results')

    vlan_groups = dict()
    for vlan_group in json_results:
        vlan_groups[vlan_group['name']] = {'id': vlan_group['id']}

    return vlan_groups


def get_vlans(url, headers):
    """Get dictionary of existing vlans"""

    api_url = f'{url}/api/ipam/vlans/'
    response = requests.request('GET', api_url, headers=headers)
    json_results = response.json().get('results')

    vlans = dict()
    for vlan in json_results:
        vlans[vlan['name']] = {
            'id': vlan['id'],
            'data': {
                'description': vlan['description'],
                'group': vlan['group'].get('id'),
                'name': vlan['name'],
                'role': vlan['role'].get('id'),
                'site': vlan['site'].get('id'),
                'status': vlan['status'].get('id'),
                'tags': vlan['tags'],
                'tenant': vlan['tenant'].get('id'),
                'vid': vlan['vid']
            }
        }

    return vlans


def add_vlan(url, headers, data, results, module):
    """Add new vlan"""

    api_url = f'{url}/api/ipam/vlans/'
    payload = data
    response = requests.request(
        'POST', api_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 201:
        vlan_name = data['name']
        results.update(changed=True,
                       msg=f'{vlan_name} successfully created!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


def update_vlan(url, headers, data, existing_vlan, results, module):
    """Update existing vlan"""

    if existing_vlan['data'] != data:
        vlan_id = existing_vlan['id']
        api_url = f'{url}/api/ipam/vlans/{vlan_id}/'
        payload = data
        response = requests.request(
            'PATCH', api_url, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            vlan_name = existing_vlan['data']['name']
            results.update(changed=True,
                           msg=f'{vlan_name} successfully updated!',
                           status_code=response.status_code
                           )
        else:
            module.fail_json(msg=response.text)


def delete_vlan(url, headers, existing_vlan, results, module):
    """Delete existing vlan"""

    vlan_id = existing_vlan['id']
    api_url = f'{url}/api/ipam/vlans/{vlan_id}/'
    response = requests.request('DELETE', api_url, headers=headers)

    if response.status_code == 204:
        vlan_name = existing_vlan['data']['name']
        results.update(changed=True,
                       msg=f'{vlan_name} successfully deleted!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


if __name__ == '__main__':
    main()
