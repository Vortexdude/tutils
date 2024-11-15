from ansible.module_utils.basic import AnsibleModule

try:
    from ansible.module_utils.docker import Docker
    from ansible.module_utils.docker_config import id_generate
except ImportError:
    from ..module_utils.docker import Docker
    from ..module_utils.docker import id_generate

STATE_CHOICES: list[str] = ['started', 'restarted', 'stopped', 'absent']


class StateManagement:
    def __init__(self, container_data=None, desired_state=None, module_args=None):
        if container_data is None:
            container_data = dict()

        if desired_state not in STATE_CHOICES:
            raise Exception(f"State should be {', '.join(STATE_CHOICES)}")

        self.module_specs: dict = module_args
        self.desired_state = desired_state
        self.container_data = container_data
        self._arg_setter()

    def _arg_setter(self):
        if not self.container_data:
            return

        for pm in self.container_data['Ports']:
            self.port_mapping = []
            if not pm:
                return []

            elif pm['IP'] == "0.0.0.0":
                self.port_mapping.append(pm)

        self.container_state = self.container_data['State']
        self.is_container_running = self._is_container_running()
        self.need_start = self._need_start()
        self.need_restart = self._need_restart()
        self.need_removal = self._need_removal()
        self.should_stop_and_removed = self._should_stop_and_remove()
        self.should_stop = self._should_stop()
        self.changes = True if self.validate_image() or self.validate_port() else False

    def _is_container_running(self):
        return "running" in self.container_state

    def _need_start(self):
        return "running" not in self.container_state and 'started' in self.desired_state

    def _need_restart(self):
        return self._is_container_running() and "restarted" in self.desired_state

    def _need_removal(self):
        return "running" not in self.container_state and 'absent' in self.desired_state

    def _should_stop_and_remove(self):
        return self._is_container_running() and "absent" in self.desired_state

    def _should_stop(self):
        return self._is_container_running() and 'stopped' in self.desired_state

    def validate_image(self):
        if 'image' not in self.module_specs:
            raise Exception("Image is required")

        if self.container_data['Image'] != self.module_specs['image']:
            return True
        return False

    def validate_port(self):
        """Return False if ports are missmatch

        if given port having public and private ports like "8080:80"
        then it will compare both the ports if they are not matched container
        should be stopped remove and restart again
        """
        if 'ports' in self.module_specs:
            given_ports = self.module_specs['ports']
            public_port, private_port = given_ports.split(":")

            for _ports in self.container_data['Ports']:
                if "IP" not in _ports:
                    return False

                if _ports['IP'] == "0.0.0.0":
                    if public_port != str(_ports['PublicPort']):
                        return True
                    if private_port != str(_ports['PrivatePort']):
                        return True
        return False


def run_module():
    module_args = dict(
        image=dict(type='str', required=True),
        version=dict(type='str', required=False),
        state=dict(type='str', default='started', choices=STATE_CHOICES),
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

    _create_container_args = dict(
        image=docker_image,
        name=container_name,
        ports=port_mapping,
        cmd=container_init
    )

    if module.check_mode:
        module.exit_json()

    dock = Docker()
    # module.fail_json({"message": dock.fetch_image_metadata("java")})
    response = {}
    changed = False

    if not container_name:
        container_name = f"{docker_image}_{id_generate()}"

    container = dock.validate_container(container_name)

    if container:
        dsm = StateManagement(container_data=container, desired_state=desired_container_state, module_args=module.params)

        if dsm.changes: # if something changed
            module.warn("Some parameters are changed")
            dock.rebuild_container(container_id=container['Id'], **_create_container_args)
            changed = True

        if dsm.need_start:
            response = dock.start_container(container['Id'])
            changed = True

        elif dsm.need_restart:
            response = dock.restart_container(container['Id'])
            changed = True

        elif dsm.need_removal:
            response = dock.remove_container(container['Id'])
            changed = True

        elif dsm.should_stop:
            dock.stop_container(container['Id'])
            changed = True

        elif dsm.should_stop_and_removed:
            dock.stop_container(container['Id'])
            response = dock.remove_container(container['Id'])
            changed = True

    else:
        if desired_container_state in {"started", "stopped"}:
            response = dock.create_container(**_create_container_args)
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
