from .keyframes import (
    build_svg_keyframes,
    calculate_brick_lifetimes,
    build_trail_keyframes,
    build_particle_keyframes,
)
from .elements import (
    rgb_to_hex,
    get_heart_svg_path,
    generate_particle_svg_node,
    generate_ambient_svg,
    generate_paddle_svg,
)

def render_svg(engine, output_path="game.svg", max_frames=2000):
    theme = engine.theme
    history = []
    step_idx = 0

    brick_hit_map = {}
    frame_idx = 0

    while len(engine.bricks) > 0 and len(history) < max_frames:
        engine.step()

        # Record exact frame where each brick is struck by ball
        for hit_rc in getattr(engine, "destroyed_this_step", []):
            if hit_rc not in brick_hit_map:
                brick_hit_map[hit_rc] = frame_idx

        active_p = []
        for p in engine.particles[:18]:
            active_p.append({
                "x": round(p["x"], 1),
                "y": round(p["y"], 1),
                "color": rgb_to_hex(p.get("color", (255, 255, 255))),
                "size": p.get("size", 2),
                "type": p.get("type", "debris")
            })

        trail_pts = [(round(tx, 1), round(ty, 1)) for tx, ty in engine.trail]

        history.append({
            "bx": round(engine.ball_x, 1),
            "by": round(engine.ball_y, 1),
            "px": round(engine.paddle_x, 1),
            "py": round(engine.paddle_y, 1),
            "trail": trail_pts,
            "particles": active_p,
            "destroyed": list(engine.bricks.keys()),
            "lives": max(0, engine.lives),
            "score": engine.score,
            "state": engine.state
        })
        frame_idx += 1

    for _ in range(15):
        history.append({
            "bx": round(engine.ball_x, 1),
            "by": round(engine.ball_y, 1),
            "px": round(engine.paddle_x, 1),
            "py": round(engine.paddle_y, 1),
            "trail": [],
            "particles": [],
            "destroyed": [],
            "lives": max(0, engine.lives),
            "score": engine.total_bricks,
            "state": "win"
        })

    total_frames = len(history)
    duration_sec = round(total_frames * 0.035, 1)

    ball_kf, paddle_kf = build_svg_keyframes(history, total_frames)

    # Compute exact hit percentages for each brick
    brick_timing_map = {}
    shatter_phase_pct = round((4 / max(1, total_frames)) * 100, 2)
    for rc, hit_frame in brick_hit_map.items():
        hit_pct = round((hit_frame / max(1, total_frames - 1)) * 100, 2)
        brick_timing_map[rc] = {
            "hit": hit_pct,
            "end": min(100.0, hit_pct + shatter_phase_pct)
        }

    # Build score digit roller keyframes (hundreds, tens, ones)
    line_h = 12
    kf_d100, kf_d10, kf_d1 = [], [], []
    for f_i, h in enumerate(history):
        pct = round((f_i / (total_frames - 1)) * 100, 2)
        sc = h.get("score", engine.total_bricks - len(h["destroyed"]))
        d100 = (sc // 100) % 10
        d10 = (sc // 10) % 10
        d1 = sc % 10
        kf_d100.append(f"{pct}% {{ transform: translateY(-{d100 * line_h}px); }}")
        kf_d10.append(f"{pct}% {{ transform: translateY(-{d10 * line_h}px); }}")
        kf_d1.append(f"{pct}% {{ transform: translateY(-{d1 * line_h}px); }}")

    score_kfs = [
        f"@keyframes score-d100 {{\n      " + "\n      ".join(kf_d100) + "\n    }",
        f"@keyframes score-d10 {{\n      " + "\n      ".join(kf_d10) + "\n    }",
        f"@keyframes score-d1 {{\n      " + "\n      ".join(kf_d1) + "\n    }"
    ]

    # Build dynamic heart life keyframes
    kf_h1, kf_h2, kf_h3 = [], [], []
    for f_i, h in enumerate(history):
        pct = round((f_i / (total_frames - 1)) * 100, 2)
        lv = h.get("lives", 3)
        kf_h1.append(f"{pct}% {{ opacity: {1 if lv >= 1 else 0}; }}")
        kf_h2.append(f"{pct}% {{ opacity: {1 if lv >= 2 else 0}; }}")
        kf_h3.append(f"{pct}% {{ opacity: {1 if lv >= 3 else 0}; }}")

    heart_kfs = [
        f"@keyframes heart-life-1 {{\n      " + "\n      ".join(kf_h1) + "\n    }",
        f"@keyframes heart-life-2 {{\n      " + "\n      ".join(kf_h2) + "\n    }",
        f"@keyframes heart-life-3 {{\n      " + "\n      ".join(kf_h3) + "\n    }"
    ]

    trail_count = 2 if engine.skin.get("trail_color") else 0
    trail_kfs = build_trail_keyframes(history, total_frames, trail_count)

    max_particles = 18
    particle_kfs, particle_info = build_particle_keyframes(history, total_frames, max_particles)

    particle_nodes = []
    for p_i in range(max_particles):
        dom_type, dom_size = particle_info[p_i]
        node_inner = generate_particle_svg_node(dom_type, dom_size)
        particle_nodes.append(f'  <g class="p-node-{p_i}">{node_inner}</g>')

    bg_hex = rgb_to_hex(theme["bg_color"])
    paddle_hex = rgb_to_hex(theme["paddle_color"])
    ball_hex = rgb_to_hex(engine.skin["color"])
    trail_hex = rgb_to_hex(engine.skin["trail_color"]) if engine.skin.get("trail_color") else ball_hex
    empty_hex = rgb_to_hex(theme["empty_brick"])
    score_hex = rgb_to_hex(theme["score_text_color"])
    heart_hex = rgb_to_hex(theme["heart_color"])

    svg = [
        f'<svg viewBox="0 0 {engine.canvas_w} {engine.canvas_h}" width="{engine.canvas_w}" height="{engine.canvas_h}" xmlns="http://www.w3.org/2000/svg">',
        '  <style>',
        f'    .bg {{ fill: {bg_hex}; }}',
        f'    .empty-cell {{ fill: {empty_hex}; }}',
        f'    .score-txt {{ fill: {score_hex}; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 10px; font-weight: bold; }}',
        f'    .heart {{ fill: {heart_hex}; }}',
        f'    .ball-node {{ fill: {ball_hex}; }}',
        f'    .ball-container {{ animation: ball-motion {duration_sec}s linear infinite; }}',
        f'    .paddle-container {{ animation: paddle-motion {duration_sec}s linear infinite; }}',
        f'    .roll-d100 {{ animation: score-d100 {duration_sec}s linear infinite; }}',
        f'    .roll-d10 {{ animation: score-d10 {duration_sec}s linear infinite; }}',
        f'    .roll-d1 {{ animation: score-d1 {duration_sec}s linear infinite; }}',
        f'    .heart-1 {{ animation: heart-life-1 {duration_sec}s linear infinite; }}',
        f'    .heart-2 {{ animation: heart-life-2 {duration_sec}s linear infinite; }}',
        f'    .heart-3 {{ animation: heart-life-3 {duration_sec}s linear infinite; }}',
        '    @keyframes flame-flicker { 0% { transform: scaleY(0.75); opacity: 0.8; } 100% { transform: scaleY(1.35); opacity: 1; } }',
        '    @keyframes spark-drift { 0% { transform: translateY(0px) scale(0.7); opacity: 1; } 100% { transform: translateY(8px) scale(1.3); opacity: 0; } }',
        '    @keyframes star-twinkle { 0%, 100% { opacity: 0.15; } 50% { opacity: 0.95; } }',
        '    @keyframes cloud-drift { 0% { transform: translateX(0); } 100% { transform: translateX(700px); } }',
        '    @keyframes pulse-glow { 0% { opacity: 0.35; transform: scale(0.9); } 100% { opacity: 0.85; transform: scale(1.15); } }',
        '    @keyframes matrix-stream { 0% { transform: translateY(0); } 100% { transform: translateY(340px); } }',
        f'    @keyframes ball-motion {{\n      ' + '\n      '.join(ball_kf) + '\n    }',
        f'    @keyframes paddle-motion {{\n      ' + '\n      '.join(paddle_kf) + '\n    }'
    ]

    for t_i, tkf in enumerate(trail_kfs):
        svg.append(f'    {tkf}')
        svg.append(f'    .trail-node-{t_i} {{ animation: trail-{t_i} {duration_sec}s linear infinite; fill: {trail_hex}; }}')

    for p_i, pkf in enumerate(particle_kfs):
        svg.append(f'    {pkf}')
        svg.append(f'    .p-node-{p_i} {{ animation: p-drift-{p_i} {duration_sec}s linear infinite; }}')

    for skf in score_kfs:
        svg.append(f'    {skf}')

    for hkf in heart_kfs:
        svg.append(f'    {hkf}')

    ambient_elements = generate_ambient_svg(theme, engine)

    brick_idx = 0
    brick_rects = []
    for r in range(engine.rows):
        for c in range(engine.cols):
            bx = engine.margin_x + c * engine.cell_w
            by = engine.margin_y + r * engine.cell_h
            val = engine.initial_grid[r][c]

            # Background empty grid slot (always present)
            brick_rects.append(f'  <rect class="empty-cell" x="{bx + 1:.1f}" y="{by + 1:.1f}" width="{engine.cell_w - 2:.1f}" height="{engine.cell_h - 2:.1f}" />')

            # Only render active playable brick if user actually has commits on this day
            if val > 0:
                palette = theme["brick_colors"]
                if val < 3:
                    bcolor = palette[0]
                elif val < 6:
                    bcolor = palette[1]
                elif val < 10:
                    bcolor = palette[2]
                else:
                    bcolor = palette[3]
                b_hex = rgb_to_hex(bcolor)

                disp_info = brick_timing_map.get((r, c))
                kf_name = f"b{brick_idx}"
                elem = engine.skin.get("element", "none")

                if disp_info is not None:
                    t_hit = disp_info["hit"]
                    t_end = disp_info["end"]
                    if elem == "ice":
                        shatter_col = "#afeeff"
                        svg.append(f'    @keyframes {kf_name} {{ 0%, {t_hit}% {{ fill: {b_hex}; opacity: 1; }} {t_hit + 0.01}% {{ fill: {shatter_col}; }} {t_end}% {{ fill: #d8f5ff; opacity: 1; }} {min(100.0, t_end + 0.05)}%, 100% {{ opacity: 0; }} }}')
                    elif elem == "fire":
                        shatter_col = "#ff4500"
                        svg.append(f'    @keyframes {kf_name} {{ 0%, {t_hit}% {{ fill: {b_hex}; opacity: 1; }} {t_hit + 0.01}% {{ fill: {shatter_col}; }} {t_end}% {{ fill: #ff8c00; opacity: 0.8; }} {min(100.0, t_end + 0.05)}%, 100% {{ opacity: 0; }} }}')
                    elif elem == "lightning":
                        shatter_col = "#ffff60"
                        svg.append(f'    @keyframes {kf_name} {{ 0%, {t_hit}% {{ fill: {b_hex}; opacity: 1; }} {t_hit + 0.01}% {{ fill: {shatter_col}; }} {t_end}% {{ fill: #d299ff; opacity: 0.9; }} {min(100.0, t_end + 0.05)}%, 100% {{ opacity: 0; }} }}')
                    elif elem == "poison":
                        shatter_col = "#238636"
                        svg.append(f'    @keyframes {kf_name} {{ 0%, {t_hit}% {{ fill: {b_hex}; opacity: 1; }} {t_hit + 0.01}% {{ fill: {shatter_col}; }} {t_end}% {{ fill: #0e4429; opacity: 0.7; }} {min(100.0, t_end + 0.05)}%, 100% {{ opacity: 0; }} }}')
                    else:
                        # Classic/default: disappear instantly on impact
                        svg.append(f'    @keyframes {kf_name} {{ 0%, {t_hit}% {{ fill: {b_hex}; opacity: 1; }} {min(100.0, t_hit + 0.02)}%, 100% {{ opacity: 0; }} }}')
                    svg.append(f'    .{kf_name} {{ fill: {b_hex}; animation: {kf_name} {duration_sec}s linear infinite; }}')
                else:
                    # Brick never hit in this preview duration: stays solid visible 100% of the time!
                    svg.append(f'    .{kf_name} {{ fill: {b_hex}; opacity: 1; }}')

                brick_rects.append(f'  <rect class="{kf_name}" x="{bx + 1:.1f}" y="{by + 1:.1f}" width="{engine.cell_w - 2:.1f}" height="{engine.cell_h - 2:.1f}" />')
                brick_idx += 1

    svg.append('  </style>')
    svg.append('  <defs>')
    svg.append(generate_paddle_svg(engine.paddle_skin, engine, paddle_hex))
    # Clip path for 3 rolling digits (hundreds, tens, ones)
    svg.append(f'    <clipPath id="score-clip"><rect x="0" y="0" width="30" height="{line_h}" /></clipPath>')
    svg.append('  </defs>')

    svg.append(f'  <rect class="bg" width="100%" height="100%" />')
    svg.extend(ambient_elements)

    # Dynamic rolling score odometer: SCORE: [000-190] / TOTAL
    digits_text = "&#10;".join(str(d) for d in range(10))
    score_label_x = engine.margin_x
    roller_x = score_label_x + 46
    total_x = roller_x + 22

    # Generate vertical digit strip (0 to 9 separated by line_h)
    def make_digit_strip(x_pos):
        tspans = "".join(f'<tspan x="{x_pos}" dy="{line_h if d > 0 else 0}">{d}</tspan>' for d in range(10))
        return f'<text class="score-txt" x="{x_pos}" y="10">{tspans}</text>'

    svg.append(f'  <text class="score-txt" x="{score_label_x}" y="18">SCORE:</text>')
    svg.append(f'  <g transform="translate({roller_x}, 8)" clip-path="url(#score-clip)">')
    # Column 1: Hundreds
    svg.append(f'    <g class="roll-d100">{make_digit_strip(0)}</g>')
    # Column 2: Tens
    svg.append(f'    <g class="roll-d10">{make_digit_strip(7)}</g>')
    # Column 3: Ones
    svg.append(f'    <g class="roll-d1">{make_digit_strip(14)}</g>')
    svg.append(f'  </g>')
    svg.append(f'  <text class="score-txt" x="{total_x}" y="18">/{engine.total_bricks}</text>')

    heart_start_x = engine.canvas_w - engine.margin_x - (3 * 16)
    for i in range(3):
        h_path = get_heart_svg_path(heart_start_x + i * 16, 14, size=5)
        svg.append(f'  <path class="heart heart-{i + 1}" d="{h_path}" />')

    svg.extend(brick_rects)

    for t_i in range(trail_count):
        r_sz = max(1, engine.ball_r - (trail_count - t_i))
        svg.append(f'  <g class="trail-node-{t_i}"><circle cx="0" cy="0" r="{r_sz}" /></g>')

    svg.extend(particle_nodes)
    svg.append(f'  <g class="ball-container"><circle class="ball-node" cx="0" cy="0" r="{engine.ball_r}" /></g>')
    svg.append(f'  <g class="paddle-container"><use href="#paddle-graphic" /></g>')
    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Generated animated {output_path} ({total_frames} frames, {duration_sec}s)")
