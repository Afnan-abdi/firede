import torch
import torch.hub
import cv2
import ssl
import shutil
from playsound import playsound
from pathlib import Path
import pathlib
from collections import deque
import time

pathlib.PosixPath = pathlib.WindowsPath

class FireDetection:
    def __init__(self, model_path, video_path):
        self.model_path = model_path
        self.video_path = video_path
        torch.hub._validate_not_a_forked_repo = lambda a, b, c: True  # Workaround for loading models from local cache without internet
        self.clear_model_cache()
        self.model = self.load_model()
        self.classes = self.model.names
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.fire_detections = deque(maxlen=10)  # Keep track of fire detections
        self.last_sound_time = 0  # To avoid playing sound repeatedly
        print('Using Device:', self.device)

    def clear_model_cache(self):
        cache_dir = torch.hub.get_dir()
        shutil.rmtree(cache_dir, ignore_errors=True)
        print("Cache cleared")

    def get_video_capture(self):
        cap = cv2.VideoCapture(str(self.video_path))  # Use the video file path
        if not cap.isOpened():
            raise FileNotFoundError(f"Error: Could not open video file {self.video_path}")
        return cap

    def load_model(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=str(self.model_path), force_reload=True)
        return model

    def score_frame(self, frame):
        self.model.to(self.device)
        frame = [frame]
        results = self.model(frame)
        labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
        return labels, cord

    def class_to_label(self, x):
        return self.classes[int(x)]

    def plot_boxes(self, results, frame):
        labels, cord = results
        x_shape, y_shape = frame.shape[1], frame.shape[0]
        current_time = time.time()
        new_fire_detections = []

        for i in range(len(labels)):
            row = cord[i]
            if row[4] >= 0.4:  # Increase the confidence threshold here to 0.4 or higher
                new_fire_detections.append((current_time, row))
                x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(row[3] * y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, self.class_to_label(labels[i]), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
                
                # Play sound only once every 10 seconds
                if current_time - self.last_sound_time > 10:
                    playsound(Path(r"C:\Users\amadeus\Desktop\FIREdetector\alarm.mp3"))
                    self.last_sound_time = current_time

        # Add new detections to the deque
        self.fire_detections.extend(new_fire_detections)

        # Draw previous fire detections
        for detection in self.fire_detections:
            detection_time, row = detection
            if current_time - detection_time < 10:  # Keep detection for 10 seconds
                x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(row[3] * y_shape)
                bgr = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
                cv2.putText(frame, 'fire', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        return frame

    def __call__(self):
        cap = self.get_video_capture()
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                results = self.score_frame(frame)
                frame_with_boxes = self.plot_boxes(results, frame)

                # Resize the frame
                frame_resized = cv2.resize(frame_with_boxes, (800, 600))  # Change the size as needed

                # Display the frame with detections
                cv2.imshow('Fire Detection', frame_resized)

                # Break the loop when 'Esc' key is pressed
                if cv2.waitKey(1) & 0xFF == 27:
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

# Use Path for handling the model file path
model_path = Path(r"C:\Users\amadeus\Desktop\fireDETEECTOR\my model.pt")
video_path = Path(r"C:\Users\amadeus\Desktop\fireDETEECTOR\videos\2548406-hd_1920_1080_24fps.mp4")  # Replace with the path to your video file

if not model_path.exists():
    raise FileNotFoundError(f"Model file not found at {model_path}")
if not video_path.exists():
    raise FileNotFoundError(f"Video file not found at {video_path}")

detector = FireDetection(model_path=model_path, video_path=video_path)
detector()



