#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pyautogui
import datetime
import time
import pyaudio
import wave

# Set the duration of the recording in seconds
duration = 10

# Get the size of the screen
screen_size = (1920, 1080)

# Get the starting time of the recording
start_time = datetime.datetime.now()

# Create a video file to save the recording
video_file = "screen_recording_" + start_time.strftime("%Y-%m-%d_%H-%M-%S") + ".avi"
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(video_file, fourcc, 20.0, screen_size)

# Create an audio file to save the recording
audio_file = "audio_recording_" + start_time.strftime("%Y-%m-%d_%H-%M-%S") + ".wav"

# Set the audio recording parameters
CHUNK = 1024 
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

# Start the audio recording
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

frames = []

while (datetime.datetime.now() - start_time).seconds < duration:
    # Get the screenshot of the entire screen
    img = pyautogui.screenshot()

    # Convert the image to a numpy array
    frame = np.array(img)

    # Change color of the image
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Write the frame to the video file
    out.write(frame)
    
    # Delay for 1/fps of a second
    time.sleep(1/20)
    data = stream.read(CHUNK)
    frames.append(data)

# Release the file handle
out.release()

# Stop the audio recording
stream.stop_stream()
stream.close()
p.terminate()

# Save the audio recording
wf = wave.open(audio_file, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

