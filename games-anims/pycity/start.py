import subprocess

from model.board import Board
from presenter.presenter import Presenter
from view.screen import PyCityView

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
