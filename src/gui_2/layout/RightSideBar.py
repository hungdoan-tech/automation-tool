from src.gui_2.layout.RenderableComponent import RenderableComponent


class RightSideBar(RenderableComponent):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

    def render(self):
        print("RightSideBar")
