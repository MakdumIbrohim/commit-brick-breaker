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

def generate_particle_svg_node(ptype, sz=1):
    if ptype == "snowflake":
        return f'<line x1="-{sz}" y1="0" x2="{sz}" y2="0" stroke="currentColor" stroke-width="1" /><line x1="0" y1="-{sz}" x2="0" y2="{sz}" stroke="currentColor" stroke-width="1" />'
    elif ptype == "crystal":
        return f'<polygon points="0,-{sz} {sz},0 0,{sz} -{sz},0" fill="currentColor" />'
    elif ptype == "ember":
        return f'<circle cx="0" cy="0" r="{sz}" fill="currentColor" />'
    elif ptype == "spark":
        return f'<line x1="0" y1="0" x2="-2" y2="-2" stroke="currentColor" stroke-width="1.2" />'
    elif ptype == "bubble":
        return f'<circle cx="0" cy="0" r="{sz}" fill="none" stroke="currentColor" stroke-width="1" />'
    elif ptype == "zap":
        return f'<line x1="-2" y1="-2" x2="2" y2="2" stroke="currentColor" stroke-width="1.2" />'
    elif ptype == "thrust":
        return f'<polygon points="-{sz},0 {sz},0 0,{sz*2.5:.1f}" fill="currentColor" />'
    elif ptype == "energy":
        return f'<circle cx="0" cy="0" r="{sz}" fill="currentColor" />'
    elif ptype == "pixel":
        return f'<rect x="-{sz}" y="-{sz}" width="{sz*2}" height="{sz*2}" fill="currentColor" />'
    else:
        return '<rect x="-1" y="-1" width="2" height="2" fill="currentColor" />'

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
                g_val = int(40 + ((clen - i) / clen) * 160)
                alpha = round(0.25 + ((clen - i) / clen) * 0.75, 2)
                col_hex = f"#00{g_val:02x}{int(g_val*0.4):02x}"
                stream_nodes.append(f'    <rect x="{x}" y="{py}" width="2" height="4" fill="{col_hex}" opacity="{alpha}" />')
            stream_nodes.append('  </g>')
            elements.append("\n".join(stream_nodes))
    return elements

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
