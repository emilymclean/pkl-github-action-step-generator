from pathlib import Path

import yaml

from .action_parser import ActionParser
from .generator import Generator


class PklGithubActionStepGenerator:
    parser: ActionParser

    def __init__(self):
        self.parser = ActionParser()

    def generate(self, action_file_path: Path):
        with action_file_path.open() as file:
            action_content = yaml.safe_load(file)
        action = self.parser.parse(action_content)
        print(action)

        generator = Generator(action)
