def promise_middleware(store, next_dispatch):
    def dispatch(action):
        if isinstance(action, dict) and 'promise' in action:
            promise = action['promise']
            promise.then(
                lambda result: next_dispatch({'type': action['type'], 'payload': result}),
                lambda error: next_dispatch({'type': f"{action['type']}_REJECTED", 'payload': error})
            )
            return
        return next_dispatch(action)

    return dispatch
