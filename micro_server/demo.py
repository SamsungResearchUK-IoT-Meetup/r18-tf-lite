# A simple test script to test python can spawn create and stop processes.

import os, subprocess, time, signal

record_command = 'parecord --rate=16000 --channels=1 /home/nherriot/test.wav'
ctrl_c_command = signal.SIGINT

print("*** Creating the record process ***")
record_process = subprocess.Popen(record_command, shell=True)
print("Record process PID is: {}".format(record_process.pid))
print("Sleeping for 10 seconds...")
time.sleep(10)
print("Stopping the record process.")
os.kill(record_process.pid, signal.SIGINT)
os.kill((record_process.pid+1), signal.SIGINT)

if record_process.poll() is None:
    os.kill(record_process.pid, signal.SIGTERM)
    print("Process is not accepting SIGINT, now trying to Terminate the process")
    time.sleep(2)
if record_process.poll() is None:  # Force kill if process is still alive
    print("Process is not accepting SIGTERM, now trying to Kill the process")
    os.kill(record_process.pid, signal.SIGKILL)