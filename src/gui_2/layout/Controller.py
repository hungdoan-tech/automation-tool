import tkinter as tk

from src.gui_2.layout.Body import Body
from src.gui_2.layout.Footer import Footer
from src.gui_2.layout.Header import Header
from src.gui_2.layout.LeftSideBar import LeftSideBar
from src.gui_2.layout.RightSideBar import RightSideBar


class Controller:

    def __init__(self, tk_instance: tk.Tk, header: Header, footer: Footer,
                 lef_side_bar: LeftSideBar, right_side_bar: RightSideBar, body: Body):
        super().__init__()
        self.root = tk_instance
        self.header = header
        self.footer = footer
        self.lef_side_bar = lef_side_bar
        self.right_side_bar = right_side_bar
        self.body = body

    def render(self):
        self.root.title("Automation Tool")
        self.root.geometry('1080x980')
        self.root.configure(bg='#FFFFFF')

        # Header
        self.header

        # Footer
        self.render_footer()

        # Main content frame
        main_frame = tk.Frame(self.root, bg='#FFFFFF')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left Sidebar
        left_sidebar = self.render_left_sidebar(main_frame)
        left_sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Right Sidebar
        right_sidebar = self.render_right_sidebar(main_frame)
        right_sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)

        # Body
        body = self.render_body(main_frame)
        body.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)


if __name__ == '__main__':
    root = tk.Tk()
    app = Controller(root)
    root.mainloop()
