import tkinter as tk


class Presenter:
    def __init__(self, board, view):
        self.board = board
        self.view = view

    def update_view(self):
        for row in range(len(self.board.cells)):
            for col in range(len(self.board.cells[row])):
                cell_value = self.board.cells[row][col]
                if cell_value:
                    label = tk.Label(self.view.main_panel, text=cell_value)
                    label.grid(row=row, column=col)

        self.view.info_panel.labels["label2"].config(text=self.board.info)

        self.view.update()
