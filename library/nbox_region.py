#!/usr/bin/env python
# (c) 2019, Larry Smith Jr. <mrlesmithjr@gmail.com>
#
# This file is a module for managing NetBox regions

from ansible.module_utils.basic import *
import json
import requests


def main():
    '''
    Main module execution
    '''
    argument_spec = dict(
        name=dict(type='str', required=True),
        netbox_token=dict(type='str', required=True),
        netbox_url=dict(type='str', required=True),
        parent=dict(type='str', default=None),
        state=dict(type='str', default='present',
                   choices=['absent', 'present']),
    )
    module = AnsibleModule(argument_spec=argument_spec)
    results = dict(changed=False)

    token = module.params['netbox_token']
    url = module.params['netbox_url']

    region = module.params['name']
    parent = module.params['parent']
    state = module.params['state']
    data = {'region': region, 'parent': parent, 'state': state}
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
    }

    existing_regions = get_regions(url, headers)

    region_lookup = existing_regions.get(region)

    if state == 'present':
        if region_lookup is None:
            add_region(url, headers, data, existing_regions, results)
        else:
            update_region(url, headers, data, existing_regions, results)
    else:
        if region_lookup is not None:
            delete_region(url, headers, data, existing_regions, results)

    module.exit_json(**results)


def get_regions(url, headers):
    '''
    Get existing regions
    '''
    regions = dict()
    api_url = f'{url}/api/dcim/regions/'
    response = requests.request('GET', api_url, headers=headers)
    json_response = response.json()
    for region in json_response['results']:
        regions[region['name']] = {'id': region['id'], 'slug': region['slug']}

    return regions


def get_slug(name):
    '''
    Convert region name to slug
    '''
    if '-' in name:
        slug = name.replace(' ', '').lower()
    elif ' ' in name:
        slug = name.replace(' ', '-').lower()
    else:
        slug = name.lower()

    return slug


def add_region(url, headers, data, existing_regions, results):
    '''
    Add new region
    '''
    api_url = f'{url}/api/dcim/regions/'
    parent = data.get('parent')
    if parent is not None:
        parent_lookup = existing_regions.get(parent)
        if parent_lookup is None:
            slug = get_slug(parent)
            payload = {'name': parent, 'slug': slug}

            response = requests.request(
                'POST', api_url, data=json.dumps(payload), headers=headers)
            json_response = response.json()
            parent_id = json_response.get('id')
        else:
            parent_id = existing_regions[parent].get('id')
    else:
        parent_id = None

    region = data.get('region')
    slug = get_slug(region)

    payload = {'name': region, 'slug': slug}
    if parent_id is not None:
        payload.update({'parent': parent_id})
    response = requests.request(
        'POST', api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 201:
        results.update(changed=True,
                       msg=f'{region} successfully created!',
                       status_code=response.status_code
                       )
    else:
        results.update(changed=False, msg=response.status_code)


def update_region(url, headers, data, existing_regions, results):
    '''
    Update an existing region
    '''
    region = data.get('region')
    region_id = existing_regions[region].get('id')
    api_url = f'{url}/api/dcim/regions/{region_id}'
    response = requests.request('GET', api_url, headers=headers)
    json_response = response.json()
    existing_parent = json_response.get('parent')
    if existing_parent is not None:
        existing_parent_id = existing_parent.get('id')
    else:
        existing_parent_id = None
    parent = data.get('parent')
    if parent is not None:
        parent_lookup = existing_regions.get(parent)
        if parent_lookup is None:
            slug = get_slug(parent)
            payload = {'name': parent, 'slug': slug}
            api_url = f'{url}/api/dcim/regions/'
            response = requests.request(
                'POST', api_url, data=json.dumps(payload), headers=headers)
            json_response = response.json()
            parent_id = json_response.get('id')
        else:
            parent_id = existing_regions[parent].get('id')
    else:
        parent_id = None

    if existing_parent_id != parent_id:
        slug = get_slug(region)
        payload = {'name': region, 'slug': slug, 'parent': parent_id}
        api_url = f'{url}/api/dcim/regions/{region_id}/'
        response = requests.request(
            'PATCH', api_url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            results.update(changed=True,
                           msg=f'{region} successfully updated!',
                           status_code=response.status_code
                           )
        else:
            results.update(changed=False, msg=response.status_code)


def delete_region(url, headers, data, existing_regions, results):
    '''
    Delete an existing region
    '''
    region = data.get('region')
    region_id = existing_regions[region].get('id')
    api_url = f'{url}/api/dcim/regions/{region_id}/'
    response = requests.request('DELETE', api_url, headers=headers)
    if response.status_code == 204:
        results.update(changed=True,
                       msg=f'{region} successfully deleted!',
                       status_code=response.status_code
                       )
    else:
        results.update(changed=False, msg=response.status_code)


if __name__ == '__main__':
    main()
