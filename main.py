import re

original = open("example.srt", "r")
new_srt = open("new_srt.srt", "w")

offset_hours = 0
offset_mins = 0
offset_secs = 0
offset_millis = 0

for line in original:

    cur_timestamp = re.findall("\d\d:\d\d:\d\d,\d\d\d --> \d\d:\d\d:\d\d,\d\d\d", line)

    if cur_timestamp:
        cur_start_hours = int(cur_timestamp[:2])
        cur_start_mins = int(cur_timestamp[3:5])
        cur_start_secs = int(cur_timestamp[6:8])
        cur_start_millis = int(cur_timestamp[9:12])
        cur_stop_hours = int(cur_timestamp[17:19])
        cur_stop_mins = int(cur_timestamp[20:22])
        cur_stop_secs = int(cur_timestamp[23:25])
        cur_stop_millis = int(cur_timestamp[26:])

        cur_offset_millis = offset_millis +

    else:
        new_srt.write(line)

original.close()
new_srt.close()