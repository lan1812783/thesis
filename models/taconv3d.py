from .dependencies import *

class TemporalFeatureExtractor(keras.layers.Layer):
  def __init__(self, filters_1=128, kernel_size_1=(3, 3),
                filters_2=128, kernel_size_2=(3, 3), **kwargs):
    super().__init__(**kwargs)

    self.frame_number = 100

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
    self.bn_layer_3 = BatchNormalization()
    self.temporal_max_pool = keras.layers.Lambda(
            lambda X: tf.reduce_max(X, axis=1))
    
  def call(self, inputs):        
    inputs = self.lstm_layer1(inputs)
    inputs = self.bn_layer_1(inputs)
    
    input_shape = inputs.shape[2:5]    
    print(input_shape)
    hwc = tf.math.reduce_prod(input_shape)   
    
    if not hasattr(self, 'reshape_query'):        
        self.reshape_query = Reshape((self.frame_number, inputs.shape[2] * inputs.shape[3] * inputs.shape[4]))        
    if not hasattr(self, 'reshape_key'):
        self.reshape_key = Reshape((inputs.shape[2] * inputs.shape[3] * inputs.shape[4], self.frame_number))
    if not hasattr(self, 'reshape_value'):
        self.reshape_value = Reshape((self.frame_number, inputs.shape[2] * inputs.shape[3] * inputs.shape[4]))
    if not hasattr(self, 'reshape_back'):
        self.reshape_back = Reshape((self.frame_number, inputs.shape[2], inputs.shape[3], inputs.shape[4]))
    
    mid_qk = self.lstm_layer2(inputs)
    mid_qk = self.bn_layer_2(mid_qk)    
    
    query = self.reshape_query(mid_qk)    
    key = self.reshape_key(mid_qk)    
 
    mul_matrix = tf.linalg.matmul(query, key) 
    sqrt_dq = tf.sqrt(tf.cast(query.shape[1], tf.float32))    
    mul_matrix = tf.divide(mul_matrix, sqrt_dq)
    attention_map = tf.nn.softmax(mul_matrix)      
    
    value = self.reshape_value(inputs)
    attention_map = tf.cast(attention_map, tf.float32)
    
    output = tf.linalg.matmul(attention_map, value)         
    output = self.reshape_back(output)
    output = self.bn_layer_3(output)
    tmp3d = self.temporal_max_pool(output)

    return tmp3d
    