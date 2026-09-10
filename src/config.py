# Display and Canvas Configuration
CANVAS_W = 640
CANVAS_H = 280
MARGIN_X = 16
MARGIN_Y = 28

# Gameplay & Physics Configuration
PADDLE_H = 8
BALL_R = 4
BALL_SPEED = 10.5
INITIAL_LIVES = 3

# Visual Themes with animated environmental board effects:
# - dark: cosmic starfield with twinkling distant stars
# - sky: Super Mario NES vibrant blue sky with floating clouds
# - synthwave: 80s neon horizon perspective grid
# - matrix: digital cyber rain streaming subtly in background
THEMES = {
    "dark": {
        "name": "dark",
        "bg_effect": "starfield",
        "bg_color": (13, 17, 23),
        "paddle_color": (88, 166, 255),
        "empty_brick": (22, 27, 34),
        "heart_color": (255, 107, 107),
        "score_text_color": (139, 148, 158),
        "banner_bg_color": (22, 27, 34),
        "win_text_color": (57, 211, 83),
        "lose_text_color": (248, 81, 73),
        "brick_colors": [
            (14, 68, 41),    # 1-2 commits
            (0, 109, 50),    # 3-5 commits
            (38, 166, 65),   # 6-9 commits
            (57, 211, 83)    # 10+ commits
        ]
    },
    "sky": {
        "name": "sky",
        "bg_effect": "mario_sky",
        "bg_color": (107, 140, 255),       # Classic Super Mario NES vibrant sky blue
        "paddle_color": (230, 75, 50),      # Mario red paddle
        "empty_brick": (140, 168, 255),     # Semi-translucent sky blue empty cells
        "heart_color": (255, 60, 60),
        "score_text_color": (255, 255, 255),
        "banner_bg_color": (255, 255, 255),
        "win_text_color": (34, 139, 34),
        "lose_text_color": (207, 34, 46),
        "brick_colors": [
            (255, 200, 110), # 1-2 commits (light coin gold)
            (240, 150, 40),  # 3-5 commits (mario question block orange)
            (195, 90, 20),   # 6-9 commits (brick block terracotta)
            (145, 50, 10)    # 10+ commits (hard brick brown)
        ]
    },
    "synthwave": {
        "name": "synthwave",
        "bg_effect": "neon_grid",
        "bg_color": (18, 11, 38),
        "paddle_color": (255, 0, 128),
        "empty_brick": (36, 22, 66),
        "heart_color": (255, 0, 128),
        "score_text_color": (210, 180, 255),
        "banner_bg_color": (36, 22, 66),
        "win_text_color": (0, 255, 204),
        "lose_text_color": (255, 0, 128),
        "brick_colors": [
            (88, 30, 140),
            (138, 43, 226),
            (186, 85, 211),
            (0, 255, 204)
        ]
    },
    "matrix": {
        "name": "matrix",
        "bg_effect": "matrix_rain",
        "bg_color": (5, 15, 8),
        "paddle_color": (0, 255, 70),
        "empty_brick": (12, 30, 16),
        "heart_color": (0, 255, 120),
        "score_text_color": (80, 180, 100),
        "banner_bg_color": (10, 28, 15),
        "win_text_color": (0, 255, 70),
        "lose_text_color": (255, 70, 70),
        "brick_colors": [
            (0, 60, 20),
            (0, 120, 40),
            (0, 190, 60),
            (0, 255, 70)
        ]
    }
}
DEFAULT_THEME = "dark"

# Ball Skins with specialized elements:
# - classic: pure green ball without particle/trail effects
# - fire: sparks & ember flames drifting upward
# - ice: icy snowflakes & frost crystals floating down
# - lightning: electric sparks & plasma zaps
# - poison: acidic bubbles & toxic vapor
BALL_SKINS = {
    "classic": {
        "name": "classic",
        "color": (57, 211, 83),
        "trail_color": None,
        "element": "none",
        "particle_colors": []
    },
    "fire": {
        "name": "fire",
        "color": (255, 140, 0),
        "trail_color": (255, 69, 0),
        "element": "fire",
        "particle_colors": [(255, 220, 50), (255, 140, 0), (255, 69, 0), (220, 20, 60)]
    },
    "ice": {
        "name": "ice",
        "color": (175, 238, 255),
        "trail_color": (88, 166, 255),
        "element": "ice",
        "particle_colors": [(240, 250, 255), (175, 238, 255), (120, 200, 255), (70, 150, 250)]
    },
    "lightning": {
        "name": "lightning",
        "color": (255, 255, 120),
        "trail_color": (180, 100, 255),
        "element": "lightning",
        "particle_colors": [(255, 255, 200), (255, 235, 60), (210, 140, 255), (160, 80, 255)]
    },
    "poison": {
        "name": "poison",
        "color": (57, 211, 83),
        "trail_color": (35, 134, 54),
        "element": "poison",
        "particle_colors": [(126, 231, 135), (57, 211, 83), (35, 134, 54), (0, 109, 50)]
    }
}
DEFAULT_SKIN = "classic"

# Paddle Skins with distinct visual geometry, textures & end-caps:
# - default: clean rounded pill paddle
# - laser: sci-fi plasma rail with angled laser emitter endcaps and power core
# - retro: 8-bit segmented striped block with rivet screws
# - mecha: futuristic armor plating with dual chevron side-boosters
# - cyber: pulsing grid synthwave paddle with neon border corners
PADDLE_SKINS = {
    "default": {
        "name": "default",
        "style": "default"
    },
    "laser": {
        "name": "laser",
        "style": "laser",
        "primary": (0, 245, 255),
        "core": (255, 255, 255),
        "caps": (0, 120, 215)
    },
    "retro": {
        "name": "retro",
        "style": "retro",
        "primary": (235, 130, 60),
        "stripes": (255, 215, 0),
        "caps": (160, 60, 20)
    },
    "mecha": {
        "name": "mecha",
        "style": "mecha",
        "primary": (139, 148, 158),
        "plate": (240, 246, 252),
        "booster": (255, 75, 75)
    },
    "cyber": {
        "name": "cyber",
        "style": "cyber",
        "primary": (210, 80, 255),
        "core": (0, 255, 200),
        "caps": (120, 20, 200)
    }
}
DEFAULT_PADDLE_SKIN = "default"
