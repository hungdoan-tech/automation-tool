import weakref

from src.gui_2.global_state_container.DefinedType import Reducer, States, SubscribeCallback, Action, UnsubscribeCallback
from src.gui_2.layout.RenderableComponent import RenderableComponent


class Store:
    def __init__(self, initial_state: States, reducer: Reducer):
        self.reducer: Reducer = reducer
        self.states: States = initial_state
        self.listener_callbacks: weakref.WeakKeyDictionary[
            RenderableComponent, SubscribeCallback] = weakref.WeakKeyDictionary()

    def get_state(self):
        return self.states

    def dispatch(self, action: Action) -> None:
        self.states = self.reducer(self.states, action)
        for instance, callback in self.listener_callbacks.items():
            callback(action, self.states)

    def subscribe(self, instance: RenderableComponent, callback: SubscribeCallback) -> UnsubscribeCallback:
        if instance is None:
            raise Exception('Please call method subscribe by a instance')

        def unsubscribe(removed_instance: RenderableComponent) -> None:
            del self.listener_callbacks[removed_instance]

        self.listener_callbacks[instance] = callback

        return unsubscribe

    def unsubscribe(self, removed_instance: RenderableComponent) -> None:
        del self.listener_callbacks[removed_instance]
