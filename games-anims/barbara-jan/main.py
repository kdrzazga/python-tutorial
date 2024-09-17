import sys

import arcade

from AdultBarbaraJan import AdultBarbaraJan
from BarbaraJan import BarbaraJan

if __name__ == "__main__":
    if len(sys.argv) > 1 and 'adult' in sys.argv:
        AdultBarbaraJan()
    else:
        BarbaraJan()

    arcade.run()
