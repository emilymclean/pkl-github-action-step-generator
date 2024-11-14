import unittest
from pathlib import Path

from click.testing import CliRunner

from pkl_github_actions_step_generator import from_local


class TestCli(unittest.TestCase):

    def test_local_nullable(self):
        fixtures_dir = Path(__file__).parent.joinpath("fixtures")
        runner = CliRunner()
        result = runner.invoke(from_local, [
            "--pkl-github-actions-bindings",
            str(fixtures_dir.joinpath("action_nullable.yml").resolve()),
            "actions/checkout@v4"
        ])

        with fixtures_dir.joinpath("action_nullable.pkl").open() as f:
            expected_output = f.read()

        self.assertEqual(None, result.exception)
        self.assertEqual(0, result.exit_code)
        self.assertEqual(expected_output, result.output)

    def test_local_non_nullable(self):
        fixtures_dir = Path(__file__).parent.joinpath("fixtures")
        runner = CliRunner()
        result = runner.invoke(from_local, [
            "--pkl-github-actions-bindings",
            str(fixtures_dir.joinpath("action_non_nullable.yml").resolve()),
            "actions/checkout@v4"
        ])

        with fixtures_dir.joinpath("action_non_nullable.pkl").open() as f:
            expected_output = f.read()

        self.assertEqual(None, result.exception)
        self.assertEqual(0, result.exit_code)
        self.assertEqual(expected_output, result.output)

    def test_local_deprecated(self):
        fixtures_dir = Path(__file__).parent.joinpath("fixtures")
        runner = CliRunner()
        result = runner.invoke(from_local, [
            "--pkl-github-actions-bindings",
            "--deprecated",
            str(fixtures_dir.joinpath("action_non_nullable.yml").resolve()),
            "actions/checkout@v4"
        ])

        with fixtures_dir.joinpath("action_deprecated.pkl").open() as f:
            expected_output = f.read()

        self.assertEqual(None, result.exception)
        self.assertEqual(0, result.exit_code)
        self.assertEqual(expected_output, result.output)


if __name__ == '__main__':
    unittest.main()
