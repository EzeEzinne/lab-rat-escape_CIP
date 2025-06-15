'''
This is a game called Lab Rat Escape which I am making
for my CIP final project...hopefully it turns out as good
as it did in my head...hopefully. And yes! in the process of trying to understand my coding better and 
get better inputs, I implored the help of generative AI which helped in arranging my codes
and educating me on some functions and their usages.
'''

import pygame
import sys
import os
import random

# Initialize pygame so that the modules are activated
pygame.init()

# Let us create the game window
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600  #perfect for landscape view..i've always loved landscape games
game_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Lab Rat Escape")

# Colour palette includes the following
ASH_GREY = pygame.Color("light gray")      # to give that calm background of the lab. White is too bright.
STEEL_BLUE = pygame.Color("steel blue")     # there would be need for highlights. Guess my fav color.
CHARCOAL = pygame.Color("black")         # for text. Game title.
#DARK_SLATE = pygame.Color("dimslategray")  #for the lab benches or future obstacles.
IVORY = pygame.Color("ivory")       #subtle text or fun facts at loading_screen.

BG_COLOR = ASH_GREY     #background color assigned
'''In case you cannot tell..I am going for a well polished lab ;)'''

clock = pygame.time.Clock() #so the game loop runs at a consistent speed

# Fonts setup for now...
font_large = pygame.font.SysFont('Georgia', 58)
font_small = pygame.font.SysFont('Georgia', 20)

'''Let's start THE PROLOGUE'''
def main():
    game_screen.fill(BG_COLOR)
    current_screen = "loading"
    running = True

    '''The main game loop AKA Game engine'''
    while running:      #a never-ending loop because it's always True until its false
        for event in pygame.event.get():    #checks for user's actions.
            if event.type == pygame.QUIT:   #in the event that user tries to close the game window or quit the game.
                running = False     #loop ends and game closes.

        if current_screen == "loading":
            show_loading_screen()
            current_screen = "introduction"     #so a next screen can start
        elif current_screen == "introduction":
            show_introduction_screen()
            current_screen = "game mode"        #continues till gameplay is exhausted
        elif current_screen == "game mode" :
            show_game_mode_screen()
            current_screen = "endless mode"
        elif current_screen == "endless mode":
            show_endless_mode_screen()
        #elif current_screen == "PCR mode":
            #PCR_mode_screen()


        pygame.display.flip()   #this updates the screen with the codes. Nothing will appear without this code.
        clock.tick(70)      #controls the time frame to 70 times per sec.



'''ACT ONE, SCENE ONE'''

def show_loading_screen():      #Define the Loading screen function
    title_text = font_large.render("Lab Rat Escape", True, CHARCOAL)
    loading_text = font_small.render("Loading...", True, CHARCOAL)
    fun_fact_text = font_small.render("Fun Fact: Rats were the first gamers!", True, STEEL_BLUE)

    loading_progress = 0  # to move the loading icon AKA Loading animation
    max_progress = 100
    loading_speed = 4
    # we need a loading bar...
    bar_width = 300
    bar_height = 20
    bar_x = (WINDOW_WIDTH - bar_width) // 2
    bar_y = WINDOW_HEIGHT// 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   #to enable users quit whenever
                pygame.quit()
                sys.exit()
        if loading_progress < max_progress:
            loading_progress += loading_speed
        elif loading_progress >= max_progress:
            running = False

        game_screen.fill(BG_COLOR)

        # Positions of the various texts on game_screen
        game_screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, WINDOW_HEIGHT // 3))
        game_screen.blit(loading_text, (WINDOW_WIDTH // 2 - loading_text.get_width() // 2, WINDOW_HEIGHT // 2 + 20))
        game_screen.blit(fun_fact_text, (WINDOW_WIDTH // 2 - fun_fact_text.get_width() // 2, WINDOW_HEIGHT // 2 + 90))

        # draw a dark loading bar at full length
        pygame.draw.rect(game_screen, "dark gray", (bar_x, bar_y, bar_width, bar_height))
        # to fill the drawn loading bar to show progress...
        fill_width = (loading_progress / max_progress) * bar_width
        pygame.draw.rect(game_screen, "blue", (bar_x, bar_y, fill_width, bar_height))   #the loading progress


        '''Let's draw the rat that moves with loading icon'''
        rat_x = bar_x + fill_width - 10    #to offset the rat, I noticed it kept falling off the bar lol
        rat_y = bar_y + (bar_height // 2)  # this way the rat is inside the loading rectangle
        pygame.draw.circle(game_screen, "black", (rat_x, rat_y), 10)

        pygame.display.flip()
        '''Pause briefly to simulate loading'''
        pygame.time.delay(1000)     #1 secs delay..otherwise players gets bored

'''ACT ONE, SCENE TWO'''    #PS. this is harder than I thought...
def show_introduction_screen():
    game_screen.fill(BG_COLOR)
    lab_BG = pygame.image.load(os.path.join("assets","images","final_Intro_CIP.png"))   #instead of filling with BG color
    lab_BG = pygame.transform.scale(lab_BG,(WINDOW_WIDTH,WINDOW_HEIGHT))    #so it fits to screen
    game_screen.blit(lab_BG, (0, 0))

    running_intro = True
    while running_intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  #this is how a click is detected in pygame
                running_intro = False   #we can move to next screen

         #Now, for the prompt that marks the start of the game
        if pygame.time.get_ticks() % 1000 < 500:  #the Click to play text would blink repeatedly till user clicks on the screen.
            intro_text = font_small.render("Click anywhere to ESCAPE", True, "Black")
            game_screen.blit(intro_text, (500,500))
        pygame.display.flip()

'''ACT ONE, SCENE THREE''' #between the rat and I, I don't know who wants to escape more
'''To create a customizable button object, that can be used repeatedly. This was used instead of 
having a different def function blocks for each game play mode. It helps to remove confusion and excessive 
code lines'''
class Button:   #I like to say that a class is to def, what dict is to list (that's the best of my understanding rn)
    def __init__(self, text, x, y, width, height, color, is_active=True):   #this function serves as the construct for all buttons to come.
        self.text = text    #stores the button's text
        self.rect = pygame.Rect(x, y, width, height)    #creates the rectangle; in this case, button
        self.color = color      #the button's color
        self.hover_color = "green"  #will give the buttons a raised look
        self.text_color = "blue" if is_active else "gray"   # text color for the active buttons and inactive buttons having gray
        self.is_active = is_active  #since not all game modes can be completed, some would be disabled and appear gray
    '''honestly..i hope this part of the code works because this is a whole day spent on trying to understand how this works'''
    def draw(self, game_screen, font, mouse_pos):
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) and self.is_active else self.color #when the mouse hovers over an active button
        pygame.draw.rect(game_screen, current_color, self.rect, border_radius=12)   #buttons will have rounded edges
        pygame.draw.rect(game_screen, "grey", self.rect, 2, border_radius=12)  # outline
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        game_screen.blit(text_surf, text_rect)

        if not self.is_active:  #this is for future game modes that cannot be worked on now...
            coming_surf = pygame.font.SysFont("Georgia", 20).render("Coming Soon", True, "black")
            coming_rect = coming_surf.get_rect(center=(self.rect.centerx, self.rect.centery + 35))
            game_screen.blit(coming_surf, coming_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos) and self.is_active


font = pygame.font.SysFont("Arial", 32)

'''Define buttons for the different game modes'''
buttons = [
    Button("Endless Mode", 250, 150, 300, 60, STEEL_BLUE, True),
    Button("PCR Mode", 250, 240, 300, 60, STEEL_BLUE, True),
    Button("Mutation Mode", 250, 330, 300, 60, STEEL_BLUE, False),
    Button("Toxin Mode", 250, 420, 300, 60, STEEL_BLUE, False)
    ]
'''Now that Class Button has been created, let's make the actual game play'''
def show_game_mode_screen():
    game_screen.fill(BG_COLOR)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()  #to get the position of the mouse/cursor
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for btn in buttons:
                    if btn.rect.collidepoint(mouse_pos):
                        if btn.text == "Endless Mode":
                            running = False     #to exit the game play screen
                            current_screen = "endless_mode"
                        elif btn.text == "PCR Mode":
                            running = False
                            current_screen = "pcr_mode"
                        elif btn.text == "Mutation Mode":
                            running = False
                            current_screen = "mutation_mode"
                        else:
                            current_screen = "toxin_mode_screen"

        for btn in buttons:
            btn.draw(game_screen, font, mouse_pos)

        pygame.display.flip()

'''ACT TWO, SCENE ONE'''    #I thought this day would never come
class Lab_Rat:  # much easier to manage,also in the case of if the rat can be increased in size..tentative tho
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def draw(self, game_screen):
        pygame.draw.ellipse(game_screen, "black", (self.x, self.y, self.width, self.height))

    def move(self, keys):  # to set the movement controls using directions or arrowheads
        if keys[pygame.K_LEFT]:  # checks if the player pressed LEFT
            self.x -= self.speed  # if so, reduces the player's x-coordinates by its speed value
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

rat = Lab_Rat(100, 300, 40, 40, 2)
rat_rect = pygame.Rect(rat.x, rat.y, rat.width, rat.height)

'''Now to create a class for obstacles that would spawn across the game window'''
class Obstacle:
    def __init__(self, x,y, width, height, speed):
        self.rect = pygame.Rect(x,y,width,height)
        self.speed = speed

    def move(self):
        self.rect.x -= self.speed

    def draw(self, game_screen):
        pygame.draw.rect(game_screen,"green", self.rect)   #using green because they might as well be bacteria lol

    def off_game_screen(self):  #for when obstacles reach the end of game screen
        return self.rect.right < 0

    def collides_with(self,rat):    #to detect when the rat collides with a bacteria
        rat_rect = pygame.Rect(rat.x, rat.y, rat.width, rat.height)
        return self.rect.colliderect(rat_rect)

def show_endless_mode_screen():
    game_screen.fill(BG_COLOR)

    '''Initially I was going for a maze-like feature but this being an endless mode leaned more
    into a scrolling background with increasing speed and increasing difficulty'''

    start_time = pygame.time.get_ticks()
    rat = Lab_Rat(100, 300, 40, 40, 2)

    '''Now, to create the endless looping of this game mode'''
    BG_flooring = pygame.image.load(os.path.join("assets", "images", "Lab_bg_EGM_CIP_1.jpg"))
    BG_flooring = pygame.transform.scale(BG_flooring,(WINDOW_WIDTH,WINDOW_HEIGHT))#the image smaller than window
    BG_width = BG_flooring.get_width()
    initial_speed = 1
    scroll_x = 0

    obstacles = []  # empty list that will progressively increase with time
    spawn_timer = pygame. USEREVENT + 1  # the said timer
    pygame.time.set_timer(spawn_timer, 2000)    #get obstacles every 2 secs


    '''About scoring system...'''
    player_score = 0
    player_score_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(player_score_timer, 1000) #player's score increases per sec


    '''HERE COMES THE ENGINE'''
    running = True
    while running:
        keys = pygame.key.get_pressed()  # checks for which key is currently being pressed by player
        '''For increasing difficulty'''
        elapsed_time = pygame.time.get_ticks() - start_time
        BG_speed = initial_speed + (elapsed_time // 15000)   #increases speed per 15 secs
        scroll_x -= BG_speed
        if scroll_x <= -BG_width:  # since the BG scrolls, its bandwidth would get exhausted; we refresh
            scroll_x = 0
        '''Two BGs should be drawn so that they loop seamlessly after each other'''
        game_screen.blit(BG_flooring, (scroll_x, 0))
        game_screen.blit(BG_flooring, (scroll_x + BG_width, 0))  # this follows immediately after the first BG

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == player_score_timer:
                player_score += 1
            if event.type == spawn_timer:
                spawn_height = random.randint(40,80)    #random obs size
                num_obs = 1
                if BG_speed >= 5:
                    num_obs = 2
                for _ in range(num_obs):
                    spawn_y = random.randint(0, WINDOW_HEIGHT - spawn_height) #so obs can appear from various height
                    obstacles.append(Obstacle (WINDOW_WIDTH, spawn_y, 40, spawn_height, BG_speed)) #add of new obstacles)
        rat.move(keys)
        rat.draw(game_screen)

        '''Calling upon the obstacles'''
        for obs in obstacles:
            obs.move()
            obs.draw(game_screen)

        '''Collision detection!!!'''
        for obstacle in obstacles:
            if obstacle.collides_with(rat):
                print("Infected!!!")
                result = show_game_over_screen(player_score)
                if result == "game mode":
                    show_game_mode_screen()
                running = False
            if obstacle.off_game_screen():
                obstacles.remove(obstacle)

        player_score_text = font_small.render(f"Score: {player_score}", True, "Blue")
        game_screen.blit(player_score_text, (20, 20))

        pygame.display.flip()

def show_game_over_screen(player_score):
    game_screen.fill("red")
    game_over_text = font_large.render("You were infected.", True, "green")
    score_board = font_small.render(f"You survived {player_score} seconds of possible infection", True, "black")

    game_screen.blit(game_over_text, (WINDOW_WIDTH//2 - game_over_text.get_width()//2, (WINDOW_HEIGHT//2) - 100))
    game_screen.blit(score_board, (WINDOW_WIDTH//2 - score_board.get_width()//2, WINDOW_HEIGHT//2))

    game_mode_button = Button("Game Mode", WINDOW_WIDTH//2 - 220, 440, 180,50,"steel blue",
                              True)
    exit_button = Button("Exit", WINDOW_WIDTH//2 +40, 440,180,50,"steel blue",
                         True)
    mouse_pos = pygame.mouse.get_pos()
    game_mode_button.draw(game_screen,font_small,mouse_pos)
    exit_button.draw(game_screen,font_small,mouse_pos)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_mode_button.is_clicked(event.pos):
                    return "game mode"
                elif exit_button.is_clicked(event.pos):
                    pygame.quit()
                    sys.exit()
                    #waiting = False
        pygame.display.flip()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
