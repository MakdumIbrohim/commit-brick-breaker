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

# Visual Themes (Dark & Light)
THEMES = {
    "dark": {
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
    "light": {
        "bg_color": (255, 255, 255),
        "paddle_color": (9, 105, 218),
        "empty_brick": (235, 237, 240),
        "heart_color": (207, 34, 46),
        "score_text_color": (87, 96, 106),
        "banner_bg_color": (246, 248, 250),
        "win_text_color": (26, 127, 55),
        "lose_text_color": (207, 34, 46),
        "brick_colors": [
            (155, 233, 168), # 1-2 commits
            (64, 196, 99),   # 3-5 commits
            (48, 161, 78),   # 6-9 commits
            (33, 110, 57)    # 10+ commits
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
