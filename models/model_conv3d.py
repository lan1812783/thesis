"""# **Import dependencies**"""

from .defines import CONFIG_DICT
from .utilities import BackboneHandler, AccidentDetector

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

  return model, backbone, handler.get_backbone_input_size(), handler.prepare_frames
