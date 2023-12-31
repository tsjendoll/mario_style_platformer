import pygame
from support import import_folder
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index] 
        self.rect = self.image.get_rect(topleft = pos)

        # dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles
        # player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        self.facing = "right"
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        character_path = 'graphics/character'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + '/' + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.dust_run_paritcles = import_folder('graphics/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.get_status()]
        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        if self.facing == "left":
            self.image = pygame.transform.flip(animation[int(self.frame_index)],True, False)
        else:
            self.image = animation[int(self.frame_index)]

        # # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)
        # else:
        #     self.rect = self.image.get_rect(center = self.rect.center)
    
    def run_dust_animation(self):
        if self.get_status() == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_paritcles):
                self.dust_frame_index = 0
            print(self.dust_run_paritcles)
            print(int(self.dust_frame_index))

            dust_particle = self.dust_run_paritcles[int(self.dust_frame_index)]

            if self.facing == "right":
                pos = self.rect.bottomleft - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particle, pos)

            if self.facing == "left":
                dust_particle = pygame.transform.flip(self.dust_run_paritcles[int(self.dust_frame_index)],True, False)
                pos = self.rect.bottomright - pygame.math.Vector2(6,10)
                self.display_surface.blit(dust_particle, pos)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing = "left"
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing = "right"
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            return 'jump'
        elif self.direction.y > 0:
            return 'fall'
        else:
            if self.direction.x != 0:
                return 'run'
            else:
                return "idle"
        
    def jump(self):
        if self.on_ground:
            self.direction.y = self.jump_speed
            self.create_jump_particles(self.rect.midbottom)
 
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        
        
