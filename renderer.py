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
    draw.text((engine.margin_x, 10), f"GH-BRICK-BREAKER • SCORE: {score}", fill=(139, 148, 158))

    for r in range(engine.rows):
        for c in range(engine.cols):
            bx = engine.margin_x + c * engine.cell_w
            by = engine.margin_y + r * engine.cell_h
            color = get_brick_color(engine.grid[r][c]) if (r, c) in engine.bricks else EMPTY_BRICK
            draw.rectangle([bx + 1, by + 1, bx + engine.cell_w - 2, by + engine.cell_h - 2], fill=color)

    draw.rounded_rectangle(
        [engine.paddle_x, engine.paddle_y, engine.paddle_x + engine.paddle_w, engine.paddle_y + engine.paddle_h],
        radius=3, fill=PADDLE_COLOR
    )
    draw.ellipse(
        [engine.ball_x - engine.ball_r, engine.ball_y - engine.ball_r,
         engine.ball_x + engine.ball_r, engine.ball_y + engine.ball_r],
        fill=BALL_COLOR
    )
    return img

def render_gif(engine, output_path="game.gif", frames_count=120):
    frames = []
    for _ in range(frames_count):
        engine.step()
        frames.append(render_frame(engine))

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=40,
        loop=0,
        optimize=True
    )
    print(f"Generated {output_path} ({len(frames)} frames)")
