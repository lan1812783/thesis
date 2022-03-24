
# from dependencies import *

from tensorflow.keras.models import Model
from tensorflow.keras.layers import InputLayer, Input, TimeDistributed, ConvLSTM2D, BatchNormalization, Flatten, Dense, Dropout, GlobalAveragePooling2D, Lambda, Conv3D, MaxPooling3D
from tensorflow.keras.applications import inception_v3
from tensorflow.keras.applications import mobilenet
from tensorflow.keras.applications import vgg16
from tensorflow.keras.applications import resnet_v2
from tensorflow.keras.applications import densenet
from tensorflow.keras.applications import xception

"""# **Constants and utility functions**"""

class LayerWrapper:
  @staticmethod
  def flatten():
    def wrapper():
      return Flatten()
    return wrapper


  @staticmethod
  def global_average_pooling():
    def wrapper():
      return GlobalAveragePooling2D()
    return wrapper


  @staticmethod
  def dropout(dropout_rate=0.5):
    def wrapper():
      return Dropout(dropout_rate)
    return wrapper


  @staticmethod
  def dense(units=1, activation='sigmoid'):
    def wrapper():
      return Dense(units=units, activation=activation)
    return wrapper


class BackboneWrapper:
  @staticmethod
  def inceptionV3_wrapper(input_shape, include_top=False, weights='imagenet'):
    def inceptionV3():
      return inception_v3.InceptionV3(input_shape=input_shape, include_top=include_top, weights=weights)
    return inception_v3.preprocess_input, inceptionV3


  @staticmethod
  def mobilenet_wrapper(input_shape, include_top=False, weights='imagenet'):
    def mobile_net():
      return mobilenet.MobileNet(input_shape=input_shape, include_top=include_top, weights=weights)
    return mobilenet.preprocess_input, mobile_net
  

  @staticmethod
  def vgg16_wrapper(input_shape, include_top=False, weights='imagenet'):
    def vgg_16():
      return vgg16.VGG16(input_shape=input_shape, include_top=include_top, weights=weights)
    return vgg16.preprocess_input, vgg_16


  @staticmethod
  def resnet152v2_wrapper(input_shape, include_top=False, weights='imagenet'):
    def res_net_v2():
      return resnet_v2.ResNet101V2(input_shape=input_shape, include_top=False, weights='imagenet')
    return resnet_v2.preprocess_input, res_net_v2
  
  
  @staticmethod
  def densenet121_wrapper(input_shape, include_top=False, weights='imagenet'):
    def dense_net():
      return densenet.DenseNet121(input_shape=input_shape, include_top=False, weights='imagenet')
    return densenet.preprocess_input, dense_net

  @staticmethod
  def xception_wrapper(input_shape, include_top=False, weights='imagenet'):
    def x_ception():
      return xception.Xception(input_shape=input_shape, include_top=include_top, weights=weights)
    return xception.preprocess_input, x_ception

CONFIG_DICT = {
  "backbones": {
    "additional_layers": [LayerWrapper.flatten(), LayerWrapper.dense(4, 'softmax')], # 1, sigmoid
    "last_layer_trainable_count": 5,
    "inception": {
      "name": "inception",
      "input_size": (256, 256),
      "wrapper": BackboneWrapper.inceptionV3_wrapper
    },
    "mobilenet": {
      "name": "mobilenet",
      "input_size": (224, 224),
      "wrapper": BackboneWrapper.mobilenet_wrapper
    },
    "vgg16": {
      "name": "vgg16",
      "input_size": (224, 224),
      "wrapper": BackboneWrapper.vgg16_wrapper
    },
    "resnet152v2": {
      "name": "resnet152v2",
      "input_size": (224, 224),
      "wrapper": BackboneWrapper.resnet152v2_wrapper
    },
    "densenet121": {
      "name": "densenet121",
      "input_size": (224, 224),
      "wrapper": BackboneWrapper.densenet121_wrapper
    },
    "xception": {
      "name": "xception",
      "input_size": (299, 299),
      "wrapper": BackboneWrapper.xception_wrapper
    }
  }
}
