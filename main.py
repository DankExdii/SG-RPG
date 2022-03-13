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
enemy = pygame.image.load("assets/enemy.png").convert_alpha()
attack = pygame.image.load("assets/attack.png").convert_alpha()
defend = pygame.image.load("assets/defend.png").convert_alpha()
sleep = pygame.image.load("assets/sleep.png").convert_alpha()
strength = pygame.image.load("assets/strength.png").convert_alpha()
bg_tile = pygame.image.load("assets/bg tile.png").convert_alpha()
bg_tile.fill((128,128,128), special_flags=pygame.BLEND_RGBA_MULT)
high_score = 0
fighting = False
hp_player = 100
max_hp_player = 100
hp_e = 100
max_hp_e = 100
score = 0
success = False
plr_atk = 1000
e_atk = 50
plr_def = 0
e_def = 0
e_action = ["attack", "defend"]
e_choice = None
plr_action = None
done = False

with open("highscore.json") as f:
    data = json.load(f)
    high_score = data["highscore"]

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
    enemy = pygame.transform.scale(enemy, [73, 117])
    attack = pygame.transform.scale(attack, [40, 40])
    defend = pygame.transform.scale(defend, [40, 40])
    strength = pygame.transform.scale(strength, [75, 100])
    sleep = pygame.transform.scale(sleep, [75, 100])

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
    enemy = pygame.transform.scale(enemy, [110, 176])
    attack = pygame.transform.scale(attack, [50, 50])
    defend = pygame.transform.scale(defend, [50, 50])
    strength = pygame.transform.scale(strength, [125, 150])
    sleep = pygame.transform.scale(sleep, [125, 150])

#   --- whether the problem should show and allow keyboard input or not
debounce = True

#   --- draw fight screen ---
def draw_fight():
    global text
    global problem
    global attack_rect
    global defend_rect
    global strength_rect
    global sleep_rect

    screen.fill((0,0,0))

    hb_plr = big_font.render("", False, (255,255,255)) if not fighting else big_font.render(f"{hp_player}/{max_hp_player}, {plr_def}", False, (255,255,255))
    hb_e = big_font.render("", False, (255,255,255)) if not fighting else big_font.render(f"{hp_e}/{max_hp_e}, {e_def}", False, (255,255,255))
    problem_text = big_font.render("", False, (255, 255, 255)) if debounce else big_font.render(f"Колко е {problem[0]} {problem[2]} {problem[1]}?", True, (255, 255, 255))
    answer_text = normal_font.render("", False, (255, 255, 255)) if debounce else normal_font.render(f"Отговор: {text}", True, (255, 255, 255)) 

    bg_tile_rect = bg_tile.get_rect()
    problem_rect = problem_text.get_rect()
    answer_rect = answer_text.get_rect()
    player_rect = player.get_rect()
    enemy_rect = enemy.get_rect()
    hb_plr_rect = hb_plr.get_rect()
    hb_e_rect = hb_e.get_rect()
    attack_rect = attack.get_rect()
    defend_rect = defend.get_rect()
    sleep_rect = sleep.get_rect()
    strength_rect = strength.get_rect()

    problem_rect.center = (size[0] // 2, size[1] // 2)
    answer_rect.center = (size[0] // 2, size[1] // 2 + 34)
    player_rect.center = (size[0] // 5, size[1] // 1.4)
    bg_tile_rect.center = (size[0] // 2, size[1] // 2)
    enemy_rect.center = (size[0] // 1.1, size[1] // 2)
    hb_plr_rect.center = (size[0] // 5, size[1] // 1.2)
    hb_e_rect.center = (size[0] // 1.1, size[1] // 2.6)
    attack_rect.center = (size[0] // 2.1, size[1] // 1.6)
    defend_rect.center = (size[0] // 1.9, size[1] // 1.6)
    sleep_rect.center = (size[0] // 1.8, size[1] // 2)
    strength_rect.center = (size[0] // 2.2, size[1] // 2)

    screen.blit(bg_tile, bg_tile_rect)
    screen.blit(problem_text, problem_rect)
    screen.blit(answer_text, answer_rect)
    screen.blit(player, player_rect)
    if fighting:
        screen.blit(enemy, enemy_rect)
        if debounce and not done:
            screen.blit(attack, attack_rect)
            screen.blit(defend, defend_rect)
        elif not debounce:
            attack_rect.center = (size[0] // 1.1, size[1] // 1.6)
            defend_rect.center = (size[0] // 1.1, size[1] // 1.6)
            if e_choice == "defend":
                screen.blit(defend, defend_rect)
            elif e_choice == "attack":
                screen.blit(attack, attack_rect)
    else:
        if score > 0:
            screen.blit(sleep, sleep_rect)
            screen.blit(strength, strength_rect)
    screen.blit(hb_plr, hb_plr_rect)
    screen.blit(hb_e, hb_e_rect)
        
    pygame.display.update()

#    --- main game loop ---
def game():
    global text
    global problem
    global debounce
    global hp_e
    global max_hp_e
    global score
    global success
    global hp_player
    global bg_tile
    global plr_action
    global plr_def
    global e_def
    global done
    global e_choice
    global fighting
    global high_score
    global plr_atk
    global max_hp_player
    text = ""

    bg_tile = pygame.image.load("assets/bg fight.png")
    bg_tile.fill((128,128,128), special_flags=pygame.BLEND_RGBA_MULT)
    if size == [720,480]:
        bg_tile = pygame.transform.scale(bg_tile, [720, 480])
    else:
        bg_tile = pygame.transform.scale(bg_tile, [1280, 720])

    #   --- keep the program alive ---
    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        #   --- event handling ---
        for e in pygame.event.get():
            
            #   --- if close then close ---
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if fighting:
                if e.type == pygame.MOUSEBUTTONDOWN and debounce:                
                    e_choice = e_action[random.randint(0, 1)]
                    if attack_rect.collidepoint(mouse_x, mouse_y):
                        debounce = False
                        plr_action = "attack"
                        print("attacked")
                    elif defend_rect.collidepoint(mouse_x, mouse_y):
                        debounce = False
                        plr_action = "defend"
                        print("defended")

                #   --- input handling ---
                if e.type == pygame.KEYDOWN:
                    if not debounce: 
                        
                        #   --- if enter is pressed ---
                        if e.key == pygame.K_RETURN:
                            if text != "":
                                if check(int(text), problem[0], problem[1], problem [2]):
                                    problem = functions.newProblem.newProblem(random.choice(["+", "-", ".", "/"]))
                                    success = True
                                    debounce = True
                                else:
                                    problem = functions.newProblem.newProblem(random.choice(["+", "-", ".", "/"]))
                                    success = False
                                    debounce = True
                            text = ""
                        
                        #   --- if backspace is pressed please kill me omg ---
                        elif e.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        
                        #   --- if any number key is pressed send help please ---
                        elif e.key == pygame.K_0 or e.key == pygame.K_1 or e.key == pygame.K_2 or e.key == pygame.K_3 or e.key == pygame.K_4 or e.key == pygame.K_5 or e.key == pygame.K_6 or e.key == pygame.K_7 or e.key == pygame.K_8 or e.key == pygame.K_9:
                            text += e.unicode
            else:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if strength_rect.collidepoint(mouse_x, mouse_y):
                        plr_atk += 10
                        fighting = True
                    elif sleep_rect.collidepoint(mouse_x, mouse_y):
                        max_hp_player += max_hp_player * 0.1
                        hp_player += max_hp_player * 0.45
                        fighting = True

        if debounce and not done:
            if plr_action == "attack" and success:
                hp_e -= plr_atk - e_def
                e_def -= plr_atk
                if e_def < 0:
                    e_def = 0
                plr_action = None
                done = True
            elif plr_action == "defend" and success:
                plr_def += random.randint(1, 5)
                plr_action = None
                done = True
            if e_choice == "attack":
                hp_player -= e_atk - plr_def
                plr_def -= e_atk
                if plr_def < 0:
                    plr_def = 0
                print("enemy has attacked")
                done = False
            elif e_choice == "defend":
                increment = random.randint(1, 5)
                e_def += increment
                print(f"enemy defense rose +{increment}, {e_def}")
                done = False
            e_choice = None
            
        
        if hp_e <= 0:
            score += 1
            fighting = False
            max_hp_e += 10
            hp_e = max_hp_e
            e_def = 0
        elif hp_player <= 0:
            if score > high_score:
                with open("highscore.json", "w") as f:
                    json.dump({"highscore": score}, f)
                high_score = score
            hp_player = max_hp_player
            e_def = 0
            plr_def = 0
            return
            

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
    global strength
    global sleep
    global defend
    global attack
    global player
    global enemy

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
                        strength = pygame.transform.scale(strength, [125, 150])
                        sleep = pygame.transform.scale(sleep, [125, 150])
                        player = pygame.transform.scale(player, [110, 176])
                        enemy = pygame.transform.scale(enemy, [110, 176])
                        defend = pygame.transform.scale(defend, [50, 50])
                        attack = pygame.transform.scale(attack, [50, 50])

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
                        strength = pygame.transform.scale(strength, [75, 100])
                        sleep = pygame.transform.scale(sleep, [75, 100])
                        player = pygame.transform.scale(player, [73, 117])
                        enemy = pygame.transform.scale(enemy, [73, 117])
                        defend = pygame.transform.scale(defend, [40, 40])
                        attack = pygame.transform.scale(attack, [40, 40])

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
    
    screen.fill((0,0,0))

    title = big_font.render("SG RPG", False, (255,255,255))
    high_score_text = normal_font.render(f"рекорд: {high_score}", False, (255,255,255))
    
    title_rect = title.get_rect()
    settings_rect = settings_button.get_rect()
    play_rect = play_button.get_rect()
    bg_tile_rect = bg_tile.get_rect()
    high_score_text_rect = high_score_text.get_rect()

    title_rect.center = (size[0] // 2, size[1] // 4)
    high_score_text_rect.center = (size[0] // 2, size[1] // 3)
    bg_tile_rect.center = (size[0] // 2, size[1] // 2)
    settings_rect.center = (size[0] // 2, size[1] // 2 + 24) if size == [720, 480] else (size[0] //  2, size[1] // 2 + 48)
    play_rect.center = (size[0] // 2, size[1] // 2 - 24) if size == [720, 480] else (size[0] //  2, size[1] // 2 - 48)

    screen.blit(bg_tile, bg_tile_rect)
    screen.blit(title, title_rect)
    screen.blit(high_score_text, high_score_text_rect)
    screen.blit(settings_button, settings_rect)
    screen.blit(play_button, play_rect)
    pygame.display.update()

#   --- main screen loop ---
def main():
    global fighting
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
                    print("clicked play")
                    fighting = True
                    game()
        draw_main()
        clock.tick(60)

#   --- start the program ---
if __name__ == "__main__":
    main()