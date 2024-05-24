def print_results(detections):
    for detection in detections:
        print(f"Detected {detection['object']} with count {detection['count']} on {detection['date']}")
