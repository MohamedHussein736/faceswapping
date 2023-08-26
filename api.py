from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
import subprocess
import os

app = FastAPI()

# New route for the welcome message
@app.get("/")
async def welcome():
    message = """
    <html>
    <head>
        <title>Welcome to FastAPI Face Swapping</title>
    </head>
    <body>
        <h2>Welcome to FastAPI Face Swapping for image and video</h2>
    </body>
    </html>
    """
    return HTMLResponse(content=message)

@app.post("/process")
async def process_video(
    source: UploadFile = File(...),
    target: UploadFile = File(...),
    output: str = "output.mp4",
    IsVideo: bool = True,
    frame_processors: str = "face_swapper",
    similar_face_distance: float = 0.85,
):
    # Save uploaded files temporarily
    source_path = f"temp/source{os.path.splitext(source.filename)[1]}"
    target_path = f"temp/target{os.path.splitext(target.filename)[1]}"
    with open(source_path, "wb") as s, open(target_path, "wb") as t:
        s.write(source.file.read())
        t.write(target.file.read())

    # Construct the command
    command = [
        "python", "run.py",
        "-s", source_path,
        "-t", target_path,
        "-o", output,
        "--frame-processor", frame_processors,
        "--similar-face-distance", str(similar_face_distance)
    ]

    # Remove empty strings from command
    command = [arg for arg in command if arg]

    # Run the command and capture output
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        return {"error": "Processing failed"}

    # Clean up temporary files
    os.remove(source_path)
    os.remove(target_path)
    if IsVideo:
        # Return the generated video file for download
        return FileResponse(output, media_type="video/mp4")
    else:
        # Return the generated image file for download
        return FileResponse(output, media_type="image/jpeg")
