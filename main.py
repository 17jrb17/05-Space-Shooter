import sys, logging, open_color, arcade, assets, space_starter_kit, os, random

#check to make sure we are running the right version of Python
version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

#turn on logging, in case we have to leave ourselves debugging messages
logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 30
INITIAL_VELOCITY = 3
SCREEN_TITLE = "Shoot the things I guess"

NUM_ENEMIES = 20
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
ENEMY_HP = 100
HIT_SCORE = 10
KILL_SCORE = 100

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        super().__init__("assets/laser.png", 0.5)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage
    
    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/player2.png", 0.5)
        (self.center_x, self.center_y) = STARTING_LOCATION

class Enemy(arcade.Sprite):
    def __init__(self, position):
        super().__init__("assets/rock.png", 0.5)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position

class Window(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.set_mouse_visible(True)
        arcade.set_background_color(open_color.black)
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0



    def setup(self):
        for i in range(NUM_ENEMIES):
            x = random.randint(MARGIN,SCREEN_WIDTH-MARGIN)
            y = random.randint(MARGIN,SCREEN_HEIGHT-MARGIN)
            dx = random.uniform(-INITIAL_VELOCITY, INITIAL_VELOCITY)
            dy = random.uniform(-INITIAL_VELOCITY, INITIAL_VELOCITY)
            self.enemy = Enemy((x, y))
            self.enemy.center_x = x
            self.enemy.center_y = y
            self.enemy.dx = dx
            self.enemy.dy = dy
            self.enemy.mass = 1
            self.enemy_list.append(self.enemy)    
            #x = random.randint(50, 750)
           # y = random.randint(300, 600)
            #enemy = Enemy((x,y))
            #self.enemy_list.append(enemy)

    def update(self, delta_time):
        self.bullet_list.update()
        for e in self.enemy_list:

            damage = arcade.check_for_collision_with_list(e, self.bullet_list)
            for d in damage:
                e.hp = e.hp - d.damage
                d.kill()
                if e.hp < 0:
                    e.kill() 
                    self.score = self.score + KILL_SCORE
                else:
                    self.score = self.score + HIT_SCORE

            e.center_x += e.dx
            e.center_y += e.dy

            collisions = e.collides_with_list(self.enemy_list)
            for c in collisions:
                x = e.dx
                y = e.dy
                
                e.dx = c.dx
                e.dy = c.dy

                c.dx = x
                c.dy = y

            if e.center_x <= MARGIN:
                e.center_x = MARGIN
                e.dx = abs(e.dx)
            if e.center_x >= SCREEN_WIDTH - MARGIN:
                e.center_x = SCREEN_WIDTH - MARGIN
                e.dx = abs(e.dx)*-1
            if e.center_x <= MARGIN:
                e.center_x = MARGIN
                e.dx = abs(e.dx)
            if e.center_y <= MARGIN:
                e.center_y = MARGIN
                e.dy = abs(e.dy)
            if e.center_y >= SCREEN_HEIGHT - MARGIN:
                e.center_y = SCREEN_HEIGHT - MARGIN
                e.dy = abs(e.dy)*-1

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 40, open_color.white, 16)
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()




    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The player moves left and right with the mouse
        '''
        self.player.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass

    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            print("Left")
        elif key == arcade.key.RIGHT:
            print("Right")
        elif key == arcade.key.UP:
            print("Up")
        elif key == arcade.key.DOWN:
            print("Down")

    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        pass


def main():
    
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()