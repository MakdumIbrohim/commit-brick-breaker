from PIL import Image, ImageDraw

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

def render_frame(engine):
    theme = engine.theme
    img = Image.new("RGB", (engine.canvas_w, engine.canvas_h), theme["bg_color"])
    draw = ImageDraw.Draw(img)

    score = engine.total_bricks - len(engine.bricks)
    draw.text((engine.margin_x, 8), f"SCORE: {score}/{engine.total_bricks}", fill=theme["score_text_color"])

    # Render remaining life hearts
    heart_start_x = engine.canvas_w - engine.margin_x - (engine.lives * 16)
    for i in range(max(0, engine.lives)):
        draw_heart(draw, heart_start_x + i * 16, 14, color=theme["heart_color"], size=5)

    # Render active bricks
    for r in range(engine.rows):
        for c in range(engine.cols):
            bx = engine.margin_x + c * engine.cell_w
            by = engine.margin_y + r * engine.cell_h
            color = get_brick_color(engine.grid[r][c], theme) if (r, c) in engine.bricks else theme["empty_brick"]
            draw.rectangle([bx + 1, by + 1, bx + engine.cell_w - 2, by + engine.cell_h - 2], fill=color)

    # Render specialized element particles
    for p in engine.particles:
        px, py = p["x"], p["y"]
        sz = p["size"]
        col = p["color"]
        ptype = p.get("type", "debris")

        if ptype == "snowflake":
            draw.line([(px - sz, py), (px + sz, py)], fill=col, width=1)
            draw.line([(px, py - sz), (px, py + sz)], fill=col, width=1)
        elif ptype == "crystal":
            draw.polygon([(px, py - sz), (px + sz, py), (px, py + sz), (px - sz, py)], fill=col)
        elif ptype == "ember":
            draw.ellipse([px - sz, py - sz, px + sz, py + sz], fill=col)
        elif ptype == "spark":
            draw.line([(px, py), (px - p["vx"] * 1.5, py - p["vy"] * 1.5)], fill=col, width=1)
        elif ptype == "bubble":
            draw.ellipse([px - sz, py - sz, px + sz, py + sz], outline=col, width=1)
        elif ptype == "zap":
            draw.line([(px, py), (px + p["vx"], py + p["vy"])], fill=col, width=1)
        elif ptype == "thrust":
            # Mecha rocket flame jet
            draw.polygon([(px - sz, py), (px + sz, py), (px, py + sz * 2.5)], fill=col)
        elif ptype == "energy":
            # Laser power discharge dot
            draw.ellipse([px - sz, py - sz, px + sz, py + sz], fill=col)
        elif ptype == "pixel":
            # 8-bit square digital pixel
            draw.rectangle([px - sz, py - sz, px + sz, py + sz], fill=col)
        else:
            draw.rectangle([px - 1, py - 1, px + 1, py + 1], fill=col)

    # Render motion trail for ball skin
    if engine.skin.get("trail_color"):
        for i, (tx, ty) in enumerate(engine.trail):
            r = max(1, engine.ball_r - (len(engine.trail) - i))
            draw.ellipse([tx - r, ty - r, tx + r, ty + r], fill=engine.skin["trail_color"])

    # Render paddle with custom geometric design and structural details
    pskin = engine.paddle_skin
    style = pskin.get("style", "default")
    x1, y1 = engine.paddle_x, engine.paddle_y
    x2, y2 = engine.paddle_x + engine.paddle_w, engine.paddle_y + engine.paddle_h
    mid_y = (y1 + y2) / 2
    pw = engine.paddle_w

    if style == "laser":
        # Sci-Fi Laser Rail: dual heavy battery end-caps + glowing plasma chamber
        cap_w = 7
        draw.rectangle([x1, y1 - 2, x1 + cap_w, y2 + 2], fill=pskin["caps"])
        draw.rectangle([x2 - cap_w, y1 - 2, x2, y2 + 2], fill=pskin["caps"])
        draw.rounded_rectangle([x1 + cap_w, y1, x2 - cap_w, y2], radius=2, fill=pskin["primary"])
        draw.rectangle([x1 + cap_w + 3, mid_y - 1, x2 - cap_w - 3, mid_y + 1], fill=pskin["core"])
        # Emitter tip dots
        draw.rectangle([x1 + 2, mid_y - 1, x1 + 4, mid_y + 1], fill=(255, 255, 255))
        draw.rectangle([x2 - 4, mid_y - 1, x2 - 2, mid_y + 1], fill=(255, 255, 255))

    elif style == "retro":
        # 8-bit Arcade Segmented Bar: angled bumpers, hazard striping, bolt studs
        cap_w = 8
        draw.polygon([(x1, y2), (x1 + cap_w, y1), (x1 + cap_w, y2)], fill=pskin["caps"])
        draw.polygon([(x2, y2), (x2 - cap_w, y1), (x2 - cap_w, y2)], fill=pskin["caps"])
        draw.rectangle([x1 + cap_w, y1, x2 - cap_w, y2], fill=pskin["primary"])
        # Racing / Hazard stripes
        for sx in range(int(x1 + cap_w + 6), int(x2 - cap_w - 6), 12):
            draw.polygon([(sx, y2), (sx + 4, y1), (sx + 8, y1), (sx + 4, y2)], fill=pskin["stripes"])
        draw.rectangle([x1 + cap_w, y1, x2 - cap_w, y1 + 1], fill=(255, 255, 255))

    elif style == "mecha":
        # Armored Mecha Rail: segmented steel plates + red rocket thrusters at flanks
        bw = 6
        # Left and right red booster jets
        draw.polygon([(x1, y1 + 2), (x1 + bw, y1 - 1), (x1 + bw, y2 + 1), (x1, y2 - 2)], fill=pskin["booster"])
        draw.polygon([(x2, y1 + 2), (x2 - bw, y1 - 1), (x2 - bw, y2 + 1), (x2, y2 - 2)], fill=pskin["booster"])
        # Heavy armor body
        draw.rectangle([x1 + bw, y1, x2 - bw, y2], fill=pskin["primary"])
        # Center reinforced armor plate
        cx = (x1 + x2) / 2
        draw.rounded_rectangle([cx - pw * 0.22, y1 - 1, cx + pw * 0.22, y2 + 1], radius=2, fill=pskin["plate"])
        draw.line([(x1 + bw, y1 + 1), (x2 - bw, y1 + 1)], fill=(255, 255, 255), width=1)

    elif style == "cyber":
        # Synthwave Cyber Rail: neon gradient border, power conduits, luminous cyan diode
        draw.rounded_rectangle([x1, y1, x2, y2], radius=4, fill=pskin["caps"], outline=pskin["primary"], width=1)
        # Inner energy conduit
        draw.rectangle([x1 + 6, y1 + 2, x2 - 6, y2 - 2], fill=pskin["primary"])
        # Central glowing diode chip
        draw.ellipse([(x1 + x2) / 2 - 4, mid_y - 2, (x1 + x2) / 2 + 4, mid_y + 2], fill=pskin["core"])

    else:
        # Default smooth pill paddle
        draw.rounded_rectangle([x1, y1, x2, y2], radius=3, fill=theme["paddle_color"])

    # Render ball
    if engine.state in ("playing", "win") or (engine.state == "life_lost" and engine.state_timer > 4):
        draw.ellipse(
            [engine.ball_x - engine.ball_r, engine.ball_y - engine.ball_r,
             engine.ball_x + engine.ball_r, engine.ball_y + engine.ball_r],
            fill=engine.skin["color"]
        )

    # Game status banners
    if engine.state == "win":
        draw.rectangle([engine.canvas_w / 2 - 90, engine.canvas_h / 2 - 18, engine.canvas_w / 2 + 90, engine.canvas_h / 2 + 18], fill=theme["banner_bg_color"])
        draw.text((engine.canvas_w / 2 - 60, engine.canvas_h / 2 - 8), "STAGE CLEARED!", fill=theme["win_text_color"])
    elif engine.state == "game_over":
        draw.rectangle([engine.canvas_w / 2 - 80, engine.canvas_h / 2 - 18, engine.canvas_w / 2 + 80, engine.canvas_h / 2 + 18], fill=theme["banner_bg_color"])
        draw.text((engine.canvas_w / 2 - 45, engine.canvas_h / 2 - 8), "GAME OVER", fill=theme["lose_text_color"])

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
