import unittest
from pathlib import Path

import yaml
from click.testing import CliRunner

from pkl_github_actions_step_generator import PklGithubActionStepGenerator


class TestPklProj(unittest.TestCase):

    def test_generation(self):
        fixtures_dir = Path(__file__).parent.joinpath("fixtures")
        core = PklGithubActionStepGenerator()

        with fixtures_dir.joinpath("action_nullable.yml").open() as f:
            content = f.read()

        result = core.generate_project(
            content,
            "actions/checkout",
            "v4",
            "example.com/packages"
        )

        with fixtures_dir.joinpath("test.PklProject").open() as f:
            expected_output = f.read()

        self.assertEqual(expected_output, result)


if __name__ == '__main__':
    unittest.main()