from ansible.module_utils.basic import AnsibleModule
try:
    from ansible.module_utils.docker import Docker
except ImportError:
    from ..module_utils.docker import Docker

def run_module():
    module_args = dict(
        image=dict(type='str', required=True),
        version=dict(type='str', required=False),
        state=dict(type='str', required=True),
        cmd=dict(type='list', required=False),
        container_name=dict(type='str', required=False),
    )

    result = dict(
        changed=False,
        message="",
        image=""
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    docker_image = module.params.get('image')
    container_init = module.params.get('cmd')
    container_state = module.params.get('state')

    if module.check_mode:
        module.exit_json()

    dock = Docker()
    if container_state == 'started':
        response = dock.create_container(image=docker_image, cmd=container_init)
        container_id = response['Id']

        result['response'] = dock.start_container(container_id)
        # result['response'] = container_id

    module.exit_json(**result)


def main():
    run_module()

if __name__ == "__main__":
    main()
