import pygame
import time
import random
import copy

pygame.init()

#necessities
WIDTH, HEIGHT = 1200, 980
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SNAKE!")
FPS = 60
clock = pygame.time.Clock()
word_font = pygame.font.SysFont("calibri", 60)


box_width = 20

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

num_row_boxes = (HEIGHT - 100) // box_width
num_col_boxes = WIDTH // box_width

class Box:
    def __init__(self, row, col, width):
        self.__row = row
        self.__col = col
        self.__x = col * width
        self.__y = (row * width) + 100
        self.__width = width
        self.__color = WHITE

    def draw_background(self, win):

        if self.__row == 0 or self.__row == num_row_boxes-1 or self.__col == 0 or self.__col == num_col_boxes-1:
            pygame.draw.rect(win, YELLOW, (self.__x, self.__y, self.__width + 1, self.__width + 1)) # filling
        else:
            pygame.draw.rect(win, BLACK, (self.__x, self.__y, self.__width+2, self.__width+2)) # outline
            pygame.draw.rect(win, self.__color, (self.__x + 1, self.__y + 1, self.__width, self.__width)) # filling


class Snake:
    def __init__(self, row, col, direction=None):
        self.__row = row
        self.__col = col
        self.__x = self.__col * box_width
        self.__y = (self.__row * box_width) + 100
        self.__width = box_width
        self.__color = GREEN
        self.__direction = direction
        self.__length = 0

    def get_direction(self):
        return self.__direction

    def change_direction_n(self):
        self.__direction = "n"

    def change_direction_e(self):
        self.__direction = "e"

    def change_direction_s(self):
        self.__direction = "s"

    def change_direction_w(self):
        self.__direction = "w"

    def get_row(self):
        return self.__row

    def change_row_n(self):
        self.__row -= 1
        self.__y = (self.__row * box_width) + 100

    def change_row_s(self):
        self.__row += 1
        self.__y = (self.__row * box_width) + 100

    def get_col(self):
        return self.__col

    def change_col_e(self):
        self.__col += 1
        self.__x = self.__col * box_width

    def change_col_w(self):
        self.__col -= 1
        self.__x = self.__col * box_width

    def set_row(self, value):
        self.__row = value
        self.__y = (self.__row * box_width) + 100

    def set_col(self, value):
        self.__col = value
        self.__x = self.__col * box_width

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def add_length(self, num):
        self.__length += num

    def get_length(self):
        return self.__length

    def draw_snake(self, win):
        if self.__row == 0 or self.__row == num_row_boxes - 1 or self.__col == 0 or self.__col == num_col_boxes - 1:
            pygame.draw.rect(win, BLACK, (self.__x, self.__y, self.__width + 1, self.__width + 1)) # outline
            pygame.draw.rect(win, self.__color, (self.__x + 1, self.__y + 1, self.__width-1, self.__width-1))
        else:
            pygame.draw.rect(win, self.__color, (self.__x + 1, self.__y + 1, self.__width-1, self.__width-1))


class Apple():
    def __init__(self, row, col, num_row_boxes, num_col_boxes):
        self.__row = row
        self.__col = col
        self.__num_row_boxes = num_row_boxes
        self.__num_col_boxes = num_col_boxes
        self.__x = self.__col * box_width
        self.__y = (self.__row * box_width) + 100
        self.__color = RED
        self.__width = box_width

    def get_row(self):
        return self.__row

    def get_col(self):
        return self.__col

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_rand_row(self):
        self.__row = random.randint(1, self.__num_row_boxes-2)

    def set_rand_col(self):
        self.__col = random.randint(1, self.__num_col_boxes-2)

    def draw_apple(self, win):
        self.__x = self.__col * box_width
        self.__y = (self.__row * box_width) + 100
        pygame.draw.rect(win, self.__color, (self.__x + 1, self.__y + 1, self.__width-1, self.__width-1))


class Node:
    def __init__(self, data, next=None):
        self.__data = data
        self.__next = next

    def __str__(self):
        return self.__data

    def get_data(self):
        return self.__data

    def get_next(self):
        return self.__next

    def set_data(self, new_data):
        self.__data = new_data

    def set_next(self, new_next):
        self.__next = new_next


class DirectionLinkedList:
    def __init__(self):
        self.__head = None
        self.__tail = None
        self.__next = None

    def __str__(self):
        list = "["
        current = self.__head

        if current == None:
            return "[]"

        while current.get_next() != None:
            list = list + current.get_data() +  ", "
            current = current.get_next()

        list = list + current.get_data() + "]"

        return list

    def get_head(self):
        return self.__head

    def get_tail(self):
        return self.__tail

    def add(self, value):
        node = Node(value)
        node.set_next(self.__head)
        self.__head = node


class Score:
    def __init__(self, score=0):
        self.__score = score

    def __str__(self):
        return str(self.__score)

    def add_score(self, value):
        self.__score += value

    def draw_score(self, win, num):
        self.__word_font = pygame.font.SysFont("calibri", 20)
        self.__word_label = self.__word_font.render("Score: " + str(num), 1, BLACK)
        win.blit(self.__word_label, (50, (100 - self.__word_label.get_height())//2))
        pygame.display.update()


def make_background():
    num_row_boxes = (HEIGHT - 100) // box_width

    num_col_boxes = WIDTH // box_width

    box_list = []

    for row in range(num_row_boxes):
        box_list.append([])
        for col in range(num_col_boxes):
            box_list[row].append(Box(row, col, box_width))

    return box_list


def draw(win, grid, snake_list, apple, score):
    win.fill(pygame.Color("white"))

    # title
    title_label = word_font.render("SNAKE!", 1, BLACK)
    win.blit(title_label, (round(WIDTH/2 - title_label.get_width()//2), (100 - title_label.get_height())//2))

    # background (grid)
    for row in grid:
        for box in row:
            box.draw_background(win)

    # snake
    for snake in snake_list:
        snake.draw_snake(win)

    #apple
    apple.draw_apple(win)

    # score
    number = snake_list[0].get_length()
    score.draw_score(win, number)


def main_menu():
    game_state = True

    while game_state:
        WIN.fill(WHITE)
        word_font = pygame.font.SysFont("calibri", 60)
        title_text = word_font.render("CLICK ANY BUTTON TO PLAY", 1, BLACK)
        WIN.blit(title_text, (round(WIDTH/2 - title_text.get_width()/2), round(HEIGHT/2 - title_text.get_height()/2)))

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
            elif event.type == pygame.QUIT:
                game_state = False

        pygame.display.update()
    pygame.quit()


def display_message(message):

    pygame.time.delay(1000)
    WIN.fill(WHITE)
    win_text = word_font.render(message, 1, BLACK)
    WIN.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - win_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    run = True
    directions = DirectionLinkedList()

    snake_length = 1
    num_row_boxes = (HEIGHT - 100) // box_width
    num_col_boxes = WIDTH // box_width
    mid_row = num_row_boxes // 2
    mid_col = num_col_boxes // 2

    original_snake = Snake(mid_row, mid_col)
    snake_list = [original_snake]

    apple_start_row = random.randint(1, num_row_boxes-2)
    apple_start_col = random.randint(1, num_col_boxes-2)

    apple = Apple(apple_start_row, apple_start_col, num_row_boxes, num_col_boxes)

    score = Score(0)

    dirty_rects = []

    while run:

        clock.tick(FPS)
        pygame.display.update()

        grid = make_background()
        draw(WIN, grid, snake_list, apple, score)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            #if direction key pressed, add instruction to head of linked list to determine direction of movement
            if event.type == pygame.KEYDOWN:
                # when up arrow pressed move up
                if len(snake_list) == 1:
                    if event.key == pygame.K_UP:
                        directions.add("n")
                    elif event.key == pygame.K_DOWN:
                        directions.add("s")
                    elif event.key == pygame.K_LEFT:
                        directions.add("w")
                    elif event.key == pygame.K_RIGHT:
                        directions.add("e")
                    elif event.key == pygame.K_SPACE:
                        print(directions)
                else:
                    if event.key == pygame.K_UP and directions.get_head().get_data() != "s":
                        directions.add("n")
                    elif event.key == pygame.K_DOWN and directions.get_head().get_data() != "n":
                        directions.add("s")
                    elif event.key == pygame.K_LEFT and directions.get_head().get_data() != "e":
                        directions.add("w")
                    elif event.key == pygame.K_RIGHT and directions.get_head().get_data() != "w":
                        directions.add("e")
                    elif event.key == pygame.K_SPACE:
                        print(directions)

        # controlling the movement of the snake
        if directions.get_head() != None:
            #print("ROW:", snake_list[0].get_row(), "COL:", snake_list[0].get_row(), "x:",snake_list[0].get_row(), "y:", snake_list[0].get_row(), directions.get_head().get_data())

            if directions.get_head().get_data() == "n" and original_snake.get_row() >= 0:

                #coords for each snake part
                #snake_list_str_1 = [(snake.get_row(), snake.get_col()) for snake in snake_list]
                #print(snake_list_str_1)

                if len(snake_list) > 1:
                    for i in range(len(snake_list)-1, 0, -1):
                        snake_list[i] = copy.deepcopy(snake_list[i-1])
                elif len(snake_list) == 2:
                    new_snake = copy.deepcopy(snake_list[0])
                    snake_list[1] = new_snake

                snake_list[0].change_row_n()

                draw(WIN, grid, snake_list, apple, score)

                pygame.display.update()
                time.sleep(0.01)

            elif directions.get_head().get_data() == "s" and original_snake.get_row() <= num_row_boxes - 1:

                if len(snake_list) > 1:
                    for i in range(len(snake_list)-1, 0, -1):
                        snake_list[i] = copy.deepcopy(snake_list[i-1])
                elif len(snake_list) == 2:
                    new_snake = copy.deepcopy(snake_list[0])
                    snake_list[1] = new_snake

                snake_list[0].change_row_s()

                draw(WIN, grid, snake_list, apple, score)

                pygame.display.update()
                time.sleep(0.01)

            elif directions.get_head().get_data() == "e" and original_snake.get_col() <= num_col_boxes - 1:

                if len(snake_list) > 1:
                    for i in range(len(snake_list)-1, 0, -1):
                        snake_list[i] = copy.deepcopy(snake_list[i-1])
                elif len(snake_list) == 2:
                    new_snake = copy.deepcopy(snake_list[0])
                    snake_list[1] = new_snake

                snake_list[0].change_col_e()

                draw(WIN, grid, snake_list, apple, score)

                pygame.display.update()
                time.sleep(0.01)

            elif directions.get_head().get_data() == "w" and original_snake.get_col() >= 0:

                if len(snake_list) > 1:
                    for i in range(len(snake_list)-1, 0, -1):
                        snake_list[i] = copy.deepcopy(snake_list[i-1])
                elif len(snake_list) == 2:
                    new_snake = copy.deepcopy(snake_list[0])
                    snake_list[1] = new_snake

                snake_list[0].change_col_w()

                draw(WIN, grid, snake_list, apple, score)

                pygame.display.update()
                time.sleep(0.01)


        # when snake touches a apple
        if original_snake.get_row() == apple.get_row() and original_snake.get_col() == apple.get_col():
            snake_list[0].add_length(1)
            apple.set_rand_row()
            apple.set_rand_col()

            if directions.get_head().get_data() == "n":

                last_snake_section = snake_list[len(snake_list)-1]
                last_snake_section_row = last_snake_section.get_row()
                last_snake_section_col = last_snake_section.get_col()
                new_snake = Snake(last_snake_section_row + 1, last_snake_section_col)
                snake_list.append(new_snake)

            elif directions.get_head().get_data() == "e":

                last_snake_section = snake_list[len(snake_list)-1]
                last_snake_section_row = last_snake_section.get_row()
                last_snake_section_col = last_snake_section.get_col()
                new_snake = Snake(last_snake_section_row, last_snake_section_col - 1)
                snake_list.append(new_snake)

            elif directions.get_head().get_data() == "s":

                last_snake_section = snake_list[len(snake_list)-1]
                last_snake_section_row = last_snake_section.get_row()
                last_snake_section_col = last_snake_section.get_col()
                new_snake = Snake(last_snake_section_row - 1, last_snake_section_col)
                snake_list.append(new_snake)

            elif directions.get_head().get_data() == "w":

                last_snake_section = snake_list[len(snake_list)-1]
                last_snake_section_row = last_snake_section.get_row()
                last_snake_section_col = last_snake_section.get_col()
                new_snake = Snake(last_snake_section_row, last_snake_section_col + 1)
                snake_list.append(new_snake)


        #when snake touches the edge of the boundary
        #north boundary
        if not (1 <= snake_list[0].get_row()) and directions.get_head().get_data() == "n":
            display_message("You Lost")
            main_menu()

            draw(WIN, grid, snake_list, apple, score)

        #east boundary
        if not (snake_list[0].get_col() <= num_col_boxes - 2) and directions.get_head().get_data() == "e":
            display_message("You Lost")
            main_menu()

            draw(WIN, grid, snake_list, apple, score)

        #south boundary
        if not (snake_list[0].get_row() <= num_row_boxes - 2) and directions.get_head().get_data() == "s":
            display_message("You Lost")
            main_menu()

            draw(WIN, grid, snake_list, apple, score)

        #west boundary
        if not (1 <= snake_list[0].get_col()) and directions.get_head().get_data() == "w":
            display_message("You Lost")
            main_menu()

        #what if snake hits itself?????
        head_pos = (snake_list[0].get_row(), snake_list[0].get_col())

        body_pos = []

        for i in range(1, len(snake_list)-1):
            if snake_list[i].get_row() == head_pos[0]:
                if snake_list[i].get_col() == head_pos[1]:
                    display_message("You Lost")
                    main_menu()

        draw(WIN, grid, snake_list, apple, score)

    pygame.quit()

main_menu()
