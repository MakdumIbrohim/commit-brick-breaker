from PIL import Image, ImageDraw
from src.config import (
    BG_COLOR, PADDLE_COLOR, BALL_COLOR, EMPTY_BRICK,
    HEART_COLOR, SCORE_TEXT_COLOR, BANNER_BG_COLOR,
    WIN_TEXT_COLOR, LOSE_TEXT_COLOR
)

def get_brick_color(count):
    if count == 0:
        return EMPTY_BRICK
    if count < 3:
        return (14, 68, 41)
    if count < 6:
        return (0, 109, 50)
    if count < 10:
        return (38, 166, 65)
    return (57, 211, 83)

def draw_heart(draw, cx, cy, size=5):
    coords = [
        (cx, cy + size),
        (cx - size, cy),
        (cx - size, cy - size // 2),
        (cx - size // 2, cy - size),
        (cx, cy - size // 2),
        (cx + size // 2, cy - size),
        (cx + size, cy - size // 2),
        (cx + size, cy),
    ]
    draw.polygon(coords, fill=HEART_COLOR)

def render_frame(engine):
    img = Image.new("RGB", (engine.canvas_w, engine.canvas_h), BG_COLOR)
    draw = ImageDraw.Draw(img)

    score = engine.total_bricks - len(engine.bricks)
    draw.text((engine.margin_x, 8), f"SCORE: {score}/{engine.total_bricks}", fill=SCORE_TEXT_COLOR)

    # Render remaining life hearts
    heart_start_x = engine.canvas_w - engine.margin_x - (engine.lives * 16)
    for i in range(max(0, engine.lives)):
        draw_heart(draw, heart_start_x + i * 16, 14, size=5)

    # Render active bricks
    for r in range(engine.rows):
        for c in range(engine.cols):
            bx = engine.margin_x + c * engine.cell_w
            by = engine.margin_y + r * engine.cell_h
            color = get_brick_color(engine.grid[r][c]) if (r, c) in engine.bricks else EMPTY_BRICK
            draw.rectangle([bx + 1, by + 1, bx + engine.cell_w - 2, by + engine.cell_h - 2], fill=color)

    # Render specialized element particles
    for p in engine.particles:
        px, py = p["x"], p["y"]
        sz = p["size"]
        col = p["color"]
        ptype = p.get("type", "debris")

        if ptype == "snowflake":
            # Cross snowflake shape (+)
            draw.line([(px - sz, py), (px + sz, py)], fill=col, width=1)
            draw.line([(px, py - sz), (px, py + sz)], fill=col, width=1)
        elif ptype == "crystal":
            # Diamond frost crystal
            draw.polygon([(px, py - sz), (px + sz, py), (px, py + sz), (px - sz, py)], fill=col)
        elif ptype == "ember":
            # Glowing ember round particle
            draw.ellipse([px - sz, py - sz, px + sz, py + sz], fill=col)
        elif ptype == "spark":
            # Sharp spark line along trajectory
            draw.line([(px, py), (px - p["vx"] * 1.5, py - p["vy"] * 1.5)], fill=col, width=1)
        elif ptype == "bubble":
            # Hollow translucent bubble
            draw.ellipse([px - sz, py - sz, px + sz, py + sz], outline=col, width=1)
        elif ptype == "zap":
            # Jagged lightning branch
            draw.line([(px, py), (px + p["vx"], py + p["vy"])], fill=col, width=1)
        else:
            draw.rectangle([px - 1, py - 1, px + 1, py + 1], fill=col)

    # Render paddle
    draw.rounded_rectangle(
        [engine.paddle_x, engine.paddle_y, engine.paddle_x + engine.paddle_w, engine.paddle_y + engine.paddle_h],
        radius=3, fill=PADDLE_COLOR
    )

    # Render motion trail for ball skin
    if engine.skin.get("trail_color"):
        for i, (tx, ty) in enumerate(engine.trail):
            r = max(1, engine.ball_r - (len(engine.trail) - i))
            draw.ellipse([tx - r, ty - r, tx + r, ty + r], fill=engine.skin["trail_color"])

    # Render ball
    if engine.state in ("playing", "win") or (engine.state == "life_lost" and engine.state_timer > 4):
        draw.ellipse(
            [engine.ball_x - engine.ball_r, engine.ball_y - engine.ball_r,
             engine.ball_x + engine.ball_r, engine.ball_y + engine.ball_r],
            fill=engine.skin["color"]
        )

    # Game status banners
    if engine.state == "win":
        draw.rectangle([engine.canvas_w / 2 - 90, engine.canvas_h / 2 - 18, engine.canvas_w / 2 + 90, engine.canvas_h / 2 + 18], fill=BANNER_BG_COLOR)
        draw.text((engine.canvas_w / 2 - 60, engine.canvas_h / 2 - 8), "STAGE CLEARED!", fill=WIN_TEXT_COLOR)
    elif engine.state == "game_over":
        draw.rectangle([engine.canvas_w / 2 - 80, engine.canvas_h / 2 - 18, engine.canvas_w / 2 + 80, engine.canvas_h / 2 + 18], fill=BANNER_BG_COLOR)
        draw.text((engine.canvas_w / 2 - 45, engine.canvas_h / 2 - 8), "GAME OVER", fill=LOSE_TEXT_COLOR)

    return img

def render_gif(engine, output_path="game.gif", max_frames=3000):
    frames = []
    # Jalankan simulasi sampai SELURUH balok hancur (0 tersisa)
    while len(engine.bricks) > 0 and len(frames) < max_frames:
        engine.step()
        frames.append(render_frame(engine))

    # Tampilkan banner STAGE CLEARED! sebelum animasi loop ulang
    engine.state = "win"
    for _ in range(25):
        engine.step()
        frames.append(render_frame(engine))

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=36,
        loop=0,
        optimize=True
    )
    print(f"Generated {output_path} ({len(frames)} frames), remaining: {len(engine.bricks)}, lives: {engine.lives}")
