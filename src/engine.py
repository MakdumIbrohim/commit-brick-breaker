import math
import random
from src.config import (
    CANVAS_W, CANVAS_H, MARGIN_X, MARGIN_Y,
    PADDLE_H, BALL_R, BALL_SPEED, INITIAL_LIVES,
    BALL_SKINS, DEFAULT_SKIN, THEMES, DEFAULT_THEME,
    PADDLE_SKINS, DEFAULT_PADDLE_SKIN
)
from src.ambient import init_ambient_effects, update_ambient_effects
from src.particles import (
    create_ball_particles, create_paddle_particles, update_particles
)

class BrickBreakerEngine:
    def __init__(self, grid, canvas_w=CANVAS_W, canvas_h=CANVAS_H, margin_x=MARGIN_X, margin_y=MARGIN_Y, skin=DEFAULT_SKIN, theme=DEFAULT_THEME, paddle_skin=DEFAULT_PADDLE_SKIN):
        self.initial_grid = [row[:] for row in grid]
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.canvas_w = canvas_w
        self.canvas_h = canvas_h
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.skin_name = skin if skin in BALL_SKINS else DEFAULT_SKIN
        self.skin = BALL_SKINS[self.skin_name]
        self.theme_name = theme if theme in THEMES else DEFAULT_THEME
        self.theme = THEMES[self.theme_name]
        self.paddle_skin_name = paddle_skin if paddle_skin in PADDLE_SKINS else DEFAULT_PADDLE_SKIN
        self.paddle_skin = PADDLE_SKINS[self.paddle_skin_name]

        # Scale cell width dynamically to fit all weeks from Jan 1
        available_w = canvas_w - 2 * margin_x
        self.cell_w = max(10, available_w / self.cols)
        self.cell_h = 13

        self.paddle_w = max(55, min(75, canvas_w * 0.12))
        self.paddle_h = PADDLE_H
        self.paddle_y = canvas_h - 25
        self.ball_r = BALL_R
        self.speed = BALL_SPEED

        self.reset_game()

    def reset_game(self):
        self.grid = [row[:] for row in self.initial_grid]
        self.bricks = {(r, c): self.grid[r][c] for r in range(self.rows) for c in range(self.cols) if self.grid[r][c] > 0}
        self.initial_grid_bricks = list(self.bricks.keys())
        self.total_bricks = len(self.bricks)
        self.lives = INITIAL_LIVES
        self.state = "playing"  # playing, life_lost, game_over, win
        self.state_timer = 0
        self.particles = []
        self.trail = []
        self.shattering_bricks = {}  # (r, c): {"timer": int, "max": int, "elem": str, "bx": float, "by": float}
        self.sim_steps = 0
        self.miss_active = False
        self.miss_side = None
        self.ambient_items = init_ambient_effects(self.theme, self.canvas_w, self.canvas_h)

        self.reset_ball()

    def reset_ball(self):
        # Paddle and ball positioned dynamically across bottom
        self.paddle_x = random.uniform(self.margin_x + 10, self.canvas_w - self.margin_x - self.paddle_w - 10)
        self.ball_x = self.paddle_x + self.paddle_w / 2
        self.ball_y = self.paddle_y - self.ball_r - 4

        # Completely randomized organic launch angles across full upper arc (-155 deg to -25 deg)
        launch_deg = random.uniform(-155, -25)
        # Avoid near-horizontal launch angles
        if -100 < launch_deg < -80:
            launch_deg = random.choice([random.uniform(-150, -105), random.uniform(-75, -30)])
        rad = math.radians(launch_deg)
        self.vx = self.speed * math.cos(rad)
        self.vy = self.speed * math.sin(rad)

        self.miss_active = False
        self.miss_side = None
        self.trail = []

    def spawn_particles(self, x, y, count=8, is_trail=False):
        new_p = create_ball_particles(self.skin, x, y, count=count, is_trail=is_trail)
        if new_p:
            self.particles.extend(new_p)

    def spawn_paddle_particles(self):
        new_p = create_paddle_particles(self.paddle_skin, self.paddle_x, self.paddle_y, self.paddle_w, self.paddle_h)
        if new_p:
            self.particles.extend(new_p)

    def step(self):
        self.sim_steps += 1

        self.particles = update_particles(self.particles, self.sim_steps)

        # Update shattering bricks animation & release finale burst
        expired_shatters = []
        for (r, c), sh in self.shattering_bricks.items():
            sh["timer"] -= 1
            if sh["timer"] <= 0:
                expired_shatters.append((r, c))
                # Release element-specific burst when shattering concludes
                elem = sh["elem"]
                cx = sh["bx"] + self.cell_w / 2
                cy = sh["by"] + self.cell_h / 2
                if elem == "ice":
                    # Frost shards break apart
                    self.spawn_particles(cx, cy, count=7)
                elif elem == "fire":
                    # Ashes and burning embers burst
                    self.spawn_particles(cx, cy, count=6)
                elif elem == "lightning":
                    # Overload sparks burst
                    self.spawn_particles(cx, cy, count=6)
                elif elem == "poison":
                    # Toxic acid splash
                    self.spawn_particles(cx, cy, count=5)
                else:
                    self.spawn_particles(cx, cy, count=4)

        for rc in expired_shatters:
            del self.shattering_bricks[rc]

        # Spawn ambient trail particles behind the ball in flight (subtle & short)
        if self.state == "playing" and self.sim_steps % 3 == 0:
            self.spawn_particles(self.ball_x, self.ball_y, count=1, is_trail=True)

        # Spawn specialized particles from paddle when in play
        if self.state == "playing":
            self.spawn_paddle_particles()

        # Update animated theme ambient background items
        update_ambient_effects(self.ambient_items, self.theme.get("bg_effect"), self.sim_steps, self.canvas_w, self.canvas_h)

        # Update motion trail (compact tail: max 2 points)
        if self.state == "playing":
            self.trail.append((self.ball_x, self.ball_y))
            if len(self.trail) > 2:
                self.trail.pop(0)
        else:
            self.trail = []

        # Delay before respawning ball or resetting game
        if self.state in ("life_lost", "game_over", "win"):
            self.state_timer += 1
            if self.state == "life_lost" and self.state_timer > 14:
                self.reset_ball()
                self.state = "playing"
                self.state_timer = 0
            elif self.state == "game_over" and self.state_timer > 25:
                self.reset_game()
            return

        self.ball_x += self.vx
        self.ball_y += self.vy

        # Wall collisions with subtle elemental impact sparks
        if self.ball_x - self.ball_r <= self.margin_x:
            self.ball_x = self.margin_x + self.ball_r
            self.vx = abs(self.vx)
            self.spawn_particles(self.ball_x, self.ball_y, count=3)
        elif self.ball_x + self.ball_r >= self.canvas_w - self.margin_x:
            self.ball_x = self.canvas_w - self.margin_x - self.ball_r
            self.vx = -abs(self.vx)
            self.spawn_particles(self.ball_x, self.ball_y, count=3)

        if self.ball_y - self.ball_r <= 10:
            self.ball_y = 10 + self.ball_r
            self.vy = abs(self.vy)
            self.spawn_particles(self.ball_x, self.ball_y, count=3)

        # Ensure vertical speed never stagnates horizontally
        if abs(self.vy) < 2.5:
            self.vy = -2.5 if self.vy <= 0 else 2.5

        # Dynamic miss trigger: independent roll on descent across varying heights and positions
        if self.vy > 0 and 100 < self.ball_y < 145 and not self.miss_active:
            # Chance to miss slightly varied per run, never trigger miss if lives <= 1 to avoid premature game over
            drop_prob = 0.12 if len(self.bricks) > 10 else 0.05
            if self.lives > 1 and random.random() < drop_prob:
                self.miss_active = True
                self.miss_side = random.choice([-1, 1])
                # Variable narrow gap for organic near-miss sensation
                self.miss_gap = random.uniform(3.0, 7.5)

        # Paddle tracking: stays extremely close to the ball
        if self.miss_active and self.ball_y > 150:
            if self.miss_side == 1:
                target_px = self.ball_x + self.miss_gap
            else:
                target_px = self.ball_x - self.paddle_w - self.miss_gap
            lerp_speed = random.uniform(0.68, 0.78)
        else:
            # Dynamic human-like tracking variation
            wobble = math.sin(self.sim_steps * 0.12) * random.uniform(4.0, 8.0)
            target_px = self.ball_x - self.paddle_w / 2 + wobble
            lerp_speed = 0.85

        self.paddle_x += (target_px - self.paddle_x) * lerp_speed
        self.paddle_x = max(self.margin_x, min(self.canvas_w - self.margin_x - self.paddle_w, self.paddle_x))

        # Paddle bounce
        if self.vy > 0 and (self.paddle_y - 2 <= self.ball_y + self.ball_r <= self.paddle_y + self.paddle_h + 4):
            if self.paddle_x - 3 <= self.ball_x <= self.paddle_x + self.paddle_w + 3:
                self.miss_active = False
                self.miss_side = None

                # Spawn subtle elemental impact spark on paddle bounce
                self.spawn_particles(self.ball_x, self.paddle_y, count=4)

                # Realistic physics bounce based on hit point on paddle (-1 to 1) + dynamic random tilt
                hit_offset = (self.ball_x - (self.paddle_x + self.paddle_w / 2)) / (self.paddle_w / 2)
                hit_offset = max(-0.95, min(0.95, hit_offset))
                hit_offset += random.uniform(-0.15, 0.15)
                hit_offset = max(-0.95, min(0.95, hit_offset))

                # Map hit_offset to bounce angle (-145 deg to -35 deg)
                bounce_angle = math.radians(-90 + hit_offset * 55)
                self.vx = self.speed * math.cos(bounce_angle)
                self.vy = self.speed * math.sin(bounce_angle)

                # Dynamically steer toward remaining bricks to clear board without looping forever
                pull_prob = 0.55 if len(self.bricks) > 6 else 0.90
                if self.bricks and random.random() < pull_prob:
                    target_b = random.choice(list(self.bricks.keys()))
                    tx = self.margin_x + target_b[1] * self.cell_w + self.cell_w / 2
                    ty = self.margin_y + target_b[0] * self.cell_h + self.cell_h / 2
                    dx = tx - self.ball_x
                    dy = ty - self.ball_y
                    dist = math.hypot(dx, dy)
                    if dist > 0:
                        target_ang = math.atan2(dy, dx)
                        blend_weight = 0.65 if len(self.bricks) > 6 else 0.85
                        blend_ang = bounce_angle * (1 - blend_weight) + target_ang * blend_weight
                        self.vx = self.speed * math.cos(blend_ang)
                        self.vy = -abs(self.speed * math.sin(blend_ang))

        # Ball falls below screen (miss)
        if self.ball_y - self.ball_r > self.canvas_h:
            self.lives -= 1
            self.miss_active = False
            self.miss_side = None
            self.spawn_particles(self.ball_x, self.canvas_h - 10, count=14)
            if self.lives <= 0:
                self.state = "game_over"
            else:
                self.state = "life_lost"
            self.state_timer = 0
            return

        # Discrete brick collision using AABB edge clamping
        for (r, c) in list(self.bricks.keys()):
            bx1 = self.margin_x + c * self.cell_w
            by1 = self.margin_y + r * self.cell_h
            bx2 = bx1 + self.cell_w
            by2 = by1 + self.cell_h

            if (bx1 - self.ball_r <= self.ball_x <= bx2 + self.ball_r and
                by1 - self.ball_r <= self.ball_y <= by2 + self.ball_r):

                del self.bricks[(r, c)]
                elem = self.skin.get("element", "none")
                # Trigger brick element transition (freezing / igniting / electrocuting / melting)
                shatter_dur = 6 if elem in ("ice", "fire", "poison") else 4
                self.shattering_bricks[(r, c)] = {
                    "timer": shatter_dur,
                    "max": shatter_dur,
                    "elem": elem,
                    "bx": bx1,
                    "by": by1,
                    "orig_val": self.grid[r][c]
                }
                # Initial light contact spark
                self.spawn_particles((bx1 + bx2) / 2, (by1 + by2) / 2, count=2)

                # Determine impact normal vector
                overlap_l = (self.ball_x + self.ball_r) - bx1
                overlap_r = bx2 - (self.ball_x - self.ball_r)
                overlap_t = (self.ball_y + self.ball_r) - by1
                overlap_b = by2 - (self.ball_y - self.ball_r)

                min_overlap = min(overlap_l, overlap_r, overlap_t, overlap_b)

                if min_overlap == overlap_l or min_overlap == overlap_r:
                    self.vx = -self.vx
                else:
                    self.vy = -self.vy

                # Brick collision deflection with natural reflection + organic angular perturbation
                angle_perturb = random.uniform(-0.35, 0.35)
                cur_angle = math.atan2(self.vy, self.vx) + angle_perturb
                self.vx = self.speed * math.cos(cur_angle)
                self.vy = self.speed * math.sin(cur_angle)

                if len(self.bricks) == 0:
                    self.state = "win"
                    self.state_timer = 0
                break
