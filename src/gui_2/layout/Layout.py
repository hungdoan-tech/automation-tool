from src.gui_2.layout.Component import Component
from src.gui_2.layout.body import Body
from src.gui_2.layout.footer import Footer
from src.gui_2.layout.header import Header
from src.gui_2.layout.left_side_bar import LeftSideBar
from src.gui_2.layout.right_side_bar.RightSideBar import RightSideBar


class Layout(Component):

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

        total_height: int = 10
        main_content_height: int = 8
        header_footer_heights: tuple[int, int] = self.decide_a_pair_components_size(total_height - main_content_height,
                                                                                    self.header, self.footer)
        header_height: int = header_footer_heights[0]
        footer_height: int = header_footer_heights[1]
        if footer_height == 0:
            header_height = 1

        total_width: int = 10
        main_content_width: int = 8
        side_bar_widths: tuple[int, int] = self.decide_a_pair_components_size(total_width - main_content_width,
                                                                              self.left_side_bar, self.right_side_bar)
        left_side_bar_width: int = side_bar_widths[0]
        right_side_bar_width: int = side_bar_widths[1]

        body_start_row = header_height
        body_row_span = total_height - header_height - footer_height
        body_start_column = left_side_bar_width
        body_column_span = total_width - left_side_bar_width - right_side_bar_width

        if header_height > 0:
            self.header.grid_configure(row=0, column=0, rowspan=header_height, columnspan=total_width, sticky='nswe')
        else:
            self.header.grid_forget()

        if left_side_bar_width > 0:
            self.left_side_bar.grid_configure(row=header_height, column=0, rowspan=body_row_span,
                                              columnspan=left_side_bar_width,
                                              sticky='nswe')
        else:
            self.left_side_bar.grid_forget()

        self.body.grid_configure(row=body_start_row, column=body_start_column, rowspan=body_row_span,
                                 columnspan=body_column_span, sticky='nswe')

        if right_side_bar_width > 0:
            self.right_side_bar.grid_configure(row=header_height, column=body_column_span + left_side_bar_width,
                                               rowspan=body_row_span, columnspan=right_side_bar_width,
                                               sticky='nswe')
        else:
            self.right_side_bar.grid_forget()

        if footer_height > 0:
            self.footer.grid_configure(row=body_row_span + header_height, column=0,
                                       rowspan=footer_height, columnspan=total_width, sticky='nswe')
        else:
            self.footer.grid_forget()

        print("Complete rendering")

    def decide_a_pair_components_size(self, total_side_bar_width: int, first_component: Component,
                                      second_component: Component) -> tuple[int, int]:
        left_side_bar_width = 0
        right_side_bar_width = 0

        is_left_side_bar_empty = self.is_render_pass(first_component)
        is_right_side_bar_empty = self.is_render_pass(second_component)

        if is_left_side_bar_empty and is_right_side_bar_empty:
            return (left_side_bar_width, right_side_bar_width)

        if is_left_side_bar_empty:
            right_side_bar_width = total_side_bar_width
            return (left_side_bar_width, right_side_bar_width)

        if is_right_side_bar_empty:
            left_side_bar_width = total_side_bar_width
            return (left_side_bar_width, right_side_bar_width)

        left_side_bar_width = int(total_side_bar_width / 2)
        right_side_bar_width = int(total_side_bar_width / 2)
        return (left_side_bar_width, right_side_bar_width)

    def is_render_pass(self, instance: Component) -> bool:
        _RETURN_NONE = (lambda: None).__code__.co_code
        return instance.render.__code__.co_code == _RETURN_NONE
