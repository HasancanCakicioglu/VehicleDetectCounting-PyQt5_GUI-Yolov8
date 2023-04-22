import os
import tensorflow as tf
import numpy as np
import cv2

from src.ai.plate_detection_controller import plateDetectionController


def initialize():
    plateDetectionController.initialize()
    plateDetectionController.getInstance("assets/model/plate_detection/saved_model")

