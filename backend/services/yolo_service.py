from ultralytics import YOLO
import cv2
import numpy as np
from backend.config import settings
import os

class YoloService:
    def __init__(self):
        self.model = YOLO(settings.MODEL_PATH)
        self.class_names = [
            "Ants", "Bees", "Beetles", "Caterpillars", "Earthworms", 
            "Earwigs", "Grasshoppers", "Moths", "Slugs", "Snails", 
            "Wasps", "Weevils"
        ]

    def predict_image(self, image_path):
        # Run inference
        results = self.model(image_path)
        
        # Process results
        result = results[0]
        
        # Generate output image with boxes
        output_filename = "pred_" + os.path.basename(image_path)
        output_path = os.path.join(settings.UPLOAD_DIR, output_filename)
        
        # Plot results on image
        # Ultralytics plot() returns a BGR numpy array
        im_array = result.plot()  
        cv2.imwrite(output_path, im_array)
        
        # Extract statistics
        detections = []
        class_counts = {}
        
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = self.class_names[cls_id]
            
            detections.append({
                "class": label,
                "confidence": conf,
                "box": box.xyxy[0].tolist()
            })
            
            class_counts[label] = class_counts.get(label, 0) + 1
            
        return {
            "output_path": output_path,
            "detections": detections,
            "counts": class_counts
        }

    def predict_video_frame(self, frame):
        results = self.model(frame)
        result = results[0]
        annotated_frame = result.plot()
        return annotated_frame

yolo_service = YoloService()

