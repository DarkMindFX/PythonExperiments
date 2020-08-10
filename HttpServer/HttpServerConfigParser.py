
import json
import HttpServerConfig as hsc


class HttpServerConfigParser:

    def Parse(self, filePath):
        with open(filePath, 'r') as json_file:
            data = json.load(json_file)

            config = hsc.HttpServerConfig(
                int(data['Port']),
                str(data['Root']),
                str(data['DefaultPages']),
                data['ScriptsExtensions'],
                bool(data['IsMaster']),
                data['Others']
            )

            return config

