from detector import ObjectDetector
from database import Database
import datetime

def main():
    print("Initializing Object Detector...")
    detector = ObjectDetector()

    print("Initializing Database...")
    db = Database()

    print("Processing Video...")
    video_path = 'C:\\Users\\Dell\\Downloads\\newv.mp4'
    output_path = r'C:\Users\Dell\Downloads\card.mp4'
    detector.process_video(video_path, output_path)

    print("Video processing completed. Output saved to:", output_path)

    print("Processing detections...")
    current_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for object_class, ids in detector.detected_ids.items():
        unique_count = len(ids)
        db.insert_detection({'date': current_date, 'object': object_class, 'count': unique_count})
    print("Detections saved to database.")

if __name__ == "__main__":
    main()

