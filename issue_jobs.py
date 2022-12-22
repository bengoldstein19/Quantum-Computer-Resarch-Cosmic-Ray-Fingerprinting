#!/usr/local/bin/python3

from qiskit import QuantumCircuit, IBMQ, transpile
from time import sleep
import datetime
import os

TOTAL_JOBS = 100 # total number of jobs to execute
INTERVAL = 0.1 #interval (minutes) at which to run/reap jobs


TOKEN = os.environ.get('IBMQ_TOKEN')

if __name__ == "__main__":
    #MARK: define QuantumCircuit
    circuit = QuantumCircuit(7)
    circuit.x([0, 2, 3, 4, 6])
    circuit.measure_all()

    jobs = set()

    #MARK: configuring IBM Account, getting backend
    IBMQ.delete_account()
    IBMQ.save_account(TOKEN)
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub="ibm-q-research-2", group="yale-uni-5", project="main")

    backend = provider.get_backend("ibmq_jakarta")

    #MARK: transpiling circuit
    transpiled_circuit = transpile(circuit, backend=backend)

    #MARK: Initializing variables for job running/reaping, create/run first job
    num_minutes = 0
    num_jobs = 1

    job = backend.run(transpiled_circuit, memory=True)
    jobs.add(job)
    sleep(60 * INTERVAL)

    #MARK: Loop that runs and reaps jobs
    while(len(jobs) > 0):
        for job in jobs:
            if (job.done()):
                print(job.result())
                with open(f"jobs_{datetime.datetime.now().strftime('%d/%m/%y')}/{job.job_id()}.json", "w") as f:
                    f.write(job.result())
                jobs.remove(job)
        if num_jobs < TOTAL_JOBS:
            job = backend.run(transpiled_circuit, memory=True)
            jobs.add(job)
            num_jobs += 1
        sleep(60*INTERVAL)
