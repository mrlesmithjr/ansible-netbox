#!/usr/bin/env python
# (c) 2019, Larry Smith Jr. <mrlesmithjr@gmail.com>
#
# This file is a module for managing NetBox sites

from ansible.module_utils.basic import *
import json
import requests

SITE_STATUS_CODES = {
    'Active': 1,
    'Planned': 2,
    'Retired': 4
}


def main():
    '''
    Main module execution
    '''
    argument_spec = dict(
        asn=dict(type='int', default=None),
        comments=dict(type='str', default=''),
        contact_email=dict(type='str', default=''),
        contact_name=dict(type='str', default=''),
        contact_phone=dict(type='str', default=''),
        custom_fields=dict(type='dict', default=dict()),
        description=dict(type='str', default=''),
        facility=dict(type='str', default=''),
        latitude=dict(type='str', default=None),
        longitude=dict(type='str', default=None),
        name=dict(type='str', required=True),
        netbox_token=dict(type='str', required=True, no_log=True),
        netbox_url=dict(type='str', required=True),
        physical_address=dict(type='str', default=''),
        region=dict(type='str', default=None),
        shipping_address=dict(type='str', default=''),
        state=dict(type='str', default='present',
                   choices=['absent', 'present']),
        status=dict(type='str', required=True,
                    choices=['Active', 'Planned', 'Retired']),
        tags=dict(type='list', default=[]),
        tenant=dict(type='str', default=None),
        time_zone=dict(type='str', default=''),
    )
    module = AnsibleModule(argument_spec=argument_spec)
    data = {
        'asn': module.params['asn'],
        'comments': module.params['comments'],
        'contact_email': module.params['contact_email'],
        'contact_name': module.params['contact_name'],
        'contact_phone': module.params['contact_phone'],
        'custom_fields': module.params['custom_fields'],
        'description': module.params['description'],
        'facility': module.params['facility'],
        'latitude': module.params['latitude'],
        'longitude': module.params['longitude'],
        'name': module.params['name'],
        'physical_address': module.params['physical_address'],
        'region': module.params['region'],
        'shipping_address': module.params['shipping_address'],
        'status': module.params['status'],
        'tags': module.params['tags'],
        'tenant': module.params['tenant'],
        'time_zone': module.params['time_zone'],
    }
    results = dict(changed=False)

    token = module.params['netbox_token']
    url = module.params['netbox_url']

    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
    }

    existing_regions = get_regions(url, headers)
    existing_sites = get_sites(url, headers)
    existing_tenants = get_tenants(url, headers)

    site_name = module.params['name']
    state = module.params['state']
    site_status_code = SITE_STATUS_CODES.get(data['status'])

    site = dict()
    site['data'] = data
    slug = get_slug(site_name)
    site['data']['slug'] = slug
    site['data']['status'] = site_status_code

    site_region = data.get('region')
    if site_region is not None:
        site_region_id = existing_regions[site_region]['id']
        site['data']['region'] = site_region_id

    site_tenant = data.get('tenant')
    if site_tenant is not None:
        site_tenant_id = existing_tenants[site_tenant]['id']
        site['data']['tenant'] = site_tenant_id

    if state == 'present':
        if site_name not in existing_sites:
            add_site(url, headers, site['data'], results, module)
        else:
            site_lookup = existing_sites.get(site_name)
            site_lookup_data = site_lookup['data']
            site_lookup_id = site_lookup['id']
            if site_lookup_data != site['data']:
                site['id'] = site_lookup_id
                update_site(url, headers, site, results, module)
    else:
        if site_name in existing_sites:
            site_lookup = existing_sites.get(site_name)
            site_lookup_id = site_lookup['id']
            site['id'] = site_lookup_id
            delete_site(url, headers, site, results, module)

    module.exit_json(**results)


def get_regions(url, headers):
    '''
    Get dictionary existing regions
    '''
    regions = dict()
    api_url = f'{url}/api/dcim/regions/'
    response = requests.request('GET', api_url, headers=headers)
    json_response = response.json()
    for region in json_response['results']:
        regions[region['name']] = {'id': region['id'], 'slug': region['slug']}

    return regions


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
                'custom_fields': site['custom_fields'],
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


def get_tenants(url, headers):
    '''
    Get dictionary of existing tenants
    '''
    api_url = f'{url}/api/tenancy/tenants/'
    tenants = dict()
    response = requests.request('GET', api_url, headers=headers)
    json_results = response.json().get('results')
    for tenant in json_results:
        tenants[tenant['name']] = {
            'id': tenant['id'],
            'slug': tenant['slug'],
            'group': tenant['group'],
            'description': tenant['description'],
            'comments': tenant['comments'],
            'tags': tenant['tags']
        }
    return tenants


def get_slug(name):
    '''
    Convert site name to slug
    '''
    if '-' in name:
        slug = name.replace(' ', '').lower()
    elif ' ' in name:
        slug = name.replace(' ', '-').lower()
    else:
        slug = name.lower()

    return slug


def add_site(url, headers, data, results, module):
    '''
    Add new site
    '''
    api_url = f'{url}/api/dcim/sites/'
    payload = data
    response = requests.request(
        'POST', api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 201:
        site_name = data['name']
        results.update(changed=True,
                       msg=f'{site_name} successfully created!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


def update_site(url, headers, site, results, module):
    '''
    Update existing site
    '''
    site_id = site['id']
    api_url = f'{url}/api/dcim/sites/{site_id}/'
    payload = site['data']
    response = requests.request(
        'PATCH', api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        site_name = site['data']['name']
        results.update(changed=True,
                       msg=f'{site_name} successfully updated!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


def delete_site(url, headers, site, results, module):
    '''
    Delete existing site
    '''
    site_id = site['id']
    api_url = f'{url}/api/dcim/sites/{site_id}/'
    response = requests.request('DELETE', api_url, headers=headers)
    if response.status_code == 204:
        site_name = site['data']['name']
        results.update(changed=True,
                       msg=f'{site_name} successfully deleted!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


if __name__ == '__main__':
    main()
