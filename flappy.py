import pygame
import random

class Hoop:

    def __init__(self):
        x = random.randint(2,5)
        self.back = hoop_back_surface.get_rect(center = (WIDTH+150, HEIGHT//x))
        self.front = hoop_front_surface.get_rect(center = (WIDTH+150, HEIGHT//x))
        self.direction = random.choice(['d', 'u'])
        self.crossed = False
    
    def draw_back(self):
        if self.crossed:
            screen.blit(hoop_back_win_surface, self.back)
        else:    
            screen.blit(hoop_back_surface, self.back)

    def draw_front(self):
        screen.blit(hoop_front_surface, self.front)

    def move(self):
        for pos in [self.back, self.front]:
            pos.centerx -= HOOP_VEL_X

            if pos.top <= 0:
                pos.centery += HOOP_VEL_Y
                self.direction = 'd'
            elif pos.bottom >= HEIGHT - FLOOR_HEIGHT:
                pos.centery -= HOOP_VEL_Y
                self.direction = 'u'
            else:
                if self.direction == 'u':
                    pos.centery -= HOOP_VEL_Y
                else:
                    pos.centery += HOOP_VEL_Y
    
    def update(self):
        global points
        if self.back.centerx == bat_rect.left:
            self.crossed = True
            points += 1


def display_logo():
    global angle
    logo_surf = pygame.transform.rotate(k_logo, angle)
    logo_rect = logo_surf.get_rect(center = (25, 25))
    screen.blit(logo_surf, logo_rect)
    angle -= 1

def move_hoops(hoops):
    for hoop in hoops:
        hoop.move()

def update_hoops(hoops):
    for hoop in hoops:
        hoop.update()

def rotate_bat(bat):
    new_bat = pygame.transform.rotate(bat, bat_y * 2.5)
    return new_bat

def display_bat():
    rotated_bat = rotate_bat(bat_surface)
    screen.blit(rotated_bat, bat_rect)

def draw_hoops_n_bat(hoops):
    for hoop in hoops:
        hoop.draw_back()
    display_bat()
    for hoop in hoops:
        hoop.draw_front()    

def draw_floor(floorx):
    if state == "run":
        floorx -= FLOOR_VEL
    screen.blit(floor, (floorx, HEIGHT-FLOOR_HEIGHT))
    screen.blit(floor1, (floorx + WIDTH, HEIGHT-FLOOR_HEIGHT))
    if floorx <= -WIDTH:
        floorx = 0
    return floorx

def display_score(p):
    if state == "run":
        msg = str(p)
        points_display = points_font.render(msg, True, (0,128,128))
        points_w, points_h = points_font.size(msg)
        add = 0
    if state == "end":
        msg = "Final Score: " + str(p)
        points_display = final_font.render(msg, True, (0,128,128))
        points_w, points_h = final_font.size(msg)
        add = 5
    screen.blit(points_display, ((WIDTH-points_w)//2, HEIGHT-LOSE_HEIGHT+add))

highscore = None
def display_high_score(p):
    global highscore
    if p > highscore:
        with open ("highscore.txt", 'w') as f:
            f.write(str(p))
            highscore = p
    msg = "High Score: " + str(highscore)
    points_display = high_font.render(msg, True, (200, 230, 230))
    points_w, points_h = high_font.size(msg)
    screen.blit(points_display, ((WIDTH-points_w)//2, 20))    

def check_collision(hoop_list):
    for hoop in hoop_list:
        if hoop.back.left < bat_rect.left and hoop.back.right > bat_rect.right:
            """
            Slightly lenient for the User
            if not bat_rect.colliderect(hoop.back):
                return True
            else:
                return False
            """
            if bat_rect.top <= hoop.back.top - LEEWAY or bat_rect.bottom >= hoop.back.bottom:
                return True
            else:
                return False

def check_loss(hoops):
    if check_collision(hoops):
        return True
    if bat_rect.bottom >= HEIGHT-LOSE_HEIGHT or bat_rect.top <= 0:
        return True
    return False

def restart():
    global state, hoop_list, bat_y, bat_rect, points, floor_xpos, bg_surface
    state = "run"
    hoop_list = []
    bat_rect.centery = HEIGHT//2
    bat_y = 0
    points = 0
    floor_xpos = 0
    bg_surface = pygame.image.load("assets/backgrounds/bg" + str(random.randint(1,7)) + ".jpg").convert()
    bg_surface = pygame.transform.scale(bg_surface, (WIDTH, HEIGHT))


# Constants
WIDTH = 288
HEIGHT = 486
FLOOR_HEIGHT = 122
LOSE_HEIGHT = 42
HOOP_WIDTH = 50
HOOP_HEIGHT = 100
FLOOR_VEL = 1.5
HOOP_VEL_X = 1
HOOP_VEL_Y = 1
GRAVITY = 0.2
JUMP_HEIGHT = 5
LEEWAY = 5

# Variables
bat_index = 0
angle = 0
floor_xpos = 0
bat_y = 0
points = 0
state = "start"

# Initialisation
pygame.init()
points_font = pygame.font.SysFont("monospace", 40)
final_font = pygame.font.SysFont("monospace", 25, bold=True)
high_font = pygame.font.SysFont("rockwell", 30)

# Screen and Clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Title & Icon
pygame.display.set_caption("Acro-bat")
icon = pygame.image.load("assets/icon.png").convert()
pygame.display.set_icon(icon)

# Background
bg_surface = pygame.image.load("assets/backgrounds/start.jpg").convert()
bg_surface = pygame.transform.scale(bg_surface, (WIDTH, HEIGHT))

# K Logo
k_logo = pygame.image.load("assets/K_logo.png")
k_logo = pygame.transform.scale(k_logo, (50, 50))

# High Score
with open("highscore.txt") as f:
    highscore = int(f.read())

# Floor
floor = pygame.image.load("assets/floor.png")
floor = pygame.transform.scale(floor, (WIDTH, FLOOR_HEIGHT))
floor1 = pygame.image.load("assets/floor.png")
floor1 = pygame.transform.scale(floor1, (WIDTH, FLOOR_HEIGHT))

# Bat

bat_downflap = pygame.image.load("assets/bat/downflap.png").convert_alpha()
bat_upflap = pygame.image.load("assets/bat/upflap.png").convert_alpha()
bat_frames = [bat_downflap, bat_upflap]
bat_surface = bat_frames[bat_index]
bat_rect = bat_surface.get_rect(center = (WIDTH//4, HEIGHT//2))



BATFLAP = pygame.USEREVENT
pygame.time.set_timer(BATFLAP, 250)

# Hoop
hoop_front_surface = pygame.image.load("assets/front.png")
hoop_front_surface = pygame.transform.scale(hoop_front_surface, (HOOP_WIDTH, HOOP_HEIGHT))
hoop_back_surface = pygame.image.load("assets/back.png")
hoop_back_surface = pygame.transform.scale(hoop_back_surface, (HOOP_WIDTH, HOOP_HEIGHT))
hoop_back_win_surface = pygame.image.load("assets/back-success.png")
hoop_back_win_surface = pygame.transform.scale(hoop_back_win_surface, (HOOP_WIDTH, HOOP_HEIGHT))

# Game Over
game_over = pygame.image.load("assets/gameover.png")
game_over = pygame.transform.scale(game_over, (WIDTH, HEIGHT))


hoop_list = []
SPAWNHOOP = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWNHOOP, 1500)


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and state == "start":
                restart()
            if event.key == pygame.K_SPACE and state == "run":
                bat_y = 0
                bat_y -= JUMP_HEIGHT
            if event.key == pygame.K_SPACE and state == "end":
                restart()
                state = "run"
            if event.key == pygame.K_ESCAPE and state == "end":
                running = False
            
        if event.type == BATFLAP and state == "run":
            if bat_index < len(bat_frames)-1 :
                bat_index += 1
            else:
                bat_index = 0
            bat_surface = bat_frames[bat_index]
            bat_rect = bat_surface.get_rect(center = (bat_rect.centerx, bat_rect.centery))
    
        if event.type == SPAWNHOOP and state == "run":
            hoop_list.append(Hoop())

    screen.blit(bg_surface, (0, 0))

    if state == "start":
        display_logo()

    if state == "run":
        bat_y += GRAVITY
        bat_rect.centery += bat_y
        
        move_hoops(hoop_list)
        update_hoops(hoop_list)
        draw_hoops_n_bat(hoop_list)
        
        floor_xpos = draw_floor(floor_xpos)
        display_score(points)

        
        if check_loss(hoop_list):
            state = "end"

    if state == "end":
        draw_hoops_n_bat(hoop_list)
        floor_xpos = draw_floor(floor_xpos)
        display_score(points)
        display_high_score(points)
        screen.blit(game_over, (0, 0))

    pygame.display.update()
    clock.tick(90)

print("fin.")
