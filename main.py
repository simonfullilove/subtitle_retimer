import re
import datetime

original = open("example.srt", "r")
new_srt = open("new_srt.srt", "w")

offset_hours = 0
offset_mins = -3
offset_secs = -31
offset_millis = 1

def offset_srt_timestamp(srt_timestamp, hrs, mins, secs, millis):
    offset_timestamp = datetime.datetime.strptime(srt_timestamp, "%H:%M:%S,%f")
    offset_timestamp = offset_timestamp + datetime.timedelta(milliseconds=millis)
    offset_timestamp = offset_timestamp + datetime.timedelta(seconds=secs)
    offset_timestamp = offset_timestamp + datetime.timedelta(minutes=mins)
    offset_timestamp = offset_timestamp + datetime.timedelta(hours=hrs)
    return str(offset_timestamp)[11:23].replace(".",",")

for line in original:
    timestamps = re.findall("\d\d:\d\d:\d\d,\d\d\d", line)
    if timestamps:
        cur_start = timestamps[0]
        cur_stop = timestamps[1]
        new_start = offset_srt_timestamp(cur_start, offset_hours, offset_mins, offset_secs, offset_millis)
        new_stop = offset_srt_timestamp(cur_stop, offset_hours, offset_mins, offset_secs, offset_millis)
        new_srt.write(f'{new_start}  --> {new_stop}\n')
    else:
        new_srt.write(line)

original.close()
new_srt.close()