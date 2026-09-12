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

    while len(engine.bricks) > 0 and len(history) < max_frames:
        engine.step()
        if step_idx % 2 == 0:
            active_p = []
            for p in engine.particles[:14]:
                active_p.append({
                    "x": round(p["x"], 1),
                    "y": round(p["y"], 1),
                    "color": rgb_to_hex(p.get("color", (255, 255, 255))),
                    "size": p.get("size", 1),
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

    trail_count = 4 if engine.skin.get("trail_color") else 0
    trail_kfs = build_trail_keyframes(history, total_frames, trail_count)

    max_particles = 14
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
        '    @keyframes star-twinkle { 0%, 100% { opacity: 0.15; } 50% { opacity: 0.95; } }',
        '    @keyframes cloud-drift { 0% { transform: translateX(0); } 100% { transform: translateX(700px); } }',
        '    @keyframes pulse-glow { 0% { opacity: 0.35; } 100% { opacity: 0.85; } }',
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

    ambient_elements = generate_ambient_svg(theme, engine)

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
