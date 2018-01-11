#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Desc: the Object Detetction version of the WeChat jump game, the test device is iPhone6/iPhone6s,
if your device is not that, please tune parameters by yourself. here for more details:
https://github.com/wangshub/wechat_jump_game/wiki/Android-%E5%92%8C-iOS-%E6%93%8D%E4%BD%9C%E6%AD%A5%E9%AA%A4
the program is tested on TensorFlow v1.4.0.
'''

import tensorflow as tf
import numpy as np
import time
import os
import wda
import cv2
from utils import label_map_util
from utils import visualization_utils as vis_util
import random
 
# model configuration
model_path = 'model/model.pb'
model_config = 'config/label_map.pbtxt'
class_num = 7

chess_x = 0
distance = 0

# load the model
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(model_path, 'rb') as fid:
        od_graph_def.ParseFromString(fid.read())
        tf.import_graph_def(od_graph_def, name='')

# load num of classes
label_map = label_map_util.load_labelmap(model_config)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=class_num, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

# open the session
client = wda.Client()
session = client.session()

def get_screenshot():
    client.screenshot('screenshot.png')

# read image data
def read_image(path):
    image_np = cv2.imread(path)
    image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    width = image_np.shape[1]
    height = image_np.shape[0]
    images = np.expand_dims(image_np, axis=0)
    return image_np, images, width, height

# get detection result
def get_positions(objects, classes, scores, category_index):
    chess_position = [1, 1, 1, 1]
    board_position = [1, 1, 1, 1]
    target_type = ''
    score_thresh = .5

# get the highest object as the next board
    for i in range(objects.shape[0]):
        if scores[i] > score_thresh:
            # the preset threshold
            if objects[i][0] < 0.3 or objects[i][2] > 0.8:
                continue
            if category_index[classes[i]]['name'] == 'chess':
                chess_position = objects[i]
            elif objects[i][0] < board_position[0]:
                board_position = objects[i]
                target_type = category_index[classes[i]]['name']

    return chess_position, board_position, target_type

def jump(jump_count, distance):
    press_time = max(int(distance * 1800), 200) * 0.001
    session.tap_hold(200, 200, press_time)
    print('Press Time: {}'.format(press_time) + 's')
    print('Jump Count: {}'.format(jump_count))

with detection_graph.as_default():
    with tf.Session(graph=detection_graph) as sess:

        # tensorflow predefined configuration
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        detection_objects = detection_graph.get_tensor_by_name('detection_boxes:0')
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        
        jump_count = 0
        while True:
            get_screenshot()
            image_np, images, width, height = read_image('screenshot.png')

            (objects, scores, classes, num) = sess.run(
                [detection_objects, detection_scores, detection_classes, num_detections], 
                feed_dict={image_tensor: images})

            objects = np.reshape(objects, (-1, objects.shape[-1]))
            scores = np.reshape(scores, (-1))
            classes = np.reshape(classes, (-1)).astype(np.int32)

            vis_util.visualize_objects_and_labels_on_image_array(image_np, objects, classes, scores, category_index, use_normalized_coordinates=True, line_thickness=10)
            
            # get detected image
            image = cv2.imwrite('detection.png', cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR))

            # get the positon of chess and board
            chess_position, board_position, target_type = get_positions(objects, classes, scores, category_index)
        
            chess_x = (chess_position[1] + chess_position[3]) / 2
            board_x = (board_position[1] + board_position[3]) / 2
            distance = np.abs(chess_x - board_x)

            print("Next Object:", target_type)
            jump_count += 1
            jump(jump_count, distance)

            # take a break, make sure the chess is safety
            time.sleep(random.uniform(1, 1.1))
