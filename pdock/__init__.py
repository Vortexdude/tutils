
def main():
    from client import Docker
    docker = Docker()
    client = docker.from_env()
    containers = client.containers.list()
    print(containers[0].ImageID)
    container = client.containers.get(container_id=containers[0].short_id)
    print(container.ImageID)


if __name__ == "__main__":
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()
