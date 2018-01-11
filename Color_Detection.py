#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Desc: the RGB color detetction version of the WeChat jump game, the test device is iPhone6/iPhone6s,
if your device is not that, please tune parameters by yourself. here for more details:
https://github.com/wangshub/wechat_jump_game/wiki/Android-%E5%92%8C-iOS-%E6%93%8D%E4%BD%9C%E6%AD%A5%E9%AA%A4
'''

import os
import shutil
import math
import wda
import time
from PIL import Image, ImageDraw
import random

# some predefined parameters
chess_tune = 13       # chess parameter tune
chess_width = 49      # the width of the chess
distance_time = 0.002 # the mapping from distance to press time

client = wda.Client()
session = client.session()

def get_screenshot():
    client.screenshot('screenshot.png')

# get the position via the different of RGB channel
def get_position(screenshot):
    w, h = screenshot.size # get the screensize
    chess_y = 0
    board_x = 0
    board_y = 0
    scan_width_border = int(w / 8)  # size filter, as it's not necessary for the whole screen
    scan_height_begin = 150  # the begin of height

    # load all the RGB channel
    screen_pixel = screenshot.load()
    
    chess_x_suit_sum = 0
    chess_x_suit_count = 0
    # scan region
    for i in range(scan_height_begin, int(h * 2 / 3)): # height region
        for j in range(scan_width_border, w - scan_width_border): # width region
            pixel = screen_pixel[j, i]
            # get the chess region, average for the chess position
            if (50 < pixel[0] < 60) and (53 < pixel[1] < 63) and (95 < pixel[2] < 110):
                chess_x_suit_sum += j
                chess_x_suit_count += 1
                chess_y = max(i, chess_y)

    # if not get any point
    if not all((chess_x_suit_sum, chess_x_suit_count)):
        return 0, 0, 0, 0

    chess_x = chess_x_suit_sum / chess_x_suit_count
    # adjustment
    chess_y = chess_y - chess_tune

    # get the board position
    for i in range (int (h / 3), int (h * 2 / 3)):
        last_pixel = screen_pixel[0, i]

        # judge get the value, break
        if board_x or board_y:
            break
        board_x_sum = 0
        board_x_count = 0

        for j in range(w):
            pixel = screen_pixel[j, i]

            # a special case, the y position of chess is higher than board
            if abs(j - chess_x) < chess_width:
                continue

            # get those different x position
            if abs(pixel[0] - last_pixel[0]) + abs(pixel[1] - last_pixel[1]) + abs(pixel[2] - last_pixel[2]) > 10:
                board_x_sum += j
                board_x_count += 1

        if board_x_sum:
            board_x = board_x_sum / board_x_count

    # calcuate the y position of the next board
    board_y = chess_y - abs(board_x - chess_x) * math.sqrt(3) / 3

    if not all((board_x, board_y)):
        return 0, 0, 0, 0

    return chess_x, chess_y, board_x, board_y

def jump(jump_count, distance):
    press_time = distance * distance_time
    print('Press Time: {}'.format(press_time) + 's')
    print('Jump Count: {}'.format(jump_count))
    session.tap_hold(200, 200, press_time)

screenshot_backup_dir = 'screenshot/'
if os.path.isdir(screenshot_backup_dir):
    shutil.rmtree(screenshot_backup_dir) 
if not os.path.isdir(screenshot_backup_dir):
    os.mkdir(screenshot_backup_dir)

def save_marked_creenshot(jump_count, image, chess_x, chess_y, board_x, board_y):
    draw = ImageDraw.Draw(image)
    # mark the positon for debug
    draw.line((chess_x, chess_y) + (board_x, board_y), fill=2, width=3)
    draw.line((chess_x, 0, chess_x, image.size[1]), fill=(255, 0, 255))
    draw.line((0, chess_y, image.size[0], chess_y), fill=(255, 0, 255))

    draw.line((board_x, 0, board_x, image.size[1]), fill=(0, 0, 255))
    draw.line((0, board_y, image.size[0], board_y), fill=(0, 0, 255))
    
    draw.ellipse((chess_x - 10, chess_y - 10, chess_x + 10, chess_y + 10), fill=(255, 0, 255))
    draw.ellipse((board_x - 10, board_y - 10, board_x + 10, board_y + 10), fill=(0, 0, 255))
    del draw
    # image.save('{}{}.png'.format(screenshot_backup_dir, jump_count))

def main():
    jump_count = 395
    while True:
        # get the current screenshot
        get_screenshot()
        screenshot = Image.open("./screenshot.png")

        # get the position of the chess and board
        chess_x, chess_y, board_x, board_y = get_position(screenshot)

        print('Chess Position: < {}, {}>'.format(chess_x, chess_y))
        print('Board Position: < {}, {}>'.format(board_x, board_y))

        # not detected, game over 
        if chess_x == 0:
            return

        # caculate the distance and jump
        distance = math.sqrt((board_x - chess_x) ** 2 + (board_y - chess_y) ** 2)
        jump_count += 1
        jump(jump_count, distance)

        # save the position screenshot for debug
        # save_marked_creenshot(jump_count, screenshot, chess_x, chess_y, board_x, board_y)

        screenshot.save('{}{}.png'.format(screenshot_backup_dir, jump_count))
        # take a break, make sure the chess is safety
        time.sleep(random.uniform(1, 1.1))

if __name__ == '__main__':
    main()
