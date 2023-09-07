from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
import subprocess
import os

def format_folder(folder_path):
    folder_name = 'temp'
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    try:
        # Confirm that the folder exists
        if os.path.exists(folder_path):
            # Remove all files and subfolders within the folder
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for file in files:
                    file_path = os.path.join(root, file)
                    os.remove(file_path)
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    os.rmdir(dir_path)
            print(f"Contents of folder '{folder_path}' have been formatted.")
        else:
            print(f"Folder '{folder_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

app = FastAPI()

async def run_video_processing(
    source_path,
    target_path,
    output_path,
    frame_processors,
    reference_face_position,
    similar_face_distance,
):
    # Construct the command
    command = [
        "python", "run.py",
        "-s", source_path,
        "-t", target_path,
        "-o", output_path,
        "--frame-processor", frame_processors,
        "--reference-face-position", str(reference_face_position),
        "--similar-face-distance", str(similar_face_distance)
    ]

    # Remove empty strings from command
    command = [arg for arg in command if arg]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        return {"error": "Processing failed"}

@app.post("/process")
async def process_video(
    source: UploadFile = File(...),
    target: UploadFile = File(...),
    output: str = "output.mp4",
    IsVideo: bool = True,
    frame_processors: str = "face_swapper",
    similar_face_distance: float = 0.85,
    reference_face_position: int = 0,
    background_tasks: BackgroundTasks,
):

    format_folder('./temp')
    # Save uploaded files temporarily
    source_path = f"temp/source{os.path.splitext(source.filename)[1]}"
    target_path = f"temp/target{os.path.splitext(target.filename)[1]}"
    output_path = f"temp/{output}"

    with open(source_path, "wb") as s, open(target_path, "wb") as t:
        s.write(source.file.read())
        t.write(target.file.read())

    # Start the video processing in the background
    background_tasks.add_task(
        run_video_processing,
        source_path,
        target_path,
        output_path,
        frame_processors,
        reference_face_position,
        similar_face_distance,
    )

    if IsVideo:
        # Return a response indicating that processing has started
        return {"message": "Processing video. Result will be available shortly."}
    else:
        # Return a response indicating that processing has started
        return {"message": "Processing image. Result will be available shortly."}
