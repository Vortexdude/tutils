from ansible.module_utils.basic import AnsibleModule
try:
    from ansible.module_utils.docker import Docker
    from ansible.module_utils.docker_config import id_generate
except ImportError:
    from ..module_utils.docker import Docker
    from ..module_utils.docker_config import id_generate


def run_module():
    module_args = dict(
        image=dict(type='str', required=True),
        version=dict(type='str', required=False),
        state=dict(type='str', default='started', choices=['started', 'stopped', 'absent']),
        cmd=dict(type='list', required=False),
        ports=dict(type='str', required=False),
        container_name=dict(type='str', required=False, aliases=['container-name']),
    )

    result = dict(
        changed=False,
        message="",
        image=""
    )
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    container_name = module.params.get("container_name")
    docker_image = module.params.get('image')
    image_Version = module.params.get('version')
    container_init = module.params.get('cmd')
    desired_container_state = module.params.get('state')
    port_mapping = module.params.get('ports')

    if module.check_mode:
        module.exit_json()

    dock = Docker()
    response = {}
    changed = False

    if not container_name:
        container_name = f"{docker_image}_{id_generate()}"

    container = dock.validate_container(container_name)

    if container:
        if "running" not in container['State'] and 'started' in desired_container_state:
            response = dock.start_container(container['Id'])
            changed = True
            result['message'] = "inside the stated_condition"

        elif "running" not in container['State'] and 'absent' in desired_container_state:
            response = dock.remove_container(container['Id'])
            result['message'] = "inside the absent condition"
            changed = True

        elif "running" in container['State']:
            if "stopped" in desired_container_state:
                dock.stop_container(container['Id'])
                changed = True
            elif "absent" in desired_container_state:
                dock.stop_container(container['Id'])
                response = dock.remove_container(container['Id'])
                changed = True

    else:
        if desired_container_state == "started" or desired_container_state == "stopped":
            result['message'] = "creating new container"
            response = dock.create_container(image=docker_image, name=container_name, ports=port_mapping,
                                             cmd=container_init)
            changed = True
            if desired_container_state == "started":
                container_id = response['Id']
                response = dock.start_container(container_id)

    result['response'] = response
    result['changed'] = changed

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
