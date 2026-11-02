import sys
from pathlib import Path

project_directory = Path(__file__).resolve().parent
snippets_directory = project_directory / "snippets"
sys.path.insert(0, str(snippets_directory))
sys.path.insert(0, str(project_directory))

from tutorial.application import TutorialApplication


def main():
    TutorialApplication(snippets_directory).run()


if __name__ == "__main__":
    main()
