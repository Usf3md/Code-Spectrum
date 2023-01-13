# BREAKER TOKEN
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW
import pygame
import os
import time

with open(r"Assets\Data\user_data.txt", "r") as file:
    TIME_DELAY = float(list(map(lambda x: x.split(": ")[1], file.read().split("\n")))[0])


class Scraper():
    def __init__(self, win, folder_name, color, padding, dark_theme, background, language, data, show_browser, file_prefix, font, text_padding):
        initial_text = f"searching for files..."
        intital_obj = font.render(initial_text, True, (255, 255, 255))
        initial_size = font.size(initial_text)
        win.blit(intital_obj, (text_padding, text_padding))
        pygame.display.update()
        win.fill((19, 19, 19), (text_padding, text_padding,
                 initial_size[0], initial_size[1]))

        self.folder_name = folder_name
        self.color = int(color) - 1
        self.padding = int(padding) - 1
        self.dark_theme = int(dark_theme)
        self.background = int(background) - 1
        self.language = language
        self.data = data
        self.show_browser = show_browser
        self.file_prefix = file_prefix
        self.font = font
        self.status = "idle"
        self.downloaded = 0
        self.total_files = 0
        self.text_padding = text_padding
        try:
            os.makedirs(folder_name)
        except FileExistsError:
            pass

        self.prefs = {"download.default_directory": (
            os.getcwd() + r"\\" + self.folder_name).replace(r"\\", "\\")}

        service = Service(r"CHOOSE_DRIVER\chromedriver.exe")
        service.creationflags = CREATE_NO_WINDOW

        self.options = ChromeOptions()
        self.options.headless = not self.show_browser
        self.options.add_experimental_option("prefs", self.prefs)
        self.driver = webdriver.Chrome(options=self.options, service=service)
        self.driver.get("https://ray.so/")
        ActionChains(self.driver).send_keys(
            f"{self.color*'c'}{self.padding*'p'}{self.dark_theme*'d'}{self.background*'b'}l{language.lower()}").perform()
        self.driver.find_element_by_xpath(
            '//*[@id="app"]/main/section/div[5]/div/div/div/div[2]/div[2]').click()

    def get_suffix_files(self, dir_name="."):
        list_of_file = os.listdir(dir_name)
        all_files = []
        for entry in list_of_file:
            pygame.event.pump()
            full_path = os.path.join(dir_name, entry)
            if os.path.isdir(full_path):
                all_files = all_files + self.get_suffix_files(full_path)
            elif os.path.splitext(os.path.basename(full_path))[1][1:] in self.data[self.language]:
                all_files.append(
                    (full_path, os.path.splitext(os.path.basename(full_path))[0]))
        return all_files

    def display_text(self, win):
        pygame.event.pump()
        if self.total_files:
            prefix_text = f"prefix: {self.file_prefix}"
            prefix = self.font.render(prefix_text, True, (255, 255, 255))
            prefix_size = self.font.size(prefix_text)
            win.blit(prefix, (self.text_padding, self.text_padding))

            status_text = f"status: {self.status}"
            status = self.font.render(status_text, True, (255, 255, 255))
            status_size = self.font.size(status_text)
            win.blit(status, (self.text_padding,
                              prefix_size[1] + self.text_padding))

            files_text = f"{self.total_files} files found"
            files_obj = self.font.render(files_text, True, (255, 255, 255))
            files_size = self.font.size(files_text)
            win.blit(
                files_obj, (self.text_padding, prefix_size[1] + status_size[1] + self.text_padding))

            downloaded_text = f"{self.downloaded} {self.language} files downloaded out of {self.total_files}"
            downloaded_obj = self.font.render(
                downloaded_text, True, (255, 255, 255))
            downloaded_size = self.font.size(downloaded_text)
            win.blit(
                downloaded_obj, (self.text_padding, prefix_size[1] + status_size[1] + files_size[1] + self.text_padding))
        else:
            no_files_text = f"No {self.language} files found!"
            no_files = self.font.render(no_files_text, True, (255, 255, 255))
            no_files_size = self.font.size(no_files_text)
            win.blit(no_files, (self.text_padding, self.text_padding))

        pygame.display.update()
        if self.total_files:
            win.fill((19, 19, 19), (self.text_padding, self.text_padding,
                                    prefix_size[0], prefix_size[1]))
            win.fill((19, 19, 19),
                     (self.text_padding, prefix_size[1] + self.text_padding, status_size[0], status_size[1]))
            win.fill((19, 19, 19),
                     (self.text_padding,  prefix_size[1] + status_size[1] + self.text_padding, files_size[0], files_size[1]))
            win.fill((19, 19, 19),
                     (self.text_padding,  prefix_size[1] + status_size[1] + files_size[1] + self.text_padding, downloaded_size[0], downloaded_size[1]))
        else:
            win.fill((19, 19, 19), (self.text_padding, self.text_padding,
                                    no_files_size[0], no_files_size[1]))

    def create_images(self, win, files):
        self.status = "creating images"
        self.total_files = len(files)
        self.display_text(win)
        for file_path, file_name in files:
            self.display_text(win)
            with open(file_path, "r") as file:
                code = file.read().strip("\n").split("\n")
                if "# BREAKER TOKEN" in code:
                    self.total_files -= 1
                    continue
            self.driver.find_element_by_class_name("title").click()
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).key_down(Keys.BACKSPACE).key_up(
                Keys.BACKSPACE).send_keys(f"{self.file_prefix} {file_name}").key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
            time.sleep(TIME_DELAY)
            self.driver.find_element_by_class_name("CodeMirror-code").click()
            time.sleep(TIME_DELAY)
            ActionChains(self.driver).key_down(Keys.CONTROL).send_keys("a").key_up(
                Keys.CONTROL).key_down(Keys.BACKSPACE).key_up(Keys.BACKSPACE).perform()
            self.display_text(win)
            for i, line in enumerate(code):
                if not i:
                    ActionChains(self.driver).key_down(Keys.LEFT_SHIFT).key_down(Keys.HOME).key_up(
                        Keys.LEFT_SHIFT).key_up(Keys.HOME).send_keys(line).perform()
                else:
                    ActionChains(self.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).key_down(Keys.LEFT_SHIFT).key_down(
                        Keys.HOME).key_up(Keys.LEFT_SHIFT).key_up(Keys.HOME).send_keys(line).perform()
                pygame.event.pump()
            self.driver.find_element_by_xpath(
                '//*[@id="app"]/main/section/div[6]/div/button').click()
            time.sleep(TIME_DELAY)
            self.downloaded += 1
            self.display_text(win)
        else:
            while True:
                images = list(map(lambda x: os.path.splitext(
                    os.path.basename(x))[0], os.listdir(self.folder_name)))
                for p, n in files:
                    if f"{self.file_prefix} {n}" not in images:
                        print(n)
                        break
                else:
                    print("done")
                    break
        self.driver.quit()
        self.status = "done!"
        self.display_text(win)
