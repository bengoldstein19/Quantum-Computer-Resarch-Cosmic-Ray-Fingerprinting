#!/usr/local/bin/python3

import json
import datetime
import matplotlib.pyplot as plt

GEOMAG_FILES=["geomag_data/GEOMAGDATA_BRW_01:01:22-06:01:22.json", "geomag_data/GEOMAGDATA_BRW_06:01:22-11:29:22.json"]

if __name__ == "__main__":
    timestamps = []
    values = []
    
    for filename in GEOMAG_FILES:
        with open(filename, "r") as file:
            try:
                geomag_data = json.load(file)
            except json.decoder.JSONDecodeError as e:
                print(f"ERROR PARSING JSON FILE {filename}: {e}. IGNORING")
                continue
            timestamps += geomag_data.get('times', [])
            values += geomag_data.get('values', [{}])[0].get('values', [])

    start_timestamp = datetime.datetime.now().timestamp()
    for datestr in timestamps:
        date = datetime.datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S.000Z")
        if date.timestamp() < start_timestamp:
            start_timestamp = date.timestamp()
    timestamps = [(datetime.datetime.strptime(t, "%Y-%m-%dT%H:%M:%S.000Z").timestamp() - start_timestamp) / (3600 * 24) for t in timestamps]
    null_counts = [0 for i in range(365)]
    for i,t in enumerate(timestamps):
        if (values[i] == None):
            null_counts[int(t)] += 1
    print(f"NULL_COUNTS: {null_counts}")
    fig, ax = plt.subplots()
    ax.plot(timestamps, values, linestyle='-')
    ax.set(xlabel=f'Time Since {datetime.datetime.fromtimestamp(start_timestamp)} (days)', ylabel='Geomagnetic Value', title='Geomagnetic Data Over Time (2022)')
    fig.savefig('plots/geomag_BRW_01-01-22-11-29-22_plot.png')
    plt.show()

    