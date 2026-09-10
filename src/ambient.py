import math
import random

def init_ambient_effects(theme, canvas_w, canvas_h):
    effect = theme.get("bg_effect", "starfield")
    items = []
    if effect == "starfield":
        for _ in range(35):
            items.append({
                "x": random.uniform(5, canvas_w - 5),
                "y": random.uniform(5, canvas_h - 10),
                "brightness": random.uniform(0.2, 1.0),
                "speed": random.uniform(0.02, 0.06),
                "size": 1 if random.random() < 0.8 else 2
            })
    elif effect == "mario_sky":
        cloud_configs = [
            {"x": 30, "y": 140, "speed": 0.24, "scale": 1.1},
            {"x": 260, "y": 185, "speed": 0.18, "scale": 0.85},
            {"x": 480, "y": 148, "speed": 0.22, "scale": 1.25},
            {"x": -70, "y": 170, "speed": 0.20, "scale": 0.95}
        ]
        for cc in cloud_configs:
            items.append(cc)
    elif effect == "matrix_rain":
        cols = int(canvas_w / 16)
        for c in range(cols):
            items.append({
                "x": c * 16 + 8,
                "y": random.uniform(0, canvas_h),
                "speed": random.uniform(1.2, 2.5),
                "len": random.randint(4, 9)
            })
    return items

def update_ambient_effects(items, effect, sim_steps, canvas_w, canvas_h):
    if effect == "starfield":
        for s in items:
            s["brightness"] = (math.sin(sim_steps * s["speed"] + s["x"]) + 1) / 2
    elif effect == "mario_sky":
        for c in items:
            c["x"] += c["speed"]
            if c["x"] > canvas_w + 60:
                c["x"] = -100
    elif effect == "matrix_rain":
        for col in items:
            col["y"] += col["speed"]
            if col["y"] > canvas_h + 30:
                col["y"] = -random.uniform(10, 40)

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
