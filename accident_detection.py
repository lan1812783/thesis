from models.dependencies import *
from models.model_conv3d import construct_model
from models.visualize import save_grad_cam

SEGMENT_LENGTH = 100

def load_video(video_file, start_timestamp = 0, end_timestamp = 0, frame_size = (224, 224), preprocess_func = (lambda x: x)):
    # Open the video file
    video = cv2.VideoCapture(video_file)

    # Get fps and number of frame information of the video
    fps = video.get(cv2.CAP_PROP_FPS)
    num_frame = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate starting and ending frame index
    # start_frame_index = int(start_timestamp * fps)
    end_frame_index = int(end_timestamp * fps)
    start_frame_index = end_frame_index - SEGMENT_LENGTH

    # The first argument of set() function, number 1 means that
    # second argument should be the starting frame index in integer
    video.set(1, start_frame_index)

    # Retrieve each frame from video segment
    frames = []                       # initialize frame list
    is_success, frame = video.read()  # begin by reading the first frame
    # frame_count = 0
    while is_success and start_frame_index < end_frame_index:
      frame_tensor = tf.convert_to_tensor(frame)                # convert frame from numpy -> tensor
      frame_tensor = tf.image.resize(frame_tensor, frame_size)  # resize the frame to 224x224
      frames.append(frame_tensor)                               # add to the frame list

      is_success, frame = video.read()                          # read next frame

      start_frame_index += 1                                    # next frame index

      # if frame_count == SEGMENT_LENGTH: break
      # frame_count += 1

    # Close the video file
    print(video_file + " ----- " + str(len(frames)))
    video.release()

    return preprocess_func(tf.convert_to_tensor(frames)) # return retrieved frame list after preprocessing

def process_video(video_name, start_timestamp=0, end_timestamp=3, input_size=(224, 224), preprocess_func=(lambda x: x)):
    loaded_data = tf.expand_dims(load_video(
                            video_name,
                            start_timestamp,
                            end_timestamp,
                            input_size,
                            preprocess_func), axis=0)

    return tf.convert_to_tensor(loaded_data)

def predict(video_name="", start_timestamp=0, end_timestamp=3, backbone_name="mobilenet", temporal_model="con3d"):
    model, backbone, input_size, preprocess_func = construct_model(backbone_name, temporal_model)

    processed_video = process_video(video_name, start_timestamp, end_timestamp, input_size, preprocess_func)
    prediction_result = model.predict(processed_video)
    # not good
    if backbone_name == "cbam":
        backbone = backbone.build_graph()
    grad_cam_result = save_grad_cam(backbone, processed_video[0])
    # return model.predict(processed_video), save_grad_cam(backbone, processed_video[0])
    return prediction_result, grad_cam_result

def get_prediction(video_name="videos/RoadAccidents002_x264.mp4", start_timestamp=0, end_timestamp=3, backbone_name="mobilenet", temporal_model="conv3d"):
    prediction, grad_cam_path = predict(video_name, start_timestamp, end_timestamp, backbone_name, temporal_model)

    return prediction, grad_cam_path
