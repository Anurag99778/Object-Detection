import cv2
import tensorflow as tf
import numpy as np
import traceback

class ObjectDetector:
    def __init__(self):
        print("Loading model...")
        self.model = tf.saved_model.load('models/ssd_mobilenet_v2_320x320_coco17_tpu-8/saved_model')
        print("Model loaded successfully.")
        self.category_index = {1: 'person', 2: 'suitcase', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',
                               7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant'}
        self.trackers = cv2.legacy.MultiTracker_create()  # Using MultiTracker to handle multiple objects
        self.next_id = 0
        self.detected_ids = {}

    def process_video(self, video_path, output_path):
        print(f"Opening video file: {video_path}")
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print("Error: Could not open video file.")
            return

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            print(f"Processing frame {frame_count}...")

            try:
                frame, frame_detections = self.process_frame(frame)
                out.write(frame)
            except Exception as e:
                print(f"Error processing frame {frame_count}: {e}")
                traceback.print_exc()

        cap.release()
        out.release()
        print("Video processing completed.")
        for object_class, ids in self.detected_ids.items():
            print(f"Unique {object_class}s detected: {len(ids)}")

    def process_frame(self, frame):
        detections = self.detect_objects(frame)
        frame = self.draw_detections(frame, detections)
        self.update_trackers(frame)
        return frame, detections

    def detect_objects(self, frame):
        try:
            input_tensor = tf.convert_to_tensor(frame)
            input_tensor = input_tensor[tf.newaxis, ...]

            detections = self.model(input_tensor)

            num_detections = int(detections.pop('num_detections'))
            detections = {key: value[0, :num_detections].numpy() for key, value in detections.items()}
            detections['num_detections'] = num_detections

            return detections
        except Exception as e:
            print(f"Error during detection: {e}")
            traceback.print_exc()
            return None

    def draw_detections(self, frame, detections):
        if detections is None:
            return frame

        try:
            for i in range(detections['detection_boxes'].shape[0]):
                box = detections['detection_boxes'][i]
                class_id = int(detections['detection_classes'][i])
                score = detections['detection_scores'][i]

                if score > 0.5:
                    y1, x1, y2, x2 = box
                    height, width, _ = frame.shape
                    p1 = (int(x1 * width), int(y1 * height))
                    p2 = (int(x2 * width), int(y2 * height))
                    cv2.rectangle(frame, p1, p2, (0, 0, 255), 2)

                    class_name = self.category_index.get(class_id, 'N/A')
                    cv2.putText(frame, class_name, (p1[0], p1[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                    tracker = cv2.legacy.TrackerKCF_create()
                    self.trackers.add(tracker, frame, (p1[0], p1[1], p2[0] - p1[0], p2[1] - p1[1]))

                    if class_name not in self.detected_ids:
                        self.detected_ids[class_name] = set()
                    self.detected_ids[class_name].add(i)
        except Exception as e:
            print(f"Error during drawing detections: {e}")
            traceback.print_exc()

        return frame

    def update_trackers(self, frame):
        success, boxes = self.trackers.update(frame)
        if success:
            for i, newbox in enumerate(boxes):
                p1 = (int(newbox[0]), int(newbox[1]))
                p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2)

                for class_name, ids in self.detected_ids.items():
                    if i not in ids:
                        self.detected_ids[class_name].add(i)
        else:
            self.trackers = cv2.legacy.MultiTracker_create()
