import random, pygame, sys
from src.states.BaseState import BaseState
from src.constants import *
from src.Dependency import *
import src.CommonRender as CommonRender
from src.Dragon import Dragon
from src.PowerUp import PowerUp

# List to track power-ups
g_power_ups = []

class PlayState(BaseState):
    def __init__(self):
        super(PlayState, self).__init__()
        self.paused = False
        self.dragon = None
        self.show_menu = False  # Flag to display the pause menu
        self.menu_option = 1  # 1 = Resume, 2 = Home
        self.awaiting_serve = True  # Track if the game is awaiting serve

        # List to track multiple balls
        self.balls = []

        # Variable to track if a power-up has dropped in the level
        self.power_up_dropped = False
        self.bricks_broken_count = 0  # Track how many bricks have been broken
        self.required_drops = 2  # Minimum power-ups to drop per level

    def Enter(self, params):
        self.paddle = params['paddle']
        self.bricks = params['bricks']
        self.health = params['health']
        self.score = params['score']
        self.high_scores = params['high_scores']
        self.ball = params['ball']
        self.level = params['level']

        self.recover_points = 5000
        self.balls = [self.ball]  # Add the initial ball to the balls list

        self.ball.dx = random.randint(-600, 600)  # Randomize ball direction
        self.ball.dy = random.randint(-180, -150)

        # Add the dragon starting from level 2
        if self.level >= 2:
            self.dragon = Dragon()  # Create a dragon instance
        else:
            self.dragon = None  # No dragon in level 1

        # Reset power-up tracking for the new level
        self.power_up_dropped = False
        self.bricks_broken_count = 0

    # Function to add an extra ball
    def add_extra_ball(self):
        new_ball = Ball(1)  # Create a new ball instance
        new_ball.rect.x = self.balls[0].rect.x  # Start new ball where the main ball is
        new_ball.rect.y = self.balls[0].rect.y
        new_ball.dx = random.randint(-600, 600)  # Randomize its direction
        new_ball.dy = random.randint(-180, -150)
        self.balls.append(new_ball)  # Add to the list of balls

    def update(self, dt, events):
        global g_power_ups

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Check for Esc to display the pause menu
                if event.key == pygame.K_ESCAPE:
                    if not self.paused:
                        self.paused = True
                        self.show_menu = True  # Show pause menu
                    else:
                        if self.show_menu:
                            self.paused = False  # Resume the game

                # Handle menu navigation if the menu is being shown
                if self.show_menu:
                    if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                        self.menu_option = 1 if self.menu_option == 2 else 2  # Toggle between Resume and Home
                    if event.key == pygame.K_RETURN:
                        if self.menu_option == 1:  # Resume
                            self.show_menu = False
                            self.paused = False
                        elif self.menu_option == 2:  # Go to Home (Restart game)
                            self.reset_game_to_start()

            # Serve the ball if awaiting serve and Enter is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.awaiting_serve:
                self.awaiting_serve = False

        if self.paused:
            return  # Pause the game updates when paused

        # Update paddle
        self.paddle.update(dt)

        # Update all the balls
        for ball in self.balls:
            ball.update(dt)

            # Check if the ball collides with the paddle
            if ball.Collides(self.paddle):
                ball.rect.y = self.paddle.rect.y - 24
                ball.dy = -ball.dy
                gSounds['paddle-hit'].play()

            # Remove the ball if it falls below the screen
            if ball.rect.y >= HEIGHT:
                self.balls.remove(ball)

        # Check if no balls remain (game over)
        if len(self.balls) == 0:
            self.health -= 1
            gSounds['hurt'].play()
            if self.health == 0:
                g_state_manager.Change('game-over', {
                    'score': self.score,
                    'high_scores': self.high_scores
                })
            else:
                g_state_manager.Change('serve', {
                    'level': self.level,
                    'paddle': self.paddle,
                    'bricks': self.bricks,
                    'health': self.health,
                    'score': self.score,
                    'high_scores': self.high_scores,
                    'recover_points': self.recover_points
                })

        # Update dragon
        if self.dragon:
            self.dragon.update(dt)

        # Handle power-ups falling and collection by paddle
        for power_up in g_power_ups:
            power_up.update(dt)
            if power_up.Collides(self.paddle):
                if power_up.type == 'heart':
                    self.health = min(self.health + 1, 3)  # Max 3 health
                elif power_up.type == 'ball':
                    self.add_extra_ball()  # Add extra ball
                g_power_ups.remove(power_up)  # Remove collected power-up

        # Ball collision with bricks
        for k, brick in enumerate(self.bricks):
            for ball in self.balls:  # Make all balls interact with bricks
                if brick.alive and ball.Collides(brick):
                    self.score = self.score + (brick.tier * 200 + brick.color * 25)
                    brick.Hit()
                    self.bricks_broken_count += 1

                    if self.score > self.recover_points:
                        self.health = min(3, self.health + 1)
                        self.recover_points = min(100000, self.recover_points * 2)
                        gSounds['recover'].play()

                    if self.CheckVictory():
                        gSounds['victory'].play()
                        g_state_manager.Change('victory', {
                            'level': self.level,
                            'paddle': self.paddle,
                            'health': self.health,
                            'score': self.score,
                            'high_scores': self.high_scores,
                            'ball': self.balls[0],  # Make sure the next level has a main ball
                            'recover_points': self.recover_points
                        })

                    # Random chance for power-up drop (ensure that at least 2 power-ups drop per level)
                    if not self.power_up_dropped and self.bricks_broken_count % (len(self.bricks) // self.required_drops) == 0:
                        chance = random.random()
                        if chance <= 0.30:
                            g_power_ups.append(PowerUp(brick.rect.x, brick.rect.y, 'heart'))  # 30% chance for heart
                        else:
                            g_power_ups.append(PowerUp(brick.rect.x, brick.rect.y, 'ball'))  # 70% chance for ball
                        self.power_up_dropped = True if self.bricks_broken_count >= self.required_drops else False

                    # Ball collision logic with bricks
                    if ball.rect.x + 6 < brick.rect.x and ball.dx > 0:
                        ball.dx = -ball.dx
                        ball.rect.x = brick.rect.x - 24
                    elif ball.rect.x + 18 > brick.rect.x + brick.width and ball.dx < 0:
                        ball.dx = -ball.dx
                        ball.rect.x = brick.rect.x + 96
                    elif ball.rect.y < brick.rect.y:
                        ball.dy = -ball.dy
                        ball.rect.y = brick.rect.y - 24
                    else:
                        ball.dy = -ball.dy
                        ball.rect.y = brick.rect.y + 48

                    if abs(ball.dy) < 450:
                        ball.dy = ball.dy * 1.02

                    break


        # Handle dragon collision with the ball
        if self.dragon:
            for ball in self.balls:  # Make all balls interact with the dragon
                if self.dragon.check_collision_with_ball(ball):
                    self.health -= 1
                    gSounds['hurt'].play()
                    if self.health == 0:
                        g_state_manager.Change('game-over', {
                            'score': self.score,
                            'high_scores': self.high_scores
                        })
                    else:
                        g_state_manager.Change('serve', {
                            'level': self.level,
                            'paddle': self.paddle,
                            'bricks': self.bricks,
                            'health': self.health,
                            'score': self.score,
                            'high_scores': self.high_scores,
                            'recover_points': self.recover_points
                        })

    def Exit(self):
        pass

    def render(self, screen):
        for brick in self.bricks:
            brick.render(screen)

        self.paddle.render(screen)
        for ball in self.balls:
            ball.render(screen) 

        CommonRender.RenderScore(screen, self.score)
        CommonRender.RenderHealth(screen, self.health)

        if self.level >= 2 and self.dragon:
            self.dragon.render(screen)

        
        for power_up in g_power_ups:
            power_up.render(screen)

        if self.paused and self.show_menu:
            self.render_menu(screen)  

        if self.paused and not self.show_menu:
            t_pause = gFonts['large'].render("PAUSED", False, (255, 255, 255))
            rect = t_pause.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(t_pause, rect)

    def render_menu(self, screen):
        
        menu_bg = pygame.Surface((WIDTH, HEIGHT))
        menu_bg.set_alpha(128)  
        menu_bg.fill((0, 0, 0))
        screen.blit(menu_bg, (0, 0))

        resume_color = (0, 255, 0) if self.menu_option == 1 else (255, 255, 255)
        home_color = (0, 255, 0) if self.menu_option == 2 else (255, 255, 255)

        t_resume = gFonts['large'].render("Resume", False, resume_color)
        rect = t_resume.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        screen.blit(t_resume, rect)

        t_home = gFonts['large'].render("Home", False, home_color)
        rect = t_home.get_rect(center=(WIDTH / 2, HEIGHT / 2))
        screen.blit(t_home, rect)

    def CheckVictory(self):
        for brick in self.bricks:
            if brick.alive:
                return False
        return True

    def reset_game_to_start(self):
        self.paused = False  
        self.show_menu = False  
        gSounds['confirm'].play()
        g_state_manager.Change('start', {
            'high_scores': self.high_scores
        })

