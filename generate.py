import os
import sys
from src.fetcher import fetch_contributions
from src.engine import BrickBreakerEngine
from src.renderer import render_gif
from src.config import DEFAULT_SKIN, DEFAULT_THEME

def main():
    username = sys.argv[1] if len(sys.argv) > 1 else os.getenv("GITHUB_ACTOR", "MakdumIbrohim")
    token = os.getenv("GITHUB_TOKEN", None)
    output_path = sys.argv[2] if len(sys.argv) > 2 else "game.gif"
    skin = sys.argv[3] if len(sys.argv) > 3 else os.getenv("BALL_SKIN", DEFAULT_SKIN)
    theme = sys.argv[4] if len(sys.argv) > 4 else os.getenv("THEME", DEFAULT_THEME)

    grid = fetch_contributions(username, token)
    engine = BrickBreakerEngine(grid, skin=skin, theme=theme)
    render_gif(engine, output_path=output_path)

if __name__ == "__main__":
    main()
