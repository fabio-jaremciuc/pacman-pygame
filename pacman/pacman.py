import pygame
from abc import ABCMeta, abstractmethod

pygame.init()

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
VELOCITY = 1

screen = pygame.display.set_mode((800, 600), 0)
word_format = pygame.font.SysFont("arial", 24, True, False)


class GameElement(metaclass=ABCMeta):
    @abstractmethod
    def print(self, screen):
        pass

    @abstractmethod
    def movement_rules(self):
        pass

    @abstractmethod
    def events_processing(self, evts):
        for e in evts:
            if e.type == pygame.QUIT:
                exit()


class Pacman(GameElement):
    def __init__(self, pacman_size):
        self.row = 1
        self.column = 1
        self.center_x = 400
        self.center_y = 300
        self.size = pacman_size
        self.vel_x = 0
        self.vel_y = 0
        self.radius = self.size // 2  # the "//" get only the entire part of the division as int(x)
        # intention movement to interact with the scenario
        self.mov_column_intention = self.column
        self.mov_row_intention = self.row

    def movement_rules(self):
        # intention movement to interact with the scenario
        self.mov_column_intention = self.column + self.vel_x
        self.mov_row_intention = self.row + self.vel_y
        self.center_x = int(self.column * self.size + self.radius)
        self.center_y = int(self.row * self.size + self.radius)

    def print(self, screen):
        # pacman's body
        pygame.draw.circle(screen, YELLOW, (self.center_x, self.center_y), self.radius, 0)

        # pacman's mouth
        start_mouth = (self.center_x, self.center_y)
        upper_mouth = (self.center_x + self.radius, self.center_y - self.radius)
        bottom_mouth = (self.center_x + self.radius, self.center_y)
        points = [start_mouth, upper_mouth, bottom_mouth]
        pygame.draw.polygon(screen, BLACK, points, 0)

        # pacman's eyes
        eye_x = int(self.center_x + self.radius / 8)
        eye_y = int(self.center_y - self.radius * 0.65)
        eye_radius = int(self.radius / 6)
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), eye_radius, 0)

    def events_processing(self, evts):
        for e in evts:
            self.key_down(e)
            self.key_up(e)

    def key_up(self, e):
        if e.type == pygame.KEYUP:
            # x axis
            if e.key == pygame.K_RIGHT:
                self.vel_x = 0
            if e.key == pygame.K_LEFT:
                self.vel_x = 0
            # y axis
            if e.key == pygame.K_UP:
                self.vel_y = 0
            if e.key == pygame.K_DOWN:
                self.vel_y = 0

    def key_down(self, e):
        if e.type == pygame.KEYDOWN:
            # x axis
            if e.key == pygame.K_RIGHT:
                self.vel_x = VELOCITY
            if e.key == pygame.K_LEFT:
                self.vel_x = -VELOCITY
            # y axis
            if e.key == pygame.K_UP:
                self.vel_y = -VELOCITY
            if e.key == pygame.K_DOWN:
                self.vel_y = VELOCITY

    def movement_accept(self):
        self.row = self.mov_row_intention
        self.column = self.mov_column_intention


class Scenario(GameElement):
    def __init__(self, size, var_pacman):
        self.pacman = var_pacman
        self.size = size
        self.point = 0
        self.matrix = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def print_points(self, screen):
        points_x = self.size * 30
        points_y = 50
        image_points = word_format.render("Score: {}".format(self.point * 20 - 20), True, YELLOW)
        screen.blit(image_points, (points_x, points_y))

    def print_row(self, screen, row_number, row):
        for column_number, column in enumerate(row):
            x = column_number * self.size
            y = row_number * self.size
            half_axis = self.size // 2
            color = BLACK
            if column == 2:
                color = BLUE
            pygame.draw.rect(screen, color, (x, y, self.size, self.size), 0)
            if column == 1:
                pygame.draw.circle(screen, WHITE, (x + half_axis, y + half_axis), self.size // 10, 0)

    def print(self, screen):
        for row_number, row in enumerate(self.matrix):
            self.print_row(screen, row_number, row)
        self.print_points(screen)

    def movement_rules(self):
        col = self.pacman.mov_column_intention
        row = self.pacman.mov_row_intention
        if 0 <= col < 28 and 0 <= row < 29 and self.matrix[row][col] != 2:
            self.pacman.movement_accept()
            # sum points for each white point in the screen
            if self.matrix[row][col] ==1:
                self.point += 1
                self.matrix[row][col] = 0

    def events_processing(self, evts):
        pass


class Ghost(GameElement):
    def __init__(self, color, size):
        self.column = 6.0
        self.row = 8.0
        self.size = size
        self.color = color

    def print(self, screen):
        side = self.size // 8
        pixel_x = int(self.column * self.size)
        pixel_y = int(self.row * self.size)
        ghost_curve = [(pixel_x, pixel_y + self.size),
                       (pixel_x + side, pixel_y + side * 2),
                       (pixel_x + side * 2, pixel_y + side // 2),
                       (pixel_x + side * 3, pixel_y),
                       (pixel_x + side * 5, pixel_y),
                       (pixel_x + side * 6, pixel_y + side // 2),
                       (pixel_x + side * 7, pixel_y + side * 2),
                       (pixel_x + size, pixel_y + size)]
        pygame.draw.polygon(screen, self.color, ghost_curve, 0)

        pass

    def movement_rules(self):
        pass

    def events_processing(self, events):
        pass


if __name__ == "__main__":
    size = 600 // 30
    pacman = Pacman(size)
    blink = Ghost(RED, size)
    scenario = Scenario(size, pacman)

    while True:
        # movement rules
        pacman.movement_rules()
        scenario.movement_rules()

        # print all items
        screen.fill(BLACK)
        scenario.print(screen)
        pacman.print(screen)
        blink.print(screen)
        pygame.display.update()
        pygame.time.delay(100)

        events = pygame.event.get()
        pacman.events_processing(events)
        scenario.events_processing(events)