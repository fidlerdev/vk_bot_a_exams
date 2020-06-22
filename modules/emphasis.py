# -*- coding: utf-8 -*-

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO

from typing import Tuple, Dict, Optional


class WordImage:

    LOWER_RANGE = range(1072, 1104)
    UPPER_RANGE = range(1040, 1072)
    K = 1.7


    def __init__(self, img: str, font: str, text: str, fill_normal: Tuple, vowels: Dict, index: Optional):
        self.bg = Image.open(img)

        self.IMAGE_W = self.bg.size[0]
        self.IMAGE_H = self.bg.size[1]
        self.text = text
        self.vowels = vowels

        self.font = ImageFont.truetype(font=font, size=self.get_font_size(text))

        self.fill_normal = fill_normal

        self.font_wh = self.font.getsize(text)

        self.draw = ImageDraw.Draw(self.bg)

        self.draw_text()

        if index:
            import os
            self.bg.save('../res/emphasises/img_{}.png'.format(index))

    @staticmethod
    def return_image(img):
        temp = BytesIO()
        img.bg.save(temp, format='png')
        return temp

    def draw_text(self):

        text = self.text

        for ind, char in enumerate(self.text):
            if ord(char) in self.UPPER_RANGE:
                fill = char
                char_index = ind
                break

        try:
            text = text[:char_index] + self.vowels[fill.lower()] + text[char_index+1:]
        except UnboundLocalError:
            text = text.capitalize()

        self.draw.text(
            (self.IMAGE_W/2 - self.font_wh[0]/2, self.IMAGE_H/2 - self.font_wh[1]/2),
            text=text.capitalize(),
            fill=self.fill_normal,
            font=self.font
        )
        

    def get_font_size(self, text):
        char_count = len(text)
        width = self.IMAGE_W - 40
        return int(width / char_count * self.K)



if __name__ == '__main__':
    import json
    import random

    with open('../data/stress_vowels.json', 'r') as file:
        vowels = json.load(file)

    with open('../data/emphasises.json', 'r') as file:
        words = json.load(file)

    for index, word in enumerate(words):
        WordImage(
            img='../res/BG.png',
            font='../res/arial.ttf',
            text=word,
            fill_normal=(255, 255, 255),
            vowels=vowels,
            index=index
        )
    # while True:
    #     cmd = input()
    #     if cmd == '0':
    #         break
    #     elif cmd == '1':
    #         rand_int = random.randint(0, len(words)-1)
    #         word = words[rand_int]
    #         print(word)
    #         WordImage(
    #             img='../res/BG.png',
    #             font='../res/arial.ttf',
    #             text=word,
    #             fill_normal=(255, 255, 255),
    #             vowels=vowels
    #         )
        