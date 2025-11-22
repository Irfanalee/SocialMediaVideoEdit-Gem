import os
import shutil
import uuid
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ai_engine import AIEngine
from video_processor import VideoProcessor

app = FastAPI(title="Agentic Video Editor API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for video playback
os.makedirs("uploads", exist_ok=True)
os.makedirs("processed", exist_ok=True)
app.mount("/static", StaticFiles(directory="processed"), name="static")

ai_engine = AIEngine()
video_processor = VideoProcessor()

# In-memory job store (replace with DB in production)
jobs = {}

@app.get("/")
async def root():
    return {"message": "Agentic Video Editor API is running"}

@app.post("/upload")
def upload_video(file: UploadFile = File(...)):
    print(f"Receiving upload: {file.filename}")
    file_id = str(uuid.uuid4())
    file_path = f"uploads/{file_id}_{file.filename}"
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        print(f"Upload saved: {file_path}")
    except Exception as e:
        print(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
    return {"id": file_id, "filename": file.filename, "path": file_path}

async def process_video_task(job_id: str, file_path: str):
    jobs[job_id]["status"] = "analyzing"
    try:
        # 1. Analyze with AI
        highlights = await ai_engine.analyze_video(file_path)
        jobs[job_id]["highlights"] = highlights
        
        if not highlights:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = "No highlights found"
            return

        jobs[job_id]["status"] = "processing"
        
        # 2. Process Video
        output_filename = f"processed_{job_id}.mp4"
        output_path = f"processed/{output_filename}"
        
        success = video_processor.process_highlights(file_path, highlights, output_path)
        
        if success:
            jobs[job_id]["status"] = "completed"
            jobs[job_id]["output_url"] = f"/static/{output_filename}"
        else:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["error"] = "Video processing failed"
            
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)

@app.post("/process/{file_id}")
async def start_processing(file_id: str, background_tasks: BackgroundTasks):
    # Find file (in a real app, look up in DB)
    # For now, we just look in uploads folder matching the ID
    files = [f for f in os.listdir("uploads") if f.startswith(file_id)]
    if not files:
        raise HTTPException(status_code=404, detail="File not found")
    
    file_path = f"uploads/{files[0]}"
    job_id = str(uuid.uuid4())
    
    jobs[job_id] = {
        "id": job_id,
        "file_id": file_id,
        "status": "queued"
    }
    
    background_tasks.add_task(process_video_task, job_id, file_path)
    
    return jobs[job_id]

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]
