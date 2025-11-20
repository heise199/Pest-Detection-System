from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
import cv2
import json

from backend.database import get_db
from backend.models import User, Detection
from backend.schemas import DetectionResponse
from backend.dependencies import get_current_active_user
from backend.services.yolo_service import yolo_service
from backend.config import settings

router = APIRouter(prefix="/detection", tags=["detection"])

@router.post("/upload", response_model=DetectionResponse)
async def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # Save uploaded file
    file_location = os.path.join(settings.UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Process with YOLO
    try:
        result = yolo_service.predict_image(file_location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
    
    # Save to DB
    db_detection = Detection(
        user_id=current_user.id,
        image_path=result["output_path"], # Save path to annotated image
        detection_type="image",
        result_json=result["counts"]
    )
    db.add(db_detection)
    db.commit()
    db.refresh(db_detection)
    
    return db_detection

@router.get("/history", response_model=List[DetectionResponse])
def get_history(
    skip: int = 0, 
    limit: int = 100, 
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    detections = db.query(Detection).filter(Detection.user_id == current_user.id).order_by(Detection.created_at.desc()).offset(skip).limit(limit).all()
    return detections

# Camera Streaming Logic
def generate_frames():
    camera = cv2.VideoCapture(0) # Open default camera
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # YOLO Inference
        annotated_frame = yolo_service.predict_video_frame(frame)
        
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()

@router.get("/video_feed")
def video_feed():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

from fpdf import FPDF
from fastapi.responses import FileResponse

@router.get("/report/{detection_id}")
def generate_report(
    detection_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    detection = db.query(Detection).filter(Detection.id == detection_id).first()
    if not detection:
        raise HTTPException(status_code=404, detail="Detection not found")
    
    if detection.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Pest Detection Report #{detection.id}", ln=1, align="C")
    pdf.cell(200, 10, txt=f"Date: {detection.created_at}", ln=1, align="L")
    
    # Add counts
    if detection.result_json:
        pdf.cell(200, 10, txt="Detected Pests:", ln=1, align="L")
        for pest, count in detection.result_json.items():
            pdf.cell(200, 10, txt=f"- {pest}: {count}", ln=1, align="L")
            
    # Add image
    if detection.image_path and os.path.exists(detection.image_path):
        pdf.image(detection.image_path, x=10, y=60, w=100)
        
    output_path = f"uploads/report_{detection.id}.pdf"
    pdf.output(output_path)
    
    return FileResponse(output_path, filename=f"report_{detection.id}.pdf")

