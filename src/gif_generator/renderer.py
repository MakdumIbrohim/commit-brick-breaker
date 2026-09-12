from PIL import Image, ImageDraw
from .elements import draw_ambient_background, draw_particles

def get_brick_color(count, theme):
    if count == 0:
        return theme["empty_brick"]
    palette = theme["brick_colors"]
    if count < 3:
        return palette[0]
    if count < 6:
        return palette[1]
    if count < 10:
        return palette[2]
    return palette[3]

def draw_heart(draw, cx, cy, color, size=5):
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
    draw.polygon(coords, fill=color)

def draw_paddle(draw, engine, theme):
    pskin = engine.paddle_skin
    style = pskin.get("style", "default")
    x1, y1 = engine.paddle_x, engine.paddle_y
    x2, y2 = engine.paddle_x + engine.paddle_w, engine.paddle_y + engine.paddle_h
    mid_y = (y1 + y2) / 2
    pw = engine.paddle_w

    if style == "laser":
        cap_w = 7
        draw.rectangle([x1, y1 - 2, x1 + cap_w, y2 + 2], fill=pskin["caps"])
        draw.rectangle([x2 - cap_w, y1 - 2, x2, y2 + 2], fill=pskin["caps"])
        draw.rounded_rectangle([x1 + cap_w, y1, x2 - cap_w, y2], radius=2, fill=pskin["primary"])
        draw.rectangle([x1 + cap_w + 3, mid_y - 1, x2 - cap_w - 3, mid_y + 1], fill=pskin["core"])
        draw.rectangle([x1 + 2, mid_y - 1, x1 + 4, mid_y + 1], fill=(255, 255, 255))
        draw.rectangle([x2 - 4, mid_y - 1, x2 - 2, mid_y + 1], fill=(255, 255, 255))

    elif style == "retro":
        cap_w = 8
        draw.polygon([(x1, y2), (x1 + cap_w, y1), (x1 + cap_w, y2)], fill=pskin["caps"])
        draw.polygon([(x2, y2), (x2 - cap_w, y1), (x2 - cap_w, y2)], fill=pskin["caps"])
        draw.rectangle([x1 + cap_w, y1, x2 - cap_w, y2], fill=pskin["primary"])
        for sx in range(int(x1 + cap_w + 6), int(x2 - cap_w - 6), 12):
            draw.polygon([(sx, y2), (sx + 4, y1), (sx + 8, y1), (sx + 4, y2)], fill=pskin["stripes"])
        draw.rectangle([x1 + cap_w, y1, x2 - cap_w, y1 + 1], fill=(255, 255, 255))

    elif style == "mecha":
        bw = 6
        draw.polygon([(x1, y1 + 2), (x1 + bw, y1 - 1), (x1 + bw, y2 + 1), (x1, y2 - 2)], fill=pskin["booster"])
        draw.polygon([(x2, y1 + 2), (x2 - bw, y1 - 1), (x2 - bw, y2 + 1), (x2, y2 - 2)], fill=pskin["booster"])
        draw.rectangle([x1 + bw, y1, x2 - bw, y2], fill=pskin["primary"])
        cx = (x1 + x2) / 2
        draw.rounded_rectangle([cx - pw * 0.22, y1 - 1, cx + pw * 0.22, y2 + 1], radius=2, fill=pskin["plate"])
        draw.line([(x1 + bw, y1 + 1), (x2 - bw, y1 + 1)], fill=(255, 255, 255), width=1)
        # Multi-layer dual rocket flame thrust (100% attached to booster base)
        flame_h = 5 + (engine.sim_steps % 3) * 2
        # Outer red flame
        draw.polygon([(x1 + 1, y2 - 1), (x1 + bw - 1, y2 - 1), (x1 + bw / 2, y2 + flame_h)], fill=(255, 60, 20))
        draw.polygon([(x2 - 1, y2 - 1), (x2 - bw + 1, y2 - 1), (x2 - bw / 2, y2 + flame_h)], fill=(255, 60, 20))
        # Inner yellow hot flame core
        draw.polygon([(x1 + 2, y2 - 1), (x1 + bw - 2, y2 - 1), (x1 + bw / 2, y2 + flame_h - 2)], fill=(255, 235, 59))
        draw.polygon([(x2 - 2, y2 - 1), (x2 - bw + 2, y2 - 1), (x2 - bw / 2, y2 + flame_h - 2)], fill=(255, 235, 59))

    elif style == "cyber":
        draw.rounded_rectangle([x1, y1, x2, y2], radius=4, fill=pskin["caps"], outline=pskin["primary"], width=1)
        draw.rectangle([x1 + 6, y1 + 2, x2 - 6, y2 - 2], fill=pskin["primary"])
        draw.ellipse([(x1 + x2) / 2 - 4, mid_y - 2, (x1 + x2) / 2 + 4, mid_y + 2], fill=pskin["core"])

    else:
        draw.rounded_rectangle([x1, y1, x2, y2], radius=3, fill=theme["paddle_color"])

def render_frame(engine):
    theme = engine.theme
    img = Image.new("RGB", (engine.canvas_w, engine.canvas_h), theme["bg_color"])
    draw = ImageDraw.Draw(img)

    # 1. Environmental background
    draw_ambient_background(draw, engine, theme)

    # Score preserves accumulated broken bricks across life resets
    draw.text((engine.margin_x, 8), f"SCORE: {engine.score}/{engine.total_bricks}", fill=theme["score_text_color"])

    # 2. Hearts
    heart_start_x = engine.canvas_w - engine.margin_x - (engine.lives * 16)
    for i in range(max(0, engine.lives)):
        draw_heart(draw, heart_start_x + i * 16, 14, color=theme["heart_color"], size=5)

    # 3. Bricks
    for r in range(engine.rows):
        for c in range(engine.cols):
            bx = engine.margin_x + c * engine.cell_w
            by = engine.margin_y + r * engine.cell_h
            if (r, c) in engine.bricks:
                color = get_brick_color(engine.grid[r][c], theme)
                draw.rectangle([bx + 1, by + 1, bx + engine.cell_w - 2, by + engine.cell_h - 2], fill=color)
            elif (r, c) in engine.shattering_bricks:
                # Elemental transition state before disappearing
                sh = engine.shattering_bricks[(r, c)]
                elem = sh["elem"]
                prog = 1.0 - (sh["timer"] / sh["max"])
                if elem == "ice":
                    # Freezing ice crystal block
                    draw.rectangle([bx + 1, by + 1, bx + engine.cell_w - 2, by + engine.cell_h - 2], fill=(175, 238, 255), outline=(240, 250, 255), width=1)
                elif elem == "fire":
                    # Glowing molten burning block
                    burn_col = (255, int(140 * (1 - prog)), 0)
                    draw.rectangle([bx + 1, by + 1, bx + engine.cell_w - 2, by + engine.cell_h - 2], fill=burn_col)
                elif elem == "lightning":
                    # Electrified flashing block
                    flash = (255, 255, 150) if sh["timer"] % 2 == 0 else (200, 100, 255)
                    draw.rectangle([bx + 1, by + 1, bx + engine.cell_w - 2, by + engine.cell_h - 2], fill=flash)
                elif elem == "poison":
                    # Acid dissolving melted block
                    draw.rectangle([bx + 1, by + 1 + int(prog * 4), bx + engine.cell_w - 2, by + engine.cell_h - 2], fill=(40, 180, 60))
                else:
                    draw.rectangle([bx + 1, by + 1, bx + engine.cell_w - 2, by + engine.cell_h - 2], fill=(200, 200, 200))
            else:
                draw.rectangle([bx + 1, by + 1, bx + engine.cell_w - 2, by + engine.cell_h - 2], fill=theme["empty_brick"])

    # 4. Particles
    draw_particles(draw, engine.particles)

    # 5. Motion trail
    if engine.skin.get("trail_color"):
        for i, (tx, ty) in enumerate(engine.trail):
            r = max(1, engine.ball_r - (len(engine.trail) - i))
            draw.ellipse([tx - r, ty - r, tx + r, ty + r], fill=engine.skin["trail_color"])

    # 6. Paddle
    draw_paddle(draw, engine, theme)

    # 7. Ball
    if engine.state in ("playing", "win") or (engine.state == "life_lost" and engine.state_timer > 4):
        draw.ellipse(
            [engine.ball_x - engine.ball_r, engine.ball_y - engine.ball_r,
             engine.ball_x + engine.ball_r, engine.ball_y + engine.ball_r],
            fill=engine.skin["color"]
        )

    # 8. Banners
    if engine.state == "win":
        draw.rectangle([engine.canvas_w / 2 - 90, engine.canvas_h / 2 - 18, engine.canvas_w / 2 + 90, engine.canvas_h / 2 + 18], fill=theme["banner_bg_color"])
        draw.text((engine.canvas_w / 2 - 60, engine.canvas_h / 2 - 8), "STAGE CLEARED!", fill=theme["win_text_color"])
    elif engine.state == "game_over":
        draw.rectangle([engine.canvas_w / 2 - 80, engine.canvas_h / 2 - 18, engine.canvas_w / 2 + 80, engine.canvas_h / 2 + 18], fill=theme["banner_bg_color"])
        draw.text((engine.canvas_w / 2 - 45, engine.canvas_h / 2 - 8), "GAME OVER", fill=theme["lose_text_color"])

    return img

def render_gif(engine, output_path="game.gif", max_frames=3000):
    frames = []
    while len(engine.bricks) > 0 and len(frames) < max_frames:
        engine.step()
        frames.append(render_frame(engine))

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
