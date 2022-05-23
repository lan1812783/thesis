class TemporalFeatureExtractor(keras.layers.Layer):
  def __init__(self, filters_1=64, kernel_size_1=(3, 3), 
                dropout_1=0.2, recurrent_dropout_1=0.1,
                filters_2=64, kernel_size_2=(3, 3), 
                dropout_2=0.2, recurrent_dropout_2=0.1, **kwargs):
    super().__init__(**kwargs)

    self.lstm_layer1 = ConvLSTM2D(
                                  filters=filters_1, 
                                  kernel_size=kernel_size_1, 
                                  dropout=dropout_1, 
                                  recurrent_dropout=recurrent_dropout_1, 
                                  return_sequences=True
    )
    self.lstm_layer2 = ConvLSTM2D(          
                                  filters=filters_2, 
                                  kernel_size=kernel_size_2, 
                                  dropout=dropout_2, 
                                  recurrent_dropout=recurrent_dropout_2, 
                                  return_sequences=False
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

class TemporalFeatureExtractor(keras.layers.Layer):
  def __init__(self, filters_1=64, kernel_size_1=(3, 3), 
                dropout_1=0.2, recurrent_dropout_1=0.1,
                filters_2=64, kernel_size_2=(3, 3), 
                dropout_2=0.2, recurrent_dropout_2=0.1, **kwargs):
    super().__init__(**kwargs)

    self.lstm_layer1 = Bidirectional(ConvLSTM2D(
                                  filters=filters_1, 
                                  kernel_size=kernel_size_1, 
                                  dropout=dropout_1, 
                                  recurrent_dropout=recurrent_dropout_1, 
                                  return_sequences=True
    ))
    self.lstm_layer2 = Bidirectional(ConvLSTM2D(          
                                  filters=filters_2, 
                                  kernel_size=kernel_size_2, 
                                  dropout=dropout_2, 
                                  recurrent_dropout=recurrent_dropout_2, 
                                  return_sequences=False
    ))
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