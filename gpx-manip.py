#!/bin/python3

import xml.dom.minidom as md
import datetime
import sys


if sys.argv.__len__() < 3:
    print("No input file And/Or output file!")
    exit(-1)

outputfile = sys.argv[2]
gpx_data = md.parse(sys.argv[1])
gpx_root = gpx_data.documentElement

timestamps = []

for trk in gpx_root.getElementsByTagName("trk"):
    for trkseg in trk.getElementsByTagName("trkseg"):
        for trkpt in trk.getElementsByTagName("trkpt"):
            time = trkpt.getElementsByTagName("time")[0]
            dt = datetime.datetime.strptime(time.childNodes[0].data, '%Y-%m-%dT%H:%M:%SZ')
            timestamps.append(int(dt.timestamp()))

if len(timestamps) == 0:
    exit(-1)

time_min = timestamps[0]
time_max = timestamps[-1]
duration_seconds = time_max - time_min
print(f"Race Began at: {time_min}")
print(f"Race Ended at: {time_max}")
print(f"Race Durated for {duration_seconds} seconds!")

preferred_duration = int(input("How long do you want your race to be?: "))

time_scale = preferred_duration / duration_seconds


for trk in gpx_root.getElementsByTagName("trk"):
    for trkseg in trk.getElementsByTagName("trkseg"):
        for trkpt in trk.getElementsByTagName("trkpt"):
            time = trkpt.getElementsByTagName("time")[0]
            dt = datetime.datetime.strptime(time.childNodes[0].data, '%Y-%m-%dT%H:%M:%SZ')
            seconds = int(dt.timestamp())
            seconds_from_start = seconds - time_min
            new_time = int(seconds_from_start * time_scale + time_min)
            new_dt = datetime.datetime.fromtimestamp(new_time)
            print(new_dt.strftime('%Y-%m-%dT%H:%M:%SZ'))
            trkpt.getElementsByTagName("time")[0].childNodes[0].data = new_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

with open(outputfile, "w") as f:
    gpx_data.writexml(f)
