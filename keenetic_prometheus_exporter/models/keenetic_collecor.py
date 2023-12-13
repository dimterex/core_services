from models.keenetic_api import KeeneticClient, KeeneticApiException
from typing import List

from models.value_normalizer import normalize_value


class KeeneticCollector(object):

    def __init__(self, keenetic_client: KeeneticClient, command, params, root, tags, values):
        self._keenetic_client = keenetic_client
        self._command: str = command
        self._params = params
        self._root = root
        self._tags = tags
        self._values = values

    def collect(self) -> List[dict]:
        metrics = []
        try:
            response = self._keenetic_client.metric(self._command, self._params)
        except KeeneticApiException as e:
            print(f"Skipping metric '{self._command}' collection. Reason keenetic api exception, "
                            f"status: {e.status_code}, response: {e.response_text}")
            return metrics

        roots = self._root.find(response)

        for root in roots:
            tags = []
            for tagName, tagPath in self._tags.items():
                if tagPath == '~':
                    value = root.path.fields[0]
                elif str(tagPath).startswith('`parent`'):
                    full_path = root.full_path.child(tagPath)
                    value = self.get_first_value(full_path.find(response))
                else:
                    value = self.get_first_value(tagPath.find(root.value))
                if value is not None:
                    tags.append(f'{tagName}="{value}"')

            for valueName, valuePath in self._values.items():
                value = self.get_first_value(valuePath.find(root.value))
                if value is not None:
                    labels = ','.join(tags)
                    metrics.append(f'keenetic_{self._command}_{valueName}({labels}) {normalize_value(value)}')

        return metrics

    def get_first_value(self, array):
        if array and len(array) > 0:
            return array[0].value
        else:
            return None
