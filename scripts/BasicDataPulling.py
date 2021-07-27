"""""""""""
Zomata Project

"""""""""""

"""""""""""
Basic Data Pulling

"""""""""""



### Top 5 most and least restaurantes of any feature in the dataframe

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

def restaurantesGeolocation(restaurantsDF):
    
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
    
    Return restaurantsGeolocation
    
    




