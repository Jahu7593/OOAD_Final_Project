import pygame
import bird
import pipe
import restart
import scoreObserver
import command
import screen

class Game(screen.Screen):  #Concrete method for starting/stopping game loop
    # imports all pygame modules and then initialzes it
    pygame.init()
    #init game clock, frames per second
    def __init__(self, x):
        self.screen_height = x.screen_height
        self.screen_width = x.screen_width
        self.screen = x.screen

        global clock, fps
        clock = pygame.time.Clock()
        fps = 60
        #make new instance of score observer
        global subject
        subject = scoreObserver.Subject()
        file_observer = scoreObserver.FileWriter()
        subject.register_observer(file_observer)
        # load default background images
        global background_img
        background_img = pygame.image.load('img/city.png')
        global ground
        ground = pygame.image.load('img/ground.png')
        #font & color definitions
        global font, white
        font = pygame.font.SysFont('Bauhaus 93', 60)
        white = (255, 255, 255)
        self.high_score = 0

        print("Game Object Initialized")
    
    # This is to write the score to a file/img
    @staticmethod
    def draw_text(text, font, text_col, x, y, self):
        img = font.render(text, True, text_col)
        self.screen.blit(img, (x, y))

    #@staticmethod
    def reset_game(self):
        pipe.pipe_group.empty()
        bird.flappy.rect.x = 100
        bird.flappy.rect.y = int(self.screen_height / 2)
        score = 0
        return score

    @staticmethod
    def quit_game():
        # Exit Game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def main(self, bg_img):
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

        # we want to run the game until someone exits out of it
        while run:

            # Quit
            self.quit_game()

            clock.tick(fps)

            # load the background image into the game
            self.screen.blit(bg_img, (0, 0))

            bird.bird_group.draw(self.screen)
            bird.bird_group.update()

            pipe.pipe_group.draw(self.screen)

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

            self.draw_text(str(score), font, white, int(self.screen_width/2), 20, self)

            # load the ground image into the game (scrolling background)
            # x coordinate needs to change so that the ground can move
            self.screen.blit(ground, (scroll, 768))

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
                if self.high_score < score:
                    self.high_score = score
                    subject.notify_observers(self.high_score)
                    # print("new high score", high_score)
                if restart.button.draw() == True:
                    # game has been restarted but isn't over
                    game_over = False
                    added = False
                    bird.Bird.game_over = game_over
                    curr_score = score
                    score = self.reset_game()
                    #Return to main menu here...
                    return curr_score, self.high_score  #return to main menu with current score, after selecting restart

            for event in pygame.event.get():
                # if someone selects the exit out of the game button
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
                    flying = True
                    bird.Bird.flying = flying

            pygame.display.update()

        pygame.quit()