import weakref

from src.gui_2.global_state.DefinedType import Reducer, States, SubscribeCallback, Action, \
    UnsubscribeCallback, Middleware
from src.gui_2.global_state.middleware.ErrorHandlingMiddleware import error_handling_middleware
from src.gui_2.global_state.middleware.LoggingMiddeware import logging_middleware
from src.gui_2.global_state.middleware.PromiseMiddleware import promise_middleware
from src.gui_2.global_state.reducer.CombinedReducer import combine_reducers
from src.gui_2.global_state.reducer.TaskReducer import task_name_reducer


class Store:

    def __init__(self, initial_state: States, reducer: Reducer, middlewares: list[Middleware]):
        self.reducer: Reducer = reducer
        self.states: States = initial_state
        self.listener_callbacks: weakref.WeakSet[SubscribeCallback] = weakref.WeakSet()
        self.middlewares = middlewares or []
        self.dispatch = self._apply_middlewares(self.dispatch)

    def get_state(self):
        return self.states

    def dispatch(self, action: Action) -> None:
        self.states = self.reducer(self.states, action)
        for callback in self.listener_callbacks:
            callback(action, self.states)

    def subscribe(self, callback: SubscribeCallback) -> UnsubscribeCallback:
        self.listener_callbacks.add(callback)
        return lambda: self.listener_callbacks.discard(callback)

    def _apply_middlewares(self, dispatch):
        for middleware in self.middlewares:
            dispatch = middleware(self, dispatch)
        return dispatch


# Combine reducers
root_reducer = combine_reducers([task_name_reducer])

# Initial state
initial_state = {}

# Create the store
store = Store(initial_state, root_reducer, [error_handling_middleware, logging_middleware, promise_middleware])
