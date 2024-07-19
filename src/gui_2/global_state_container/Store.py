import weakref

from src.gui_2.global_state_container.DefinedType import Reducer, States, SubscribeCallback, Action, UnsubscribeCallback


class Store:
    def __init__(self, initial_state: States, reducer: Reducer):
        self.reducer: Reducer = reducer
        self.states: States = initial_state
        self.listener_callbacks: weakref.WeakSet[SubscribeCallback] = weakref.WeakSet()

    def get_state(self):
        return self.states

    def dispatch(self, action: Action) -> None:
        self.states = self.reducer(self.states, action)
        for callback in self.listener_callbacks:
            callback(action, self.states)

    def subscribe(self, callback: SubscribeCallback) -> UnsubscribeCallback:
        self.listener_callbacks.add(callback)
        return lambda: self.listener_callbacks.discard(callback)
