from dataclasses import asdict
from typing import Dict, Any

from .action_parser import Action, ActionInputParameter, ActionOutputParameter
from jinja2 import Environment, PackageLoader, select_autoescape


class Generator:
    action: Action
    extra: Dict[str, Any]
    env: Environment

    def __init__(self, action: Action):
        self.action = action
        self.env = Environment(
            loader=PackageLoader("pkl_github_action_step_generator", "templates"),
            autoescape=select_autoescape()
        )
        self.extra = {}
        self._prepare_data()

    def _prepare_data(self):
        self.extra["module"] = "test"
        self.extra["pkl_github_actions"] = {
            "enabled": True,
            "version": "0.1.0-alpha.96"
        }

        self.action.call = "test/action@v1"

    def generate(self) -> str:
        print(self.action)
        template = self.env.get_template("main.pkl.jinja")
        return template.render({
            "action": asdict(self.action),
        } | self.extra)

