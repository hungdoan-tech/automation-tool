from src.gui_2.layout.RenderableComponent import RenderableComponent


class Footer(RenderableComponent):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)

    def render(self):
        print("Footer")
