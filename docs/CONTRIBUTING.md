# Contribution Guildelines



## Introduction

Welcome, brave contributor!

This project is Plants vs Zombies: Shattered Universe, a Plants vs Zombies-esque tower defense built using Pygame. Whether you're a coder, artist, bux fixer, or just someone with cool ideas, you're welcome here.

Before you dive in, please read these guidelines to make sure your contributions align with the project goals and standards.



## How to Contribute

To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b my-cool-feature`
3. Make your changes.
4. Test thoroughly.
5. Commit with clear messages.
6. Push and create a Pull Request (PR).

Make sure your PR describes:
- What the change is
- Why it was made
- Any related issues or discussions



## Code Style and Standards

- Try your best to follow [PEP8](https://peps.python.org/pep-0008/) (Python Style Guide)
- Use `snake_case` for variables and functions, `PascalCase` for class names
- Avoid deep nesting (> 3 levels)
- Add one or more comments where logic is complex
- Write [docstrings](https://en.wikipedia.org/wiki/Docstring) for complex classes or functions
- Limit lines to 150 characters



## Testing & Validation

- Run the game to make sure it still starts and loads correctly
- Test your feature thoroughly in both development and in-game contexts
- If you're fixing a bug, explain how to reproduce the issue before and after your fix
- You can take screenshots in-game by pressing the F12 key



## Directory & File Structure

- `Root\` - all code goes there
- - `Root\ASSETS\` - sprites, sounds, music, etc.
- - `Root\TOOLS\` - not to be confused with `Root\utils.py`, tools provide various helper scripts for testing performance
- - `Root\SCREENSHOTS\` - screenshots taken will be automatically placed there. You can take screenshots in-game via the F12 key



## Code of Construct

We follow the [Contributor Covenant](https://www.contributor-covenant.org/](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).



## Where to Ask Questions

- Issues tab on GitHub

Please be patient with responses; this is a passion project maintained in spare time!



## Issue and PR Etiquette

- Tag your PRs (e.g., `[Bugfix]`, `[Feature]`, `[Docs]`)
- Don't open PRs for half-done work unless you're requesting early feedback (label it as a Draft!)
- Link to any relevant issues using `#issue-number`
