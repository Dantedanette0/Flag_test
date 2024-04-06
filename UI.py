import pygame


#unfinished
class Button:
    def __init__(self, x, y, width, height, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = (75, 75, 75)  

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
            
        return False

def draw_text(screen, text, position, font_size=30, color=(0, 0, 0)):
    font = pygame.font.SysFont("comicsans", font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)


def main_menu(screen, fpsClock, FPS, WIDTH, HEIGHT):
    menu_run = True
    start_button = Button(WIDTH / 2 - 100, HEIGHT / 2 - 40, 200, 80, 'Start')

    while menu_run:
        screen.fill((255, 255, 255)) 

        
        start_button.draw(screen, (0, 0, 0))

        
        controls_description = [
            "'F' - Create a flag",
            "'W' - Apply wind effect",
            "'left click' - Select and move points",
            "Right-Click - Remove a constraint"
        ]
        for i, desc in enumerate(controls_description):
            draw_text(screen, desc, (50, HEIGHT / 2 + 100 + i * 40))  

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                pygame.quit()
                return False  

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_over(pos):
                    menu_run = False 

        pygame.display.update()
        fpsClock.tick(FPS)

    return True  


class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val):

        self.rect = pygame.Rect(x, y, w, h) 
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val

        self.handle_pos = x + w * ((initial_val - min_val) / (max_val - min_val))

    def draw(self, surface):

        pygame.draw.rect(surface, (200, 200, 200), self.rect)

        handle_rect = pygame.Rect(self.handle_pos - 10, self.rect.y - 5, 20, self.rect.height + 10)
        pygame.draw.rect(surface, (100, 100, 100), handle_rect)

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
            elif event.type == pygame.MOUSEMOTION and self.dragging:

                self.handle_pos = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
                self.value = self.min_val + ((self.handle_pos - self.rect.x) / self.rect.width) * (self.max_val - self.min_val)

