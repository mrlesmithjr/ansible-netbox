#!/usr/bin/env python
# (c) 2019, Larry Smith Jr. <mrlesmithjr@gmail.com>
#
# This file is a module for managing NetBox tags

from ansible.module_utils.basic import *
import json
import requests


def main():
    '''
    Main module execution
    '''
    argument_spec = dict(
        color=dict(type='str', default='9e9e9e'),
        comments=dict(type='str', default=''),
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

    tag = module.params['name']
    color = module.params['color']
    comments = module.params['comments']
    state = module.params['state']

    data = {'tag': tag, 'color': color, 'comments': comments, 'state': state}

    headers = {
        'Authorization': f'Token {token}',
        'Content-Type': 'application/json',
    }

    existing_tags = get_tags(url, headers)

    if state == 'present':
        if tag not in existing_tags:
            add_tag(url, headers, data, results, module)
        else:
            update_tag(url, headers, existing_tags, data, results, module)
    else:
        if tag in existing_tags:
            delete_tag(url, headers, existing_tags, data, results, module)

    module.exit_json(**results)


def get_tags(url, headers):
    '''
    Get dictionary of existing tags
    '''
    tags = dict()
    api_url = f'{url}/api/extras/tags/'
    response = requests.request('GET', api_url, headers=headers)
    json_response = response.json()
    for tag in json_response['results']:
        tags[tag['name']] = {
            'id': tag['id'], 'slug': tag['slug'],
            'color': tag['color'],
            'comments': tag['comments']
        }

    return tags


def get_slug(name):
    '''
    Convert tag name to slug
    '''
    if '-' in name:
        slug = name.replace(' ', '').lower()
    elif ' ' in name:
        slug = name.replace(' ', '-').lower()
    else:
        slug = name.lower()

    return slug


def add_tag(url, headers, data, results, module):
    '''
    Add a new tag
    '''
    tag = data.get('tag')
    color = data.get('color')
    comments = data.get('comments')
    api_url = f'{url}/api/extras/tags/'
    slug = get_slug(tag)

    payload = {'name': tag, 'slug': slug, 'color': color, 'comments': comments}
    response = requests.request(
        'POST', api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 201:
        results.update(changed=True, msg=f'{tag} successfully created!')
    else:
        module.fail_json(msg=response.text)


def update_tag(url, headers, existing_tags, data, results, module):
    '''
    Update an existing tag
    '''
    changed = False

    # Define new values
    tag = data.get('tag')
    color = data.get('color')
    comments = data.get('comments')

    # Define existing values
    existing_color = existing_tags[tag].get('color')
    existing_comments = existing_tags[tag].get('comments')

    tag_id = existing_tags[tag].get('id')
    api_url = f'{url}/api/extras/tags/{tag_id}/'
    slug = get_slug(tag)

    payload = {'name': tag, 'slug': slug}

    if existing_color != color:
        payload.update({'color': color})
        changed = True

    if existing_comments != comments:
        payload.update({'comments': comments})
        changed = True

    response = requests.request(
        'PATCH', api_url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        results.update(changed=changed,
                       msg=f'{tag} successfully updated!',
                       status_code=response.status_code
                       )
    else:
        module.fail_json(msg=response.text)


def delete_tag(url, headers, existing_tags, data, results, module):
    '''
    Delete an existing tag
    '''
    tag = data.get('tag')
    tag_id = existing_tags[tag].get('id')

    api_url = f'{url}/api/extras/tags/{tag_id}'

    response = requests.request(
        'DELETE', api_url, headers=headers)

    if response.status_code == 204:
        results.update(changed=True, msg=f'{tag} successfully deleted!')
    else:
        module.fail_json(msg=response.text)


if __name__ == '__main__':
    main()
