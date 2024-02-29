import pygame
import sys
from button import ImageButton
import os
import random

'''инициализация и параметры экрана'''
pygame.init()
WIDTH, HEIGHT = 1320, 844 #WIDTH, HEIGHT = 960, 600
MAX_FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
main_background = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
clock = pygame.time.Clock()
'''инициализация и параметры экрана'''

'''Загрузка и установка курсора'''
cursor = pygame.image.load("data\cursor.png")
pygame.mouse.set_visible(False)  # Скрываем стандартный курсор
'''Загрузка и установка курсора'''


'''группы спрайтов 1'''
tiles_group = pygame.sprite.Group()
end_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
'''группы спрайтов 1'''


'''группы спрайтов 2'''
first_tiles_group = pygame.sprite.Group()
first_dalle_dark_group = pygame.sprite.Group()
first_all_sprites = pygame.sprite.Group()
'''группы спрайтов 2'''

'''общий счет и музыкальное сопровождение'''
SCORE = 0 #общий счет
sound = pygame.mixer.Sound('data\click.mp3')
sound_zvuk_oshibki = pygame.mixer.Sound('data\zvuk-oshibki-vyibora.mp3')
zvuk_pobedyi = pygame.mixer.Sound('data\zvuk-pobedyi-v-igrovom-urovne-30120.mp3')
'''общий счет и музыкальное сопровождение'''

'''выход'''
def terminate():
    pygame.quit()
    sys.exit()
'''выход'''

'''Отображение курсора в текущей позиции мыши'''
def mouse_kursor():
    x, y = pygame.mouse.get_pos()
    screen.blit(cursor, (x-20, y-7))
'''Отображение курсора в текущей позиции мыши'''


'''загрузка и изменение размера изображений'''
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))
'''загрузка и изменение размера изображений'''


'''функция для отрисовки текста'''
font_name = pygame.font.match_font('arial')

def draw_text(surf, text, size, x=0, y=0, center=None):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (255, 255, 255))
    if center:
        text_rect = text_surface.get_rect(center=center)
    else:
        text_rect = (x, y)
    surf.blit(text_surface, text_rect)
'''функция для отрисовки текста'''



'''для 2ого''''''для 2ого''''''для 2ого''''''для 2ого''''''для 2ого''''''для 2ого''''''для 2ого''''''для 2ого'''

first_tile_images = {
    'dalle_dark': load_image('dalle.jpg'),
    'dalle_white': load_image('dalle1.jpg')
}

tile1_width = tile1_height = 80
class Tile1(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'dalle_dark':
            super().__init__(first_tiles_group, first_all_sprites, first_dalle_dark_group)
        else:
            super().__init__(first_tiles_group, first_all_sprites)
        self.image = first_tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile1_width * pos_x, tile1_height * pos_y)

def generate_plitka(level):
    x, y = None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile1('dalle_white', x, y)
            elif level[y][x] == '*':
                Tile1('dalle_dark', x, y)
    # вернем размер поля в клетках
    return x, y

class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 0
        self.top = 0
        self.cell_size = 80
        self.count = 0


    def on_click(self, cell_coords):
        if self.count == 11:
            self.count = 0
        if cell_coords:
            xc, yc = cell_coords
            otwet = {0: 6, 1: 4, 2: 2, 3: 2, 4: 0, 5: 2, 6: 2, 7: 2, 8: 0, 9: 0, 10: 0}
            if otwet[self.count] == xc and 10 - self.count == yc:
                self.count += 1
                print('yes')
                sound.play()
            else:
                sound_zvuk_oshibki.play()
                print('no')
                show_go_screen(self.board_score())
                self.count = 0

    def board_score(self):
        return self.count

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        print(cell)
        self.on_click(cell)


    def get_cell(self, mouse_pos):
        x = (mouse_pos[0] - self.left) // self.cell_size
        y = (mouse_pos[1] - self.top ) // self.cell_size
        if 0 <= x <= self.width and 0 <= y <= self.height:
            return x, y
        else:
            return None

def show_go_screen(score):
    screen.blit(main_background, (0, 0))
    draw_text(screen, f'Ваш счёт {score}', 64, center=(WIDTH / 2, HEIGHT / 4))
    #draw_text(screen, "Arrow keys move, Space to fire", 22, center=(WIDTH / 2, HEIGHT / 2))
    draw_text(screen, "Нажмите англ 'a' кнопку для начала заново", 64, center=(WIDTH / 2, HEIGHT * 3 / 4))

    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(MAX_FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYUP:
                waiting = False

def show_win1_screen(score):
    global SCORE
    # Создание кнопок
    back_button = ImageButton(WIDTH/2-(252/2), 350, 252, 74, "Заново", "data\green_button2.jpg", "data\green_button2_hover.jpg", "data\click.mp3")
    next_button = ImageButton(WIDTH/2-(252/2), 150, 252, 74, "Дальше", "data\green_button2.jpg", "data\green_button2_hover.jpg", "data\click.mp3")
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, 0))
        #фон
        text = f"Вы прошли первый уровень и набрали {score}"
        draw_text(screen, text, 72, center=(WIDTH/2,100))
        #настройки

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    #выход в игру для прохождения заново
                    fade()
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_button:
                fade()
                running = False
                #выход в игру для прохождения заново

            if event.type == pygame.USEREVENT and event.button == next_button:
                SCORE = score
                print(SCORE)
                second_level()
                running = False

            for btn in [back_button, next_button]:
                btn.handle_event(event)

        for btn in [back_button, next_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
            #отрисовка и наведение

        # Отображение курсора в текущей позиции мыши
        mouse_kursor()

        pygame.display.flip() #обновление экран

'''для 2ого''''''для 2ого''''''для 2ого''''''для 2ого''''''для 2ого''''''для 2ого''''''для 2ого''''''для 2ого'''



'''для 1ого''''''для 1ого''''''для 1ого''''''для 1ого''''''для 1ого''''''для 1ого''''''для 1ого''''''для 1ого'''

'''загрузка стен и пола, выхода'''
tile_images = {
    'wall': load_image('stena.png'),
    'empty': load_image('pol.png'),
    'exit': load_image('go_out.png')
}

'''размер тайлов'''
tile_width = tile_height = 100
'''размер тайлов'''

'''размер тайлов'''
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(tiles_group, all_sprites, walls_group)
        elif tile_type == 'exit':
            super().__init__(tiles_group, all_sprites, end_group)
        else:
            super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), (tile_width, tile_height)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

class Player(AnimatedSprite):
    def __init__(self, pos_x, pos_y):

        sheet = load_image("pers1.png")
        super().__init__(sheet, 6, 12, 0, 0)
        player_group.add(self)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self, move_type: str):
        super().update()

        old = self.rect.copy()
        keys = pygame.key.get_pressed()
        
        if move_type is not None:
            if move_type == 'right':
                self.rect.x += tile_width
            elif move_type == 'left':
                self.rect.x -= tile_width
            elif move_type == 'up':
                self.rect.y -= tile_height
            elif move_type == 'down':
                self.rect.y += tile_height

        if pygame.sprite.spritecollideany(self, walls_group):
            self.rect = old
    
        if pygame.sprite.spritecollideany(self, end_group):
            show_win2_screen(10)
        
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '*':
                Tile('wall', x, y)
            elif level[y][x] == 'q':
                Tile('exit', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                xp, yp = x, y
    # вернем игрока, а также размер поля в клетках
    new_player = Player(xp, yp)
    return new_player, x, y, xp, yp

class Camera:
    #зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
        #сдвинуть объект abj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
            
        #позиционировать камеру на объект target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def show_win2_screen(score):
    global SCORE, tiles_group, end_group, walls_group, player_group, all_sprites
    tiles_group = pygame.sprite.Group()
    end_group = pygame.sprite.Group()
    walls_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    zvuk_pobedyi.play()
    # Создание кнопок
    back_button = ImageButton(WIDTH/2-(252/2), 350, 252, 74, "Заново", "data\green_button2.jpg", "data\green_button2_hover.jpg", "data\click.mp3")
    running = True
    while running:
        #фон
        if SCORE + score == 21:
            fon = pygame.transform.scale(pygame.image.load("data\start_s.jpg"), (WIDTH, HEIGHT))
            screen.blit(fon, (0, 0))
            text = f"Вы прошли все уровни и набрали {score + SCORE}"
            draw_text(screen, text, 72, center=(WIDTH/2,100))
        else:
            screen.fill((0, 0, 0))
            screen.blit(main_background, (0, 0))
            text = f"Вы прошли второй уровень и набрали {score}"
            draw_text(screen, text, 72, center=(WIDTH/2,100))
        #настройки

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

            if event.type == pygame.KEYDOWN:
                # Возврат в меню
                if event.key == pygame.K_ESCAPE:
                    SCORE = 0
                    main_menu()
                    fade()
                    running = False

            if event.type == pygame.USEREVENT and event.button == back_button:
                SCORE = 0
                main_menu()
                fade()
                running = False
                #выход обратно в меню

            for btn in [back_button]:
                btn.handle_event(event)

        for btn in [back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
            #отрисовка и наведение

        # Отображение курсора в текущей позиции мыши
        mouse_kursor()

        pygame.display.flip() #обновление экрана

'''для 1ого''''''для 1ого''''''для 1ого''''''для 1ого''''''для 1ого''''''для 1ого''''''для 1ого''''''для 1ого'''




def start_screen():
    intro_text = ["КРЕПОСТЬ ФАРАОНА",
        "",
        "Перемещение героя - по стрелкам",
        "",
                  "первый уровень - волшебные плитки",
                  "второй уровень - лабиринт"]
    fon = pygame.transform.scale(pygame.image.load("data\start_s.jpg"), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 100
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру


        pygame.display.flip()
        clock.tick(MAX_FPS)

start_screen()

def main_menu():
    
    # Создание кнопок
    start1_button = ImageButton(WIDTH/2-(252/2), 150, 252, 74, "Первый уровень", "data\green_button2.jpg", "data\green_button2_hover.jpg", "data\click.mp3")
    start_button = ImageButton(WIDTH/2-(252/2), 250, 252, 74, "Второй уровень", "data\green_button2.jpg", "data\green_button2_hover.jpg", "data\click.mp3")
    exit_button = ImageButton(WIDTH/2-(252/2), 450, 252, 74, "Выйти", "data\green_button2.jpg", "data\green_button2_hover.jpg", "data\click.mp3")
    #середина экрана - половина кнопки - чтобы по центру


    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, 0))
        #фон
        text = f"Меню"
        draw_text(screen, text, 72, center=(WIDTH/2,100))
        #название вверху меню

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #выход из проги
                running = False
                terminate()

            if event.type == pygame.USEREVENT and event.button == start_button:
                print("Кнопка 'Старт' была нажата!")
                fade()
                second_level()

            elif event.type == pygame.USEREVENT and event.button == start1_button:
                print("Кнопка 'Старт' была нажата!")
                fade()
                first_level()


            if event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
                #выход при нажатии кнопки выход
                terminate()

            for btn in [start_button, start1_button, exit_button]:
                #по циклу проходимся по всем кнопкам и каждому вызываем обработку event
                btn.handle_event(event)

        for btn in [start_button, start1_button, exit_button]:
            #отрисовка и наведение
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        # Отображение курсора в текущей позиции мыши
        mouse_kursor()

        pygame.display.flip()


def info_first_game():
    fon1 = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon1, (0, 0))
    yy = 0
    text = ["Как играть: На полосе номер 1 считается", 
        "количество светлых и темных плит. Из большего числа",
        "вычитается меньшее. Число получившееся в ответе",
        "отсчитывается на этой полосе слева направо. На ту плиту,",
        "на которой остановился счёт, вам надо становиться.",
        "Так же и остальные полосы. Важно: нажатие на любую плиту",
        "на уже пройденной полосе считается как ошибка."]

    back_button = ImageButton(10, 10, 252, 74, "Назад", "data\green_button2.jpg", "data\green_button2_hover.jpg", "data\click.mp3")
    running = True
    while running:
        fon1 = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon1, (0, 0))
        for a in text:
            yy += 40
            draw_text(screen, a, 36, x=150, y=yy)
        yy = 100
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

            if event.type == pygame.USEREVENT and event.button == back_button:
                fade()
                running = False
                #выход обратно в меню

            for btn in [ back_button]:
                btn.handle_event(event)

        for btn in [back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
            #отрисовка и наведение

        # Отображение курсора в текущей позиции мыши
        mouse_kursor()
        pygame.display.flip() #обновление экрана

def info_second_game():
    fon1 = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon1, (0, 0))
    yy = 0
    text = ["Ваша цель - добраться до выхода (синей плитки).",
    "Удачи!"]

    back_button = ImageButton(10, 10, 252, 74, "Назад", "data\green_button2.jpg", "data\green_button2_hover.jpg", "data\click.mp3")
    running = True
    while running:
        fon1 = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon1, (0, 0))
        for a in text:
            yy += 40
            draw_text(screen, a, 36, x=150, y=yy)
        yy = 100
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

            if event.type == pygame.USEREVENT and event.button == back_button:
                fade()
                running = False
                #выход обратно в меню

            for btn in [ back_button]:
                btn.handle_event(event)

        for btn in [back_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
            #отрисовка и наведение

        # Отображение курсора в текущей позиции мыши
        mouse_kursor()
        pygame.display.flip() #обновление экрана

def second_level():
    global tiles_group, end_group, walls_group, player_group, all_sprites
    # Создание кнопок
    screen.fill((0, 0, 0))
    back_button1 = ImageButton(0, 0, 252, 74, "Назад", "data\green_button2.jpg", "data\green_button2_hover.jpg", "data\click.mp3")
    info_button = ImageButton(0, 70, 252, 74, "Инфо", "data\green_button2.jpg", "data\green_button2_hover.jpg", "data\click.mp3")
    running = True
    player = None
    player, level_x, level_y, xp, yp = generate_level(load_level('map.txt'))

    
    camera = Camera()
    move_type = None

    while running:
        screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                tiles_group = pygame.sprite.Group()
                end_group = pygame.sprite.Group()
                walls_group = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                all_sprites = pygame.sprite.Group()
                terminate()

            if event.type == pygame.KEYDOWN:
                # Возврат в меню
                if event.key == pygame.K_ESCAPE:
                    tiles_group = pygame.sprite.Group()
                    end_group = pygame.sprite.Group()
                    walls_group = pygame.sprite.Group()
                    player_group = pygame.sprite.Group()
                    all_sprites = pygame.sprite.Group()
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                move_type = 'right'
            elif keys[pygame.K_LEFT]:
                move_type = 'left'
            elif keys[pygame.K_UP]:
                move_type = 'up'
            elif keys[pygame.K_DOWN]:
                move_type = 'down'


            # Возврат в меню
            if event.type == pygame.USEREVENT and event.button == back_button1:
                tiles_group = pygame.sprite.Group()
                end_group = pygame.sprite.Group()
                walls_group = pygame.sprite.Group()
                player_group = pygame.sprite.Group()
                all_sprites = pygame.sprite.Group()
                main_menu()
                running = False

            if event.type == pygame.USEREVENT and event.button == info_button:
                info_second_game()

            for btn in [back_button1, info_button]:
                btn.handle_event(event)



        
        



        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            
            camera.apply(sprite)

        all_sprites.update(move_type)
        
        # изменяем ракурс камеры
        camera.update(player)
        
        move_type = None
        all_sprites.draw(screen)
        #player_group.draw(screen)

        for btn in [back_button1, info_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)
            #отображение кнопки
        
        # Отображение курсора в текущей позиции мыши
        mouse_kursor()


        clock.tick(MAX_FPS)
        pygame.display.flip()

def first_level():
    global SCORE
    SCORE = 0
    # Создание кнопок
    back_button = ImageButton(880, 10, 252, 74, "Назад", "data\green_button2.jpg", "data\green_button2_hover.jpg", "data\click.mp3")
    info_button = ImageButton(880, 70, 252, 74, "Инфо", "data\green_button2.jpg", "data\green_button2_hover.jpg", "data\click.mp3")
    board = Board(10, 10)

    clock = pygame.time.Clock()
    l_x, l_y = generate_plitka(load_level('map1.txt'))
    #move_type1 = None

    running = True
    while running:
        screen.fill((0, 0, 0))
        fon1 = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))

        screen.blit(fon1, (0, 0))
        #ad_b = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                terminate()

            if event.type == pygame.KEYDOWN:
                # Возврат в меню
                if event.key == pygame.K_ESCAPE:
                    running = False

            # Возврат в меню
            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False


            if event.type == pygame.USEREVENT and event.button == info_button:
                info_first_game()

            for btn in [back_button, info_button]:
                btn.handle_event(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                board.get_click(event.pos)
                SCORE = board.board_score()
                if SCORE == 11:
                    zvuk_pobedyi.play()
                    show_win1_screen(SCORE)

        first_all_sprites.draw(screen)

        for btn in [back_button, info_button]:
            btn.check_hover(pygame.mouse.get_pos())
            btn.draw(screen)

        # Отображение курсора в текущей позиции мыши
        mouse_kursor()

        clock.tick(MAX_FPS)
        pygame.display.flip()


'''затемнение'''
def fade():
    running = True
    fade_alpha = 0  # Уровень прозрачности для анимации

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Анимация затухания текущего экрана
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))

        # Увеличение уровня прозрачности
        fade_alpha += 5
        if fade_alpha >= 105:
            fade_alpha = 255
            running = False

        pygame.display.flip()
        clock.tick(MAX_FPS)  # Ограничение FPS
'''затемнение'''

if __name__ == "__main__":
    main_menu()
