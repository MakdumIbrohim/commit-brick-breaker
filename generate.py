import os
import sys
from src.fetcher import fetch_contributions
from src.engine import BrickBreakerEngine
from src.gif_generator import render_gif
from src.svg_generator import render_svg
from src.config import DEFAULT_SKIN, DEFAULT_THEME, DEFAULT_PADDLE_SKIN

def main():
    username = sys.argv[1] if len(sys.argv) > 1 else os.getenv("GITHUB_ACTOR", "MakdumIbrohim")
    token = os.getenv("GITHUB_TOKEN", None)
    output_path = sys.argv[2] if len(sys.argv) > 2 else "game.gif"
    skin = sys.argv[3] if len(sys.argv) > 3 else os.getenv("BALL_SKIN", DEFAULT_SKIN)
    theme = sys.argv[4] if len(sys.argv) > 4 else os.getenv("THEME", DEFAULT_THEME)
    paddle_skin = sys.argv[5] if len(sys.argv) > 5 else os.getenv("PADDLE_SKIN", DEFAULT_PADDLE_SKIN)

    grid = fetch_contributions(username, token)
    engine = BrickBreakerEngine(grid, skin=skin, theme=theme, paddle_skin=paddle_skin)

    # Choose generator by output file extension (.svg or .gif)
    if output_path.lower().endswith(".svg"):
        render_svg(engine, output_path=output_path)
    else:
        render_gif(engine, output_path=output_path)

if __name__ == "__main__":
    main()
