import yaml
import os
import shutil
import docker
from git import Repo

SOURCE_FOLDER = os.getcwd()
TARGET_FOLDER = 'C:\\Users\\UseR\\Downloads\\Temp deploy'

SOURCE_PAGES = 'D:\\Projects\\web_host_application\\build'
WEB_HOST_SERVICE = 'web_host'
WEB_HOST_PAGES = 'pages'

DEBUG = False

IGNORE_FOLDERS = [
    '.git',
    '.idea',
    'docker_templates',
    '__pycache__',
    'core',
]

CONFIG_NAME = 'config.yml'
DOCKER_COMPOSE_FILE = 'docker-compose.yml'

UPDATE_SCRIPT_FILE_NAME = 'update.sh'
DOCKER_REMOTE_BASE_URL = 'tcp://dimterex-ubuntu:2375'


def main():
    print("---- Starting deploy script")

    if os.path.exists(TARGET_FOLDER):
        shutil.rmtree(TARGET_FOLDER)
    os.mkdir(TARGET_FOLDER)

    repo = Repo(SOURCE_FOLDER)
    changes = repo.git.diff(None, name_only=True).splitlines()

    changed_modules = []
    for item in changes:
        top_level_dir = item.split('/')[0]
        if not os.path.isdir(top_level_dir):
            continue
        if top_level_dir not in changed_modules:
            changed_modules.append(top_level_dir)

    print(f'Количество изменений: {len(changed_modules)}')
    for dir_name in changed_modules:
        print(dir_name)

    for directory in changed_modules:
        if directory in IGNORE_FOLDERS:
            continue

        docker_folder_path = os.path.join(TARGET_FOLDER, directory)

        source_full_path = os.path.join(SOURCE_FOLDER, directory)
        copy_for_docker_image(source_full_path, directory, docker_folder_path)

        if directory == WEB_HOST_SERVICE:
            copy_web_pages(SOURCE_PAGES, os.path.join(docker_folder_path, WEB_HOST_PAGES))

        print(f'{directory} copied')

    update_script_content = {}
    for directory in os.listdir(TARGET_FOLDER):
        image_content_path = os.path.join(TARGET_FOLDER, directory)
        previous_version, version = get_image_versions(directory)
        update_script_content[directory] = previous_version

        if not DEBUG:
            build_docker_image(image_content_path, directory, version, DOCKER_REMOTE_BASE_URL)

        for root, dirs, files in os.walk(image_content_path, topdown=False):
            for name in files:
                if name == DOCKER_COMPOSE_FILE:
                    update_docker_compose(root, directory, version)
                    continue
                if not DEBUG:
                    os.remove(os.path.join(root, name))
            if not DEBUG:
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

    os.startfile(TARGET_FOLDER)
    generate_update_script(update_script_content)

    print("---- Ended deploy script")


def generate_update_script(update_script_content):
    with open(os.path.join(TARGET_FOLDER, UPDATE_SCRIPT_FILE_NAME), 'w', newline="\n") as script:
        for name in update_script_content:
            previous_version = update_script_content[name]
            script.write(f'docker stop {name}\n')
            script.write(f'docker container rm {name}\n')
            script.write(f'cd {name}/\n')
            script.write('docker-compose up -d\n')
            if previous_version != str():
                script.write(f'docker image rm {name}:{previous_version}\n')
            script.write('cd ../\n')


def update_docker_compose(path, image_name, tag):
    compose_file_path = os.path.join(path, 'docker-compose.yml')
    with open(compose_file_path, 'r', encoding='utf-8') as file:
        compose_data = yaml.safe_load(file)

    for service_name, service_config in compose_data['services'].items():
        service_config['image'] = f"{image_name}:{tag}"
        service_config['container_name'] = image_name
        service_config['hostname'] = image_name
        service_config['command'] = f'python /app/{image_name}/main.py'

    with open(compose_file_path, 'w', encoding='utf-8') as file:
        yaml.dump(compose_data, file, allow_unicode=True, sort_keys=False)


def get_image_versions(image_name) -> tuple[str, str]:
    version = str()
    new_version = "0.1"

    if DEBUG:
        return version, new_version

    with open(CONFIG_NAME, 'r') as f:
        config = yaml.safe_load(f)
        if config is None:
            config = {}

    if image_name in config:
        version = config[image_name]
        major, minor = map(int, version.split('.'))
        minor += 1
        new_version = f"{major}.{minor}"

    config[image_name] = new_version

    with open(CONFIG_NAME, 'w') as f:
        yaml.dump(config, f)

    return version, new_version


def build_docker_image(path, tag, version, remote_base_url):
    image_tag = f'{tag}:{version}'
    client = docker.DockerClient(base_url=remote_base_url)
    print(f"Image {image_tag} building ...")
    image, _ = client.images.build(path=path, tag=image_tag)
    print(f"Image {image_tag} saved successfully.")


def copy_web_pages(source: str, target: str):
    shutil.copytree(source, target, dirs_exist_ok=True)


def copy_for_docker_image(source: str, directory: str, target: str):
    shutil.copytree(
        source,
        os.path.join(target, directory),
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns('*.pyc'))

    shutil.copytree(
        os.path.join(SOURCE_FOLDER, 'core'),
        os.path.join(target, 'core'),
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns('*.pyc'))

    shutil.copytree(
        os.path.join(SOURCE_FOLDER, 'docker_templates'),
        os.path.join(target),
        dirs_exist_ok=True)

    shutil.move(
        os.path.join(target, directory, 'docker-compose.yml'),
        os.path.join(target, 'docker-compose.yml'))


if __name__ == '__main__':
    main()
