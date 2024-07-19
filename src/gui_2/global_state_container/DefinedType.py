from typing import Callable

from src.gui_2.layout.RenderableComponent import RenderableComponent

States = dict[str, object]

Action = dict[str, object]

Reducer = Callable[[States, Action], States]

SubscribeCallback = Callable[[RenderableComponent, Action, States], None]

UnsubscribeCallback = Callable[[RenderableComponent], None]
