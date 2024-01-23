import os
from moviepy.editor import VideoFileClip, AudioFileClip
import cv2
import numpy as np

input_folder = 'willblurvideos'
output_folder = 'blurvideos'
audio_output_folder = 'audios'

os.makedirs(output_folder, exist_ok=True)
os.makedirs(audio_output_folder, exist_ok=True)

def blur_video(video_path, blur_factor=169):
    video_clip = VideoFileClip(video_path)

    frames = [cv2.cvtColor(frame, cv2.COLOR_RGB2BGR) for frame in video_clip.iter_frames()]

    blurred_frames = [cv2.GaussianBlur(frame, (blur_factor, blur_factor), 0) for frame in frames]

    temp_video_path = 'temp_blurred_video.mp4'
    height, width, _ = blurred_frames[0].shape
    writer = cv2.VideoWriter(temp_video_path, cv2.VideoWriter_fourcc(*'mp4v'), video_clip.fps, (width, height))

    for frame in blurred_frames:
        writer.write(frame)

    writer.release()

    return VideoFileClip(temp_video_path, audio=False)

def process_video(video_path):
    audio_clip = VideoFileClip(video_path).audio
    audio_path = os.path.join(audio_output_folder, f'{os.path.basename(video_path)}_audio.mp3')
    audio_clip.write_audiofile(audio_path, codec='mp3')

    blurred_clip = blur_video(video_path)

    audio_clip = AudioFileClip(audio_path)

    final_clip = blurred_clip.set_audio(audio_clip)

    output_path = os.path.join(output_folder, f'{os.path.basename(video_path)}_blurred.mp4')
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

    os.remove('temp_blurred_video.mp4')

video_files = [f for f in os.listdir(input_folder) if f.endswith('.mp4')]
for video_file in video_files:
    video_path = os.path.join(input_folder, video_file)
    process_video(video_path)
