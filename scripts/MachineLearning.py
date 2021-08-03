"""""""""""
Zomata Project: Machine Learning 

"""""""""""

# split the data to two categories: 
# new restaurant - 0 rate
# old restaurants with rating different then 0 for the trainning models 

def initiatorMachineLearning(zomatoDF):

    newRestauransDF = zomatoDF[zomatoDF['rated']==0]

    trainTestRestaurantsDF = zomatoDF[zomatoDF['rated']==1]