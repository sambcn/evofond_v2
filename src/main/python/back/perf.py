import time as t
from back.utils import time_to_string
import pandas as pd

class Performance:
    """
    class used for storing times spent by each function using the decorator @measure_perf
    """
    dict_of_perf = dict()
    time_start = None
    time_end = None

    @staticmethod
    def get_perf_table():
        """
        return the table of the stored performances
        """
        if Performance.time_end == None:
            print("automatic stop of perf measure.")
            Performance.time_end = t.time()
        te = Performance.time_end
        ts = Performance.time_start
        df = pd.DataFrame({'method name':[], '% of the execution time':[], 'total time spent (s)':[], 'number of call':[], 'mean time spent by call (s)':[]})
        for key, value in Performance.dict_of_perf.items():
            new_row = {'method name':key, '% of the execution time':f"{100*(value[0]/(te-ts)):.2f}%", 'total time spent (s)':float(f"{value[0]:.8f}"), 'number of call':f"{value[1]}", 'mean time spent by call (s)':f"{value[0]/value[1]:.8f}"}
            # new_row = [key, f"{100*(value[0]/(te-ts)):.2f}%", float(f"{value[0]:.8f}"), f"{value[1]}", f"{value[0]/value[1]:.8f}"]
            df = df.append(new_row, ignore_index=True)
        return df

    @staticmethod
    def print_perf():
        ts = Performance.time_start
        te = Performance.time_end
        if ts == None:
            print("nothing measured")
        else:
            if te == None:
                print("automatic stop of perf measure.")
                Performance.time_end = t.time()
                te = Performance.time_end
            print(f"total time : {time_to_string(te-ts)} \n")
            df = Performance.get_perf_table()
            df.sort_values(by=['total time spent (s)'], inplace=True, ascending=False)
            # for key, value in Performance.dict_of_perf.items():
            #     table.add_row([key, f"{100*(sum(value)/(te-ts)):.2f}%", f"{sum(value):.2f}s", f"{len(value)}", f"{np.mean(value)}s"])
            print(df.to_string())

    @staticmethod
    def save_perf(filename):
        df = Performance.get_perf_table()
        df.sort_values(by=['total time spent (s)'], inplace=True, ascending=False)
        with open(filename, 'w') as f:
            f.writelines(f"total time = {Performance.time_end - Performance.time_start}\n")
            f.writelines(df.to_string())

    @staticmethod
    def start():
        Performance.time_start = t.time()

    @staticmethod
    def stop():
        Performance.time_end = t.time()

    @staticmethod
    def measure_perf(func):
        """
        decorator home-made in order to store time spent in the decorated method during the full execution
        """
        def wrapper(*args, **kargs):
            if Performance.time_start == None:
                return func(*args, **kargs)
            ts = t.time()
            result = func(*args, **kargs)
            te = t.time()
            if func.__name__ in Performance.dict_of_perf:
                Performance.dict_of_perf[func.__name__] = Performance.dict_of_perf[func.__name__][0]+(te-ts), Performance.dict_of_perf[func.__name__][1]+1
            else:
                Performance.dict_of_perf[func.__name__] = (te-ts), 1
            return result
        return wrapper
