import pygame
import random
pygame.init()
pygame.display.set_caption("Python Pong")

WIDTH, HEIGHT = 700, 501  # height and width of display window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


FPS = 60
WHITE = (255, 255, 255)
BLUE = (1, 9, 56)

PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont("comicsans", 25)

WINNING_SCORE = 10


class Paddle:
    # Class attributes
    COLOR = WHITE
    VELOCITY = 4  # distance/frame

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y,
                         self.width, self.height))  # draw paddle

    def move(self, up=True):  # true is up false is down
        if(up):
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


class Ball:
    MAX_VEL = -5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        # move ball in x direction on program start (randomized which direction)
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel *= -1
        self.y_vel = 0


def draw(win, paddles, ball, left_score, right_score):
    win.fill(BLUE)  # fill with blue

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)

    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH*(3/4) -
             right_score_text.get_width()//2, 20))
    for paddle in paddles:
        paddle.draw(win)  # draw each paddle in the list of paddles

    for i in range(10, HEIGHT, HEIGHT//20):  # draw dotted line
        if i % 2 == 1:
            continue

        # 20 rectangles 10 drawn rectangles with width = 2px
        pygame.draw.rect(win, WHITE, (WIDTH//2 - 1, i, 2, HEIGHT//20))

    ball.draw(win)
    pygame.display.update()  # display draw updates


def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:  # if it hits the ceiling
        ball.y_vel *= -1
    elif ball.y-ball.radius <= 0:  # if it hits the ceiling
        ball.y_vel *= -1

    # CHANGE X and Y velocity
    if ball.x_vel < 0:  # hitting the left paddle
        # if the ball is within the y range of the height of the paddle
        if ball.y >= left_paddle.y and ball.y < left_paddle.y + left_paddle.height:
            # if the ball hits the right edge of the paddle
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                # Y velocity equation: half of height/ reduction factor = max velocity => half of height/max velocity =reduction
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = ball.y-middle_y
                reduction_factor = (left_paddle.height/2)/ball.MAX_VEL
                # squeez the velocity in range of -5 and 5
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel*-1

    else:  # hitting the right paddle
        # if the ball is within the y range of the height of the paddle
        if ball.y >= right_paddle.y and ball.y < right_paddle.y + right_paddle.height:
            if ball.x+ball.radius >= right_paddle.x:  # if the ball hits the left edge of the paddle
                ball.x_vel *= -1

                # Y velocity equation: half of height/ reduction factor = max velocity => half of height/max velocity =reduction
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = ball.y-middle_y
                reduction_factor = (right_paddle.height/2)/ball.MAX_VEL
                # squeez the velocity in range of -5 and 5
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel*-1


def handle_paddle_movement(keys, left_paddle, right_paddle):

    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0:
        left_paddle.move(up=True)  # move left paddle up
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)  # move left paddle down

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0:
        right_paddle.move(up=True)  # move left paddle up
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)  # move left paddle down


def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2-PADDLE_HEIGHT //
                         2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT //
                          2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH//2, HEIGHT//2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        clock.tick(FPS)  # 60 fps cap (regulates speed of while loop)
        draw(WIN, [left_paddle, right_paddle], ball,
             left_score, right_score)  # constantly draw screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()  # returns a list of keys pressed
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()

        won = False
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left player won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right player won!"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH//2 - text.get_width() //
                     2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()


if __name__ == '__main__':
    main()
