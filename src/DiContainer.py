
class DiContainer:
    def __init__(self):
        self.dependencies = []

    def add_dependency(self, dependency, dependency_name):
        self.dependencies.append((dependency_name, dependency))

    def get_dependency(self, _dependency_name):
        for (dependency_name, dependency) in self.dependencies:
            if (_dependency_name is dependency_name):
                return dependency
