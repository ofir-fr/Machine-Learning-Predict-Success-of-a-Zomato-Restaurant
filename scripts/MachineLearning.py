"""""""""""
Zomata Project: Machine Learning 

"""""""""""

### Random forest function receives: DF, test size and random state
### Function returns predictions arrays, the confusion matrix of the test and its accuracy score

def applyRandomForest(finalZomatoDF, testSize, randomState):

    x = finalZomatoDF.drop('target', axis=1)
    y = finalZomatoDF['target']
    
    
    
    x_train, x_test, y_train, y_test =  train_test_split(x, y, test_size = testSize, random_state = randomState47)
    
    model = RandomForestClassifier()
    
    model.fit(x_train, y_train)
    
    predictions = model.predict(x_test)
    
   return predictions, confusion_matrix(predictions, y_test), accuracy_score(predictions, y_test)
    
