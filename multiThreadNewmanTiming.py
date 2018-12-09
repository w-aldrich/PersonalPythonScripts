# This would be used to test timing results for RESTFUL API testing
# This program uses POSTMAN collections and environments
# Must have newman installed to run
from multiprocessing import Process
import os, sys, subprocess, datetime

def run_newman(collection, environment, number):
    subprocess.run("newman run " + collection + " -e " + environment +
    "| grep -e \"\[*\]\" -e \"average response time:\" >" + number + environment + ".txt", shell=True)

if __name__ == '__main__':
    if len(sys.argv) != 4 or not sys.argv[1].isdigit():
        print("Usage: <number of threads> <postman collection> <postman environment>")
    else:
        runtime = str(datetime.datetime.now()).replace(":", "-").replace(".", "-").replace(" ", "--")
        threadRange = int(sys.argv[1])
        collection = sys.argv[2]
        environment = sys.argv[3]
        processes = []
        for i in range(threadRange):
            processes.append(Process(target=run_newman, args=(collection, environment, str(i))))
        for i in range(threadRange):
            processes[i].start()
        for i in range(threadRange):
            processes[i].join()
        file = open(runtime + ".txt", "w")
        for i in range(threadRange):
            file.write(open((str(i) + environment + ".txt")).read())
            os.remove((str(x) + environment + ".txt"))
