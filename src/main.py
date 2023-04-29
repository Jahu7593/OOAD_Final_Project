import pygame
import bird
import pipe
import restart
import scoreObserver

class Main():
    # imports all pygame modules and then initialzes it
    pygame.init()

    global clock, fps
    clock = pygame.time.Clock()
    fps = 60

    global restart_condition
    restart_condition = False

    global bird_selected, location_selected
    bird_selected = 0
    location_selected = 0   #indices track which bird/location the player has selected, intialized at 0
    global location_list
    location_list = ["City"]   #may want to encapsulate in seperate "Map" or "Location" class later
    global bird_list
    bird_list = ["Flappy", "Cessna"]

    #make new instance of score observer
    global subject
    subject = scoreObserver.Subject()
    file_observer = scoreObserver.FileWriter()
    subject.register_observer(file_observer)

    # game window
    global screen_width, screen_height
    screen_width = 864
    screen_height = 936

    global screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    restart.screen = screen
    pygame.display.set_caption('Flappy Bird Game')

    # we need a background image for our game:
    global background_img
    background_img = pygame.image.load('img/background.png')
    global ground
    ground = pygame.image.load('img/ground.png')

    global font, small_font, white, orange
    font = pygame.font.SysFont('Bauhaus 93', 60)
    small_font = pygame.font.SysFont('Bauhaus 93', 35)
    white = (255, 255, 255)
    orange = (255, 124, 31)

    global game_stopped
    game_stopped = True

    # This is to write the score to a file/img
    @staticmethod
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

    @staticmethod
    def reset_game():
        pipe.pipe_group.empty()
        bird.flappy.rect.x = 100
        bird.flappy.rect.y = int(screen_height / 2)
        score = 0
        return score

    @staticmethod
    def quit_game():
        # Exit Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def main(self):

        scroll = 0
        # how many pixels the ground moves
        speed = 4
        # To handle the start of the game
        flying = False
        game_over = False
        #to make sure the score gets recorded
        added = False
        # this means we'll satrt making pipes right away
        last_pipe = pygame.time.get_ticks() - pipe.pipe_frequency
        run = True
        score = 0
        pass_pipe = False
        high_score = 0

        # we want to run the game until someone exits out of it
        while run:

            # Quit
            self.quit_game()

            clock.tick(fps)

            # load the background image into the game
            screen.blit(background_img, (0, 0))

            bird.bird_group.draw(screen)
            bird.bird_group.update()

            pipe.pipe_group.draw(screen)

            # checking the score
            if len(pipe.pipe_group) > 0:
                # checking to see if bird has passed through the left hand side of the pipe
                if bird.bird_group.sprites()[0].rect.left > pipe.pipe_group.sprites()[0].rect.left\
                        and bird.bird_group.sprites()[0].rect.right < pipe.pipe_group.sprites()[0].rect.right\
                        and pass_pipe == False:
                    pass_pipe = True
                if pass_pipe == True:
                    # Has the bird exited the pipe?
                    if bird.bird_group.sprites()[0].rect.left > pipe.pipe_group.sprites()[0].rect.right:
                        score += 1
                        pass_pipe = False

            self.draw_text(str(score), font, white, int(screen_width/2), 20)

            # load the ground image into the game (scrolling background)
            # x coordinate needs to change so that the ground can move
            screen.blit(ground, (scroll, 768))

            if pygame.sprite.groupcollide(bird.bird_group, pipe.pipe_group, False, False) or bird.flappy.rect.top < 0:
                if not added:
                    # subject.notify_observers(score)
                    added = True
                game_over = True
                bird.Bird.game_over = game_over

            # checking if the bird has hit the ground:
            if bird.flappy.rect.bottom >= 768:
                game_over = True
                bird.Bird.game_over = game_over
                flying = False
                bird.Bird.flying = flying

            if game_over == False and flying == True:
                # generate new pipes
                last_pipe = pipe.new_pipes(last_pipe)

                scroll -= speed
                # This ensures that the ground looks like it's continuously moving
                if abs(scroll) > 35:
                    scroll = 0

                # we only want to update the pipes when the game is running
                pipe.pipe_group.update()

            # checking if the game is over or we need to reset
            if game_over == True:
                if high_score < score:
                    high_score = score
                    subject.notify_observers(high_score)
                    # print("new high score", high_score)
                if restart.button.draw() == True:
                    # game has been restarted but isn't over
                    game_over = False
                    added = False
                    bird.Bird.game_over = game_over
                    score = self.reset_game()

            for event in pygame.event.get():
                # if someone selects the exit out of the game button
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
                    flying = True
                    bird.Bird.flying = flying

            pygame.display.update()

        pygame.quit()

    def image_to_image():
        return

    def main_menu(self):
        if restart_condition == True:
            btn1_string = "Restart"
        else:
            btn1_string = "Start"

        while True: # Draw Main Menu
            #get mouse pointer position
            mx, my = pygame.mouse.get_pos()
            #get width/length of text for centering
            fb_width, fb_height = font.size("FLAPPY BIRD")    
            start_width, start_height = small_font.size(btn1_string)
            options_width, options_height = small_font.size("Options")
            exit_width, exit_height = small_font.size("Exit")
            #Set positions
            button_width = 200
            button_height = 50
            title_y = int(screen_height/2 - fb_height/2 - 300)
            b1x = int(screen_width/2 - button_width/2)   #center x
            b1y = title_y + 100    #y below title
            b2y = b1y + button_height + 30
            b3y = b1y + 2*button_height + 60
            #initialize buttons
            button1 = pygame.Rect(b1x, b1y, button_width, button_height)   #(x, y, width, height)
            button2 = pygame.Rect(b1x, b2y, button_width, button_height)
            button3 = pygame.Rect(b1x, b3y, button_width, button_height)
            #draw buttons
            pygame.draw.rect(screen, orange, button1, 0, 15)
            pygame.draw.rect(screen, orange, button2, 0, 15)
            pygame.draw.rect(screen, orange, button3, 0, 15)
            #draw white borders around buttons
            pygame.draw.rect(screen, white, pygame.Rect(b1x, b1y, button_width, button_height), 5, 15)
            pygame.draw.rect(screen, white, pygame.Rect(b1x, b1y + button_height + 30, button_width, button_height), 5, 15)
            pygame.draw.rect(screen, white, pygame.Rect(b1x, b1y + 2*button_height + 60, button_width, button_height), 5, 15)
            #draw text
            self.draw_text("FLAPPY BIRD", font, white, int(screen_width/2 - fb_width/2), title_y)  #draw "Flappy Bird" title
            self.draw_text(btn1_string, small_font, white, int(screen_width/2 - start_width/2), b1y + 5)  
            self.draw_text("Options", small_font, white, int(screen_width/2 - options_width/2), b2y + 5)  
            self.draw_text("Exit", small_font, white, int(screen_width/2 - exit_width/2), b3y + 5)  
            #check for clicks on buttons
            if button1.collidepoint((mx, my)):   #Start button returns to game loop
                if click:
                    return
            if button2.collidepoint((mx, my)):   #Options button opens options menu
                if click:
                    self.options_menu()
            if button3.collidepoint((mx, my)):   #Exit button quits the program (or escape)
                if click:
                    event.type = pygame.QUIT
            
            #event listner
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        event.type = pygame.QUIT
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()
        
    def options_menu(self):
        while True: # Draw Options Menu
            global location_selected, bird_selected   #need global keywork (again) when assigning to global variable in a local scope
            location_str = location_list[location_selected]
            bird_str = bird_list[bird_selected]
            #get mouse pointer position
            mx, my = pygame.mouse.get_pos()
            #get width/length of text for centering
            fb_width, fb_height = font.size("FLAPPY BIRD")    
            location_width, location_height = small_font.size(location_str)
            birdname_width, birdname_height = small_font.size(bird_str)
            back_width, back_height = small_font.size("Back")
            #Set positions
            button_width = 200
            button_height = 50
            title_y = int(screen_height/2 - fb_height/2 - 300)
            b1x = int(screen_width/2 - button_width/2)   #center x
            b1y = title_y + 100    #y below title
            b2y = b1y + button_height + 30
            b3y = b1y + 2*button_height + 60
            #initialize buttons
            left_button1 = pygame.draw.polygon(screen, orange, [[b1x-50, b1y+(button_height/2)], [b1x, b1y+button_height], [b1x, b1y]], 0)
            right_button1 = pygame.draw.polygon(screen, orange, [[b1x+button_width+50, b1y+(button_height/2)], [b1x+button_width, b1y+button_height], [b1x+button_width, b1y]], 0)
            left_button2 = pygame.draw.polygon(screen, orange, [[b1x-50, b2y+(button_height/2)], [b1x, b2y+button_height], [b1x, b2y]], 0)
            right_button2 = pygame.draw.polygon(screen, orange, [[b1x+button_width+50, b2y+(button_height/2)], [b1x+button_width, b2y+button_height], [b1x+button_width, b2y]], 0)
            button5 = pygame.Rect(b1x, b3y, button_width, button_height)
            #draw 2 orange backgrounds (for birdname and location)
            pygame.draw.rect(screen, orange, pygame.Rect(b1x, b1y, button_width, button_height), 0, 15)
            pygame.draw.rect(screen, orange, pygame.Rect(b1x, b1y + button_height + 30, button_width, button_height), 0, 15)
            #draw button 5 (back)
            pygame.draw.rect(screen, orange, button5, 0, 15)
            #draw white borders around buttons
            pygame.draw.rect(screen, white, pygame.Rect(b1x, b1y, button_width, button_height), 5, 15)
            pygame.draw.rect(screen, white, pygame.Rect(b1x, b1y + button_height + 30, button_width, button_height), 5, 15)
            pygame.draw.rect(screen, white, pygame.Rect(b1x, b1y + 2*button_height + 60, button_width, button_height), 5, 15)
            #draw text
            self.draw_text("FLAPPY BIRD", font, white, int(screen_width/2 - fb_width/2), title_y)  #draw "Flappy Bird" title
            self.draw_text(location_str, small_font, white, int(screen_width/2 - location_width/2), b1y + 5)  
            self.draw_text(bird_str, small_font, white, int(screen_width/2 - birdname_width/2), b2y + 5)  
            self.draw_text("Back", small_font, white, int(screen_width/2 - back_width/2), b3y + 5)  
            #check for clicks on buttons
            if left_button1.collidepoint((mx, my)):   #Left through MAPS list
                if click:
                    if(location_selected == 0):
                        location_selected = len(location_list) - 1
                    else:
                        location_selected -= 1
            if right_button1.collidepoint((mx, my)):   #Right through MAPS list
                if click:
                    if(location_selected == len(location_list)-1):
                        location_selected = 0
                    else:
                        location_selected += 1
            if left_button2.collidepoint((mx, my)):   #Left through BIRDS list
                if click:
                    if(bird_selected == 0):
                        bird_selected = len(bird_list) - 1
                    else:
                        bird_selected -= 1
            if right_button2.collidepoint((mx, my)):   #Right through BIRDS list
                if click:
                    if(bird_selected == len(bird_list)-1):
                        bird_selected = 0
                    else:
                        bird_selected += 1
            if button5.collidepoint((mx, my)):   #Back button returns to main_menu
                if click:
                    #load the same images as selected previously
                    img = pygame.image.load("img/background.png")  #destroy triangles by drawing over w/ location and bird
                    screen.blit(img, (0, 0))
                    bird = pygame.image.load("img/Flappy1.png")
                    screen.blit(bird, (100, int(screen_height/2)))
                    return
            
            #event listner
            click = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        event.type = pygame.QUIT
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()


    # Menu
    def start(self):
        skyline_image = pygame.image.load("img/background.png")
        ground_image = pygame.image.load("img/ground.png")
        bird_img = pygame.image.load("img/Flappy1.png")
        start_image = pygame.image.load("img/start.png")
        
        global game_stopped
        while game_stopped:
            self.quit_game()

            # Draw Menu
            screen.fill((0, 0, 0))
            screen.blit(skyline_image, (0, 0))
            screen.blit(ground_image, (0, 768))
            screen.blit(bird_img, (100, int(screen_height/2)))
            self.main_menu()
            restart_condition = True   #will render "restart" instead of "start" after the first main menu call
            screen.blit(start_image, (screen_width // 2 - start_image.get_width() // 2,
                                    screen_height // 2 - start_image.get_height() // 2))
            # User Input
            user_input = pygame.mouse.get_pressed()
            if user_input[0]:
                bird.clicked = True
                self.main()

            pygame.display.update()

obj = Main()
obj.start()  #Start the program