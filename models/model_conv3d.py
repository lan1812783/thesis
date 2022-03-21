"""# **Import dependencies**"""

# import numpy as np
# import cv2
# import tensorflow as tf
# from tensorflow import keras
from tensorflow.keras import Sequential
# from tensorflow.keras.layers import InputLayer, Input, TimeDistributed
# from tensorflow.keras.layers import ConvLSTM2D, BatchNormalization, Flatten, Dense, Dropout, GlobalAveragePooling2D, Lambda, Conv3D, MaxPooling3D
# from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy, CategoricalCrossentropy, SparseCategoricalCrossentropy
from tensorflow.keras.metrics import Precision, Recall

from .defines import CONFIG_DICT
from .utilities import BackboneHandler, AccidentDetector
# from visualize import *

def get_file_weights_name(backbone_name):
  return "models/model_weights/" + backbone_name + '_weight.h5'

def construct_model(backbone_name="mobilenet"):
  """
  # **
    Return a tuple of:
      + Constructed model with the specific backbone
      + Model's input size
      + Backbone prepocess function
    **
  """

  if backbone_name not in CONFIG_DICT["backbones"]:
    raise AssertionError("No backbone found!")

  BACKBONE_NAME = backbone_name
  handler = BackboneHandler(BACKBONE_NAME)
  backbone = handler.get_model()
  # backbone.summary()
  model = AccidentDetector(backbone)
  model.build((None, None, *handler.get_backbone_input_shape()))
  model.summary()
  # model.compile(optimizer=Adam(0.0001), loss=BinaryCrossentropy(), metrics=['accuracy', Precision(), Recall()])

  model.load_weights(get_file_weights_name(BACKBONE_NAME))

  return model, handler.get_backbone_input_size(), handler.prepare_frames
