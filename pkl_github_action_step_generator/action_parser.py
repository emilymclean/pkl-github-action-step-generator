from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ActionInputParameter:
    name: str
    description: Optional[str]
    required: bool
    default: Optional[str]
    deprecation_message: Optional[str]
    constraint: str = "String"


@dataclass
class ActionOutputParameter:
    name: str
    description: Optional[str]


@dataclass
class Action:
    name: str
    author: str
    description: str
    inputs: List[ActionInputParameter]
    outputs: List[ActionOutputParameter]
    call: str = ""


class ActionParser:

    def parse(self, data) -> Action:
        name = data["name"]
        author = data["author"]
        description = data["description"]
        inputs = self.parse_inputs(data["inputs"]) if "inputs" in data else []
        outputs = self.parse_outputs(data["outputs"]) if "outputs" in data else []
        return Action(name, author, description, inputs, outputs)

    def parse_inputs(self, inputs) -> List[ActionInputParameter]:
        o = []
        for k, v in inputs.items():
            o.append(
                ActionInputParameter(
                    k,
                    v["description"] if "description" in v else None,
                    v["required"] if "required" in v else False,
                    v["default"] if "default" in v else None,
                    v["deprecationMessage"] if "deprecationMessage" in v else None,
                )
            )
        return o

    def parse_outputs(self, outputs) -> List[ActionOutputParameter]:
        o = []
        for k, v in outputs.items():
            o.append(
                ActionOutputParameter(
                    k,
                    v["description"] if "description" in v else None,
                )
            )
        return o
