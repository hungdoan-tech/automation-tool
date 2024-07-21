def error_handling_middleware(store, next_dispatch):
    def dispatch(action):
        try:
            return next_dispatch(action)
        except Exception as e:
            print(f"Error occurred during dispatch: {e}")
            raise e

    return dispatch
