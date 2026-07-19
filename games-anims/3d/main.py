from libs.app import CubeApp
from libs.globals import INFO_LINES1, INFO_LINES2


def info():
    for line in (INFO_LINES1 + INFO_LINES2):
        print(line)


if __name__ == "__main__":
    info()
    print("MUSIC: Dance All Night by Gasman/Hooy-Program")
    CubeApp().run()
