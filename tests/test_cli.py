import unittest
from pathlib import Path

from click.testing import CliRunner
from src import from_local


class TestCli(unittest.TestCase):

    def test_local(self):
        print(Path("fixtures/action.yml").resolve())
        runner = CliRunner()
        result = runner.invoke(from_local, ["--pkl-github-actions-bindings", "fixtures/action.yml", "actions/checkout@v4"])

        with Path("fixtures/action.pkl").open() as f:
            expected_output = f.read()

        self.assertEqual(0, result.exit_code)
        self.assertEqual(expected_output, result.output)


if __name__ == '__main__':
    unittest.main()
