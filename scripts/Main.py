
"""""""""""
Zomata Project

"""""""""""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

#!pip install geopy
from geopy.geocoders import Nominatim

from DF_PreProcessing import *
from BasicDataPulling import *

def main():
    zomatoDF = pd.read_csv('zomato.csv')                 # Database Import
    
    zomatoDF = zomataDFPreProcessing(zomatoDF)           # Data Pre-processing
    
    print("Data Pre-processing is Done...")
    
    ### Creat a new smaller DF with only votes, cost & rating for data analysis
    ratingVotesCost = zomatoDF.groupby('name').agg({'votes':'sum', 'url':'count','approx_cost(for two people)':'mean','rate':'mean'})
    ratingVotesCost.columns = ['total_votes','total_unities','avg_approx_cost','mean_rating']
    ratingVotesCost['votes_per_unity'] = ratingVotesCost['total_votes']/ratingVotesCost['total_unities']
    popularity = ratingVotesCost.sort_values(by='total_unities', ascending=False)
    
    
    # Extract and present top&least 5 restaurants by quantity of votes
    topVotes, leastVote = topFive(popularity, 'total_votes')
    
    sn.set()
    
    fig, axes = plt.subplots(1,2,figsize=(10,5),sharey=True)
    
    axes[0].set_title('Top 5 most voted')
    sn.barplot(ax=axes[0],x=topVotes['total_votes'],y=topVotes.index)
    
    axes[1].set_title('Top 5 least voted')
    sn.barplot(ax=axes[1],x=leastVote['total_votes'],y=topVotes.index)
    
    
    # Extract and present top&least 5 restaurants by Meal price
    topPrice, leastPrice = topFive(popularity, 'avg_approx_cost')
    
    sn.set()
    
    fig, axes = plt.subplots(1,2,figsize=(10,5),sharey=True)
    
    axes[0].set_title('Top 5 expensive')
    sn.barplot(ax=axes[0],x=topPrice['avg_approx_cost'],y=topPrice.index)
    
    axes[1].set_title('Top 5 least expensive')
    sn.barplot(ax=axes[1],x=leastPrice['avg_approx_cost'],y=leastPrice.index)
    
    # How many restaurants offer table booking?
    axes[0].set_title('Online booking availability')
    axes[0] = plt.subplot2grid((1,2),(0,0))
    plt.pie(zomatoDF['book_table'].value_counts(), labels = ['cannot book', 'can book'], autopct='%1.0f%%')  # Pie chart showing table booking availability of the restaurants
    
    
    ### How many restaurants offer online orders?
    axes[1].set_title('Online ordering availability')
    axes[1] = plt.subplot2grid((1,2),(0,1))
    plt.pie(zomatoDF['online_order'].value_counts(), labels = ['accept orders', 'do not accept orders'], autopct='%1.0f%%')  # Pie chart showing online oders availability of the restaurants
    
    ### Best budget restaurant
    budgetRestaurants = restaurantsFiler(zomatoDF, 400, 'BTM', 4, 'Quick Bites'):
    budgetRestaurants['name'].unique()


 
if __name__ == "__main__":
    main()
