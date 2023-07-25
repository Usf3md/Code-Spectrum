# BREAKER TOKEN
try:
    import pygame
    from scraper import Scraper
    from utils import *
    from data import *

    def app():
        width = 1024
        height = 512
        fps = 60

        pygame.init()
        win = pygame.display.set_mode((width, height))
        font_path = r"Assets\Fonts\LEMONMILK-Bold.otf"
        images_path = r"Assets\Images"
        icon_path = r"Assets\Icons\icon.jpg"
        pygame.display.set_icon(pygame.image.load(icon_path))
        pygame.display.set_caption("Code Spectrum")
        clock = pygame.time.Clock()
        font = pygame.font.Font(font_path, 18)
        label_font = pygame.font.Font(font_path, 10)
        label_font_big = pygame.font.Font(font_path, 15)
        pad_font = pygame.font.Font(font_path, 11)
        image_name = ["1", "1", "1", "1"]
        language = list(LANGUAGES)[0]
        image = Image(f"{images_path}\\{''.join(image_name)}.png")
        border_rect_width, border_rect_height = 550, 155
        padding = (width - image.image_width - border_rect_width)//2
        inner_padding = padding // 4
        border_rectangle = Rectangle(padding, height - border_rect_height - padding,
                                     border_rect_width, border_rect_height, (44, 44, 44))
        canvas_rectangle = Rectangle(border_rectangle.x + inner_padding, border_rectangle.y + inner_padding,
                                     border_rect_width - 2*inner_padding, border_rect_height - 2*inner_padding, (25, 25, 25))
        maximum_language = max(LANGUAGES, key=lambda x: len(x))
        maximum_color = max(COLORS, key=lambda x: len(x))
        language_select = Triangle(canvas_rectangle.x + 20, canvas_rectangle.y + 20, 30,
                                   (185, 49, 167), font, label_font, maximum_language, (255, 255, 255), list(LANGUAGES), "language:", (60, 244, 192), (244, 134, 229))

        color_select = Triangle(language_select.x2 + language_select.triangle_height + 30, canvas_rectangle.y + 20, 30,
                                (185, 49, 167), font, label_font, maximum_color, (255, 255, 255), list(COLORS), "colors:", (60, 244, 192),  (244, 134, 229))

        current_color = list(COLORS)[0]
        padding_16 = Checkbox(language_select.x + 10 + language_select.side,
                              language_select.y + 95 - 8, 20, 20, COLORS[current_color][1][0], selected_color=COLORS[current_color][1][1], hover_color=COLORS[current_color][1][2], label_font=label_font, label_text="padding:", label_color=COLORS[current_color][2][0], font=pad_font, text="16")
        paddings = [padding_16]
        pad_vals = ["16", "32", "64", "128"]
        for i in range(1, 4):
            paddings.append(Checkbox(padding_16.x + (padding_16.rect_width+4)*i, padding_16.y, padding_16.rect_width,
                                     padding_16.rect_height, padding_16.color, selected_color=padding_16.selected_color, hover_color=padding_16.hover_color, font=pad_font, text=pad_vals[i]))
        paddings[2].checked = True
        paddings[2].correct_arrangment = False
        paddings[2].color, paddings[2].selected_color = paddings[2].selected_color, paddings[2].color

        dark_mode = RadioCheckbox(color_select.x + 10 + language_select.side,
                                  paddings[-1].y - 4 - 24 - 6, 24, 24, COLORS[current_color][1][0], selected_color=COLORS[current_color][1][1], hover_color=COLORS[current_color][1][2], label_font=label_font_big, label_text="dark mode", label_color=COLORS[current_color][2][0], checked=True)
        background = RadioCheckbox(color_select.x + 10 + language_select.side,
                                   paddings[-1].y - 4, 24, 24, COLORS[current_color][1][0], selected_color=COLORS[current_color][1][1], hover_color=COLORS[current_color][1][2], label_font=label_font_big, label_text="background", label_color=COLORS[current_color][2][0], checked=True)

        button = Button(color_select.x + 210,
                        color_select.y, 104, 104, COLORS[current_color][2][1], hover_color=COLORS[current_color][2][2], font=font, text="export")

        run = True
        while run:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            image.image_load(f"{images_path}\\{''.join(image_name)}.png")
            language = language_select.event_check(event)
            color, color_index = color_select.event_check(event)
            back_check = background.event_check(event)
            dark_check = dark_mode.event_check(event)
            button_check = button.event_check(event)
            for main_pad in paddings:
                if main_pad.event_check(event):
                    for pad in paddings:
                        if pad is main_pad:
                            image_name[1] = str(
                                (paddings.index(pad) + 2) % 4 + 1)
                            continue
                        pad.checked = False
                        if not pad.correct_arrangment:
                            pad.color, pad.selected_color = pad.selected_color, pad.color
                            pad.correct_arrangment = True
                    break

                image_name[2] = str(2 - (dark_check * 1))
                image_name[3] = str(2 - (back_check * 1))
            if color != current_color:
                color_vals = COLORS[color]
                for i in [language_select, color_select]:
                    i.lcolor = color_vals[0][0]
                    i.rcolor = color_vals[0][0]
                    i.lhover_color = color_vals[0][1]
                    i.rhover_color = color_vals[0][1]
                    i.correct_arrangment = [True, True]
                    i.label_text_obj = label_font.render(
                        i.label_text, True, color_vals[2][0])

                for i in [paddings[0], dark_mode, background]:
                    i.label_text_obj = i.label_font.render(
                        i.label_text, True, color_vals[2][0])

                for i in paddings:
                    i.color = color_vals[1][0]
                    i.selected_color = color_vals[1][1]
                    i.hover_color = color_vals[1][2]
                    if not i.correct_arrangment:
                        i.color, i.selected_color = i.selected_color, i.color

                for i in [dark_mode, background]:
                    i.color = color_vals[1][0]
                    i.selected_color = color_vals[1][1]
                    i.hover_color = color_vals[1][2]
                    if i.checked:
                        i.color, i.selected_color = i.selected_color, i.color

                button.color = color_vals[2][1]
                button.hover_color = color_vals[2][2]
                current_color = color

            if button_check:
                for i in [image, border_rectangle, canvas_rectangle, language_select, color_select, background, dark_mode, button] + paddings:
                    i.draw(win)
                scraper = Scraper(win, "CODE_IMAGES", image_name[0], image_name[1],
                                  image_name[2], image_name[3], language[0], LANGUAGES, False, "Problem", font, padding)
                scraper.create_images(
                    win, scraper.get_suffix_files("YOUR_CODE_HERE"))

            for i in [image, border_rectangle, canvas_rectangle, language_select, color_select, background, dark_mode, button] + paddings:
                i.draw(win)

            image_name[0] = str(color_index)
            pygame.display.update()
            win.fill((19, 19, 19))

        pygame.quit()

    if __name__ == "__main__":
        app()
except Exception as e:
    with open("ERROR_LOGGER.txt", "w") as file:
        print(repr(e), file=file)
