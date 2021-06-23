# -*- coding: utf-8 -*-
"""""""""""
Zomata Project

"""""""""""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

from DF_PreProcessing import *
from BasicDataPulling import *

zomatoDF = pd.read_csv('zomato.csv')                 # Database Import

zomatoDF = zomataDFPreProcessing(zomatoDF)           # Data Pre-processing

print("Data Pre-processing is Done...")

### Creat a new smaller DF with only votes, cost & rating for data analysis
ratingVotesCost = zomatoDF.groupby('name').agg({'votes':'sum', 'url':'count','approx_cost(for two people)':'mean','rate':'mean'})
ratingVotesCost.columns = ['total_votes','total_unities','ang_approx_cost','mean_rating']
ratingVotesCost['votes_per_unity'] = ratingVotesCost['total_votes']/ratingVotesCost['total_unities']
popularity = ratingVotesCost.sort_values(by='total_unities', ascending=False)


topVotes, leastVote = topFive(popularity)

sn.set()

fig, axes = plt.subplots(1,2,figsize=(10,5),sharey=True)

axes[0].set_title('Top 5 most voted')
sn.barplot(ax=axes[0],x=topVotes['total_votes'],y=topVotes.index)

axes[1].set_title('Top 5 least voted')
sn.barplot(ax=axes[1],x=leastVote['total_votes'],y=topVotes.index)
