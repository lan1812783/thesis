
from .dependencies import *

class CBAM(keras.layers.Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.depth_max_pool = keras.layers.Lambda(
            lambda X: tf.expand_dims(tf.reduce_max(X, axis=-1), -1))
        self.depth_avg_pool = keras.layers.Lambda(
            lambda X: tf.expand_dims(tf.reduce_mean(X, axis=-1), -1))
        self.concat = keras.layers.Lambda(
            lambda X: tf.concat([X[0], X[1]], axis=-1))
        self.conv_1 = Conv2D(filters=1, kernel_size=1)

    def call(self, inputs):
        filters = inputs.shape[-1]
        U_s = self.concat((self.depth_max_pool(inputs), self.depth_avg_pool(inputs)))
        V_s = tf.keras.activations.softmax(self.conv_1(U_s))
        outputs = tf.multiply(inputs, V_s)
        return outputs

class ResidualUnit(keras.layers.Layer):
    def __init__(self, filters, strides=1, is_first=False, activation="relu", **kwargs):
        super().__init__(**kwargs)
        self.activation = keras.activations.get(activation)
        self.main_layers = [
            Conv2D(filters=filters, strides=strides, kernel_size=1, padding="same"),
            keras.layers.BatchNormalization(),
            self.activation,
            Conv2D(filters=filters, kernel_size=3, padding="same"),
            keras.layers.BatchNormalization(),
            self.activation,
            Conv2D(filters=filters * 4, kernel_size=1, padding="same"),
            keras.layers.BatchNormalization(),
            CBAM(),
            keras.layers.BatchNormalization()]
        self.skip_layers = []
        if strides > 1 or is_first:
            self.skip_layers = [
                Conv2D(filters=filters * 4, kernel_size=1, strides=strides, padding="same"),
                keras.layers.BatchNormalization()]

    def call(self, inputs):
        Z = inputs
        for layer in self.main_layers:
            Z = layer(Z)
        skip_Z = inputs
        for layer in self.skip_layers:
            skip_Z = layer(skip_Z)
        return self.activation(Z + skip_Z)


        """
        RES1: input = (56, 56, 64), output = (56, 56, 256)
        RES2: input = (56, 56, 256), output = (56, 56, 256)
        RES3: input = (56, 56, 256), output = (56, 56, 256)
        RES4: input = (56, 56, 256), output = (28, 28, 512)
        """
class VisualAttentionModule(keras.layers.Layer):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.output_H = 224
    self.output_W = 224
    # , input_shape=(self.output_H, self.output_W, 3)
    self.conv_2d = Conv2D(64, kernel_size=7, strides=2, padding="same")
    self.batch_norm = keras.layers.BatchNormalization()
    self.activation = keras.layers.Activation("relu")
    self.max_pool_2d = keras.layers.MaxPool2D(pool_size=3, strides=2, padding="SAME")
    
    self.filter_list = [64] * 2 + [128] * 4 + [256] * 6 + [512] * 3
    
    self.res_unit_list = list()
    self.res_unit_list.append(ResidualUnit(self.filter_list[0], strides=1, is_first = True))
    prev_filters = self.filter_list[0]
    for filters in self.filter_list:
      strides = 1 if filters == prev_filters else 2
      self.res_unit_list.append(ResidualUnit(filters, strides=strides, is_first=False))
      prev_filters = filters 

    self.dimen_reduce = 64
    self.conv_2d_1 =  Conv2D(filters=self.dimen_reduce, kernel_size=1)

    self.output_H >>= 5
    self.output_W >>= 5    
    
    # self.output_H >>= 4
    # self.output_W >>= 4


  def call(self, inputs):
    # Z = inputs
    Z = self.conv_2d(inputs)
    Z = self.batch_norm(Z)
    Z = self.activation(Z)
    Z = self.max_pool_2d(Z)
    for res_unit in self.res_unit_list:
      Z = res_unit(Z)       
    Z = self.conv_2d_1(Z)
    return Z

  def compute_output_shape(self, batch_input_shape):
    return tf.TensorShape([None, self.output_H, self.output_W, self.dimen_reduce])

  def get_backbone_input_shape(self):
    return (224, 224, 3)

class TemporalFeatureExtractor(keras.layers.Layer):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    self.lstm_layer = ConvLSTM2D(
        filters=64, kernel_size=(3, 3),
        dropout=0.2,
        recurrent_dropout=0.1,
        return_sequences=False)
    self.bn_layer = BatchNormalization()

  def call(self, inputs):
    Z = inputs
    Z = self.lstm_layer(Z)
    Z = self.bn_layer(Z)

    return Z
    
class DecisionMaker(keras.layers.Layer):
  def __init__(self, units_1=400, activation_1="tanh", 
              units_2=100, activation_2="tanh",
              units_3=1, activation_3="sigmoid", 
              dropout_rate_1=0.3, dropout_rate_2=0.3, **kwargs):
    super().__init__(**kwargs)
    
    self.globle_pool = GlobalAveragePooling2D()
    self.flatten = Flatten()
    self.fc = Dense(units=1, activation='sigmoid')

  def call(self, inputs):
    Z = inputs
    Z = self.globle_pool(Z)
    Z = self.flatten(Z)
    Z = self.fc(Z)
    return Z

class AccidentDetector(keras.Model):
  def __init__(self, backbone, **kwargs):
    super().__init__(**kwargs)
    backbone.trainable = False

    self.visual_attention_module = keras.Sequential([backbone])
    self.temporal_feature_extractor = TemporalFeatureExtractor()
    self.decision_maker = DecisionMaker()
  
  def call(self, inputs):
    Z = inputs
    Z = TimeDistributed(self.visual_attention_module)(Z)
    Z = self.temporal_feature_extractor(Z)
    Z = self.decision_maker(Z)
    return Z