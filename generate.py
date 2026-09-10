import os
import sys
import math
import random
import urllib.request
import json
from PIL import Image, ImageDraw

def fetch_contributions(username, token=None):
    # ponytail: GraphQL real GitHub query ceiling, fallback mock grid if offline/no-token
    if token:
        query = """
        query($username: String!) {
          user(login: $username) {
            contributionsCollection {
              contributionCalendar {
                weeks {
                  contributionDays {
                    contributionCount
                    date
                  }
                }
              }
            }
          }
        }
        """
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": query, "variables": {"username": username}}).encode("utf-8"),
            headers={"Authorization": f"Bearer {token}", "User-Agent": "gh-brick-breaker"}
        )
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
                # Ambil 20 minggu terakhir
                recent = weeks[-20:]
                grid = []
                for d in range(7):
                    row = []
                    for w in recent:
                        if d < len(w["contributionDays"]):
                            row.append(w["contributionDays"][d]["contributionCount"])
                        else:
                            row.append(0)
                    grid.append(row)
                return grid
        except Exception as e:
            print(f"Fetch failed ({e}), using fallback grid.")

    # Fallback / mockup grid (7 rows x 20 cols)
    random.seed(42)
    return [[random.choice([0, 1, 2, 4, 8]) for _ in range(20)] for _ in range(7)]

def generate_game_gif(output_path="game.gif", username="MakdumIbrohim", token=None):
    grid = fetch_contributions(username, token)
    rows = len(grid)
    cols = len(grid[0])

    # Canvas config
    cell_w, cell_h = 24, 12
    margin_x, margin_y = 20, 30
    canvas_w = margin_x * 2 + cols * cell_w
    canvas_h = 260

    # Colors
    bg_color = (13, 17, 23)
    paddle_color = (88, 166, 255)
    ball_color = (240, 246, 252)
    empty_brick = (22, 27, 34)

    def brick_color(count):
        if count == 0:
            return empty_brick
        if count < 3:
            return (14, 68, 41)
        if count < 6:
            return (0, 109, 50)
        if count < 10:
            return (38, 166, 65)
        return (57, 211, 83)

    # Convert grid to active bricks: { (r, c): count }
    bricks = {(r, c): grid[r][c] for r in range(rows) for c in range(cols) if grid[r][c] > 0}
    total_bricks = len(bricks)

    # Paddle & Ball initial
    paddle_w, paddle_h = 70, 8
    paddle_y = canvas_h - 25
    paddle_x = canvas_w / 2 - paddle_w / 2

    ball_r = 4
    ball_x = canvas_w / 2
    ball_y = paddle_y - ball_r - 2
    speed = 6.0
    angle = -random.uniform(math.pi * 0.25, math.pi * 0.75)
    vx = speed * math.cos(angle)
    vy = speed * math.sin(angle)

    frames = []
    max_frames = 120

    for frame_idx in range(max_frames):
        # Move ball
        ball_x += vx
        ball_y += vy

        # Wall collisions
        if ball_x - ball_r <= margin_x:
            ball_x = margin_x + ball_r
            vx = abs(vx)
        elif ball_x + ball_r >= canvas_w - margin_x:
            ball_x = canvas_w - margin_x - ball_r
            vx = -abs(vx)

        if ball_y - ball_r <= 10:
            ball_y = 10 + ball_r
            vy = abs(vy)

        # Paddle track ball (AI paddle)
        target_px = ball_x - paddle_w / 2
        paddle_x += (target_px - paddle_x) * 0.35
        paddle_x = max(margin_x, min(canvas_w - margin_x - paddle_w, paddle_x))

        # Paddle collision
        if vy > 0 and (paddle_y <= ball_y + ball_r <= paddle_y + paddle_h + 4):
            if paddle_x - 5 <= ball_x <= paddle_x + paddle_w + 5:
                vy = -abs(vy)
                offset = (ball_x - (paddle_x + paddle_w / 2)) / (paddle_w / 2)
                vx = speed * offset * 1.2

        # Floor reset if ball misses
        if ball_y > canvas_h:
            ball_x = paddle_x + paddle_w / 2
            ball_y = paddle_y - ball_r - 2
            vy = -abs(speed)

        # Brick collision check
        col_hit = int((ball_x - margin_x) // cell_w)
        row_hit = int((ball_y - margin_y) // cell_h)
        if (row_hit, col_hit) in bricks:
            del bricks[(row_hit, col_hit)]
            vy = -vy

        # Draw frame
        img = Image.new("RGB", (canvas_w, canvas_h), bg_color)
        draw = ImageDraw.Draw(img)

        # Header / title
        draw.text((margin_x, 10), f"GH-BRICK-BREAKER • SCORE: {total_bricks - len(bricks)}", fill=(139, 148, 158))

        # Draw bricks
        for r in range(rows):
            for c in range(cols):
                bx = margin_x + c * cell_w
                by = margin_y + r * cell_h
                color = brick_color(grid[r][c]) if (r, c) in bricks else empty_brick
                draw.rectangle([bx + 1, by + 1, bx + cell_w - 2, by + cell_h - 2], fill=color)

        # Draw paddle
        draw.rounded_rectangle([paddle_x, paddle_y, paddle_x + paddle_w, paddle_y + paddle_h], radius=3, fill=paddle_color)

        # Draw ball
        draw.ellipse([ball_x - ball_r, ball_y - ball_r, ball_x + ball_r, ball_y + ball_r], fill=ball_color)

        frames.append(img)

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=40,
        loop=0,
        optimize=True
    )
    print(f"Generated {output_path} ({len(frames)} frames)")

if __name__ == "__main__":
    uname = sys.argv[1] if len(sys.argv) > 1 else os.getenv("GITHUB_ACTOR", "MakdumIbrohim")
    tok = os.getenv("GITHUB_TOKEN", None)
    out = sys.argv[2] if len(sys.argv) > 2 else "game.gif"
    generate_game_gif(out, uname, tok)
