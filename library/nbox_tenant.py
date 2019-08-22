#!/usr/bin/env python
# (c) 2019, Larry Smith Jr. <mrlesmithjr@gmail.com>
#
# This file is a module for managing NetBox tenants


from ansible.module_utils.basic import *
import json
import requests


def main():
    '''
    Main module execution
    '''
    argument_spec = dict(
        comments=dict(type='str', default=''),
        description=dict(type='str', default=''),
        group=dict(type='str', default=None),
        name=dict(type='str', required=True),
        netbox_token=dict(type='str', required=True, no_log=True),
        netbox_url=dict(type='str', required=True),
        state=dict(type='str', default='present',
                   choices=['absent', 'present']),
        tags=dict(type='list', default=[])
    )
    module = AnsibleModule(argument_spec=argument_spec)
    results = dict(changed=False)

    token = module.params['netbox_token']
    url = module.params['netbox_url']

    group = module.params.get('group')
    tenant = module.params['name']
    state = module.params['state']
    description = module.params.get('description')
    comments = module.params.get('comments')
    tags = module.params.get('tags')
    data = {'group': group, 'tenant': tenant, 'state': state,
            'description': description, 'comments': comments, 'tags': tags}
    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
    }

    existing_tenant_groups = get_tenant_groups(url, headers)
    existing_tenants = get_tenants(url, headers)

    if state == 'present':
        if (group is not None and
                group not in existing_tenant_groups):
            module.fail_json(msg=f'{group} not found!')
        else:
            group_id = existing_tenant_groups[group].get('id')
            data.update({'group_id': group_id})
            if tenant not in existing_tenants:
                add_tenant(url, headers, data, results, module)
            else:
                # tenant_id = existing_tenants[tenant].get('id')
                # data.update({'tenant_id': tenant_id})
                update_tenant(url, headers, existing_tenants,
                              data, results, module)
    else:
        if tenant in existing_tenants:
            delete_tenant(url, headers, existing_tenants,
                          data, results, module)

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
    Convert tenant name to slug
    '''
    if '-' in name:
        slug = name.replace(' ', '').lower()
    elif ' ' in name:
        slug = name.replace(' ', '-').lower()
    else:
        slug = name.lower()

    return slug


def add_tenant(url, headers, data, results, module):
    '''
    Add new tenant
    '''
    api_url = f'{url}/api/tenancy/tenants/'
    tenant = data.get('tenant')
    group_id = data.get('group_id')
    description = data.get('description')
    comments = data.get('comments')
    tags = data.get('tags')
    slug = get_slug(tenant)
    payload = {'name': tenant, 'slug': slug,
               'group': group_id, 'description': description,
               'comments': comments, 'tags': tags}
    response = requests.request(
        'POST', api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 201:
        results.update(changed=True,
                       msg=f'{tenant} successfully created!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


def update_tenant(url, headers, existing_tenants, data, results, module):
    '''
    Update an existing tenant
    '''
    changed = False

    # Define new values
    tenant = data.get('tenant')
    tenant_id = existing_tenants[tenant].get('id')
    description = data.get('description')
    comments = data.get('comments')
    tags = data.get('tags')

    # Define existing values
    existing_description = existing_tenants[tenant].get('description')
    existing_comments = existing_tenants[tenant].get('comments')
    existing_tags = existing_tenants[tenant].get('tags')

    api_url = f'{url}/api/tenancy/tenants/{tenant_id}/'

    slug = get_slug(tenant)

    payload = {'name': tenant, 'slug': slug}

    if existing_description != description:
        payload.update({'description': description})
        changed = True
    if existing_comments != comments:
        payload.update({'comments': comments})
        changed = True
    if existing_tags != tags:
        payload.update({'tags': tags})
        changed = True

    response = requests.request(
        'PATCH', api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        results.update(changed=changed,
                       msg=f'{tenant} successfully updated!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


def delete_tenant(url, headers, existing_tenants, data, results, module):
    '''
    Delete an existing tenant
    '''
    tenant = data.get('tenant')
    tenant_id = existing_tenants[tenant].get('id')

    api_url = f'{url}/api/tenancy/tenants/{tenant_id}/'

    response = requests.request(
        'DELETE', api_url, headers=headers)

    if response.status_code == 204:
        results.update(changed=True, msg=f'{tenant} successfully deleted!')
    else:
        module.fail_json(msg=response.text)


if __name__ == '__main__':
    main()
