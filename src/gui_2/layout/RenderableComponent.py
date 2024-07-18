from abc import ABC, abstractmethod
from tkinter import Frame


class RenderableComponent(Frame, ABC):

    def __init__(self, master, props: dict[str,] = None, *args, **kwargs):
        super().__init__(master=master, *args, **kwargs)
        self.state: dict[str,] = {}
        self.props: dict[str,] = props if props is not None else {}
        self._is_mounted = False
        self._initialize_state()
        self._bind_lifecycle_methods()

    def _initialize_state(self) -> dict[str,]:
        """
        Initialize state with default values.
        This method can be overridden by subclasses to set initial state.
        """
        pass

    def _bind_lifecycle_methods(self):
        self.bind("<Map>", self._on_mount)
        self.bind("<Unmap>", self._on_unmount)

    def _on_mount(self, event):
        if not self._is_mounted:
            self._is_mounted = True
            self.component_did_mount()

    def _on_unmount(self, event):
        if self._is_mounted:
            self._is_mounted = False
            self.component_will_unmount()

    def set_state(self, new_state):
        """
        Update the state with new values and re-render the component if needed.
        """
        prev_state = self.state.copy()
        self.state.update(new_state)  # Merge the new state with the existing state

        if self.should_frame_update(prev_state, self.state):
            self.render()
            self.component_did_update()

    @abstractmethod
    def render(self):
        pass

    def component_did_mount(self):
        """
        Lifecycle method called after the frame is added to the screen.
        Override to provide custom behavior.
        """
        pass

    def should_frame_update(self, prev_state, next_state) -> bool:
        """
        Determine if the frame should update.
        Override to provide custom behavior.
        """
        return prev_state != next_state

    def component_did_update(self):
        """
        Lifecycle method called after the frame updates.
        Override to provide custom behavior.
        """
        pass

    def component_will_unmount(self):
        """
        Lifecycle method called before the frame is removed from the screen.
        Override to provide custom behavior.
        """
        pass
