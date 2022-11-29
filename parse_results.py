import os
import json
import datetime
import matplotlib.pyplot as plt

#path to folder containing jobs output
ROOTDIR = "/Users/benjamingoldstein/Desktop/Desktop/Coding/EENG468/jobs_11-20-22"
#bitmasks to extract qubit values from hex, note only qubits 0, 2, 3, 4, 6 in use
MASKS = [0b0000001, 0b0000010, 0b0000100, 0b0001000, 0b0010000, 0b0100000, 0b1000000]

if __name__ == "__main__":
    filenames = os.listdir(ROOTDIR)
    filenames = [f for f in filenames if "-output.json" in f]
    points = []
    counts = [0 for _ in range(6)]
    total_jobs = 0
    total_time = 0
    for filename in filenames:
        path = os.path.join(ROOTDIR, filename)
        with open(path, "r") as file:
            output = json.load(file)
            time_taken = output.get('time_taken', 0)
            if (time_taken == 0):
                print(f"ERROR: TIME TAKEN FOR FILE {filename} = 0. IGNORING")
                break
            start_datestr = output.get('date')
            try:
                start_date = datetime.datetime.strptime(start_datestr, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError as v:
                print(f"ERROR PARSING DATE {start_datestr} IN FILE {filename}: {v}. IGNORING")
                break
            start_date_seconds = start_date.timestamp()
            results = output.get('results', [{}])[0]
            num_shots = results.get('shots', 0)
            total_time += time_taken
            total_jobs += 1
            if (num_shots == 0):
                print(f"ERROR: NUM SHOTS FOR FILE {filename} = 0. IGNORING")
                break
            shot_duration = time_taken / num_shots
            data = results.get('data', {})
            memory = data.get('memory', [])
            curr_time = start_date_seconds
            for datapoint in memory:
                shot = int(datapoint, 16)
                n_errors = 0
                if shot & MASKS[0] == 0:
                    n_errors += 1
                if shot & MASKS[2] == 0:
                    n_errors += 1
                if shot & MASKS[3] == 0:
                    n_errors += 1
                if shot & MASKS[4] == 0:
                    n_errors += 1
                if shot & MASKS[6] == 0:
                    n_errors += 1

                points.append((curr_time, n_errors))
                counts[n_errors] += 1
                curr_time += shot_duration
    start_time = datetime.datetime.now().timestamp()
    for p in points:
        if p[0] < start_time:
            start_time = p[0]
    points = [(p[0] - start_time, p[1]) for p in points]
    points.sort()
    fig, ax = plt.subplots()
    ax.scatter([p[0] for p in points], [p[1] for p in points])
    ax.set(xlabel=f'Time Since {datetime.datetime.fromtimestamp(start_time)} (s)', ylabel='Error Count', title='Error Counts vs Time')
    fig.savefig("jobs_plot_11-20-22.png")
    print(f"COUNTS: {counts}")
    with open("results.csv", "w") as file:
        file.write("timestamp,errorcount,,errorcount_val,errorcount_freq,,startdate\n")
        file.write(f"{points[0][0]},{points[0][1]},,0,{counts[0]},,{datetime.datetime.fromtimestamp(start_time)}\n")
        for i in range(1,6):
            file.write(f"{points[i][0]},{points[i][1]},,{i},{counts[i]}\n")
        for i in range(6, len(points)):
            file.write(f"{points[i][0]},{points[i][1]}\n")
    plt.show()





