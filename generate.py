import os
import sys
from src.fetcher import fetch_contributions
from src.engine import BrickBreakerEngine
from src.gif_generator import render_gif
from src.svg_generator import render_svg
from src.config import DEFAULT_SKIN, DEFAULT_THEME, DEFAULT_PADDLE_SKIN


def clean_arg(val):
    if not val:
        return val
    # Strip inline YAML comments like 'value # comment'
    return val.split("#")[0].strip()


def main():
    raw_user = (
        sys.argv[1] if len(sys.argv) > 1 else os.getenv("GITHUB_ACTOR", "MakdumIbrohim")
    )
    raw_output = sys.argv[2] if len(sys.argv) > 2 else "game.svg"
    raw_skin = (
        sys.argv[3] if len(sys.argv) > 3 else os.getenv("BALL_SKIN", DEFAULT_SKIN)
    )
    raw_theme = sys.argv[4] if len(sys.argv) > 4 else os.getenv("THEME", DEFAULT_THEME)
    raw_paddle = (
        sys.argv[5]
        if len(sys.argv) > 5
        else os.getenv("PADDLE_SKIN", DEFAULT_PADDLE_SKIN)
    )

    username = clean_arg(raw_user) or "MakdumIbrohim"
    output_path = clean_arg(raw_output) or "game.svg"
    skin = clean_arg(raw_skin) or DEFAULT_SKIN
    theme = clean_arg(raw_theme) or DEFAULT_THEME
    paddle_skin = clean_arg(raw_paddle) or DEFAULT_PADDLE_SKIN
    token = os.getenv("GITHUB_TOKEN", None)

    grid = fetch_contributions(username, token)
    engine = BrickBreakerEngine(grid, skin=skin, theme=theme, paddle_skin=paddle_skin)

    # Pilih generator berdasarkan ekstensi file output (.svg atau .gif)
    if output_path.lower().endswith(".svg"):
        render_svg(engine, output_path=output_path)
    else:
        render_gif(engine, output_path=output_path)


if __name__ == "__main__":
    main()
