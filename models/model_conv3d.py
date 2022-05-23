"""# **Import dependencies**"""

from .defines import CONFIG_DICT
from .utilities import BackboneHandler, AccidentDetector
from .cbam import AccidentDetector as CBAMAccidentDetector
from .cbam import VisualAttentionModule
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy, CategoricalCrossentropy, SparseCategoricalCrossentropy
from tensorflow.keras.metrics import Precision, Recall
from tensorflow import keras

def get_file_weights_name(backbone_name, temporal_model):
  return "models/model_weights/" + backbone_name + "_" + temporal_model + '_weight.h5'

def construct_model(backbone_name="mobilenet", temporal_model="conv3d"):
  """
  # **
    Return a tuple of:
      + Constructed model with the specific backbone
      + Model's input size
      + Backbone prepocess function
    **
  """
  print(backbone_name)
    
  BACKBONE_NAME = backbone_name
  
  if backbone_name in ["cbam", "se"]:
    handler = BackboneHandler("resnet152v2")
    backbone = VisualAttentionModule(backbone_name)
    # backbone.call(keras.layers.Input(shape=(224, 224, 3)))
    backbone.build((None, *handler.get_backbone_input_shape()))
    model = CBAMAccidentDetector(backbone)
    model.call(keras.layers.Input(shape=(None, 224, 224, 3)))
  else:
    if backbone_name not in CONFIG_DICT["backbones"]:
      raise AssertionError("No backbone found!")
    handler = BackboneHandler(BACKBONE_NAME)
    backbone = handler.get_model()
    model = AccidentDetector(backbone, temporal_model)
  model.build((None, None, *handler.get_backbone_input_shape()))
  model.summary()

  model.load_weights(get_file_weights_name(BACKBONE_NAME, temporal_model))

  return model, backbone, handler.get_backbone_input_size(), handler.prepare_frames
