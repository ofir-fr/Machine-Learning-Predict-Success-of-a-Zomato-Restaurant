
"""""""""""
Zomata Project

"""""""""""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import re                           #  provides regular expression matching operations

#!pip install geopy
from geopy.geocoders import Nominatim
#!pip install folium
import folium
from folium.plugins import HeatMap
#!pip install wordcloud
from wordcloud import WordCloud, STOPWORDS

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
    
    
    ### Extract and present top&least 5 restaurants by quantity of votes
   
    topVotes, leastVote = topFive(popularity, 'total_votes')
    
    sn.set()
    
    fig, axes = plt.subplots(1,2,figsize=(10,5),sharey=True)
    
    axes[0].set_title('Top 5 most voted')
    sn.barplot(ax=axes[0],x=topVotes['total_votes'],y=topVotes.index)
    
    axes[1].set_title('Top 5 least voted')
    sn.barplot(ax=axes[1],x=leastVote['total_votes'],y=topVotes.index)
    
    
    ### Extract and present top&least 5 restaurants by Meal price

    topPrice, leastPrice = topFive(popularity, 'avg_approx_cost')
    
    sn.set()
    
    fig, axes = plt.subplots(1,2,figsize=(10,5),sharey=True)
    
    axes[0].set_title('Top 5 expensive')
    sn.barplot(ax=axes[0],x=topPrice['avg_approx_cost'],y=topPrice.index)
    
    axes[1].set_title('Top 5 least expensive')
    sn.barplot(ax=axes[1],x=leastPrice['avg_approx_cost'],y=leastPrice.index)
    
    ### How many restaurants offer table booking?
    
    axes[0].set_title('Online booking availability')
    axes[0] = plt.subplot2grid((1,2),(0,0))
    plt.pie(zomatoDF['book_table'].value_counts(), labels = ['cannot book', 'can book'], autopct='%1.0f%%')  # Pie chart showing table booking availability of the restaurants
    
    
    ### How many restaurants offer online orders?
    
    axes[1].set_title('Online ordering availability')
    axes[1] = plt.subplot2grid((1,2),(0,1))
    plt.pie(zomatoDF['online_order'].value_counts(), labels = ['accept orders', 'do not accept orders'], autopct='%1.0f%%')  # Pie chart showing online oders availability of the restaurants
    
    ### Best budget restaurant
    
    budgetRestaurants = restaurantsFiler(zomatoDF, 400, 'BTM', 4, 'Quick Bites')
    budgetRestaurants['name'].unique()

    ### Generate Geolocation map of the restaurants
   
    geolocator = Nominatim(user_agent='app')                     # geolocator class object
    data = geolocator.geocode(zomatoDF['name'][0])               # geoPosition object
    restaurantsLocations = restaurantesGeolocation(zomatoDF)     # Calls function 'restaurantesGeolocation' that returns geolocation of all restaurants on the DF
    restaurantsLocations = restaurantsLocations.dropna()         # Remove unfound restaurants from the locations DF - note: investigate why restaurant was nto found
    
    Basemap = folium.Map(location=[12.97,77.59])                                        # Initial positioning of the map in the gloab
    HeatMap(data = restaurantsLocations[['latitude','longitude']]).add_to(Basemap)      # Add restaurant locations to the map
    Basemap                                                                             # Show map


    ### Generate words analyser to identify the most common meals
   
    restaurantTypeWords = input("Restaurant type ('all' = no filtering): ")             # ask user for restaurant type
    zomatoMealsWordCloud = retrieveMealsWordCloud(zomatoDF, restaurantTypeWords)             # Call word cloud generator function with relevant DF and restaurant type    
    if zomatoWordCloud == None:                                                         # If restaurant type is not availble an error will return
        print('error occured')
    else:
        plt.axis('off')                                                                 # Turn off graph axis
        plt.imshow(zomatoWordCloud)                                                     # Generate word cloud image


    ### Generate words analyser to identify the most common review comments

    restaurantTypeWords = input("Restaurant type ('all' = no filtering): ")             # ask user for restaurant type
    zomatoReviewsMealsWordCloud = retrieveReviewsWordCloud(zomatoDF, restaurantTypeWords)             # Call word cloud generator function with relevant DF and restaurant type    
    if zomatoReviewsMealsWordCloud == None:                                                         # If restaurant type is not availble an error will return
        print('error occured')
    else:
        plt.axis('off')                                                                 # Turn off graph axis
        plt.imshow(zomatoReviewsMealsWordCloud)                                                     # Generate word cloud image   
    
    
    ####################################
    ### Final reorganizing of the DF ###
    ####################################

    
    trainTestRestaurantsDF = zomataDFReorganizing(zomatoDF, 75, 0.4):                                                # prepare target data with 1/0 for old and new restaurants
    plt.pie(trainTestRestaurantsDF['target'].value_counts(),labels=trainTestRestaurantsDF['target'].value_counts().index) # examine if the groups are balanced

    
    # Seperate numerice and non-numeric features
    objectFeaturesList = [column for column in reducedTrainTestRestaurantsDF.columns if reducedTrainTestRestaurantsDF[column].dtype=='O']
    numericalFeaturesList = [column for column in reducedTrainTestRestaurantsDF.columns if reducedTrainTestRestaurantsDF[column].dtype!='O']

    for feature in objectFeaturesList:
      print('{} has totayl {} unique features'.format(feature,reducedTrainTestRestaurantsDF[feature].nunique()))
    
    ###########################################
    ### initiate Machine Learning(zomatoDF) ###
    ###########################################    

    
    
    
    
    
if __name__ == "__main__":
    main()
