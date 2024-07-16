import threading

from src.observer.EventHandler import EventHandler


class EventBroker:
    __instance = None

    __class_lock = threading.Lock()

    @staticmethod
    def get_instance():
        if EventBroker.__instance is None:
            EventBroker.__instance = EventBroker()
        return EventBroker.__instance

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:

            with cls.__class_lock:

                if cls.__instance is None:
                    cls.__instance = super(EventBroker, cls).__new__(cls)

        return cls.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            with self.__class_lock:
                if not hasattr(self, '_initialized'):
                    self.__topicToSetOfObserver: dict[str, set[EventHandler]] = {}
                    self.__instance_lock = threading.Lock()
                    self._initialized = True

    def subscribe(self, topic: str, observer: EventHandler) -> None:
        with self.__instance_lock:
            if topic not in self.__topicToSetOfObserver:
                self.__topicToSetOfObserver[topic] = set()
            self.__topicToSetOfObserver.get(topic).add(observer)

    def publish(self, topic: str, event: threading.Event) -> None:
        observers: set[EventHandler] = self.__topicToSetOfObserver.get(topic, set())
        observer: EventHandler
        for observer in observers:
            thread: threading.Thread = threading.Thread(target=observer.handle_incoming_event,
                                                        args=[event],
                                                        daemon=False)
            thread.start()
