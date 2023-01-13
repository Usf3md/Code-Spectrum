# BREAKER TOKEN
import pygame
import math


class Utilities:
    WIDTH, HEIGHT = 1024, 512

    def click_check(self, event, start_x, start_y, end_x, end_y):
        mx, my = pygame.mouse.get_pos()
        if start_x <= mx <= end_x and start_y <= my <= end_y:
            if pygame.MOUSEBUTTONUP == event.type:
                pygame.mouse.set_pos((mx+1, my))
                pygame.mouse.set_pos((mx, my))
                return (True, True)
            return (True, False)
        return (False, False)


class Image(Utilities):
    def __init__(self, path):
        self.path = path
        self.image = pygame.image.load(self.path)
        self.image_width, self.image_height = self.image.get_width(), self.image.get_height()

    def image_load(self, path):
        if path != self.path:
            self.image = pygame.image.load(path)
            self.path = path
            self.image_width, self.image_height = self.image.get_width(), self.image.get_height()

    def draw(self, win):
        win.blit(self.image, (self.WIDTH - self.image_width, 0))


class Rectangle(Utilities):
    def __init__(self, x, y, rect_width, rect_height, color, checked=False, radio=False, selected_color=0, hover_color=0, stroke=1, stroke_color=(0, 0, 0), label_font=0, label_text="", label_color=0, font=0, text=""):
        self.x = x
        self.y = y
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.color = color
        self.selected_color = selected_color
        self.hover_color = hover_color if hover_color else color
        self.stroke = stroke
        self.stroke_color = stroke_color
        self.correct_arrangment = True
        self.checked = checked
        if self.checked:
            self.color, self.selected_color = self.selected_color, self.color
        self.radio = radio
        self.label_font = label_font
        self.label_text = label_text
        self.label_text_obj = self.label_font.render(
            self.label_text, True, label_color) if self.label_text else 0
        self.font = font
        self.text = text
        self.text_obj = font.render(
            self.text, True, (255, 255, 255)) if self.font else 0

    def draw(self, win):
        if self.stroke:
            win.fill(self.stroke_color, (self.x - self.stroke, self.y - self.stroke,
                     self.rect_width + 2*self.stroke, self.rect_height + 2*self.stroke))
        win.fill(self.color, (self.x, self.y, self.rect_width, self.rect_height))


class Checkbox(Rectangle):
    def event_check(self, event):
        action = self.click_check(
            event, self.x, self.y, self.x+self.rect_width, self.y+self.rect_height)
        if action[0] and self.correct_arrangment and not self.checked:
            self.color, self.selected_color = self.selected_color, self.color
            self.correct_arrangment = False
        elif not action[0] and not self.correct_arrangment and not self.checked:
            self.color, self.selected_color = self.selected_color, self.color
            self.correct_arrangment = True
        if action[1] and not self.checked:
            self.checked = True
        return action[1]

    def draw(self, win):
        if self.stroke:
            win.fill(self.stroke_color, (self.x - self.stroke, self.y - self.stroke,
                     self.rect_width + 2*self.stroke, self.rect_height + 2*self.stroke))
        win.fill(self.color, (self.x, self.y, self.rect_width, self.rect_height))
        if self.label_text:
            win.blit(self.label_text_obj, (self.x,
                                           self.y - self.label_font.size(self.label_text)[1]-3))
        if self.text:
            win.blit(self.text_obj, (self.x + (self.rect_width - self.font.size(self.text)
                     [0])//2, self.y + (self.rect_height - self.font.size(self.text)[1])//2))


class RadioCheckbox(Rectangle):
    def event_check(self, event):
        action = self.click_check(
            event, self.x, self.y, self.x+self.rect_width, self.y+self.rect_height)
        if action[1]:
            self.checked = False if self.checked else True
            self.color, self.selected_color = self.selected_color, self.color
        return self.checked

    def draw(self, win):
        if self.stroke:
            win.fill(self.stroke_color, (self.x - self.stroke, self.y - self.stroke,
                     self.rect_width + 2*self.stroke, self.rect_height + 2*self.stroke))
        win.fill(self.color, (self.x, self.y, self.rect_width, self.rect_height))
        if self.label_text:
            win.blit(self.label_text_obj, (self.x + self.rect_width + 5,
                                           self.y + (self.rect_height - self.label_font.size(self.label_text)[1])//2))


class Button(Rectangle):
    def event_check(self, event):
        action = self.click_check(
            event, self.x, self.y, self.x+self.rect_height, self.y+self.rect_width)
        if action[0] and self.correct_arrangment:
            self.color, self.hover_color = self.hover_color, self.color
            self.correct_arrangment = False
        elif not action[0] and not self.correct_arrangment:
            self.color, self.hover_color = self.hover_color, self.color
            self.correct_arrangment = True
        return action[1]

    def draw(self, win):
        if self.stroke:
            win.fill(self.stroke_color, (self.x - self.stroke, self.y - self.stroke,
                     self.rect_width + 2*self.stroke, self.rect_height + 2*self.stroke))
        win.fill(self.color, (self.x, self.y, self.rect_width, self.rect_height))
        win.blit(self.text_obj, (self.x + (self.rect_width - self.font.size(self.text)
                 [0])//2, self.y + (self.rect_height - self.font.size(self.text)[1])//2))


class Triangle(Utilities):
    def __init__(self, x, y, side, color, font, label_font, text, font_color, data, label_text, label_color, hover_color=0, stroke=1, stroke_color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.x2 = x
        self.side = side
        self.lcolor = color
        self.rcolor = color
        self.font = font
        self.text = text
        self.text_obj = font.render(self.text, True, font_color)
        self.label_font = label_font
        self.label_text = label_text
        self.label_text_obj = label_font.render(
            self.label_text, True, label_color)
        self.padding = 20
        self.x2 += font.size(self.text)[0] + self.side + self.padding
        self.lhover_color = hover_color
        self.rhover_color = hover_color
        self.stroke = stroke
        self.stroke_color = stroke_color
        self.correct_arrangment = [True, True]
        self.triangle_height = self.side*math.cos(math.radians(30))
        self.index = 0
        self.font_color = font_color
        self.data = data

    def event_check(self, event):
        laction = self.click_check(
            event, self.x, self.y, self.x+self.side, self.y+self.side)
        if laction[0] and self.correct_arrangment[0]:
            self.lcolor, self.lhover_color = self.lhover_color, self.lcolor
            self.correct_arrangment[0] = False
        elif not laction[0] and not self.correct_arrangment[0]:
            self.lcolor, self.lhover_color = self.lhover_color, self.lcolor
            self.correct_arrangment[0] = True
        if laction[1]:
            self.index -= 1

        raction = self.click_check(
            event, self.x2, self.y, self.x2+self.side, self.y+self.side)
        if raction[0] and self.correct_arrangment[1]:
            self.rcolor, self.rhover_color = self.rhover_color, self.rcolor
            self.correct_arrangment[1] = False
        elif not raction[0] and not self.correct_arrangment[1]:
            self.rcolor, self.rhover_color = self.rhover_color, self.rcolor
            self.correct_arrangment[1] = True
        if raction[1]:
            self.index += 1
        self.text = self.data[self.index % len(self.data)]
        self.text_obj = self.font.render(
            self.text, True, self.font_color)
        return self.text, self.index % len(self.data) + 1

    def draw(self, win):
        if self.stroke:
            pygame.draw.polygon(win, self.stroke_color, ((
                self.side + self.x + self.stroke, self.y - self.stroke*2), (self.side + self.x + self.stroke, self.side + self.y + self.stroke*2), (self.side - self.triangle_height + self.x - self.stroke*2, self.side//2 + self.y)))
            pygame.draw.polygon(win, self.stroke_color, ((
                self.x2 - self.stroke, self.y - self.stroke*2), (self.x2 - self.stroke, self.side + self.y + self.stroke*2), (self.triangle_height + self.x2 + self.stroke*2, self.side//2 + self.y)))

        pygame.draw.polygon(win, self.lcolor, ((
            self.side + self.x, self.y), (self.side + self.x, self.side + self.y), (self.side - self.triangle_height + self.x, self.side//2 + self.y)))
        pygame.draw.polygon(win, self.rcolor, ((
            self.x2, self.y), (self.x2, self.side + self.y), (self.triangle_height + self.x2, self.side//2 + self.y)))
        win.blit(self.text_obj, (self.x + self.side + (self.x2 -
                 self.x - self.side - self.font.size(self.text)[0])//2, self.y))
        win.blit(self.label_text_obj, (self.x + self.side + 12,
                 self.y - self.label_font.size(self.label_text)[1]))
