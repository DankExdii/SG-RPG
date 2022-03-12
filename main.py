import random
import pygame
import sys
import functions.checkVal
import functions.newProblem
import json

pygame.init()

size = []
with open("settings.json") as f:
    data = json.load(f)
    size = data["resolution"]
    f.close()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SG RPG")
clock = pygame.time.Clock()
text = ""
check = functions.checkVal.checkVal
problem = functions.newProblem.newProblem(random.choice(["+", "-", ".", "/"]))
settings_button = pygame.image.load("assets/settings.png").convert_alpha()
play_button = pygame.image.load("assets/play.png").convert_alpha()
home_button = pygame.image.load("assets/home.png").convert_alpha()
player = pygame.image.load("assets/player.png").convert_alpha()
bg_tile = pygame.image.load("assets/bg tile.png").convert_alpha()
bg_tile.fill((128,128,128), special_flags=pygame.BLEND_RGBA_MULT)

if size == [720, 480]:
    resolution_button = pygame.image.load("assets/480.png").convert_alpha()
    resolution_button = pygame.transform.scale(resolution_button, [100, 50])
    settings_button = pygame.transform.scale(settings_button, [100, 50])
    play_butoon = pygame.transform.scale(play_button, [100, 50])
    home_button = pygame.transform.scale(home_button, [100, 50])
    big_font = pygame.font.Font("assets/font.TTF", 32)
    normal_font = pygame.font.Font("assets/font.TTF", 28)
    player = pygame.transform.scale(player, [73, 117])
    bg_tile = pygame.transform.scale(bg_tile, [720, 480])
else:
    resolution_button = pygame.image.load("assets/720.png").convert_alpha()
    resolution_button = pygame.transform.scale(resolution_button, [150, 75])
    settings_button = pygame.transform.scale(settings_button, [150, 75])
    play_button = pygame.transform.scale(play_button, [150, 75])
    home_button = pygame.transform.scale(home_button, [150, 75])
    normal_font = pygame.font.Font("assets/font.TTF", 36)
    big_font = pygame.font.Font("assets/font.TTF", 40)
    player = pygame.transform.scale(player, [110, 176])
    bg_tile = pygame.transform.scale(bg_tile, [1280, 720])


#   --- whether the problem should show and allow keyboard input or not
debounce = False

def draw_tutorial():
    screen.fill((0,0,0))
    text_text = big_font.render("Tutorial", False, (255, 255, 255))
    text_text_rect = text_text.get_rect()
    bg_tile_rect = bg_tile.get_rect()

    text_text_rect.center = (size[0] // 2, size[1] // 2)
    bg_tile_rect.center = (size[0] // 2, size[1] // 2)

    screen.blit(bg_tile, bg_tile_rect)
    screen.blit(text_text, text_text_rect)
    pygame.display.update()

def tutorial():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        draw_tutorial()
        clock.tick(60)

def draw_level_select():
    screen.fill((0,0,0))
    text_text = big_font.render("Level Select", False, (255,255,255))
    text_text_rect = text_text.get_rect()
    bg_tile_rect = bg_tile.get_rect()

    text_text_rect.center = (size[0] // 2, size[1] // 2)
    bg_tile_rect.center = (size[0] // 2, size[1] // 2)

    screen.blit(bg_tile, bg_tile_rect)
    screen.blit(text_text, text_text_rect)
    pygame.display.update()

def level_select():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return
        draw_level_select()
        clock.tick(60)

#   --- draw fight screen ---
def draw_fight():
    global text
    global problem

    screen.fill((0,0,0))

    problem_text = big_font.render("", False, (255, 255, 255)) if debounce else big_font.render(f"Колко е {problem[0]} {problem[2]} {problem[1]}?", True, (255, 255, 255))
    answer_text = normal_font.render("", False, (255, 255, 255)) if debounce else normal_font.render(f"Отговор: {text}", True, (255, 255, 255)) 

    bg_tile_rect = bg_tile.get_rect()
    problem_rect = problem_text.get_rect()
    answer_rect = answer_text.get_rect()
    player_rect = player.get_rect()
    problem_rect.center = (size[0] // 2, size[1] // 2)
    answer_rect.center = (size[0] // 2, size[1] // 2 + 34)
    player_rect.center = (size[0] // 10, size[1] // 2)
    bg_tile_rect.center = (size[0] // 2, size[1] // 2)

    screen.blit(bg_tile, bg_tile_rect)
    screen.blit(problem_text, problem_rect)
    screen.blit(answer_text, answer_rect)
    screen.blit(player, player_rect)
        
    pygame.display.update()

#    --- main game loop ---
def game():
    global text
    global problem
    global debounce
    text = ""
    counter = 0

    with open("tutorial.json") as f:
        data = json.load(f)
        if data["done_tutorial"] == False:
            tutorial()
        else:
            level_select()

    #   --- keep the program alive ---
    while True:
        
        #   --- event handling ---
        for e in pygame.event.get():
            
            #   --- if close then close ---
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #   --- input handling ---
            if e.type == pygame.KEYDOWN:
                if not debounce: 
                    
                    #   --- if enter is pressed ---
                    if e.key == pygame.K_RETURN:
                        if text != "":
                            if check(int(text), problem[0], problem[1], problem [2]):
                                problem = functions.newProblem.newProblem(random.choice(["+", "-", "*", "/"]))
                                debounce = True
                                counter = 0
                            else:
                                counter += 1
                                if counter >= 3:
                                    counter = 0
                                    problem = functions.newProblem.newProblem(random.choice(["+", "-", "*", "/"]))
                        text = ""
                    
                    #   --- if backspace is pressed please kill me omg ---
                    elif e.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    
                    #   --- if any number key is pressed send help please ---
                    elif e.key == pygame.K_0 or e.key == pygame.K_1 or e.key == pygame.K_2 or e.key == pygame.K_3 or e.key == pygame.K_4 or e.key == pygame.K_5 or e.key == pygame.K_6 or e.key == pygame.K_7 or e.key == pygame.K_8 or e.key == pygame.K_9:
                        text += e.unicode


        draw_fight()
        clock.tick(60)

#   --- draw settings screen ---
def draw_settings():
    global resolution_rect
    global home_rect
    resolution_rect = resolution_button.get_rect()
    bg_tile_rect = bg_tile.get_rect()
    home_rect = home_button.get_rect()
    
    resolution_rect.center = (size[0] // 2, size[1] // 2 - 24) if size == [720, 480] else (size[0] //  2, size[1] // 2 - 48)
    home_rect.center = (size[0] // 2, size[1] // 2 + 24) if size == [720, 480] else (size[0] //  2, size[1] // 2 + 48)
    bg_tile_rect.center = (size[0] // 2, size[1] // 2)

    screen.blit(bg_tile, bg_tile_rect)
    screen.blit(resolution_button, resolution_rect)
    screen.blit(home_button, home_rect)
    pygame.display.update()

#   --- settings loop ---
def settings():
    global resolution_button
    global settings_button
    global play_button
    global home_button
    global normal_font
    global big_font
    global size
    global screen
    global bg_tile

    while True:
        screen.fill((0, 0, 0))
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resolution_rect.collidepoint(mouse_x, mouse_y):
                    if size == [720, 480]:
                        with open("settings.json", "w") as f:                           
                            json.dump({"resolution": [1280, 720]}, f)
                            f.close()

                        settings_button = pygame.transform.scale(settings_button, [150, 75])
                        play_button = pygame.transform.scale(play_button, [150, 75])
                        home_button = pygame.transform.scale(home_button, [150, 75])
                        resolution_button = pygame.image.load("assets/720.png").convert_alpha()
                        resolution_button = pygame.transform.scale(resolution_button, [150, 75])
                        bg_tile = pygame.transform.scale(bg_tile, [1280, 720])

                        normal_font = pygame.font.Font(None, 36)
                        big_font = pygame.font.Font(None, 40)

                        size = [1280, 720]
                        screen = pygame.display.set_mode(size)
                    else:
                        with open("settings.json", "w") as f:
                            json.dump({"resolution": [720, 480]}, f)
                            f.close()

                        settings_button = pygame.transform.scale(settings_button, [100, 50])
                        play_button = pygame.transform.scale(play_button, [100, 50])
                        home_button = pygame.transform.scale(home_button, [100, 50])
                        resolution_button = pygame.image.load("assets/480.png").convert_alpha()
                        resolution_button = pygame.transform.scale(resolution_button, [100, 50])
                        bg_tile = pygame.transform.scale(bg_tile, [720, 480])

                        normal_font = pygame.font.Font(None, 28)
                        big_font = pygame.font.Font(None, 32)
                      
                        size = [720, 480]
                        screen = pygame.display.set_mode(size)
                if home_rect.collidepoint(mouse_x, mouse_y):
                    return

        draw_settings()
        clock.tick(60)

#    --- draw main screen ---
def draw_main():
    global settings_rect
    global play_rect
    settings_rect = settings_button.get_rect()
    play_rect = play_button.get_rect()
    bg_tile_rect = bg_tile.get_rect()

    bg_tile_rect.center = (size[0] // 2, size[1] // 2)
    settings_rect.center = (size[0] // 2, size[1] // 2 + 24) if size == [720, 480] else (size[0] //  2, size[1] // 2 + 48)
    play_rect.center = (size[0] // 2, size[1] // 2 - 24) if size == [720, 480] else (size[0] //  2, size[1] // 2 - 48)

    screen.blit(bg_tile, bg_tile_rect)
    screen.blit(settings_button, settings_rect)
    screen.blit(play_button, play_rect)
    pygame.display.update()

#   --- main screen loop ---
def main():
    while True:
        for e in pygame.event.get():
            
            #   --- if close then close ---
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.MOUSEBUTTONDOWN:  
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if settings_rect.collidepoint(mouse_x, mouse_y):
                    settings()
                if play_rect.collidepoint(mouse_x, mouse_y):
                    game()
        draw_main()
        clock.tick(60)

#   --- start the program ---
if __name__ == "__main__":
    main()