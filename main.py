from pathlib import Path

from pkl_github_action_step_generator import *

if __name__ == '__main__':
    generator = PklGithubActionStepGenerator()
    generator.generate(
        Path("test/test_action.yml"),
        "https://github.com/emilymclean/pkl-swift-action",
        "v2"
    )
