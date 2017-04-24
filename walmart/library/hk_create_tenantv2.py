#!/usr/bin/python

from ansible.module_utils.basic import *
import socket
import json
import requests

def main():

  fields = {
        "action": dict(choices=['post', 'get'], default='post'),
        "tenant_name": dict(type='str'),
        "host": dict(required=True),
        "username": dict(type='str', default='admin'),
        "password": dict(type='str', default='rovikumar'),
        "protocol": dict(choices=['http', 'https'], default='http'),
        "state": dict(choices=['present', 'absent'], default="present", type='str' )
    }
  module = AnsibleModule(argument_spec=fields)

  tenant_name = module.params['tenant_name']
  username = module.params['username']
  password = module.params['password']
  protocol = module.params['protocol']
  host = socket.gethostbyname(module.params['host'])
  action = module.params['action']
  state = module.params['state'].lower()

  if state == "present":
    status_state = "created,modified"
#    status_state = "created"
  if state == "absent":
    status_state = "deleted"

  post_uri = '/api/mo/uni.json'
  get_uri = 'api/node/class/fvTenant.json'

  ''' Config payload to enable the physical interface '''

  config_data = {
      "fvTenant":{
          "attributes":{
              "name":tenant_name,
              "status":status_state
          }
      }
  }

  payload_data = json.dumps(config_data)

  ''' authentication || || Throw an error otherwise'''
  apic = "{0}://{1}/".format(protocol, host)

  auth = dict(aaaUser=dict(attributes=dict(name=username, pwd=password)))
  url=apic+'api/aaaLogin.json'

  authenticate = requests.post(url, data=json.dumps(auth), timeout=2, verify=False)

  if authenticate.status_code != 200:
      module.fail_json(msg='could not authenticate to apic', status=authenticate.status_code, response=authenticate.text)



  ''' Sending the request to APIC '''
  if post_uri.startswith('/'):
      post_uri = post_uri[1:]
  post_url = apic + post_uri

  if get_uri.startswith('/'):
      get_uri = get_uri[1:]
  get_url = apic + get_uri

  if action == 'post':
      req = requests.post(post_url, cookies=authenticate.cookies,
                          data=payload_data, verify=False)
  elif action == 'get':
      req = requests.get(get_url, cookies=authenticate.cookies,
                         data=payload_data, verify=False)

  ''' Check response status and parse it for status || Throw an error otherwise '''
  response = req.text
  status = req.status_code

  changed = False
  if req.status_code == 200:
      if action == 'post':
          changed = True
      else:
          changed = False
  # if response.imdata.error.code == 103:
  #     changed = False
  else:
      module.fail_json(msg='error issuing api request',
                       response=response, status=status)

  results = {}
  results['status'] = status
  results['response'] = response
  results['changed'] = changed

  module.exit_json(**results)

  # module.exit_json(changed=False, meta=status_state)
  # module.exit_json(changed=False, meta=response)


if __name__ == '__main__':
    main()
