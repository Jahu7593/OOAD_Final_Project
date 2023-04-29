import pygame
import bird
import pipe
import restart
import scoreObserver
import command

class Menu():  #Concrete menu implementation, controlled by Command
    # imports all pygame modules and then initialzes it
    pygame.init()
    def __init__(screen, self):  #pass in screen variable from Command
        global screen_height, screen_width
        screen_width, screen_height = pygame.display.get_surface().get_size()
        #Restart condition - False only for first menu display
        global restart_condition
        restart_condition = False  
        #init fonts/colors
        global font, small_font, white, orange
        font = pygame.font.SysFont('Bauhaus 93', 60)
        small_font = pygame.font.SysFont('Bauhaus 93', 35)
        white = (255, 255, 255)
        orange = (255, 124, 31)
        global location_selected, bird_selected
        location_selected = 0
        bird_selected = 0   #start w/ standard "Flappy" in standard "City"
        #for now storing locations/birds list here, may want to pass in from elsewhere later
        global locations_list, birds_list
        locations_list = ["City"]
        birds_list = ["Flappy"], ["Cessna"]
    
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
            location_str = locations_list[location_selected]
            bird_str = birds_list[bird_selected]
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
                        location_selected = len(locations_list) - 1
                    else:
                        location_selected -= 1
            if right_button1.collidepoint((mx, my)):   #Right through MAPS list
                if click:
                    if(location_selected == len(locations_list)-1):
                        location_selected = 0
                    else:
                        location_selected += 1
            if left_button2.collidepoint((mx, my)):   #Left through BIRDS list
                if click:
                    if(bird_selected == 0):
                        bird_selected = len(birds_list) - 1
                    else:
                        bird_selected -= 1
            if right_button2.collidepoint((mx, my)):   #Right through BIRDS list
                if click:
                    if(bird_selected == len(birds_list)-1):
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

