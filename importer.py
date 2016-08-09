import json

class Importer:

    def commit(self, commit):
        print(json.dumps(commit, indent=2))
