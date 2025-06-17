import pygame as pg
from settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('resources/textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('resources/textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'resources/textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('resources/textures/game_over.png', RES)
        self.win_image = self.get_texture('resources/textures/win.png', RES)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_crosshair()  # ← add this


    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        # Health bar config
        bar_width=300
        bar_height = 25
        bar_x = 20
        bar_y = 80
        current_health = max(self.game.player.health, 0)
        max_health = PLAYER_MAX_HEALTH
        health_ratio = current_health / max_health

     # Calculate percentage
        health_percent = int(health_ratio * 100)

        # Determine bar color
        if health_ratio > 0.5:
            color = (0, 200, 0)  # green
        elif health_ratio > 0.25:
            color = (255, 165, 0)  # orange
        else:
            color = (200, 0, 0)  # red

        # Draw bar background
        pg.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

        # Draw health fill
        pg.draw.rect(self.screen, color, (bar_x, bar_y, bar_width * health_ratio, bar_height))

        # Draw bar border
        pg.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 2)

        # Draw percentage text (ensure font module is initialized)
        if not pg.font.get_init():
            pg.font.init()
        font = pg.font.SysFont('Arial', 22, bold=True)
        text = font.render(f"{health_percent}%", True, (255, 255, 255))
        text_rect = text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        self.screen.blit(text, text_rect)
        
    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        # floor
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('resources/textures/1.png'),
            2: self.get_texture('resources/textures/2.png'),
            3: self.get_texture('resources/textures/3.png'),
            4: self.get_texture('resources/textures/4.png'),
            5: self.get_texture('resources/textures/5.png'),
        }
    def draw_crosshair(self):
        mx, my = pg.mouse.get_pos()
        crosshair_rect = self.crosshair_img.get_rect(center=(mx, my))
        self.screen.blit(self.crosshair_img, crosshair_rect)
        

        # Horizontal line
        pg.draw.line(self.screen, crosshair_color,
                     (center_x - length, center_y),
                     (center_x + length, center_y), thickness)

        # Vertical line
        pg.draw.line(self.screen, crosshair_color,
                     (center_x, center_y - length),
                     (center_x, center_y + length), thickness)
