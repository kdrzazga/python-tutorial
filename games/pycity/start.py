import subprocess

from model.board import Board
from view.screen import PyCityView
from presenter.presenter import Presenter

try:
    print("starting REST server in background...")

    cmd = ['python', 'presenter/rest.py']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    # stdout, stderr = process.communicate()
    # print("stdout:", stdout)
    # print("stderr:", stderr)

    board = Board()
    view = PyCityView()
    presenter = Presenter(board, view)

    presenter.update_view()
    view.mainloop()

except KeyboardInterrupt:
    # Handle the KeyboardInterrupt exception here
    print("Interrupted by user.")
