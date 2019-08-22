#!/usr/bin/env python
'''
Script to ingest existing NetBox data
'''
# (c) 2019, Larry Smith Jr. <mrlesmithjr@gmail.com>
#
# This file is a module for ingest existing NetBox data

#
# Module usage:
# python utils/ingest.py --token yourusersapitoken --url http(s)//:iporhostnameurl:port
# Example:
# python utils/ingest.py --token 4f552cc2e8c3b76d9613a591e3adb58984a19a6f --url http://127.0.0.1:8080
#


import argparse
import json
import requests
import yaml


def get_args():
    '''
    Get CLI command arguments
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', help='API token', required=True)
    parser.add_argument('-u', '--url', help='API host url',
                        default='http://127.0.0.1:8080')
    parser.add_argument(
        '-f', '--format', help='Format to display', choices=['json', 'yaml'],
        default='json')
    args = parser.parse_args()

    return args


def main():
    '''
    Main module execution
    '''
    args = get_args()
    api_token = args.token
    url = args.url
    headers = {
        'Authorization': f'Token {api_token}',
        'Content-Type': 'application/json',
    }

    data = dict()
    data['netbox_regions'] = get_regions(url, headers)
    data['netbox_tags'] = get_tags(url, headers)
    data['netbox_tenant_groups'] = get_tenant_groups(url, headers)
    data['netbox_tenants'] = get_tenants(url, headers)
    data['netbox_sites'] = get_sites(url, headers)
    data['netbox_vrfs'] = get_vrfs(url, headers)

    if args.format == 'json':
        print(json.dumps(data))
    else:
        print(yaml.dump(data))


def get_regions(url, headers):
    '''
    Get dictionary existing regions
    '''
    api_url = f'{url}/api/dcim/regions/'
    response = requests.request('GET', api_url, headers=headers)
    all_regions = response.json()['results']

    regions = []
    for region in all_regions:
        region_info = dict()
        region_info['name'] = region['name']
        region_info['state'] = 'present'
        if region['parent'] is not None:
            region_info['parent'] = region['parent']['name']
        else:
            region_info['parent'] = None
        regions.append(region_info)

    return regions


def get_tags(url, headers):
    '''
    Get dictionary existing tags
    '''
    api_url = f'{url}/api/extras/tags/'
    response = requests.request('GET', api_url, headers=headers)
    all_tags = response.json()['results']

    tags = []
    for tag in all_tags:
        tag_info = dict()
        tag_info['color'] = tag['color']
        tag_info['comments'] = tag['comments']
        tag_info['name'] = tag['name']
        tag_info['state'] = 'present'
        tags.append(tag_info)

    return tags


def get_tenant_groups(url, headers):
    '''
    Get dictionary of existing tenant groups
    '''
    api_url = f'{url}/api/tenancy/tenant-groups/'
    response = requests.request('GET', api_url, headers=headers)
    all_tenant_groups = response.json()['results']
    tenant_groups = []
    for tenant_group in all_tenant_groups:
        tenant_group_info = dict()
        tenant_group_info['name'] = tenant_group['name']
        tenant_group_info['state'] = 'present'
        tenant_groups.append(tenant_group_info)

    return tenant_groups


def get_tenants(url, headers):
    '''
    Get dictionary of existing tenants
    '''
    api_url = f'{url}/api/tenancy/tenants/'
    response = requests.request('GET', api_url, headers=headers)
    all_tenants = response.json()['results']
    tenants = []
    for tenant in all_tenants:
        tenant_info = dict()
        tenant_info['comments'] = tenant['comments']
        tenant_info['custom_fields'] = tenant['custom_fields']
        tenant_info['description'] = tenant['description']
        if tenant['group'] is not None:
            tenant_info['group'] = tenant['group']['name']
        tenant_info['name'] = tenant['name']
        tenant_info['state'] = 'present'
        tenant_info['tags'] = tenant['tags']
        tenants.append(tenant_info)

    return tenants


def get_sites(url, headers):
    '''
    Get dictionary of existing sites
    '''
    api_url = f'{url}/api/dcim/sites/'
    response = requests.request('GET', api_url, headers=headers)
    all_sites = response.json()['results']
    sites = []
    for site in all_sites:
        site_info = dict()
        site_info['asn'] = site['asn']
        site_info['comments'] = site['comments']
        site_info['contact_email'] = site['contact_email']
        site_info['contact_name'] = site['contact_name']
        site_info['contact_phone'] = site['contact_phone']
        site_info['custom_fields'] = site['custom_fields']
        site_info['description'] = site['description']
        site_info['facility'] = site['facility']
        site_info['latitude'] = site['latitude']
        site_info['longitude'] = site['longitude']
        site_info['name'] = site['name']
        site_info['physical_address'] = site['physical_address']
        if site['region'] is not None:
            site_info['region'] = site['region']['name']
        else:
            site_info['region'] = None
        site_info['shipping_address'] = site['shipping_address']
        site_info['state'] = 'present'
        site_info['status'] = site['status']['label']
        site_info['tags'] = site['tags']
        if site['tenant'] is not None:
            site_info['tenant'] = site['tenant']['name']
        else:
            site_info['tenant'] = None
        site_info['time_zone'] = site['time_zone']

        sites.append(site_info)

    return sites


def get_vrfs(url, headers):
    '''
    Get dictionary of existing VRFs
    '''
    vrfs = []
    api_url = f'{url}/api/ipam/vrfs/'
    response = requests.request('GET', api_url, headers=headers)
    all_vrfs = response.json()['results']
    for vrf in all_vrfs:
        vrf_info = dict()
        vrf_info['custom_fields'] = vrf['custom_fields']
        vrf_info['description'] = vrf['description']
        vrf_info['enforce_unique'] = bool(vrf['enforce_unique'])
        vrf_info['name'] = vrf['name']
        vrf_info['rd'] = vrf['rd']
        vrf_info['tags'] = vrf['tags']
        if vrf['tenant'] is not None:
            vrf_info['tenant'] = vrf['tenant']['name']
        else:
            vrf_info['tenant'] = None
        vrfs.append(vrf_info)

    return vrfs


if __name__ == '__main__':
    main()
