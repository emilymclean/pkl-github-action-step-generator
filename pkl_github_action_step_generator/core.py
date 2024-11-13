from pathlib import Path
from typing import Optional

import yaml

from .action_parser import ActionParser
from .action_transformer import ActionTransformer, DefaultActionTransformer
from .pkl_generator import PklGenerator, PklGeneratorConfig


class PklGithubActionStepGenerator:
    parser: ActionParser
    transformer: ActionTransformer

    def __init__(self, transformer: ActionTransformer = DefaultActionTransformer()):
        self.parser = ActionParser()
        self.transformer = transformer

    def generate(
            self,
            action_file_path: Path,
            hosted_url: str,
            tag: str,
            module_name: Optional[str] = None
    ) -> str:
        if hosted_url.startswith("https://github.com/"):
            hosted_url = hosted_url[len("https://github.com/"):]

        if module_name is None:
            module_name = hosted_url.replace("/", ".").rstrip(".").replace("-", "_")

        with action_file_path.open() as file:
            action_content = yaml.safe_load(file)
        action = self.transformer.transform(self.parser.parse(action_content))
        config = PklGeneratorConfig(
            hosted_url,
            tag,
            module_name,
            "0.1.0-alpha.96"
        )

        generator = PklGenerator(
            action,
            config
        )

        return generator.generate_main()
