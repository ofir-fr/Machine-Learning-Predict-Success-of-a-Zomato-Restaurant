# -*- coding: utf-8 -*-
"""""""""""
Zomata Project

"""""""""""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

from DF_PreProcessing import *

zomatoDF = pd.read_csv('zomato.csv')

zomatoDF = zomataDFPreProcessing(zomatoDF)

print("Data Pre-processing is Done...")