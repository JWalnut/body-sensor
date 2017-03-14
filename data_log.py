import json
import os
import numpy
from datetime import datetime as dt
from body_sensor import data_run
import matplotlib.pyplot as plt

class DataLog():
    def __init__(self, dir=""):
        self.run_count = 0
        self.runs = {}
        self.times = {}
        if not dir == "":
            self.directory = dir
            self.load(dir)
        else:
            self.directory = ""

    def load(self, runs_folder):
        self.directory = runs_folder
        runs_list = os.listdir(runs_folder)
        for run in runs_list:
            split_index = run.find("Data")
            name = run[:split_index - 1]
            time = None
            #print(name, "\n", run[split_index + 4:])
            try:
                time = dt.strptime(run[split_index + 5:], "%m_%d_%Y_%I_%M_%p")
            except ValueError as ve:
                #print("Skipping file \"{}\"".format(run))
                continue
            self.runs[name] = run
            self.times[name] = time
            self.run_count += 1
    
    def select(self, run_name):
        if self.runs[run_name] == None:
            return
        run = data_run.DataRun()
        #print("{}/{}/*.json".format(self.directory, self.runs[run_name]))
        run.load_data(file_name="{}/{}/*.json".format(self.directory, self.runs[run_name]))
        return run
    
    def save_log_imgs(self, data_runs=[], data_types=[]):
        if data_runs == []:
            data_runs = list(self.runs.keys())
        for run_name in data_runs:
            run = self.select(run_name)
            fig = run.display_data_run(data_types, show_plot=False)
            plt.figure(fig.number)
            plt.savefig(run_name)
