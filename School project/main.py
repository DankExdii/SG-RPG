import random
import pygame
import sys
import functions.checkVal
import functions.newProblem

pygame.init()

size = [720, 480]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("SG RPG")
clock = pygame.time.Clock()
text = ""
check = functions.checkVal.checkVal
problem = functions.newProblem.newProblem(random.choice(["+", "-", "*", "/"]))
big_font = pygame.font.Font(None, 32)
normal_font = pygame.font.Font(None, 28)
settings_button = pygame.image.load("assets/settings.png").convert()
play_button = pygame.image.load("assets/play.png").convert()
resolution_button = pygame.image.load("assets/480.png").convert()

#   --- whether the problem should show and allow keyboard input or not
debounce = False

#   --- draw fight screen ---
def draw_fight():
    global text
    global problem

    screen.fill((0,0,0))

    problem_text = big_font.render("", False, (255, 255, 255)) if debounce else big_font.render(f"Колко е {problem[0]} {problem[2]} {problem[1]}?", True, (255, 255, 255))
    answer_text = normal_font.render("", False, (255, 255, 255)) if debounce else normal_font.render(f"Отговор: {text}", True, (255, 255, 255)) 

    problem_rect = problem_text.get_rect()
    answer_rect = answer_text.get_rect()
    problem_rect.center = (720 // 2, 480 // 2)
    answer_rect.center = (720//2, 480 // 2 + 34)

    screen.blit(problem_text, problem_rect)
    screen.blit(answer_text, answer_rect)
        
    pygame.display.update()

#    --- main game loop ---
def game():
    global text
    global problem
    global debounce
    text = ""
    counter = 0

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
                        if text == "":
                            print("Invalid input")
                        else:
                            print(check(int(text), problem[0], problem[1], problem[2]))
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
                        print(text)


        draw_fight()
        clock.tick(60)

#   --- draw settings screen ---
def draw_settings():
    global resolution_rect
    resolution_rect = resolution_button.get_rect()
    resolution_rect.center = (720 // 2, 480 // 2)

    screen.blit(resolution_button, resolution_rect)
    print("s")

#   --- settings loop ---
def settings():
    global resolution_button
    global size
    global screen
    mouse_x, mouse_y = pygame.mouse.get_pos()

    while True:
        screen.fill((0, 0, 0))
        draw_settings()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if resolution_rect.collidepoint(mouse_x, mouse_y):
                    resolution_button = pygame.image.load("assets/720.png").convert()
                    size = [1280, 720]
                    screen = pygame.display.set_mode(size)
            


#    --- draw main screen ---
def draw_main():
    global settings_rect
    global play_rect
    settings_rect = settings_button.get_rect()
    settings_rect.center = (size[0] // 2, size[1] // 2 + 24)
    play_rect = play_button.get_rect()
    play_rect.center = (size[0] // 2, size[1] // 2 - 24)

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