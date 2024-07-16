import os
import sys
import threading

from src.common.RestrictCallers import only_accept_callers_from
from src.setup.packaging.path.PathResolver import PathResolver
from src.setup.packaging.path.PathResolvingService import PathResolvingService


class InternalImmutableFilePathResolver(PathResolver):

    __instance = None

    __class_lock = threading.Lock()

    @staticmethod
    @only_accept_callers_from(PathResolvingService)
    def get_instance() -> PathResolver:
        if InternalImmutableFilePathResolver.__instance is None:
            InternalImmutableFilePathResolver.__instance = InternalImmutableFilePathResolver()
        return InternalImmutableFilePathResolver.__instance

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:

            with cls.__class_lock:

                if cls.__instance is None:

                    cls.__instance = super(InternalImmutableFilePathResolver, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            with self.__class_lock:
                if not hasattr(self, '_initialized'):
                    self.root_dir = self.get_executable_directory()
                    self._initialized = True

    def get_executable_directory(self) -> str:
        try:
            # inside the packaged executable file of Pyinstaller
            # _MEIPASS will be set at runtime, just discard the warning
            temporary_internal_exe_location: str = sys._MEIPASS
            return temporary_internal_exe_location

        except Exception:
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

        if not os.path.exists(final_path):
            raise Exception(
                f'Something went wrong, the expected path {final_path} is not existed in internal immutable paths')

        return final_path
