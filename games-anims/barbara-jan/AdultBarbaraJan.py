import os

from BarbaraJan import BarbaraJan
from src.main.board import AdultBoard
from src.main.project_globals import Globals
from src.main.en_de_code import decode_base64_to_texture


class AdultBarbaraJan(BarbaraJan):

    def __init__(self):
        super().__init__()
        print("Welcome to the adult version of Barbarian/Barbara & Ian.")
        Globals.version = "adult"
        root_dir = os.path.dirname(os.path.abspath(__file__))
        texture = decode_base64_to_texture(os.path.join(root_dir, "resources", "barbar.txt"))
        self.reward_pic = decode_base64_to_texture(os.path.join(root_dir, "resources", "reward.txt"))
        self.board = AdultBoard(texture)
