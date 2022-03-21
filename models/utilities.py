# from dependencies import *

import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.layers import InputLayer, Input, TimeDistributed, ConvLSTM2D, BatchNormalization, Flatten, Dense, Dropout, GlobalAveragePooling2D, Lambda, Conv3D, MaxPooling3D


from .defines import *
from .utilities import *

class BackboneHandler:
  def __init__(self, backbone_key, **kwargs):
    super().__init__(**kwargs)
  
    backbone_dict = CONFIG_DICT["backbones"][backbone_key]

    self.__name = backbone_dict["name"]
    self.__input_size = backbone_dict["input_size"]
    self.__preprocess_fn, self.__load_fn = backbone_dict["wrapper"](self.get_backbone_input_shape())
    self.__model = self.__load_fn()
    self.__model.trainable = False

  def get_model(self):
    return self.__model

  def get_backbone_input_size(self):
    return self.__input_size

  def get_backbone_input_shape(self):
    # TODO: remove hardcoded number of channels
    return (*self.__input_size, 3)

  def prepare_frames(self, frame_list):
    return self.__preprocess_fn(frame_list)

class TemporalFeatureExtractor(keras.layers.Layer):
  def __init__(self, filters_1=128, kernel_size_1=(3, 3),
                filters_2=64, kernel_size_2=(3, 3), **kwargs):
    super().__init__(**kwargs)

    self.lstm_layer1 = Conv3D(
                              filters=filters_1, 
                              kernel_size=(3, *kernel_size_1),
                              padding='same',
                              activation='relu'
    )
    self.lstm_layer2 = Conv3D(          
                              filters=filters_2, 
                              kernel_size=(3, *kernel_size_2),
                              padding='same',
                              activation='relu'
    )
    self.bn_layer_1 = BatchNormalization()
    self.bn_layer_2 = BatchNormalization()
    self.temporal_max_pool = keras.layers.Lambda(
            lambda X: tf.reduce_max(X, axis=1))

  def call(self, inputs):
    lstm1 = self.lstm_layer1(inputs)
    bn1 = self.bn_layer_1(lstm1)
    lstm2 = self.lstm_layer2(bn1)
    bn2 = self.bn_layer_2(lstm2)
    tmp3d = self.temporal_max_pool(bn2)

    return tmp3d
    
class DecisionMaker(keras.layers.Layer):
  def __init__(self, units_1=400, activation_1="tanh", 
              units_2=100, activation_2="tanh",
              units_3=1, activation_3="sigmoid", 
              dropout_rate_1=0.3, dropout_rate_2=0.3, **kwargs):
    super().__init__(**kwargs)
    self.fc1 = Dense(units=units_1, activation=activation_1)
    self.fc2 = Dense(units=units_2, activation=activation_2)
    self.fc3 = Dense(units=units_3, activation=activation_3)
    self.drop1 = Dropout(rate=dropout_rate_1)
    self.drop2 = Dropout(rate=dropout_rate_2)
    self.flatten = Flatten()

  def call(self, inputs):
    l1 = self.flatten(inputs)
    l2 = self.fc1(l1)
    l3 = self.drop1(l2)
    l4 = self.fc2(l3)
    l5 = self.drop2(l4)
    l6 = self.fc3(l5)
    return l6

class AccidentDetector(keras.Model):
  def __init__(self, backbone, **kwargs):
    super().__init__(**kwargs)
    
    self.backbone = backbone
    self.temporal_feature_extractor = TemporalFeatureExtractor()
    self.decision_maker = DecisionMaker()
  
  def call(self, inputs):
    spatial_extractor = TimeDistributed(self.backbone)(inputs)
    temporal_extractor = self.temporal_feature_extractor(spatial_extractor)
    decision = self.decision_maker(temporal_extractor)
    return decision
