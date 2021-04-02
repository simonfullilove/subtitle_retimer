import re
import datetime
import os
from tkinter import filedialog
import tkinter as tk
from tkinter.font import Font

root = tk.Tk()
root.title('SRT Retimer')

# given the path to a .srt file, and offet values for hours, minutes, seconds, and milliseconds, produces a new .srt file with offets applied
def retime_srt(srt_path_string, srt_filename, offset_hours, offset_mins, offset_secs, offset_millis):

    if srt_path_string == "":
        output.insert(tk.END, 'No file selected...' + '\n')
        output.see(tk.END)
        return

    if srt_path_string[-4:].lower() != ".srt":
        output.insert(tk.END, 'Selected file is not .srt file...' + '\n')
        output.see(tk.END)
        return

    original = open(srt_path_string, "r")
    lines_done = 0
    
    # given a timestamp in string format and offset values for hours, minutes, seconds, and milliseconds, returns a timestamp with offsets applied
    def offset_srt_timestamp(srt_timestamp, hrs, mins, secs, millis):
        offset_timestamp = datetime.datetime.strptime(srt_timestamp, "%H:%M:%S,%f")
        offset_timestamp = offset_timestamp + datetime.timedelta(milliseconds=millis)
        offset_timestamp = offset_timestamp + datetime.timedelta(seconds=secs)
        offset_timestamp = offset_timestamp + datetime.timedelta(minutes=mins)
        offset_timestamp = offset_timestamp + datetime.timedelta(hours=hrs)
        offset_string = str(offset_timestamp)[11:23].replace(".",",")
        return offset_string

    new_srt = open(f'{dest_path}/{srt_filename[:-4]} RETIMED ({offset_hours},{offset_mins},{offset_secs},{offset_millis}).srt', "w")
    
    # applies timestamp offset to each line of subtitles
    for line in original:
        timestamps = re.findall("\d\d:\d\d:\d\d,\d\d\d", line)
        if timestamps:
            cur_start = timestamps[0]
            cur_stop = timestamps[1]
            new_start = offset_srt_timestamp(cur_start, offset_hours, offset_mins, offset_secs, offset_millis)
            new_stop = offset_srt_timestamp(cur_stop, offset_hours, offset_mins, offset_secs, offset_millis)
            new_srt.write(f'{new_start}  --> {new_stop}\n')
            lines_done += 1

        else:
            new_srt.write(line)

    original.close()
    new_srt.close()

    output.insert(tk.END, f'{lines_done} lines retimed!' + '\n')
    output.insert(tk.END, 'Finished!' + '\n')
    output.see(tk.END)

srt_path = ""
dest_path = ""
srt_filename = ""

# plots TK canvas
canvas_filechooser = tk.Canvas(root, width=300, height=0, highlightthickness=0)
canvas_filechooser.pack()

# function for button with which to choose original .srt file
def choose_srt():
    global srt_path, dest_path, srt_filename
    srt_path = filedialog.askopenfilename(title='Choose a file', filetypes=[("All .srt files", "*.srt"), ("All Files", "*.*")])
    srt_path_label.config(text=srt_path)
    dest_path = os.path.dirname(srt_path)
    dest_path_label.config(text = dest_path)
    srt_filename = os.path.basename(srt_path)

# adds button to UI
browse_button = tk.Button(canvas_filechooser, text='Select .SRT file ... ', width=18, font=Font(size=10), command=choose_srt, bg='white', fg='black')
browse_button.pack(side=tk.LEFT, padx=(10,5), pady=(10,5))

# adds label showing chosen .srt file
srt_path_label = tk.Label(canvas_filechooser)
srt_path_label.pack(side=tk.LEFT, padx=(0, 10), pady=(10, 5))
srt_path_label.config(text=" . . . ", width=95, font=Font(size=11), bg='white', fg='black', borderwidth=2, relief="sunken", anchor="nw")

canvas_destination = tk.Canvas(root, width=300, height=0, highlightthickness=0)
canvas_destination.pack()

# function for button to choose save directory
def choose_directory():
    global dest_path
    dest_path = filedialog.askdirectory(title='Choose a folder')
    dest_path_label.config(text = dest_path)

# adds button to UI
dest_button = tk.Button(canvas_destination, text='Select destination ... ', width=18, font=Font(size=10), command=choose_directory, bg='white', fg='black')
dest_button.pack(side=tk.LEFT, padx=(10,5), pady=(10,20))

# adds label showing chosen save path
dest_path_label = tk.Label(canvas_destination)
dest_path_label.pack(side=tk.LEFT, padx=(0,10), pady=(10,20))
dest_path_label.config(text=" . . . ", width=95, font=Font(size=11), bg='white', fg='black', borderwidth=2, relief="sunken", anchor="nw")

# creates new canvas section for offsets spinboxes
canvas_offsets = tk.Canvas(root, width=5, height=0, highlightthickness=0)
canvas_offsets.pack()

# adds label to Offsets canvas
label_offsets = tk.Label(canvas_offsets, text="Offsets:", font=Font(size=14, weight="bold"))
label_offsets.pack(side=tk.LEFT, padx=(5,160))

# adds spinbox and label for each offset
label_hours = tk.Label(canvas_offsets, text="Hours:", font=Font(size=11, weight="bold"))
label_hours.pack(side=tk.LEFT)
spinbox1 = tk.Spinbox(canvas_offsets, from_=-99, to=99, width=10, font=Font(size=11))
spinbox1.delete(-999,"end")
spinbox1.insert(0,0)
spinbox1.pack(side=tk.LEFT, padx=(0,15))

label_mins = tk.Label(canvas_offsets, text="Minutes:", font=Font(size=11, weight="bold"))
label_mins.pack(side=tk.LEFT)
spinbox2 = tk.Spinbox(canvas_offsets, from_=-59, to=59, width=10, font=Font(size=11))
spinbox2.delete(-59,"end")
spinbox2.insert(0,0)
spinbox2.pack(side=tk.LEFT, padx=(0,15))

label_secs = tk.Label(canvas_offsets, text="Seconds:", font=Font(size=11, weight="bold"))
label_secs.pack(side=tk.LEFT)
spinbox3 = tk.Spinbox(canvas_offsets, from_=-59, to=59, width=10, font=Font(size=11))
spinbox3.delete(-59,"end")
spinbox3.insert(0,0)
spinbox3.pack(side=tk.LEFT, padx=(0,15))

label_millis = tk.Label(canvas_offsets, text="Milliseconds:", font=Font(size=11, weight="bold"))
label_millis.pack(side=tk.LEFT)
spinbox4 = tk.Spinbox(canvas_offsets, from_=-999, to=999, width=10, font=Font(size=11))
spinbox4.delete(-999,"end")
spinbox4.insert(0,0)
spinbox4.pack(side=tk.LEFT, padx=(0,15))

# packs offset spinboxes
canvas_log = tk.Canvas(root, width=50, height=0, highlightthickness=0)
canvas_log.pack()

# adds Run button to execute program
run_button = tk.Button(canvas_log, text='Run ...', width=15, font=Font(size=13), command=lambda: retime_srt(srt_path, srt_filename, int(spinbox1.get()), int(spinbox2.get()), int(spinbox3.get()), int(spinbox4.get())), bg='white', fg='black')
run_button.pack(padx = (0,0), pady = (15, 0), anchor='ne')

# adds label to log
label_log = tk.Label(canvas_log, text="Log:", font=Font(size=10))
label_log.pack(anchor='nw')

# adds log display
output = tk.Text(canvas_log, width=120, height=20, bg='white', fg='black')
output.pack()

# adds version label to footer
label1 = tk.Label(root, text="Tsario's Subtitle Retimer v1.0")
label1.pack()

root.mainloop()