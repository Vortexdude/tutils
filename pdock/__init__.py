import os
import sys




def main():
    from client import Docker
    docker = Docker()
    client = docker.from_env()
    id = client.containers.list()


if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    main()
