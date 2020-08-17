import numpy as np
from scipy.stats import t as qt

def print_stats(micro_list, macro_list):
    folds = len(micro_list)
    med_mic = np.mean(micro_list)*100
    error_mic = abs(qt.isf(0.975,df=(folds-1)))*np.std(micro_list,ddof=1)/np.sqrt(len(micro_list))*100
    med_mac = np.mean(macro_list)*100
    error_mac = abs(qt.isf(0.975,df=(folds-1)))*np.std(macro_list,ddof=1)/np.sqrt(len(macro_list))*100
    print("Micro\tMacro")
    print("{:.2f}({:.2f})\t{:.2f}({:.2f})".format(med_mic,error_mic,med_mac,error_mac))
    #return med_mic,error_mic,med_mac,error_mac