import pygame

class ImageButton:
    def __init__(self, x, y, width, height, text, image_path, hover_image_path=None, sound_path=None):
        #координаты, размеры кнопок, текст, картинка, картинка при наведении, путь до звука
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.image = pygame.image.load(image_path)
        #загрузка изображения и подгон его машстаба
        self.image = pygame.transform.scale(self.image, (width, height))

        #картинка при наведении
        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = pygame.image.load(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height))

        self.rect = self.image.get_rect(topleft=(x, y))

        self.sound = None
        #загрузка звука
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)

        #наведена ли мышка на объект
        self.is_hovered = False


    #для рисовки кнопки
    def draw(self, screen):
        #kartinka - otobrashenie
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font(None, 36)
        #подключение текста, размер
        text_surface = font.render(self.text, True, (255, 255, 255))
        #рендер
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        #расположение по координатам

    def check_hover(self, mouse_pos):
        #позиция мыши - совпали ли координаты с прямоугольником
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        #обработка действий
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            #именно левая кнопка мыши, над кнопкой
            if self.sound:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))
            #ивент за то, что мышка была нажата



