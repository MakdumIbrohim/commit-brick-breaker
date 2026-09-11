# Contributing to Commit Brick Breaker

Thank you for your interest in contributing to Commit Brick Breaker! We welcome contributions for new elemental ball skins, paddle models, animated board themes, bug fixes, and performance improvements.

## Code of Conduct
Please be respectful, constructive, and collaborative in all issues and pull requests.

## How to Contribute

### 1. Fork & Clone
Fork this repository to your GitHub account and clone it locally:
```bash
git clone https://github.com/<your-username>/commit-brick-breaker.git
cd commit-brick-breaker
pip install pillow
```

### 2. Branching Strategy
Always create a descriptive branch for your work:
```bash
git checkout -b feature/awesome-new-skin
# or
git checkout -b fix/collision-detection
```

### 3. Architecture & Guidelines
- **Adding Ball / Paddle Skins:** Register parameters in `src/config.py`, emit particles in `src/particles.py`, and implement rendering in `src/renderer.py`.
- **Adding Board Themes:** Define palettes and triggers in `src/config.py`, and implement environmental drawing logic in `src/ambient.py`.
- **Lightweight Dependencies:** Keep the project minimal. `Pillow` is the only allowed external dependency. Do not introduce heavy libraries.
- **Local Testing:** Always test the generated GIF locally across different accounts, themes, and skins before opening a PR:
  ```bash
  python generate.py <username> test.gif [skin] [theme] [paddle_skin]
  ```

### 4. Commit Messages
Follow the Conventional Commits specification:
- `feat: ...` for new features, skins, or themes
- `fix: ...` for bug fixes and physics corrections
- `docs: ...` for documentation updates
- `refactor: ...` for code cleanup without functional changes

### 5. Submitting a Pull Request
1. Push your branch to your fork.
2. Open a Pull Request targeting the `main` branch.
3. Provide a clear description of your changes and attach a sample preview GIF if you introduced visual modifications.
