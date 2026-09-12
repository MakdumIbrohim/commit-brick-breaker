import math
import random

def create_ball_particles(skin, x, y, count=8, is_trail=False):
    elem = skin.get("element", "none")
    if elem == "none":
        return []

    colors = skin.get("particle_colors", [])
    if not colors:
        return []

    particles = []
    # Moderate balanced burst speed on impact collisions
    spd_mult = 1.0 if is_trail else 1.4
    for _ in range(count):
        color = random.choice(colors)
        if elem == "fire":
            vx = random.uniform(-1.6, 1.6) * spd_mult
            vy = (random.uniform(-3.0, -0.6) if not is_trail else random.uniform(-1.5, 0.4))
            life = random.randint(8, 13) if not is_trail else random.randint(5, 8)
            p_type = "spark" if random.random() < 0.6 else "ember"
            size = random.choice([2, 3]) if not is_trail else 1
        elif elem == "ice":
            vx = random.uniform(-1.6, 1.6) * spd_mult
            vy = random.uniform(-1.2, 2.4) if not is_trail else random.uniform(-0.6, 1.0)
            life = random.randint(9, 14) if not is_trail else random.randint(6, 9)
            p_type = "snowflake" if random.random() < 0.5 else "crystal"
            size = random.choice([2, 3]) if not is_trail else 2
        elif elem == "lightning":
            vx = random.uniform(-2.8, 2.8)
            vy = random.uniform(-2.8, 2.8)
            life = random.randint(5, 9)
            p_type = "zap"
            size = random.choice([2, 3]) if not is_trail else 1
        elif elem == "poison":
            vx = random.uniform(-1.4, 1.4) * spd_mult
            vy = random.uniform(-2.5, 0.5) if not is_trail else random.uniform(-1.6, -0.3)
            life = random.randint(9, 15) if not is_trail else random.randint(6, 10)
            p_type = "bubble"
            size = random.choice([2, 3]) if not is_trail else 2
        else:
            vx = random.uniform(-2.0, 2.0) * spd_mult
            vy = random.uniform(-2.0, 2.0) * spd_mult
            life = random.randint(6, 10)
            p_type = "debris"
            size = 1

        particles.append({
            "x": x, "y": y,
            "vx": vx, "vy": vy,
            "life": life,
            "max_life": life,
            "color": color,
            "type": p_type,
            "size": size
        })
    return particles

def create_paddle_particles(paddle_skin, paddle_x, paddle_y, paddle_w, paddle_h):
    pstyle = paddle_skin.get("style", "default")
    x1 = paddle_x
    x2 = paddle_x + paddle_w
    y = paddle_y
    particles = []

    if pstyle == "mecha":
        for bx in (x1 + 3, x2 - 3):
            particles.append({
                "x": bx + random.uniform(-1, 1),
                "y": y + paddle_h,
                "vx": random.uniform(-0.5, 0.5),
                "vy": random.uniform(1.2, 2.5),
                "life": random.randint(4, 7),
                "max_life": 7,
                "color": random.choice([(255, 60, 30), (255, 140, 0), (255, 220, 0)]),
                "type": "thrust",
                "size": random.choice([1, 2])
            })
    elif pstyle == "laser":
        for ex in (x1 + 2, x2 - 2):
            if random.random() < 0.6:
                particles.append({
                    "x": ex,
                    "y": y + random.uniform(0, paddle_h),
                    "vx": random.uniform(-1.0, 1.0),
                    "vy": random.uniform(-1.5, -0.2),
                    "life": random.randint(4, 8),
                    "max_life": 8,
                    "color": random.choice([(0, 245, 255), (180, 255, 255), (255, 255, 255)]),
                    "type": "energy",
                    "size": 1
                })
    elif pstyle == "cyber":
        if random.random() < 0.7:
            rx = random.uniform(x1 + 6, x2 - 6)
            particles.append({
                "x": rx,
                "y": y - 1,
                "vx": random.uniform(-0.3, 0.3),
                "vy": random.uniform(-1.6, -0.6),
                "life": random.randint(5, 9),
                "max_life": 9,
                "color": random.choice([(210, 80, 255), (0, 255, 200), (255, 255, 255)]),
                "type": "pixel",
                "size": 1
            })
    elif pstyle == "retro":
        if random.random() < 0.65:
            rx = random.uniform(x1 + 8, x2 - 8)
            particles.append({
                "x": rx,
                "y": y - 1,
                "vx": random.uniform(-0.4, 0.4),
                "vy": random.uniform(-1.5, -0.4),
                "life": random.randint(5, 9),
                "max_life": 9,
                "color": random.choice([(255, 215, 0), (235, 130, 60), (255, 255, 255)]),
                "type": "pixel",
                "size": random.choice([1, 2])
            })
    return particles

def update_particles(particles, sim_steps):
    surviving = []
    for p in particles:
        p["x"] += p["vx"]
        p["y"] += p["vy"]

        ptype = p.get("type")
        if ptype in ("spark", "ember"):
            p["vy"] += 0.08
            p["vx"] *= 0.95
        elif ptype in ("snowflake", "crystal"):
            p["x"] += math.sin(sim_steps * 0.2 + p["life"]) * 0.4
        elif ptype == "bubble":
            p["x"] += math.cos(sim_steps * 0.15) * 0.3
        elif ptype == "zap":
            p["vx"] += random.uniform(-0.6, 0.6)
            p["vy"] += random.uniform(-0.6, 0.6)

        p["life"] -= 1
        if p["life"] > 0:
            surviving.append(p)
    return surviving
