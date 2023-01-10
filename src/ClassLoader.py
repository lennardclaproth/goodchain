from dataclasses import dataclass
import importlib
import inspect
import os


class ClassLoader:
    @staticmethod
    def load(module: str, Type, class_registry={}):
        path = f"{os.getcwd()}/src/{module.replace('.', '/')}/"
        for filename in os.listdir(path):
            ClassLoader.gather_classes(
                module, Type, class_registry, path, filename)
        return class_registry

    @staticmethod
    def gather_classes(module, Type, class_registry, path, filename):
        if os.path.isfile(os.path.join(path, filename)) is False:
            return

        if filename == f"{Type.__name__}.py":
            return
        return ClassLoader.register_class(
            module, filename.removesuffix('.py') ,Type ,class_registry)

    @staticmethod
    def register_class(module, class_file, Type, class_registry):
        for class_name, cls in inspect.getmembers(importlib.import_module(name=f"{module}.{class_file}"), inspect.isclass):
            if module in cls.__module__ and cls is not Type:
                class_registry.update({class_name: ClassWrapper(cls)})
        return class_registry

@dataclass
class ClassWrapper:
    
    def __init__(self, class_repr):
        self.__class_repr = class_repr
        self.__instance = None

    def instantiate(self):
        self.__instance = self.__class_repr()

    def get_instance(self):
        return self.__instance