from BarbaraJan import BarbaraJan
from src.main.project_globals import Globals


class AdultBarbaraJan(BarbaraJan):

    def __init__(self):
        super().__init__("barbar.png")
        print("Welcome to the adult version of Barbarian/Barbara & Ian.")
        Globals.version = "adult"
