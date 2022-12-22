#!/usr/local/bin/python3

from qiskit import QuantumCircuit, IBMQ, transpile
from time import sleep

TOTAL_JOBS = 8 # total number of jobs to execute
INTERVAL = 5 #interval (minutes) at which to run/reap jobs
TOKEN = "71ae5003e021b05322d6aecd73e2ab63500cebcc5e1e73801c5586e0a1f8e7eea45c0507cd8767e290f174b37b412706276ef60f4c0dc4ec4a20ea2d83f392fc"

if __name__ == "__main__":
    #MARK: define QuantumCircuit
    circuit = QuantumCircuit(7)
    circuit.x([2 * i for i in range(3)])
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
                print(job.result().get_memory())
                jobs.remove(job)
        if num_jobs < TOTAL_JOBS:
            job = backend.run(transpiled_circuit, memory=True)
            jobs.add(job)
            num_jobs += 1
        sleep(60*INTERVAL)
