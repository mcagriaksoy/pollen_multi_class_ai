class PathManager:
    def __init__(self):
        self.paths = {}

    def set_path(self, key, path):
        self.paths[key] = path

    def get_path(self, key):
        return self.paths.get(key, None)

# Create a global instance of PathManager
path_manager = PathManager()