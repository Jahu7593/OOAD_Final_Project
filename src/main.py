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

    global font, white
    font = pygame.font.SysFont('Bauhaus 93', 60)
    white = (255, 255, 255)

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


    # Menu
    def menu(self):
        skyline_image = pygame.image.load("img/background.png")
        ground_image = pygame.image.load("img/ground.png")
        bird_img = pygame.image.load("img/bird1.png")
        start_image = pygame.image.load("img/start.png")

        
        global game_stopped

        while game_stopped:
            self.quit_game()

            # Draw Menu
            screen.fill((0, 0, 0))
            screen.blit(skyline_image, (0, 0))
            screen.blit(ground_image, (0, 768))
            screen.blit(bird_img, (100, int(screen_height/2)))
            screen.blit(start_image, (screen_width // 2 - start_image.get_width() // 2,
                                    screen_height // 2 - start_image.get_height() // 2))

            # User Input
            user_input = pygame.mouse.get_pressed()
            if user_input[0]:
                bird.clicked = True
                self.main()

            pygame.display.update()

obj = Main()
obj.menu()