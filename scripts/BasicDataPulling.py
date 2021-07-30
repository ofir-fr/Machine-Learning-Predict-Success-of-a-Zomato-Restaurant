"""""""""""
Zomata Project

"""""""""""

"""""""""""
Basic Data Pulling

"""""""""""



### Top 5 most votes restaurantes
### Top 5 least voted restaurantes

def topFive(popularity, Feature):
    
    topValues = popularity.sort_values(by=Feature, ascending=False).head(5)
    leastValues = popularity.sort_values(by=Feature, ascending=False).query(f'{Feature} > 0').tail(5)
    
    return topValues, leastValues


### data frame filter by max price, location, rating and food type

def restaurantsFiler(restaurantsDF, maxPrice, location, votesRate, foodType):

    filterRestaurantsIndex = (restaurantsDF['approx_cost(for two people)'] <= maxPrice) & (restaurantsDF['location'] == location) & (restaurantsDF['rate'] >= votesRate) & (restaurantsDF['rest_type'] == foodType)
    filteredRestaurants = restaurantsDF[filterRestaurantsIndex]
    return filteredRestaurants


### Translate adresses to geolocations
### Returns a new data frame with name and geolocation [lat and lon]

def restaurantesGeolocation (restaurantsDF):
    

    
    restaurantsGeolocation = pd.DataFrame({'Name':restaurantsDF['location'].unique()})
    
    lat=[]
    lon=[]
    
    for location in restaurantsGeolocation['Name']:
        location=geolocator.geocode(location)
        if location is None:
            lat.append(np.nan)
            lon.append(np.nan)
        else:
            lat.append(location.latitude)
            lon.append(location.longitude)
            
    restaurantsGeolocation['latitude'] = lat
    restaurantsGeolocation['longitude'] = lon
    
    return restaurantsGeolocation


### Returns a WordCloud object of top dishes by users based on restaurant type

def retrieveMealsWordCloud(zomatoDF, RestaurantType):
    
    from wordcloud import WordCloud, STOPWORDS
    
    if RestaurantType == 'all':
        restaurantWordsDF = zomatoDF                                          # use the entire DF
    elif zomatoDF['rest_type'].str.contains(RestaurantType).any():
        restaurantWordsDF = zomatoDF[zomatoDF['rest_type'] == RestaurantType] # unique Restaurant Type filtering of the DF
    else:
        return None                                          # restaurant type was not found
    
    dishes = ''                                              # list to individual dishes 
    
    for word in restaurantWordsDF['dish_liked'].dropna():    # scans all words for dishes   ; if the cell is empty, drop it
        wordsList = word.split()                             # split the words in the cells
        for i in range((len(wordsList))):
           wordsList[i] = wordsList[i].lower()               # reduce all letter to low case to avoide duplicates
        dishes = dishes +' '.join(wordsList)+' '             # merge words list
        
    stopwordsList = set(STOPWORDS)                           # list of stop words that we dont want to show in the word cloud
   
    return WordCloud(stopwords = stopwordsList, width = 1500, height = 1500).generate(dishes)        #generate and return the word cloud
    

### Returns a WordCloud object of top words in the reviews based on restaurant type

def retrieveReviewsWordCloud(zomatoDF, RestaurantType):
    
    from wordcloud import WordCloud, STOPWORDS
    
    if RestaurantType == 'all':
        reviewslistsDF = zomatoDF                                             # use the entire DF
    elif zomatoDF['rest_type'].str.contains(RestaurantType).any():
        reviewslistsDF = zomatoDF[zomatoDF['rest_type'] == RestaurantType]    # unique Restaurant Type filtering of the DF
    else:
        return None                                                           # restaurant type was not found

    totalReviews = ''

    for review in reviewslistsDF['reviews_list']:
        totalReviews = totalReviews + ' '.join(word for word in (str(review)).split() if len(word) >= 3)   # Accumulate all review words if >= 3 letters
        
    stopwordsList = set(STOPWORDS)      
   
    return WordCloud(stopwords = stopwordsList, width = 1500, height = 1500).generate(totalReviews)    
