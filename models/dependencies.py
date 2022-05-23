import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import InputLayer, Input, TimeDistributed, ConvLSTM2D, BatchNormalization, Flatten, Dense, Dropout, GlobalAveragePooling2D, Lambda, Conv3D, MaxPooling3D, Conv2D, Reshape, Bidirectional

SEGMENT_LENGTH = 100