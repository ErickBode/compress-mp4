from tkinter import *
from moviepy.editor import *
from moviepy.editor import VideoFileClip
import customtkinter as ctk
import tkinter as tk
import os
import sys
import threading

"""
The available preset values are:
ultrafast: The fastest encoding speed. This preset is intended for quick prototyping and testing, and may not produce the highest quality output.
superfast: Faster encoding speed, at the cost of some quality.
veryfast: A balance between encoding speed and quality.
faster: A slower encoding speed that produces higher quality output.
fast: A slower encoding speed that produces even higher quality output.
medium: A balanced setting that strikes a balance between encoding speed and quality.
slow: A slower encoding speed that produces the highest quality output.
slower: The slowest encoding speed, which produces the highest quality output but takes the longest to encode.
"""

#Classes
# Define a custom stream writer to redirect stdout and stderr to a widget
class StdoutRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.config(state="normal")  # Enable editing temporarily
        self.text_widget.insert(END, message.rstrip() + '\n')  # Add a new line after each message
        self.text_widget.see(END)  # Scroll to the end of the text
        self.text_widget.config(state="disabled")  # Disable editing again

# Functions
def get_file_size(file_path):
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)  # Convert bytes to MB
    return "{:.1f}".format(size_mb)

def compress_mp4(input_file, output_file, target_size_bytes, compression_percentage, output_text_widget):
    # Redirect stdout and stderr to the text widget
    sys.stdout = StdoutRedirector(output_text_widget)
    sys.stderr = StdoutRedirector(output_text_widget)
    
    # Get video duration
    try:
        # Get video duration
        video = VideoFileClip(input_file)
        duration = video.duration
        video.close()

        # Calculate total bitrate
        total_bitrate = target_size_bytes * 8 / duration

        # Calculate target bitrate
        target_bitrate_before = int(total_bitrate * (target_size_bytes / (os.path.getsize(input_file) * 1024 * 1024)))

        # Apply compression percentage
        target_bitrate_after = (target_bitrate_before * (compression_percentage / 100)) * 1000

        # Compress video
        video_clip = VideoFileClip(input_file)
        video_clip.write_videofile(output_file, preset='superfast', codec='libx264', bitrate=f"{target_bitrate_after}k", threads=4)
        video_clip.close()

        print(f"Compression complete. Output file: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

def compress_mp4_async(input_file, output_file, target_size_bytes, compression_percentage, output_text_widget):
    # Redirect stdout and stderr to the text widget
    sys.stdout = StdoutRedirector(output_text_widget)
    sys.stderr = StdoutRedirector(output_text_widget)
    
    # Run compression process
    compress_mp4(input_file, output_file, target_size_bytes, compression_percentage, output_text_widget)
 

def compress_video_async():
     input_file = file_path.get()
     filename = os.path.basename(input_file)
     output_folder = output_path.get()

     # Replace spaces in the filename with underscores
     filename_without_spaces = filename.replace(" ", "_")
     
     output_file = os.path.join(output_folder, "output_" + filename_without_spaces)

     target_size_bytes = os.path.getsize(input_file)
     compression_percentage = int(selected_percentValue.get())
     
     threading.Thread(target=compress_mp4_async, args=(input_file, output_file, target_size_bytes, compression_percentage, output_text)).start()

def browseFile():
      filename = ctk.filedialog.askopenfilename()
      if filename:
          file_size.set(get_file_size(filename))
          file_path.set(filename)

          current_size_mb = float(get_file_size(filename))
          target_size_mb = 24.0

          reduction_percentage = int(((target_size_mb - current_size_mb) / current_size_mb) * 100)
          reduction_percentage += 100

          target_percent_fileSize.set(reduction_percentage)

def browseFolder():
      foldername = ctk.filedialog.askdirectory()
      if foldername:
          output_path.set(foldername)

def update_value(value):
        selected_percentValue.set(f"{int(slider_percent.get())}")



# Setting up the appearance mode and color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")
    
# Create the customtkinter window
app = ctk.CTk()
app.title('Compress Video')
app.geometry("1000x600")
app.resizable(False, False)

# Create the Frame of the window
frame = ctk.CTkFrame(master=app, corner_radius=6)
frame.pack(pady=15, padx=15, fill="both", expand=True)

# Create a sub-frame inside the main frame
sub_frame = ctk.CTkFrame(master=frame,
                         corner_radius=6, 
                         height=100,
                         width=100, 
                         fg_color="#808080")
sub_frame.place(relx=0.5, rely=0.5, anchor="n")

# Create a text widget to display MoviePy progress messages
output_text = tk.Text(sub_frame,
                      wrap='word',
                      height=15,
                      width=95, 
                      font=("Arial", 12), 
                      state="disabled",
                      bg="gray")
output_text.place(relx=0.125, rely=0.05, anchor=tk.CENTER)

# Create a vertical scrollbar
scrollbar = tk.Scrollbar(sub_frame, orient="vertical", command=output_text.yview)
output_text.config(yscrollcommand=scrollbar.set)

# Pack the scrollbar on the right side of the text widget
scrollbar.pack(side="right", fill="y")

# Pack the text widget, allowing it to fill the available space and expand
output_text.pack(side="left", fill="both", expand=True)

# Label Select Input File
text_SelectFile = tk.StringVar(value="Input File (mp4): ")
label_SelectFile = ctk.CTkLabel(master=frame,
                                width=1000,
                                height=25,
                                textvariable=text_SelectFile,
                                text_color="white",
                                font=("Arial", 20),
                                corner_radius=8)
label_SelectFile.place(relx=0.125, rely=0.05, anchor=tk.CENTER)

# Label Select Output File
text_SelectFile = tk.StringVar(value="Output File Path: ")
label_SelectFile = ctk.CTkLabel(master=frame,
                                width=1000,
                                height=25,
                                textvariable=text_SelectFile,
                                text_color="white",
                                font=("Arial", 20),
                                corner_radius=8)
label_SelectFile.place(relx=0.125, rely=0.125, anchor=tk.CENTER)

# Create a label and entry for displaying the size of the selected file
text_FileSize = tk.StringVar(value="File Size (MB): ")
label_SelectSize = ctk.CTkLabel(master=frame,
                                width=1000,
                                height=25, 
                                textvariable=text_FileSize,
                                text_color="white",
                                font=("Arial", 18),
                                corner_radius=8)
label_SelectSize.place(relx=0.1124, rely=0.468, anchor=tk.CENTER)

text_OutputFileSize = tk.StringVar(value="To reach (24.0 mb): ")
label_OutputFileSize = ctk.CTkLabel(master=frame,
                                width=250,
                                height=25, 
                                textvariable=text_OutputFileSize,
                                text_color="white",
                                font=("Arial", 18),
                                corner_radius=8)
label_OutputFileSize.place(relx=0.4, rely=0.466, anchor=tk.CENTER)

# Label Select Taget Size
text_SelectSize = tk.StringVar(value="Target Size: ")
label_SelectSize = ctk.CTkLabel(master=frame,
                                width=1000,
                                height=25,
                                textvariable=text_SelectSize,
                                text_color="white",
                                font=("Arial", 18),
                                corner_radius=8)
label_SelectSize.place(relx=0.292, rely=0.19, anchor=tk.CENTER)

# Browse Input Button
browseInput_button = ctk.CTkButton(master=frame,
                                   width=100,
                                   height=29.49,
                                   text="Browse",
                                   corner_radius=4,
                                   font=("Arial", 18),
                                   command=browseFile)
browseInput_button.place(relx=0.29, rely=0.0525, anchor=tk.CENTER)

# Create the Input entry field
file_path = tk.StringVar()
entry = ctk.CTkEntry(master=frame,
                     width=600,
                     font=("Arial", 18),
                     text_color="white",
                     fg_color=("dark-gray", "gray"),
                     textvariable=file_path,
                     corner_radius=4,
                     border_width=0,
                     state="readonly")
entry.place(relx=0.654, rely=0.0525, anchor=tk.CENTER)

# Browse Output Button
browseOutput_button = ctk.CTkButton(master=frame,
                                    width=100,
                                    height=29.49,
                                    text="Browse",
                                    corner_radius=4,
                                    font=("Arial", 18),
                                    command=browseFolder)
browseOutput_button.place(relx=0.29, rely=0.12525, anchor=tk.CENTER)

# Create the Output entry field
output_path = tk.StringVar()
output = ctk.CTkEntry(master=frame,
                      width=600,
                      font=("Arial", 18),
                      text_color="white",
                      fg_color=("dark-gray", "gray"),
                      textvariable=output_path,
                      corner_radius=4,
                      border_width=0,
                      state="readonly")
output.place(relx=0.654, rely=0.12525, anchor=tk.CENTER)

# Current File Size entry field
file_size = tk.StringVar()
file_size_entry = ctk.CTkEntry(master=frame,
                               width=80,
                               height=20,
                               fg_color=("dark-gray", "gray"),
                               text_color="white",
                               font=("Arial", 18),
                               textvariable=file_size,
                               corner_radius=6,
                               state="readonly")
file_size_entry.place(relx=0.215, rely=0.468, anchor=tk.CENTER)

# Reach file size entry field
target_percent_fileSize = tk.StringVar()
file_size_reduction = ctk.CTkEntry(master=frame,
                               width=37,
                               height=20,
                               fg_color=("dark-gray", "gray"),
                               text_color="white",
                               font=("Arial", 19),
                               textvariable=target_percent_fileSize,
                               corner_radius=6,
                               state="readonly")
file_size_reduction.place(relx=0.508, rely=0.468, anchor=tk.CENTER)

# Reach file size % entry field
textLabelPercentSize = tk.StringVar(value="%")
file_size_reduction = ctk.CTkEntry(master=frame,
                               width=30,
                               height=20,
                               fg_color=("dark-gray", "gray"),
                               text_color="white",
                               textvariable=textLabelPercentSize,
                               font=("Arial", 19),
                               corner_radius=6,
                               state="readonly")
file_size_reduction.place(relx=0.545, rely=0.468, anchor=tk.CENTER)


# Start of Slider Section
slider_percent = ctk.CTkSlider(master=frame,
                               width=515,
                               height=18,
                               from_=10,
                               to=100,
                               number_of_steps=9,
                               command=update_value)
slider_percent.place(relx=0.6035, rely=0.193, anchor=tk.CENTER)

selected_percentValue = tk.StringVar(value="60")
label_selectPercent = ctk.CTkLabel(master=frame,
                                   width=50,
                                   height=25,
                                   textvariable=selected_percentValue,
                                   fg_color=("dark-gray", "gray"),
                                   text_color="white",
                                   font=("Arial", 19),
                                   corner_radius=6)
label_selectPercent.place(relx=0.905, rely=0.193, anchor=tk.CENTER)

# Create the label for displaying the '%' sign
textLabelPercent = tk.StringVar(value="%")
label_percent = ctk.CTkLabel(master=frame,
                             width=25,
                             height=25,
                             textvariable=textLabelPercent,
                             fg_color=("dark-gray", "gray"),
                             text_color="white",
                             font=("Arial", 19),
                             corner_radius=6)
label_percent.place(relx=0.948, rely=0.193, anchor=tk.CENTER)
# End of Slider Section.

# Create the Compress button
compress_button = ctk.CTkButton(master=frame,
                                width=300,
                                height=35,
                                text="Compress",
                                corner_radius=6,
                                font=("Arial", 28),
                                command=compress_video_async)
compress_button.place(relx=0.797, rely=0.46, anchor=tk.CENTER)
    

# Run the tkinter event loop
app.mainloop()
