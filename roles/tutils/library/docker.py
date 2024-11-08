from ansible.module_utils.basic import AnsibleModule


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

    result['image'] = module.params.get('image')

    if module.check_mode:
        module.exit_json()

    module.exit_json(**result)


def main():
    run_module()

if __name__ == "__main__":
    main()
