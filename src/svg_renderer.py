import math
from src.config import BALL_R

def rgb_to_hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def get_heart_svg_path(cx, cy, size=5):
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
    return f"M {coords[0][0]} {coords[0][1]} " + " ".join(f"L {x} {y}" for x, y in coords[1:]) + " Z"

def build_svg_keyframes(history, total_frames):
    ball_kf = []
    paddle_kf = []
    for i, h in enumerate(history):
        pct = round((i / (total_frames - 1)) * 100, 2)
        ball_kf.append(f"{pct}% {{ transform: translate({h['bx']}px, {h['by']}px); }}")
        paddle_kf.append(f"{pct}% {{ transform: translate({h['px']}px, {h['py']}px); }}")
    return ball_kf, paddle_kf

def calculate_brick_lifetimes(initial_bricks, history, total_frames):
    disappear_map = {}
    for (r, c) in initial_bricks:
        pct = None
        for i, h in enumerate(history):
            if (r, c) not in h["destroyed"]:
                pct = round((i / (total_frames - 1)) * 100, 2)
                break
        disappear_map[(r, c)] = pct if pct is not None else 100.0
    return disappear_map

def generate_ambient_svg(theme, engine):
    elements = []
    effect = theme.get("bg_effect")
    if effect == "starfield":
        for i, s in enumerate(getattr(engine, "ambient_items", [])):
            dur = 1.5 + (i % 5) * 0.4
            delay = (i % 7) * 0.3
            elements.append(f'  <rect x="{s["x"]:.1f}" y="{s["y"]:.1f}" width="{s["size"]}" height="{s["size"]}" fill="#ffffff" style="animation: star-twinkle {dur:.1f}s ease-in-out infinite {delay:.1f}s;" />')
    elif effect == "mario_sky":
        for i, c in enumerate(getattr(engine, "ambient_items", [])):
            cx, cy = c["x"], c["y"]
            sc = c.get("scale", 1.0)
            bw, bh = 54 * sc, 18 * sc
            dur = 25.0 + (i % 4) * 5.0
            delay = (i % 5) * -4.0
            cloud_g = [
                f'  <g style="animation: cloud-drift {dur:.1f}s linear infinite {delay:.1f}s;">',
                f'    <rect x="{cx:.1f}" y="{cy + 8 * sc:.1f}" width="{bw:.1f}" height="{bh:.1f}" rx="{bh/2:.1f}" fill="#ffffff" stroke="#000000" stroke-width="1" />',
                f'    <circle cx="{cx + 17 * sc:.1f}" cy="{cy + 13 * sc:.1f}" r="{11 * sc:.1f}" fill="#ffffff" stroke="#000000" stroke-width="1" />',
                f'    <circle cx="{cx + 34 * sc:.1f}" cy="{cy + 10 * sc:.1f}" r="{14 * sc:.1f}" fill="#ffffff" stroke="#000000" stroke-width="1" />',
                f'    <circle cx="{cx + 46 * sc:.1f}" cy="{cy + 14 * sc:.1f}" r="{10 * sc:.1f}" fill="#ffffff" stroke="#000000" stroke-width="1" />',
                f'    <rect x="{cx + 8 * sc:.1f}" y="{cy + 8 * sc:.1f}" width="{bw - 16 * sc:.1f}" height="{10 * sc:.1f}" fill="#ffffff" />',
                f'  </g>'
            ]
            elements.append("\n".join(cloud_g))
    elif effect == "neon_grid":
        horizon_y = int(engine.canvas_h * 0.65)
        elements.append(f'  <g style="animation: pulse-glow 2s ease-in-out infinite alternate;">')
        elements.append(f'    <line x1="0" y1="{horizon_y}" x2="{engine.canvas_w}" y2="{horizon_y}" stroke="#781ec8" stroke-width="1.2" />')
        for y in range(horizon_y + 12, engine.canvas_h, 16):
            elements.append(f'    <line x1="0" y1="{y}" x2="{engine.canvas_w}" y2="{y}" stroke="#5a1496" stroke-width="1" />')
        center_x = engine.canvas_w / 2
        for offset in range(-int(engine.canvas_w), int(engine.canvas_w * 2), 48):
            elements.append(f'    <line x1="{center_x + (offset - center_x) * 0.15:.1f}" y1="{horizon_y}" x2="{offset}" y2="{engine.canvas_h}" stroke="#460a78" stroke-width="1" />')
        elements.append(f'  </g>')
    elif effect == "matrix_rain":
        cols = int(engine.canvas_w / 16)
        for c_i in range(cols):
            x = c_i * 16 + 8
            clen = 6 + (c_i % 4)
            dur = 2.2 + (c_i % 5) * 0.35
            delay = (c_i % 7) * -0.4

            stream_nodes = [f'  <g style="animation: matrix-stream {dur:.1f}s linear infinite {delay:.1f}s;">']
            for i in range(clen):
                py = -i * 9
                # Identical gradient fade to GIF: brighter at head (i=0), dimmer at tail
                g_val = int(40 + ((clen - i) / clen) * 160)
                alpha = round(0.25 + ((clen - i) / clen) * 0.75, 2)
                col_hex = f"#00{g_val:02x}{int(g_val*0.4):02x}"
                # Render segmented dotted rectangles like PIL
                stream_nodes.append(f'    <rect x="{x}" y="{py}" width="2" height="4" fill="{col_hex}" opacity="{alpha}" />')
            stream_nodes.append('  </g>')
            elements.append("\n".join(stream_nodes))
    return elements

def generate_particle_svg_node(ptype, sz=1):
    if ptype == "snowflake":
        # Cross snowflake shape (+)
        return f'<line x1="-{sz}" y1="0" x2="{sz}" y2="0" stroke="currentColor" stroke-width="1" /><line x1="0" y1="-{sz}" x2="0" y2="{sz}" stroke="currentColor" stroke-width="1" />'
    elif ptype == "crystal":
        # Diamond frost crystal
        return f'<polygon points="0,-{sz} {sz},0 0,{sz} -{sz},0" fill="currentColor" />'
    elif ptype == "ember":
        # Glowing round ember
        return f'<circle cx="0" cy="0" r="{sz}" fill="currentColor" />'
    elif ptype == "spark":
        # Sharp spark streak
        return f'<line x1="0" y1="0" x2="-2" y2="-2" stroke="currentColor" stroke-width="1.2" />'
    elif ptype == "bubble":
        # Hollow poison bubble
        return f'<circle cx="0" cy="0" r="{sz}" fill="none" stroke="currentColor" stroke-width="1" />'
    elif ptype == "zap":
        # Jagged electric zap line
        return f'<line x1="-2" y1="-2" x2="2" y2="2" stroke="currentColor" stroke-width="1.2" />'
    elif ptype == "thrust":
        # Rocket flame jet
        return f'<polygon points="-{sz},0 {sz},0 0,{sz*2.5:.1f}" fill="currentColor" />'
    elif ptype == "energy":
        return f'<circle cx="0" cy="0" r="{sz}" fill="currentColor" />'
    elif ptype == "pixel":
        return f'<rect x="-{sz}" y="-{sz}" width="{sz*2}" height="{sz*2}" fill="currentColor" />'
    else:
        return '<rect x="-1" y="-1" width="2" height="2" fill="currentColor" />'

def generate_paddle_svg(pskin, engine, paddle_hex):
    style = pskin.get("style", "default")
    pw, ph = engine.paddle_w, engine.paddle_h
    mid_y = ph / 2
    svg_defs = []

    if style == "laser":
        cap_w = 7
        caps_hex = rgb_to_hex(pskin["caps"])
        prim_hex = rgb_to_hex(pskin["primary"])
        core_hex = rgb_to_hex(pskin["core"])
        svg_defs.append(f'    <g id="paddle-graphic">')
        svg_defs.append(f'      <rect x="0" y="-2" width="{cap_w}" height="{ph + 4}" fill="{caps_hex}" />')
        svg_defs.append(f'      <rect x="{pw - cap_w}" y="-2" width="{cap_w}" height="{ph + 4}" fill="{caps_hex}" />')
        svg_defs.append(f'      <rect x="{cap_w}" y="0" width="{pw - 2*cap_w}" height="{ph}" rx="2" fill="{prim_hex}" />')
        svg_defs.append(f'      <rect x="{cap_w + 3}" y="{mid_y - 1}" width="{pw - 2*cap_w - 6}" height="2" fill="{core_hex}" />')
        svg_defs.append(f'      <rect x="{cap_w/2 - 1}" y="{mid_y - 1}" width="2" height="2" fill="#ffffff" />')
        svg_defs.append(f'      <rect x="{pw - cap_w/2 - 1}" y="{mid_y - 1}" width="2" height="2" fill="#ffffff" />')
        svg_defs.append(f'    </g>')
    elif style == "mecha":
        bw = 6
        booster_hex = rgb_to_hex(pskin["booster"])
        prim_hex = rgb_to_hex(pskin["primary"])
        plate_hex = rgb_to_hex(pskin["plate"])
        cx = pw / 2
        svg_defs.append(f'    <g id="paddle-graphic">')
        svg_defs.append(f'      <polygon points="0,2 {bw},-1 {bw},{ph+1} 0,{ph-2}" fill="{booster_hex}" />')
        svg_defs.append(f'      <polygon points="{pw},2 {pw-bw},-1 {pw-bw},{ph+1} {pw},{ph-2}" fill="{booster_hex}" />')
        svg_defs.append(f'      <rect x="{bw}" y="0" width="{pw - 2*bw}" height="{ph}" fill="{prim_hex}" />')
        svg_defs.append(f'      <rect x="{cx - pw*0.22}" y="-1" width="{pw*0.44}" height="{ph+2}" rx="2" fill="{plate_hex}" />')
        svg_defs.append(f'    </g>')
    elif style == "retro":
        cap_w = 8
        prim_hex = rgb_to_hex(pskin["primary"])
        caps_hex = rgb_to_hex(pskin["caps"])
        stripes_hex = rgb_to_hex(pskin["stripes"])
        svg_defs.append(f'    <g id="paddle-graphic">')
        svg_defs.append(f'      <polygon points="0,{ph} {cap_w},0 {cap_w},{ph}" fill="{caps_hex}" />')
        svg_defs.append(f'      <polygon points="{pw},{ph} {pw-cap_w},0 {pw-cap_w},{ph}" fill="{caps_hex}" />')
        svg_defs.append(f'      <rect x="{cap_w}" y="0" width="{pw - 2*cap_w}" height="{ph}" fill="{prim_hex}" />')
        for sx in range(int(cap_w + 6), int(pw - cap_w - 6), 12):
            svg_defs.append(f'      <polygon points="{sx},{ph} {sx+4},0 {sx+8},0 {sx+4},{ph}" fill="{stripes_hex}" />')
        svg_defs.append(f'      <line x1="{cap_w}" y1="1" x2="{pw-cap_w}" y2="1" stroke="#ffffff" stroke-width="1" />')
        svg_defs.append(f'    </g>')
    elif style == "cyber":
        prim_hex = rgb_to_hex(pskin["primary"])
        core_hex = rgb_to_hex(pskin["core"])
        caps_hex = rgb_to_hex(pskin["caps"])
        cx = pw / 2
        svg_defs.append(f'    <g id="paddle-graphic">')
        svg_defs.append(f'      <rect x="0" y="0" width="{pw}" height="{ph}" rx="4" fill="{caps_hex}" stroke="{prim_hex}" stroke-width="1" />')
        svg_defs.append(f'      <rect x="6" y="2" width="{pw - 12}" height="{ph - 4}" fill="{prim_hex}" />')
        svg_defs.append(f'      <circle cx="{cx}" cy="{mid_y}" r="3" fill="{core_hex}" />')
        svg_defs.append(f'    </g>')
    else:
        svg_defs.append(f'    <g id="paddle-graphic">')
        svg_defs.append(f'      <rect x="0" y="0" width="{pw}" height="{ph}" rx="3" fill="{paddle_hex}" />')
        svg_defs.append(f'    </g>')

    return "\n".join(svg_defs)

def render_svg(engine, output_path="game.svg", max_frames=2000):
    theme = engine.theme
    history = []
    step_idx = 0

    while len(engine.bricks) > 0 and len(history) < max_frames:
        engine.step()
        if step_idx % 2 == 0:
            # Capture active debris particles exactly like renderer.py
            active_p = []
            for p in engine.particles[:14]:
                active_p.append({
                    "x": round(p["x"], 1),
                    "y": round(p["y"], 1),
                    "color": rgb_to_hex(p.get("color", (255, 255, 255))),
                    "size": p.get("size", 1),
                    "type": p.get("type", "debris")
                })

            # Capture trail points
            trail_pts = [(round(tx, 1), round(ty, 1)) for tx, ty in engine.trail]

            history.append({
                "bx": round(engine.ball_x, 1),
                "by": round(engine.ball_y, 1),
                "px": round(engine.paddle_x, 1),
                "py": round(engine.paddle_y, 1),
                "trail": trail_pts,
                "particles": active_p,
                "destroyed": list(engine.bricks.keys()),
                "state": engine.state
            })
        step_idx += 1

    for _ in range(15):
        history.append({
            "bx": round(engine.ball_x, 1),
            "by": round(engine.ball_y, 1),
            "px": round(engine.paddle_x, 1),
            "py": round(engine.paddle_y, 1),
            "trail": [],
            "particles": [],
            "destroyed": [],
            "state": "win"
        })

    total_frames = len(history)
    duration_sec = round(total_frames * 0.05, 1)

    ball_kf, paddle_kf = build_svg_keyframes(history, total_frames)
    brick_disappear = calculate_brick_lifetimes(engine.initial_grid_bricks, history, total_frames)

    # 1. Motion trail keyframes (up to 4 trail circles matching GIF)
    trail_kfs = []
    trail_count = 4 if engine.skin.get("trail_color") else 0
    for t_i in range(trail_count):
        tkf = []
        for f_i, h in enumerate(history):
            pct = round((f_i / (total_frames - 1)) * 100, 2)
            pts = h["trail"]
            if t_i < len(pts):
                pt = pts[t_i]
                tkf.append(f"{pct}% {{ transform: translate({pt[0]}px, {pt[1]}px); opacity: 0.7; }}")
            else:
                tkf.append(f"{pct}% {{ opacity: 0; }}")
        trail_kfs.append(f"@keyframes trail-{t_i} {{\n      " + "\n      ".join(tkf) + "\n    }")

    # 2. Debris particles keyframes (up to 14 flying particles matching GIF)
    particle_kfs = []
    particle_nodes = []
    max_particles = 14
    for p_i in range(max_particles):
        pkf = []
        dominant_type = "debris"
        dominant_size = 1
        for f_i, h in enumerate(history):
            pct = round((f_i / (total_frames - 1)) * 100, 2)
            pts = h["particles"]
            if p_i < len(pts):
                pt = pts[p_i]
                dominant_type = pt["type"]
                dominant_size = pt["size"]
                pkf.append(f"{pct}% {{ transform: translate({pt['x']}px, {pt['y']}px); color: {pt['color']}; opacity: 1; }}")
            else:
                pkf.append(f"{pct}% {{ opacity: 0; }}")
        particle_kfs.append(f"@keyframes p-drift-{p_i} {{\n      " + "\n      ".join(pkf) + "\n    }")
        node_inner = generate_particle_svg_node(dominant_type, dominant_size)
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
        '    @keyframes star-twinkle { 0%, 100% { opacity: 0.15; } 50% { opacity: 0.95; } }',
        '    @keyframes cloud-drift { 0% { transform: translateX(0); } 100% { transform: translateX(700px); } }',
        '    @keyframes pulse-glow { 0% { opacity: 0.35; } 100% { opacity: 0.85; } }',
        '    @keyframes matrix-stream { 0% { transform: translateY(0); } 100% { transform: translateY(340px); } }',
        f'    @keyframes ball-motion {{\n      ' + '\n      '.join(ball_kf) + '\n    }',
        f'    @keyframes paddle-motion {{\n      ' + '\n      '.join(paddle_kf) + '\n    }'
    ]

    # Add trail keyframe CSS
    for t_i, tkf in enumerate(trail_kfs):
        svg.append(f'    {tkf}')
        r_sz = max(1, engine.ball_r - (trail_count - t_i))
        svg.append(f'    .trail-node-{t_i} {{ animation: trail-{t_i} {duration_sec}s linear infinite; fill: {trail_hex}; }}')

    # Add particle keyframe CSS
    for p_i, pkf in enumerate(particle_kfs):
        svg.append(f'    {pkf}')
        svg.append(f'    .p-node-{p_i} {{ animation: p-drift-{p_i} {duration_sec}s linear infinite; }}')

    ambient_elements = generate_ambient_svg(theme, engine)

    # Bricks
    brick_idx = 0
    brick_rects = []
    for r in range(engine.rows):
        for c in range(engine.cols):
            bx = engine.margin_x + c * engine.cell_w
            by = engine.margin_y + r * engine.cell_h
            val = engine.initial_grid[r][c]

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

                disp = brick_disappear.get((r, c), 100.0)
                kf_name = f"b{brick_idx}"
                svg.append(f'    @keyframes {kf_name} {{ 0%, {disp}% {{ opacity: 1; }} {min(100.0, disp + 0.05)}%, 100% {{ opacity: 0; }} }}')
                svg.append(f'    .{kf_name} {{ fill: {b_hex}; animation: {kf_name} {duration_sec}s linear infinite; }}')

                # Brick rect matching exact PIL coordinates
                brick_rects.append(f'  <rect class="empty-cell" x="{bx + 1:.1f}" y="{by + 1:.1f}" width="{engine.cell_w - 2:.1f}" height="{engine.cell_h - 2:.1f}" />')
                brick_rects.append(f'  <rect class="{kf_name}" x="{bx + 1:.1f}" y="{by + 1:.1f}" width="{engine.cell_w - 2:.1f}" height="{engine.cell_h - 2:.1f}" />')
                brick_idx += 1
            else:
                brick_rects.append(f'  <rect class="empty-cell" x="{bx + 1:.1f}" y="{by + 1:.1f}" width="{engine.cell_w - 2:.1f}" height="{engine.cell_h - 2:.1f}" />')

    svg.append('  </style>')
    svg.append('  <defs>')
    svg.append(generate_paddle_svg(engine.paddle_skin, engine, paddle_hex))
    svg.append('  </defs>')

    svg.append(f'  <rect class="bg" width="100%" height="100%" />')
    svg.extend(ambient_elements)
    svg.append(f'  <text class="score-txt" x="{engine.margin_x}" y="18">SCORE: {engine.total_bricks}/{engine.total_bricks}</text>')
    heart_start_x = engine.canvas_w - engine.margin_x - (engine.lives * 16)
    for i in range(max(0, engine.lives)):
        h_path = get_heart_svg_path(heart_start_x + i * 16, 14, size=5)
        svg.append(f'  <path class="heart" d="{h_path}" />')

    svg.extend(brick_rects)

    # 1. Trail circles (identical to PIL render_frame)
    for t_i in range(trail_count):
        r_sz = max(1, engine.ball_r - (trail_count - t_i))
        svg.append(f'  <g class="trail-node-{t_i}"><circle cx="0" cy="0" r="{r_sz}" /></g>')

    # 2. Debris & collision particles (matching PIL particles)
    svg.extend(particle_nodes)

    # 3. Main ball (solid circle matching PIL)
    svg.append(f'  <g class="ball-container"><circle class="ball-node" cx="0" cy="0" r="{engine.ball_r}" /></g>')

    # 4. Paddle
    svg.append(f'  <g class="paddle-container"><use href="#paddle-graphic" /></g>')
    svg.append('</svg>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))

    print(f"Generated animated {output_path} ({total_frames} frames, {duration_sec}s)")
