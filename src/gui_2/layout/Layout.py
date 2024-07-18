from src.gui_2.layout.Body import Body
from src.gui_2.layout.Footer import Footer
from src.gui_2.layout.Header import Header
from src.gui_2.layout.LeftSideBar import LeftSideBar
from src.gui_2.layout.RenderableComponent import RenderableComponent
from src.gui_2.layout.RightSideBar import RightSideBar


class Layout(RenderableComponent):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        self.header: Header = None
        self.footer: Footer = None
        self.left_side_bar: LeftSideBar = None
        self.right_side_bar: RightSideBar = None
        self.body: Body = None

    def set_layout(self, header: Header, left_side_bar: LeftSideBar, body: Body, right_side_bar: RightSideBar,
                   footer: Footer):
        self.header = header
        self.left_side_bar = left_side_bar
        self.body = body
        self.right_side_bar = right_side_bar
        self.footer = footer

    def render(self):
        # The layout will be a grid 10x10
        col_num = 10
        runner = 0
        while runner < col_num:
            self.grid_rowconfigure(index=runner, weight=1)
            self.grid_columnconfigure(index=runner, weight=1)
            runner += 1

        # Define the grid layout for each section
        self.header.grid_configure(row=0, column=0, rowspan=1, columnspan=10, sticky='nswe')

        self.left_side_bar.grid_configure(row=1, column=0, rowspan=8, columnspan=2, sticky='nswe')

        self.body.grid_configure(row=1, column=2, rowspan=8, columnspan=6, sticky='nswe')

        self.right_side_bar.grid_configure(row=1, column=8, rowspan=8, columnspan=2, sticky='nswe')

        self.footer.grid_configure(row=9, column=0, rowspan=1, columnspan=10, sticky='nswe')

        # Render content in each section
        self.header.render()
        self.left_side_bar.render()
        self.body.render()
        self.right_side_bar.render()
        self.footer.render()

        print("Complete rendering")
