import os
import time
from google import genai
from config import GOOGLE_API_KEY

def analyze_video(video_path, prompt):
    """
    Uploads a video to Google GenAI File API and analyzes it with a prompt.
    """
    client = genai.Client(api_key=GOOGLE_API_KEY)
    
    print(f"Uploading file: {video_path}...")
    # Upload the video file
    video_file = client.files.upload(path=video_path)
    print(f"Completed upload: {video_file.uri}")

    # Wait for the file to be processed
    while video_file.state.name == "PROCESSING":
        print('.', end='', flush=True)
        time.sleep(5)
        video_file = client.files.get(name=video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError(f"Video processing failed: {video_file.state.name}")

    print("\nAnalyzing video...")
    # Generate content using the video and prompt
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[video_file, prompt]
    )
    
    return response.text
