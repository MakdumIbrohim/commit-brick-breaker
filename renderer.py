from PIL import Image, ImageDraw

BG_COLOR = (13, 17, 23)
PADDLE_COLOR = (88, 166, 255)
BALL_COLOR = (240, 246, 252)
EMPTY_BRICK = (22, 27, 34)

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

def render_frame(engine):
    img = Image.new("RGB", (engine.canvas_w, engine.canvas_h), BG_COLOR)
    draw = ImageDraw.Draw(img)

    score = engine.total_bricks - len(engine.bricks)
    lives_text = "♥ " * engine.lives

    # Header info
    draw.text((engine.margin_x, 8), f"SCORE: {score}", fill=(139, 148, 158))
    draw.text((engine.canvas_w - engine.margin_x - 70, 8), lives_text, fill=(248, 81, 73))

    # Draw bricks
    for r in range(engine.rows):
        for c in range(engine.cols):
            bx = engine.margin_x + c * engine.cell_w
            by = engine.margin_y + r * engine.cell_h
            color = get_brick_color(engine.grid[r][c]) if (r, c) in engine.bricks else EMPTY_BRICK
            draw.rectangle([bx + 1, by + 1, bx + engine.cell_w - 2, by + engine.cell_h - 2], fill=color)

    # Draw particles (hancuran balok / bola jatuh)
    for p in engine.particles:
        draw.rectangle([p["x"] - 1, p["y"] - 1, p["x"] + 1, p["y"] + 1], fill=p["color"])

    # Draw paddle
    draw.rounded_rectangle(
        [engine.paddle_x, engine.paddle_y, engine.paddle_x + engine.paddle_w, engine.paddle_y + engine.paddle_h],
        radius=3, fill=PADDLE_COLOR
    )

    # Draw ball (hanya jika sedang playing atau ada di layar)
    if engine.state in ("playing", "win") or (engine.state == "life_lost" and engine.state_timer > 5):
        draw.ellipse(
            [engine.ball_x - engine.ball_r, engine.ball_y - engine.ball_r,
             engine.ball_x + engine.ball_r, engine.ball_y + engine.ball_r],
            fill=BALL_COLOR
        )

    # Banner teks saat kalah atau menang
    if engine.state == "game_over":
        draw.rectangle([engine.canvas_w / 2 - 80, engine.canvas_h / 2 - 16, engine.canvas_w / 2 + 80, engine.canvas_h / 2 + 16], fill=(30, 30, 30))
        draw.text((engine.canvas_w / 2 - 50, engine.canvas_h / 2 - 8), "GAME OVER", fill=(248, 81, 73))
    elif engine.state == "win":
        draw.rectangle([engine.canvas_w / 2 - 80, engine.canvas_h / 2 - 16, engine.canvas_w / 2 + 80, engine.canvas_h / 2 + 16], fill=(30, 30, 30))
        draw.text((engine.canvas_w / 2 - 55, engine.canvas_h / 2 - 8), "STAGE CLEAR!", fill=(57, 211, 83))

    return img

def render_gif(engine, output_path="game.gif", frames_count=180):
    frames = []
    for _ in range(frames_count):
        engine.step()
        frames.append(render_frame(engine))

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=35,
        loop=0,
        optimize=True
    )
    print(f"Generated {output_path} ({len(frames)} frames)")
