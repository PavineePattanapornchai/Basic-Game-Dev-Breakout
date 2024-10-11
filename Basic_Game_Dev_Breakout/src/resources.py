import pygame
from src.Util import SpriteManager
from src.StateMachine import StateMachine

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

s_paddle_image_list = [
    sprite_collection["p_blue_1"].image,
    sprite_collection["p_green_1"].image,
    sprite_collection["p_red_1"].image,
    sprite_collection["p_purple_1"].image,
]

paddle_image_list = [
    sprite_collection["p_blue_2"].image,
    sprite_collection["p_green_2"].image,
    sprite_collection["p_red_2"].image,
    sprite_collection["p_purple_2"].image,
]

ball_image_list = [
    sprite_collection["blue_ball"].image,
    sprite_collection["green_ball"].image,
    sprite_collection["red_ball"].image,
    sprite_collection["purple_ball"].image,
    sprite_collection["gold_ball"].image,
    sprite_collection["gray_ball"].image,
    sprite_collection["last_ball"].image,
]

# Load extra paddle sprite
extra_paddle_image = sprite_collection["p_blue_2"].image  # Extra paddle

# Load power-up images (explicit entries)
power_up_images = {
    "multi_paddle": sprite_collection["p_blue_2"].image,  # This is not used for now
    "extra_life": sprite_collection["heart"].image,  # Extra life power-up
    "ball": sprite_collection["blue_ball"].image,  # Image for multi-ball power-up
}


# Load dragon sprite
dragon_image = pygame.image.load('./graphics/dragon.png')  # Ensure dragon.png is in the graphics folder

gFonts = {
    "small": pygame.font.Font("./fonts/SuperMario256.ttf", 24),
    "medium": pygame.font.Font("./fonts/SuperMario256.ttf", 48),
    "large": pygame.font.Font("./fonts/SuperMario256.ttf", 96),
}

gSounds = {
    "confirm": pygame.mixer.Sound("sounds/confirm.wav"),
    "paddle-hit": pygame.mixer.Sound("sounds/paddle_hit.wav"),
    "pause": pygame.mixer.Sound("sounds/pause.wav"),
    "recover": pygame.mixer.Sound("sounds/recover.wav"),
    "victory": pygame.mixer.Sound("sounds/victory.wav"),
    "hurt": pygame.mixer.Sound("sounds/hurt.wav"),
    "select": pygame.mixer.Sound("sounds/select.wav"),
    "no-select": pygame.mixer.Sound("sounds/no-select.wav"),
    "wall-hit": pygame.mixer.Sound("sounds/wall_hit.wav"),
    "high-score": pygame.mixer.Sound("sounds/high_score.wav"),
    "brick-hit1": pygame.mixer.Sound("sounds/brick-hit-1.wav"),
    "brick-hit2": pygame.mixer.Sound("sounds/brick-hit-2.wav"),
    # "powerup": pygame.mixer.Sound("sounds/powerup.wav"),  # Sound for collecting power-up
    #"extra_life": pygame.mixer.Sound("sounds/extra_life.wav"),  # Sound for extra life
}

brick_image_list = [
    sprite_collection["b_blue_1"].image,
    sprite_collection["b_blue_2"].image,
    sprite_collection["b_blue_3"].image,
    sprite_collection["b_blue_4"].image,
    sprite_collection["b_green_1"].image,
    sprite_collection["b_green_2"].image,
    sprite_collection["b_green_3"].image,
    sprite_collection["b_green_4"].image,
    sprite_collection["b_red_1"].image,
    sprite_collection["b_red_2"].image,
    sprite_collection["b_red_3"].image,
    sprite_collection["b_red_4"].image,
    sprite_collection["b_purple_1"].image,
    sprite_collection["b_purple_2"].image,
    sprite_collection["b_purple_3"].image,
    sprite_collection["b_purple_4"].image,
    sprite_collection["b_orange_1"].image,
    sprite_collection["b_orange_2"].image,
    sprite_collection["b_orange_3"].image,
    sprite_collection["b_orange_4"].image,
    sprite_collection["b_gray"].image,
]
