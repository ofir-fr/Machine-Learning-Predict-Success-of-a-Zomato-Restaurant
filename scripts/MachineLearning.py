"""""""""""
Zomata Project: Machine Learning 

"""""""""""

# split the data to two categories: 
# new restaurant - 0 rate
# old restaurants with rating different then 0 for the trainning models 

def initiatorMachineLearning(zomatoDF, thresholdRating):

    newRestauransDF = zomatoDF[zomatoDF['rated']==0]

    trainTestRestaurantsDF = zomatoDF[zomatoDF['rated']==1]


    ### Creation of target:
    ### rating > thresholdRating for good reateurants and rating <= thresholdRating equals bad restaurants

   trainTestRestaurantsDF['target'] = trainTestRestaurantsDF.apply(lambda x:1 if x > threshold else 0)

   # New feature: total_cuisines - the amount of meal dishes in each restaurant
   trainTestRestaurantsDF['total_cuisines'] = trainTestRestaurantsDF['cuisines'].astype(str).apply(lambda x: len(x.split(',')))
      
   # New feature: multiple_rest_type - the amount of meal types in each restaurant
   trainTestRestaurantsDF['multiple_rest_type'] = trainTestRestaurantsDF['rest_type'].astype(str).apply(lambda x: len(x.split(',')))
   

    # Feature to be considered in the machien learning
    top_features=['online_order', 'book_table', 'location', 'rest_type',
       'approx_cost(for two people)', 'listed_in(type)', 'listed_in(city)', 'target',
       'total_cuisines', 'multiple_rest_type']
   
   reducedTrainTestRestaurantsDF = trainTestRestaurantsDF[top_features] 
    
   return reducedTrainTestRestaurantsDF
    
    
    
