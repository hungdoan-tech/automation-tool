class ProgressBarManager:
    def __init__(self, progress_bar, progress_bar_label):
        self.progress_bar = progress_bar
        self.progress_bar_label = progress_bar_label

    def update_progress(self, task_name, percent):
        self.progress_bar['value'] = round(percent)
        self.progress_bar_label.configure("Text.Horizontal.TProgressbar", text="{} {}%".format(task_name, percent))
