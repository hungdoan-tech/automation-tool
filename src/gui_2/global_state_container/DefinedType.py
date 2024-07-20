from typing import Callable

States = dict[str, object]

Action = dict[str, object]

Reducer = Callable[[States, Action], States]

SubscribeCallback = Callable[[Action, States], None]

UnsubscribeCallback = Callable[[], None]

Dispatch_Func = Callable[[Action], None]

Middleware = Callable[[object, Dispatch_Func], Dispatch_Func]
