import tkinter as tk
from tkinter import font


class InfoPanel(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="green", relief="sunken", bd=3)
        self.labels = {}

        label_names = ["Label 1", "Label 2", "Label 3", "Label 4", "Label 5"]

        for i, label_name in enumerate(label_names, start=1):
            label = tk.Label(self, text=label_name, font=font.Font(size=12), bg="green")
            label.grid(row=i - 1, column=0, padx=10, pady=5, sticky="w")
            self.labels[f"label{i}"] = label


class PyCityView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PyCity Game")
        self._create_board_panels()

    def _create_board_panels(self):
        self.main_panel = tk.Frame(master=self, bg="black", relief="raised", bd=3)
        self.main_panel.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="nsew")

        self.info_panel = InfoPanel(master=self)
        self.info_panel.grid(row=0, column=3, rowspan=3, sticky="nsew")

        self.command_panel = tk.Frame(master=self, bg="grey", relief="sunken", bd=3)
        self.command_panel.grid(row=3, column=0, columnspan=4, sticky="nsew")

        for row in range(4):
            self.rowconfigure(row, weight=1, minsize=50)
        for col in range(4):
            self.columnconfigure(col, weight=1, minsize=75)


def main():
    """Create the game's board and run its main loop."""
    board = PyCityView()
    board.mainloop()


if __name__ == "__main__":
    main()
