import os
import sys
import threading

from src.common.RestrictCallers import only_accept_callers_from
from src.setup.packaging.path.PathResolver import PathResolver
from src.setup.packaging.path.PathResolvingService import PathResolvingService


class RuntimeMutableFilePathResolver(PathResolver):
    __instance = None

    __class_lock = threading.Lock()

    @staticmethod
    @only_accept_callers_from(PathResolvingService)
    def get_instance() -> PathResolver:
        if RuntimeMutableFilePathResolver.__instance is None:
            RuntimeMutableFilePathResolver.__instance = RuntimeMutableFilePathResolver()
        return RuntimeMutableFilePathResolver.__instance

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:

            with cls.__class_lock:

                if cls.__instance is None:

                    cls.__instance = super(RuntimeMutableFilePathResolver, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            with self.__class_lock:
                if not hasattr(self, '_initialized'):
                    self.root_dir = self.get_executable_directory()
                    self._initialized = True

    def get_executable_directory(self) -> str:
        if getattr(sys, 'frozen', False):
            # This is set when running as an executable created by PyInstaller or similar tools
            exe_path: str = os.path.abspath(sys.executable)
            installation_dir: str = os.path.dirname(exe_path)
            return installation_dir
        else:
            # This is for running in an IDE or standard Python interpreter
            src_dir: str = os.path.abspath(__file__)

            while not src_dir.endswith('src'):
                src_dir = os.path.dirname(src_dir)

            return os.path.dirname(src_dir)

    @only_accept_callers_from(PathResolvingService)
    def resolve(self, paths: list[str]) -> str:

        if paths.__len__() == 0:
            return self.root_dir

        final_path: str = self.root_dir
        for path in paths:
            final_path = os.path.join(final_path, path)

        if os.path.exists(final_path):
            return final_path

        if final_path.__contains__('.'):
            with open(final_path, 'w'):
                pass  # File created, do nothing
            return final_path

        os.mkdir(final_path)
        return final_path
