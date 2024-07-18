from src.gui_2.state_container.Type import Reducer, States, SubscribeCallback, Action, UnsubscribeCallback


class Store:
    def __init__(self, initial_state: States, reducer: Reducer):
        self.reducer: Reducer = reducer
        self.state: States = initial_state
        self.listener_callbacks: list[SubscribeCallback] = []

    def get_state(self):
        return self.state

    def dispatch(self, action: Action) -> None:
        self.state = self.reducer(self.state, action)
        for callback in self.listener_callbacks:
            callback(action, self.state)

    def subscribe(self, callback: SubscribeCallback) -> UnsubscribeCallback:
        self.listener_callbacks.append(callback)
        return lambda: self.listener_callbacks.remove(callback)
