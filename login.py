import sqlite3

import pygame
from pygame.locals import *
import time
import random
from tkinter import *

root = Tk()
root.geometry("1280x720")
root.title("LogIn")
sign_up_frame=LabelFrame(root).place(x=0, y=0)
scoreboard_frame=LabelFrame(root).place(x=0, y=0)
in_game_frame=LabelFrame(root).place(x=0, y=0)

def scoreboard_btn_click():

    global scoreboard_bg_img, back_btn_img, sign_out_img

    scoreboard_frame=LabelFrame(root).place(x=0, y=0)

    scoreboard_bg_img=PhotoImage(file="Images/scoreboards.png")
    back_btn_img=PhotoImage(file="Images/back.png")

    Label(scoreboard_frame,image=scoreboard_bg_img).place(x=0, y=0)

    b1=Button(scoreboard_frame,image=back_btn_img, bd=0, command=in_game_page)
    b1.place(x=56, y=43)


    conn = sqlite3.connect("UserDatabase.db")
    c = conn.cursor()

    c.execute('''SELECT * FROM user_details''')
    d = c.fetchall()
    e = len(d)
    z=241
    for i in range(0, e):
        g=d[i]
        Label(scoreboard_frame, text=g[0], bg="#000000", fg="#ffffff", font=31,).place(x=400, y=241+(i*35))
        Label(scoreboard_frame, text=g[2], bg="#000000", fg="#ffffff", font=31).place(x=660, y=241+(i*35))

def in_game_page():

    global in_game_img, start_btn_img, scoreboard_btn_img, sign_out_img

    in_game_img=PhotoImage(file="Images/in_game.png")
    in_game_frame=LabelFrame(root).place(x=0, y=0)

    Label(in_game_frame, image=in_game_img).place(x=0, y=0)

    def start_btn_click():
        maingame()

    sign_out_img = PhotoImage(file="Images/signout.png")
    sign_out_btn = Button(in_game_frame, image=sign_out_img, bd=0, command=sign_page)
    sign_out_btn.place(x=977, y=549)

    start_btn_img=PhotoImage(file="Images/Start Game.png")
    start_btn=Button(in_game_frame, image=start_btn_img, command=start_btn_click, bg="#000000", activebackground= "#000000")
    start_btn.place(x=523, y=280)

    scoreboard_btn_img=PhotoImage(file="Images/Scoreboard.png")
    scoreboard_btn=Button(in_game_frame,image=scoreboard_btn_img,command=scoreboard_btn_click, bg="#000000", activebackground= "#000000")
    scoreboard_btn.place(x=521, y=385)

def sign_page():

    global sign_up_img, sign_in_btn_img, sign_up_btn_img

    sign_up_img=PhotoImage(file="Images/sign_up.png")
    sign_up_frame=LabelFrame(root).place(x=0, y=0)

    Label(sign_up_frame, image=sign_up_img).place(x=0, y=0)

    def sign_up_click():
        conn=sqlite3.connect("UserDatabase.db")
        c=conn.cursor()

        c.execute(
            '''INSERT INTO user_details VALUES(:username, :password, :highscore)''',
            {
                "username":username1.get(),
                "password":password1.get(),
                "highscore":0
            },
        )

        conn.commit()
        conn.close()

    def sign_in_click():
        global current_username
        conn=sqlite3.connect("UserDatabase.db")
        c=conn.cursor()

        c.execute(
            '''SELECT * FROM user_details'''
        )
        f=c.fetchall()
        g=len(f)
        valid_1=False
        valid_2=False
        for i in range(0,g):
            h=f[i]
            if h[0]==username1.get():
                valid_1=True
                if h[1]==password1.get():
                    valid_2=True
        if valid_1 is True and valid_2 is False:
            Label(sign_up_frame, text="Password is incorrect.", bg="#478039", font=31).place(x=439, y=442)
        elif valid_2 is False:
            Label(sign_up_frame, text="Username is invalid.", bg="#478039", font=31).place(x=439, y=442)
        else:
            in_game_page()
            current_username=username1.get()
            print(current_username)


    sign_in_btn_img=PhotoImage(file="Images/Sign In.png")
    sign_in_btn=Button(sign_up_frame, image= sign_in_btn_img,command=sign_in_click, bg="#ffffff", activebackground= "#ffffff")
    sign_in_btn.place(x=477, y=399)

    sign_up_btn_img=PhotoImage(file="Images/Sign Up.png")
    sign_up_btn=Button(sign_up_frame, image=sign_up_btn_img,command=sign_up_click, bg="#ffffff", activebackground= "#ffffff")
    sign_up_btn.place(x=686, y=399)

    username1 = StringVar()
    password1 = StringVar()

    e1 = Entry(sign_up_frame, text=username1, bd=0, font=12, width=33)
    e1.place(x=438.57, y=270)

    e2 = Entry(sign_up_frame, text=password1, bd=0, font=12, width=33)
    e2.place(x=438.57, y=337)



def maingame():

    SIZE = 40
    BACKGROUND_COLOR = (150, 110, 5)

    class Apple:
        def __init__(self, parent_screen):
            self.parent_screen = parent_screen
            self.image = pygame.image.load("Images/apple.jpg").convert()
            self.x = 120
            self.y = 120

        def draw(self):
            self.parent_screen.blit(self.image, (self.x, self.y))
            pygame.display.flip()

        def move(self):
            self.x = random.randint(1,24)*SIZE
            self.y = random.randint(1,19)*SIZE

    class Snake:
        def __init__(self, parent_screen):
            self.parent_screen = parent_screen
            self.image = pygame.image.load("Images/snake.jpg").convert()
            self.direction = 'down'

            self.length = 1
            self.x = [40]
            self.y = [40]

        def move_left(self):
            self.direction = 'left'

        def move_right(self):
            self.direction = 'right'

        def move_up(self):
            self.direction = 'up'

        def move_down(self):
            self.direction = 'down'

        def walk(self):
            # update body
            for i in range(self.length-1,0,-1):
                self.x[i] = self.x[i-1]
                self.y[i] = self.y[i-1]

            # update head
            if self.direction == 'left':
                self.x[0] -= SIZE
            if self.direction == 'right':
                self.x[0] += SIZE
            if self.direction == 'up':
                self.y[0] -= SIZE
            if self.direction == 'down':
                self.y[0] += SIZE

            self.draw()

        def draw(self):
            for i in range(self.length):
                self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

            pygame.display.flip()

        def increase_length(self):
            self.length += 1
            self.x.append(-1)
            self.y.append(-1)



    class Game:
        def __init__(self):
            pygame.init()
            pygame.display.set_caption("Snakes 2D")

            pygame.mixer.init()

            self.surface = pygame.display.set_mode((1000, 800))
            self.snake = Snake(self.surface)
            self.snake.draw()
            self.apple = Apple(self.surface)
            self.apple.draw()

        def play_background_music(self):
            pygame.mixer.music.load('Images/bg_music_1.mp3')
            pygame.mixer.music.play(-1, 0)

        def play_sound(self, sound_name):
            if sound_name == "crash":
                sound = pygame.mixer.Sound("Images/crash.mp3")
            elif sound_name == 'ding':
                sound = pygame.mixer.Sound("Images/ding.mp3")

            pygame.mixer.Sound.play(sound)

        def reset(self):
            self.snake = Snake(self.surface)
            self.apple = Apple(self.surface)

        def is_collision(self, x1, y1, x2, y2):
            if x1 >= x2 and x1 < x2 + SIZE:
                if y1 >= y2 and y1 < y2 + SIZE:
                    return True
            return False

        def render_background(self):
            bg = pygame.image.load("Images/snakebg.jpg")
            self.surface.blit(bg, (0,0))

        def play(self):
            self.render_background()
            self.snake.walk()
            self.apple.draw()
            self.display_score()
            pygame.display.flip()

            # snake eating apple scenario
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
                self.play_sound("ding")
                self.snake.increase_length()
                self.apple.move()

            # snake colliding with itself
            for i in range(3, self.snake.length):
                if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                    self.play_sound('crash')
                    raise "Collision Occurred"

        def display_score(self):
            font = pygame.font.SysFont('Gemunu Libre',30)
            score = font.render(f"Score: {self.snake.length}",True,(200,200,200))
            self.surface.blit(score,(850,10))

            conn = sqlite3.connect("UserDatabase.db")
            c = conn.cursor()

            c.execute(f"""SELECT * FROM user_details WHERE username='{current_username}'""")
            d = c.fetchall()

            e=d[0]

            highscore = font.render(f"High Score: {e[2]}", True, (200, 200, 200))
            self.surface.blit(highscore, (850, 60))

        def show_game_over(self):
            self.render_background()
            font = pygame.font.SysFont('Gemunu Libre', 30)
            line1 = font.render(f"Game is over! Your score is {self.snake.length}.", True, (255, 255, 255))
            self.surface.blit(line1, (200, 300))
            line2 = font.render("To play again press Enter!", True, (255, 255, 255))
            self.surface.blit(line2, (200, 350))
            line3 = font.render("To exit press Escape!", True, (255, 255, 255))
            self.surface.blit(line3, (200, 400))
            pygame.mixer.music.pause()
            pygame.display.flip()

            conn = sqlite3.connect("UserDatabase.db")
            c = conn.cursor()

            c.execute(f"""SELECT * FROM user_details WHERE username='{current_username}'""")
            d = c.fetchall()

            e = d[0]
            e_0 = e[0]
            e_1 = e[1]
            e_2 = e[2]

            if self.snake.length > e_2:
                e_2=self.snake.length

            c.execute(f"""DELETE FROM user_details WHERE username='{current_username}'""")

            conn.commit()

            c.execute(
                '''INSERT INTO user_details VALUES(:username, :password, :highscore)''',
                {
                    "username": e_0,
                    "password": e_1,
                    "highscore": e_2
                },
            )

            conn.commit()
            conn.close()

        def run(self):
            running = True
            pause = False

            while running:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            running = False

                        if event.key == K_RETURN:
                            pygame.mixer.music.unpause()
                            pause = False

                        if not pause:
                            if event.key == K_LEFT:
                                self.snake.move_left()

                            if event.key == K_RIGHT:
                                self.snake.move_right()

                            if event.key == K_UP:
                                self.snake.move_up()

                            if event.key == K_DOWN:
                                self.snake.move_down()

                    elif event.type == QUIT:
                        running = False
                try:

                    if not pause:
                        self.play()

                except Exception as e:
                    self.show_game_over()
                    pause = True
                    self.reset()

                time.sleep(.25)

    if __name__ == '__main__':
        game = Game()
        game.run()

sign_page()
root.mainloop()