# README


## Overview

This is the instruction of how to run the program on your own machine, including the preliminary of run the program, the file structure and the detailed steps for run it.

## Preliminary 

1. The program is written by Python3.6.1, Please make sure you have install Python3.6.1 on your machine before run it.

2. As this game should connect to your own smartphone to the computer, please make sure your computer can access your smartphone before run it, you can see this for details -- [Android 和 iOS 操作步骤](https://github.com/wangshub/wechat_jump_game/wiki/Android-%E5%92%8C-iOS-%E6%93%8D%E4%BD%9C%E6%AD%A5%E9%AA%A4).

3. (Optional) the train process was supported by TensorFlow, please make sure you have install TensorFlow on your own machine (GPU version highly recommend, best with version 1.4.0, as all my program were tested on this version), you can use the pre-trained model directly here), for the detailed training steps and dataset, please refer [tensorflow model](https://github.com/tensorflow/models/tree/master/research/object_detection).


## File Structure

The file structure as follow:

	-- ColorDetection.py (the RGB color detection version of this game.)
	-- Object_Detection
		-- Object_Detection.py (the object detection version of this game, based on TensorFlow)
		-- model (the model folders, contain the pre-trained model)
		-- utils (contains the deeplearing util tools which is used on main program)
		-- config (contains the object detection configuration file of TensorFlow)

## Step

If you have set up the environment which is mentioned on Preliminary, please just click your phone to the WeChat jump game user interface, for the color detection version, run:

	python ColorDetection.py

if everything is ok, your chess will jump automatically and your terminal will output the detailed information (the position of chess and board, press time, etc), and you can get the marked screenshot in the current folder.

For the object detection version, run:

	python Object_Detection.py

if everything is ok, your chess will jump automatically and your terminal will output the detailed information (the class of next board, press tiomemetc), and you can get the classification results screenshot in the current folder.


