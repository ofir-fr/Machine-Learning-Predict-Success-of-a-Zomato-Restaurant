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
    
   trainTestRestaurantsDF['target'] = trainTestRestaurantsDF.apply(lambda x:i if x > threshold else 0)
    
    
    
    
    
