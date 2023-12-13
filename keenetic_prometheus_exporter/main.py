import json
import os
import time
from typing import Dict

from jsonpath_rw import parse

from models.keenetic_api import KeeneticClient
from models.keenetic_collecor import KeeneticCollector

ADMIN_ENDPOINT = 'KEENETIC_ADMIN_ENDPOINT'
LOGIN = 'KEENETIC_ADMIN_USERNAME'
PASSWORD = 'KEENETIC_ADMIN_PASSWORD'

# Documentation
# https://storage.googleapis.com/docs.help.keenetic.com/cli/3.9/ru/cli_manual_kn-1810_ru.pdf


def json_path_init(paths: Dict[str, str]):
    queries = {}

    for pathName, path in paths.items():
        if path == "~":
            queries[pathName] = path
        else:
            queries[pathName] = parse(path)

    return queries


if __name__ == '__main__':
    pwd = os.path.dirname(os.path.realpath(__file__))
    metrics_configuration = json.load(open(pwd + "/config/metrics.json", "r"))

    metrics = metrics_configuration['metrics']

    admin_endpoint = os.environ[ADMIN_ENDPOINT]
    login = os.environ[ADMIN_ENDPOINT]
    password = os.environ[ADMIN_ENDPOINT]

    collectors = []

    with KeeneticClient(admin_endpoint, login, password) as kc:
        for metric_configuration in metrics:
            _command: str = metric_configuration['command']
            _params = metric_configuration.get('param', {})
            _root = parse(metric_configuration['root'])
            _tags = json_path_init(metric_configuration['tags'])
            _values = json_path_init(metric_configuration['values'])

            collectors.append(KeeneticCollector(kc, _command, _params, _root, _tags, _values))

        wait_interval = 30
        while True:
            metrics = []
            for collector in collectors:
                metrics += collector.collect()
            time.sleep(wait_interval)
