import json

class Settings:
    def __init__(self, path:str):
        file = self._loadSettings(path)

        self.screen = file['screen']
        self.player = file['player']

    def _loadSettings(self, path:str):
        with open(path, 'r') as f:
            return json.loads(f.read())