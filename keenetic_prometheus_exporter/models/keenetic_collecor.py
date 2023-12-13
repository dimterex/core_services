from typing import List

from keenetic_prometheus_exporter.models.keenetic_api import KeeneticClient
from keenetic_prometheus_exporter.models.value_normalizer import normalize_value


class KeeneticCollector(object):

    def __init__(self, command, params, root, tags, values):
        self._command: str = command
        self._params = params
        self._root = root
        self._tags = tags
        self._values = values

    def collect(self, keenetic_client: KeeneticClient) -> List[dict]:
        metrics = []
        try:
            response = keenetic_client.metric(self._command, self._params)
        except Exception as e:
            print(f"Skipping metric '{self._command}' collection. Reason keenetic api exception: {e}")
            return metrics

        roots = self._root.find(response)

        for root in roots:
            tags = []
            for tagName, tagPath in self._params.items():
                tags.append(f'{tagName}="{tagPath}"')

            for tagName, tagPath in self._tags.items():
                value = self.get_value(tagPath, root, response)

                if value is not None:
                    if value is str:
                        value = value.replase('-', '_')
                    tagName = tagName.replace('-', '_')
                    tags.append(f'{tagName}="{value}"')

            for valueName, valuePath in self._values.items():
                value = self.get_value(valuePath, root, response)
                labels = ''
                if value is not None:
                    if len(tags) > 0:
                        labels = ','.join(tags)
                        labels = f'{{{labels}}}'

                    command_name = self._command.replace(' ', '_')
                    valueName = valueName.replace('-', '_')
                    metrics.append(f'keenetic_{command_name}_{valueName}{labels} {normalize_value(value)}\n')

        return metrics

    def get_value(self, tagPath, root, response):
        if tagPath == '~':
            return root.path.fields[0]
        elif str(tagPath).startswith('`parent`'):
            full_path = root.full_path.child(tagPath)
            return self.get_first_value(full_path.find(response))
        else:
            return self.get_first_value(tagPath.find(root.value))


    def get_first_value(self, array):
        if array and len(array) > 0:
            return array[0].value
        else:
            return None
