def draw_particles(draw, particles):
    for p in particles:
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
            draw.polygon([(px - sz, py), (px + sz, py), (px, py + sz * 2.5)], fill=col)
        elif ptype == "energy":
            draw.ellipse([px - sz, py - sz, px + sz, py + sz], fill=col)
        elif ptype == "pixel":
            draw.rectangle([px - sz, py - sz, px + sz, py + sz], fill=col)
        else:
            draw.rectangle([px - 1, py - 1, px + 1, py + 1], fill=col)

def draw_ambient_background(draw, engine, theme):
    effect = theme.get("bg_effect")
    if effect == "starfield":
        for s in getattr(engine, "ambient_items", []):
            b = int(40 + s["brightness"] * 180)
            sz = s["size"]
            draw.rectangle([s["x"], s["y"], s["x"] + sz, s["y"] + sz], fill=(b, b, min(255, b + 20)))
    elif effect == "mario_sky":
        cloud_fill = (255, 255, 255)
        cloud_outline = (0, 0, 0)
        for c in getattr(engine, "ambient_items", []):
            cx, cy = c["x"], c["y"]
            sc = c.get("scale", 1.0)
            bw, bh = 54 * sc, 18 * sc
            draw.rounded_rectangle([cx, cy + 8 * sc, cx + bw, cy + 8 * sc + bh], radius=int(bh / 2), fill=cloud_fill, outline=cloud_outline, width=1)
            d1_r = 11 * sc
            draw.ellipse([cx + 6 * sc, cy + 2 * sc, cx + 6 * sc + d1_r * 2, cy + 2 * sc + d1_r * 2], fill=cloud_fill, outline=cloud_outline, width=1)
            d2_r = 14 * sc
            draw.ellipse([cx + 20 * sc, cy - 4 * sc, cx + 20 * sc + d2_r * 2, cy - 4 * sc + d2_r * 2], fill=cloud_fill, outline=cloud_outline, width=1)
            d3_r = 10 * sc
            draw.ellipse([cx + 36 * sc, cy + 4 * sc, cx + 36 * sc + d3_r * 2, cy + 4 * sc + d3_r * 2], fill=cloud_fill, outline=cloud_outline, width=1)
            draw.rectangle([cx + 8 * sc, cy + 8 * sc, cx + bw - 8 * sc, cy + 18 * sc], fill=cloud_fill)
    elif effect == "neon_grid":
        horizon_y = int(engine.canvas_h * 0.65)
        draw.line([(0, horizon_y), (engine.canvas_w, horizon_y)], fill=(80, 20, 110), width=1)
        for y in range(horizon_y + 12, engine.canvas_h, 16):
            draw.line([(0, y), (engine.canvas_w, y)], fill=(60, 15, 85), width=1)
        center_x = engine.canvas_w / 2
        for offset in range(-int(engine.canvas_w), int(engine.canvas_w * 2), 48):
            draw.line([(center_x + (offset - center_x) * 0.15, horizon_y), (offset, engine.canvas_h)], fill=(50, 10, 75), width=1)
    elif effect == "matrix_rain":
        for col in getattr(engine, "ambient_items", []):
            cx, cy, clen = col["x"], col["y"], col["len"]
            for i in range(clen):
                py = cy - i * 9
                if 0 <= py <= engine.canvas_h:
                    g = int(40 + ((clen - i) / clen) * 160)
                    draw.rectangle([cx, py, cx + 1, py + 3], fill=(0, g, int(g * 0.4)))
