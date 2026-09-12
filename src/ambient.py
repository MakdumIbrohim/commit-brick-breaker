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
            # Loop seamlessly: if cloud leaves right edge, re-enter from left
            if c["x"] > canvas_w + 50:
                c["x"] = -110
    elif effect == "matrix_rain":
        for col in items:
            col["y"] += col["speed"]
            if col["y"] > canvas_h + 30:
                col["y"] = -random.uniform(10, 40)
