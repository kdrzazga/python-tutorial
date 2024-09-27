import sys
import arcade
import base64

from AdultBarbaraJan import AdultBarbaraJan
from BarbaraJan import BarbaraJan

if __name__ == "__main__":
    par = base64.b64decode('YWR1bHQ=').decode('ansi')
    if len(sys.argv) > 1 and par in sys.argv:
        AdultBarbaraJan()
    else:
        BarbaraJan()

    arcade.run()
