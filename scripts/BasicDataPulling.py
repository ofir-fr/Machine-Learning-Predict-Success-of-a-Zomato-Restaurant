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
