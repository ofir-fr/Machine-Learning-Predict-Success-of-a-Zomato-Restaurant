"""""""""""
Zomata Project: Machine Learning 

"""""""""""

### Function returns x_train, x_test, y_train, y_test by users test size and random state parameters

  
def prepareTrainTestSplit(finalZomatoDF, testSize, randomState):

    x = finalZomatoDF.drop('target', axis=1)
    y = finalZomatoDF['target']
      
    x_train, x_test, y_train, y_test =  train_test_split(x, y, test_size = testSize, random_state = randomState47)
    
   return x_train, x_test, y_train, y_test


