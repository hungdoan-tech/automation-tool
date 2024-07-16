import threading


class PathResolvingService:

    __instance = None

    __class_lock = threading.Lock()

    @staticmethod
    def get_instance():
        if PathResolvingService.__instance is None:
            PathResolvingService.__instance = PathResolvingService()
        return PathResolvingService.__instance

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:

            with cls.__class_lock:

                if cls.__instance is None:

                    cls.__instance = super(PathResolvingService, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            with self.__class_lock:
                if not hasattr(self, '_initialized'):
                    # regarding the user files like log, input
                    self.__instance_lock = threading.Lock()
                    self.__internal_immutable_dir_path: set[str] = {'src', 'resource'}
                    self.__task_dir: str = None
                    self.__input_dir: str = None
                    self.__output_dir: str = None
                    self.__log_dir: str = None
                    self._initialized = True


    def resolve(self, mandatory_path: str, *passing_paths) -> str:
        mandatory_path = mandatory_path.strip()
        processing_paths: list[str] = [mandatory_path]
        is_tuple = isinstance(passing_paths, (list, tuple))
        if not is_tuple:
            raise TypeError("*paths must be a list/tuple of string elements")

        for path in passing_paths:
            if not isinstance(path, str):
                raise TypeError("*paths must be a string elements")
            processing_paths.append(path.strip())

        if self.__internal_immutable_dir_path.__contains__(mandatory_path):
            from src.setup.packaging.path.InternalImmutableFilePathResolver import InternalImmutableFilePathResolver
            return InternalImmutableFilePathResolver.get_instance().resolve(processing_paths)

        from src.setup.packaging.path.RuntimeMutableFilePathResolver import RuntimeMutableFilePathResolver
        return RuntimeMutableFilePathResolver.get_instance().resolve(processing_paths)

    def get_task_dir(self):
        with self.__instance_lock:
            if self.__task_dir is None:
                self.__task_dir = self.resolve('src', 'task')
            return self.__task_dir

    def get_input_dir(self):
        with self.__instance_lock:
            if self.__input_dir is None:
                self.__input_dir = self.resolve('input')
            return self.__input_dir

    def get_output_dir(self):
        with self.__instance_lock:
            if self.__output_dir is None:
                self.__output_dir = self.resolve('output')
            return self.__output_dir

    def get_log_dir(self):
        with self.__instance_lock:
            if self.__log_dir is None:
                self.__log_dir = self.resolve('log')
            return self.__log_dir
