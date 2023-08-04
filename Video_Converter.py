import tkinter as tk
from tkinter import filedialog
from moviepy.editor import *
import ffmpeg
import subprocess
import os

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 Files", "*.mp4")])
    if file_path:
        input_file_entry.delete(0, tk.END)
        input_file_entry.insert(0, file_path)

def convert_file():
    input_file = input_file_entry.get()
    output_format = output_format_var.get()
    if input_file and output_format:
        try:
            video = VideoFileClip(input_file)
            output_file = input_file[:-4] + "." + output_format
            video.write_videofile(output_file, codec="libx264")
            status_label.config(text=f"Conversion successful! Output file: {output_file}")
        except Exception as e:
            status_label.config(text=f"Error during conversion: {str(e)}")
    else:
        status_label.config(text="Please select an input file and an output format.")

def compare_performance():
    input_file = input_file_entry.get()
    output_format = output_format_var.get()
    output_file = input_file[:-4] + "." + output_format
    try:
        original_duration = get_video_duration(input_file)
        converted_duration = get_video_duration(output_file)
        status_label.config(text=f"Original Video Duration: {original_duration}s\nConverted Video Duration: {converted_duration}s")
    except ffmpeg.Error as e:
        status_label.config(text=f"Error: {e.stderr.decode()}")
def get_video_duration(filename):
    result = subprocess.check_output(['ffprobe', '-i', filename, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=%s' % ("p=0")])
    return float(result)

root = tk.Tk()
root.title("Video Format Converter")


input_file_label = tk.Label(root, text="Select input file (MP4 format):")
input_file_label.pack()
input_file_entry = tk.Entry(root, width=50)
input_file_entry.pack()
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()


output_format_label = tk.Label(root, text="Select output format:")
output_format_label.pack()
output_format_var = tk.StringVar()
output_format_var.set("avi")
output_format_options = ["avi", "mkv", "mp4", "webm","m3u8"]
output_format_menu = tk.OptionMenu(root, output_format_var, *output_format_options)
output_format_menu.pack()


convert_button = tk.Button(root, text="Convert", command=convert_file)
convert_button.pack()


compare_button = tk.Button(root, text="Compare Performance", command=compare_performance)
compare_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
