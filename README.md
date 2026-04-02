<h2>PAGOZA Status</h2>

[![Build Status](https://github.com/dagl1/PAGOZA/actions/workflows/CI.yml/badge.svg?branch=main)](https://github.com/dagl1/PAGOZA/actions)
[![Docs Status](https://readthedocs.org/projects/pagoza/badge/?version=latest)](https://pagoza.readthedocs.io)
[![Demo Status](https://img.shields.io/website?down_color=red&down_message=offline&label=Render&style=flat&up_color=brightgreen&up_message=online&url=https%3A%2F%2Fpagoza.onrender.com)](https://pagoza.onrender.com)

<p>
  <a href="https://pagoza.readthedocs.io">Docs</a> |
  <a href="https://pagoza.onrender.com/">Live Demo</a>
</p>


________________________________________________
Required installations:

- Node.js (v14 or higher)
  - Download and install from https://nodejs.org/
  - Verify installation by running `node -v` in your terminal.
  - NPM (Node Package Manager) comes bundled with Node.js.
  - Verify installation by running `npm -v` in your terminal.
  - Optional: Install Yarn as an alternative package manager
    - Install via npm: `npm install -g yarn`
    - Verify installation by running `yarn -v` in your terminal.

- Git
  - Download and install from https://git-scm.com/
  - Verify installation by running `git --version` in your terminal.


____________________________________
Required actions:

- Github token setup:
  - Go to your GitHub account settings.
  - Navigate to "Developer settings" > "Personal access tokens".
  - Click on "Generate new token".
  - Select the necessary scopes for your project (read & write access).
    - Contents
    - Issues
    - Pull requests
    - Any additional scopes, eg. workflows
  - Generate the token and copy it securely.
  - Set the token as an environment variable in your terminal:
    - On macOS/Linux: `export PAGOZA_GITHUB_TOKEN=your_token_here`
    - On Windows (Command Prompt): `set PAGOZA_GITHUB_TOKEN=your_token_here`
    - On Windows (PowerShell): `$env:PAGOZA_GITHUB_TOKEN="your_token_here"`


- Clone the repository:
  - Open your terminal.
  - Run the command: `git clone`
  - Navigate into the project directory: `cd your-repo-name`

- Run the following commands to install and initialise the project:
  - `pip install uv` (alternatively: install uv without pip dependencies https://docs.astral.sh/uv/getting-started/installation/)
  - `uv sync` // installs all project dependencies from pyproject.toml
  - `pre-commit` // initialises pre-commit hooks
  - `uv tool install commitizen` // tool install commitizen
  - `git config core.autocrlf false` // optional
  - `uv run pre-commit install --hook-type commit-msg` // checks if exists

- Add any other tools with `uv tool install`
- Add dependencies with `uv add <package>`
- Ensure your .yaml workflows (.readthedocs.yaml, .github/workflows/*.yaml) are configured for your branch if applicable

_____________________________________

- Commiting code:
- Preferably utilise commitizen, instead of raw commits:
  - `git add file`
  - `cz commit`
  - If any problem was found, it should either be fixed by pre-commit, or the commit message was incorrect. In the former case:
    - `git add file` // re-add file, then `cz commit --retry`
  - Otherwise perform new `cz commit` after re-adding files and change the message
- If it is necessary to commit and push due to time constraints, you can get around pre-commit through: `git commit -m "message" --no-verify`

________________________________________________
