import re
from pathlib import Path
from typing import Optional

import click
import requests

from pkl_github_action_step_generator.core import PklGithubActionStepGenerator

_valid_reference = re.compile(
    r'^([\w\d](?:[\w\d]|\-(?=[\w\d])){0,38})/([\w\d.\-_]{1,100})(/[\w\d.\-_]+)*@([\w\d.\-_]+)$')
_action_file_name_options = ["action.yaml", "action.yml"]


@click.group()
def entry_point():
    pass


@click.command()
@click.argument('name')
@click.option('--output', '-o', required=False)
@click.option('--pkl-github-actions-bindings', default=False, is_flag=True)
def from_remote(
        name: str,
        output: Optional[str],
        pkl_github_actions_bindings: bool
):
    if _valid_reference.match(name) is None:
        raise click.BadParameter(f"{name} is not of the form <username>/<repo>(/path)*@<tag>")

    components = name.split("@")
    name = components[0].split("/")
    repository = "/".join(name[:2])
    path = "/".join(name[2:]) + "/" if len(name) > 2 else ""
    tag = components[1]

    content = None
    for option in _action_file_name_options:
        action_url = f"https://raw.githubusercontent.com/{repository}/refs/tags/{tag}/{path}{option}"
        response = requests.get(action_url)
        if response.status_code == requests.codes.not_found:
            continue
        if response.status_code != requests.codes.ok:
            raise Exception(f"{action_url} returned {response.status_code}")
        content = response.text
        break

    if content is None:
        raise Exception("Unable to find action file for provided action")

    core = PklGithubActionStepGenerator()

    generated = core.generate(
        content,
        components[0],
        tag,
        pkl_github_actions_bindings_version="0.1.0-alpha.96" if pkl_github_actions_bindings else None
    )

    if output is None:
        click.echo(generated)
    else:
        with Path(output).open(mode='w') as f:
            f.write(generated)


entry_point.add_command(from_remote)

if __name__ == '__main__':
    entry_point()
