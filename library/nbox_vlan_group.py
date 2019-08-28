#!/usr/bin/env python
# (c) 2019, Larry Smith Jr. <mrlesmithjr@gmail.com>
#
# This file is a module for managing NetBox VLAN Groups

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
        site=dict(type='str', default=None),
        state=dict(type='str', default='present',
                   choices=['absent', 'present']),
    )
    module = AnsibleModule(argument_spec=argument_spec)
    data = {
        'name': module.params['name'],
        'site': module.params['site'],
    }
    results = dict(changed=False)

    token = module.params['netbox_token']
    url = module.params['netbox_url']

    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
    }

    existing_sites = get_sites(url, headers)
    existing_vlan_groups = get_vlan_groups(url, headers)

    state = module.params['state']
    vlan_group_name = module.params['name']

    vlan_group = dict()
    vlan_group['data'] = data

    vlan_group_site = data.get('site')
    if vlan_group_site is not None:
        site_id = existing_sites[vlan_group_site]['id']
        vlan_group['data']['site'] = site_id

    if state == 'present':
        if vlan_group_name not in existing_vlan_groups:
            slug = get_slug(vlan_group_name)
            vlan_group['data']['slug'] = slug
            add_vlan_group(url, headers, vlan_group['data'], results, module)
        else:
            vlan_group_lookup = existing_vlan_groups.get(vlan_group_name)
            vlan_group_lookup_data = vlan_group_lookup['data']
            vlan_group_lookup_id = vlan_group_lookup['id']
            if vlan_group_lookup_data != vlan_group['data']:
                vlan_group['id'] = vlan_group_lookup_id
                update_vlan_group(url, headers, vlan_group, results, module)
    else:
        if vlan_group_name in existing_vlan_groups:
            vlan_group_lookup = existing_vlan_groups.get(vlan_group_name)
            vlan_group_lookup_data = vlan_group_lookup['data']
            vlan_group_lookup_id = vlan_group_lookup['id']
            vlan_group['id'] = vlan_group_lookup_id
            delete_vlan_group(url, headers, vlan_group, results, module)

    module.exit_json(**results)


def get_sites(url, headers):
    '''
    Get dictionary existing sites
    '''
    sites = dict()
    api_url = f'{url}/api/dcim/sites/'
    response = requests.request('GET', api_url, headers=headers)
    json_response = response.json()
    results = json_response.get('results')
    for site in results:
        sites[site['name']] = {
            'id': site['id'],
            'data': {
                'name': site['name'],
                'slug': site['slug'],
                'status': site['status'].get('value'),
                'facility': site['facility'],
                'asn': site['asn'],
                'time_zone': site['time_zone'],
                'description': site['description'],
                'physical_address': site['physical_address'],
                'shipping_address': site['shipping_address'],
                'latitude': site['latitude'],
                'longitude': site['longitude'],
                'contact_name': site['contact_name'],
                'contact_phone': site['contact_phone'],
                'contact_email': site['contact_email'],
                'comments': site['comments'],
                'tags': site['tags'],
                'custom_fields': site['custom_fields']}
        }
        if site['region'] is not None:
            sites[site['name']]['data']['region'] = site['region'].get('id')
        else:
            site[site['name']]['data']['region'] = None
        if site['tenant'] is not None:
            sites[site['name']]['data']['tenant'] = site['tenant'].get('id')
        else:
            site[site['name']]['data']['tenant'] = None

    return sites


def get_vlan_groups(url, headers):
    '''
    Get dictionary of existing vlan groups
    '''
    vlan_groups = dict()
    api_url = f'{url}/api/ipam/vlan-groups/'
    response = requests.request('GET', api_url, headers=headers)
    json_response = response.json()
    results = json_response.get('results')
    for vlan_group in results:
        if vlan_group['site'] is not None:
            vlan_group_site_id = vlan_group['site']['id']
        else:
            vlan_group_site_id = None
        vlan_groups[vlan_group['name']] = {
            'id': vlan_group['id'],
            'data': {
                'name': vlan_group['name'],
                'site': vlan_group_site_id,
            }
        }

    return vlan_groups


def get_slug(name):
    '''
    Convert vlan group name to slug
    '''
    if '-' in name:
        slug = name.replace(' ', '').lower()
    elif ' ' in name:
        slug = name.replace(' ', '-').lower()
    else:
        slug = name.lower()

    return slug


def add_vlan_group(url, headers, data, results, module):
    '''
    Add new vlan group
    '''
    api_url = f'{url}/api/ipam/vlan-groups/'
    payload = data
    response = requests.request(
        'POST', api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 201:
        vlan_group_name = data['name']
        results.update(changed=True,
                       msg=f'{vlan_group_name} successfully created!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


def update_vlan_group(url, headers, vlan_group, results, module):
    '''
    Update existing vlan group
    '''
    vlan_group_id = vlan_group['id']
    api_url = f'{url}/api/ipam/vlan-groups/{vlan_group_id}/'
    payload = vlan_group['data']
    response = requests.request(
        'PATCH', api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        vlan_group_name = vlan_group['data']['name']
        results.update(changed=True,
                       msg=f'{vlan_group_name} successfully updated!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


def delete_vlan_group(url, headers, vlan_group, results, module):
    '''
    Delete existing vlan group
    '''
    vlan_group_id = vlan_group['id']
    api_url = f'{url}/api/ipam/vlan-groups/{vlan_group_id}/'
    response = requests.request('DELETE', api_url, headers=headers)
    if response.status_code == 204:
        vlan_group_name = vlan_group['data']['name']
        results.update(changed=True,
                       msg=f'{vlan_group_name} successfully deleted!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


if __name__ == '__main__':
    main()
