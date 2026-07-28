#pyinstaller --onefile main.py
import sys

from cube3d.libs.app import CubeApp
from cube3d.libs.globals import INFO_LINES1, INFO_LINES2

WINDOWED_ARGS = ("w", "-w", "window", "-window")
TRIGGER_ARGS = ("t", "trigger", "triggered")


def info():
    for line in (INFO_LINES1 + INFO_LINES2):
        print(line)


def has_arg(names):
    return any(arg.lower() in names for arg in sys.argv[1:])


if __name__ == "__main__":
    info()
    print("MUSIC: Dance All Night by Gasman/Hooy-Program")
    CubeApp(has_arg(WINDOWED_ARGS), has_arg(TRIGGER_ARGS)).run()
