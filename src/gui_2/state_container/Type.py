from typing import Callable

States = dict[str, object]

New_State_Value = object

Action = dict[str, object]

Reducer = Callable[[dict[str, object], dict[str, object]], New_State_Value]

SubscribeCallback = Callable[[Action, States], None]

UnsubscribeCallback = Callable[[], None]
