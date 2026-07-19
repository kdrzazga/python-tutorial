import sys

from cube3d.libs.app import CubeApp
from cube3d.libs.globals import INFO_LINES1, INFO_LINES2

WINDOWED_ARGS = ("w", "-w", "window", "-window")


def info():
    for line in (INFO_LINES1 + INFO_LINES2):
        print(line)


def windowed_requested():
    return any(arg.lower() in WINDOWED_ARGS for arg in sys.argv[1:])


if __name__ == "__main__":
    info()
    print("MUSIC: Dance All Night by Gasman/Hooy-Program")
    CubeApp(windowed_requested()).run()
