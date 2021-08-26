"""""""""""
Zomata Project: PreProcessing 

"""""""""""

### Clean and organize raw data
def zomataDFPreProcessing(zomatoDF):

    import numpy as np
    import pandas as pd
    import re                           #  provides regular expression matching operations

    
    zomatoDF = pd.read_csv('zomato.csv')
    
    
    ### Creats a list of the features
    
    zomatoFeatureList= []
    for feature in zomatoDF.columns:
        if zomatoDF[feature].isnull().sum()>1:
            zomatoFeatureList.append(feature)
    
    
    ### Initial statues of the data
    #for feature in zomatoFeatureList:
    #    print("{} had {} % missing values".format(feature,np.round(zomatoDF[feature].isnull().sum()/len(zomatoDF)*100,2)))
    ###
    
    
    ### Transforms 'approx_cost(for two people)' from string to float by removing non-numeric values (',')
    
    zomatoDF["approx_cost(for two people)"] = zomatoDF["approx_cost(for two people)"].fillna("0")                                 # fills empty samples with the value 0
    zomatoDF["approx_cost(for two people)"]=zomatoDF["approx_cost(for two people)"].astype(str).apply(lambda x:x.replace(',','')) # remove ','
    zomatoDF["approx_cost(for two people)"]=zomatoDF["approx_cost(for two people)"].astype(float)                                 # convert to float
    
    
    ### Transform all non-uniform data in 'Rate' to '0/5'
    
    zomatoDF["rate"] = zomatoDF["rate"].fillna("0")                          # fills empty samples with the score 0
    zomatoDF["rate"] = zomatoDF["rate"].replace("NEW","0")                   # Converts new restaurant to grade 0
    zomatoDF["rate"] = zomatoDF["rate"].replace("-","0")                     # Converts the value '-' to 0
    zomatoDF["rate"] = zomatoDF["rate"].str.replace(" ","")                  # Remove redundant spaces
    
    
    ### Transing all 'Rate's to a value in the range of 0 to 100 by deviding the score in 5 and multiplying the result by 100
    
    SplitedRate= []
    for i in range(0,len(zomatoDF)):                                                                    # scanning the entire DF
        if zomatoDF["rate"][i] != "0":                                                                  # if sample value is not 0
            RateCalculator = zomatoDF["rate"][i].split("/")                                             # splitting the data between the score to the sum of '5'
            SplitedRate.append(np.round((float(RateCalculator[0])/float(RateCalculator[1]))*100,2))     # convert the value to a float
        else:
            SplitedRate.append(0)                                                                       # else appent 0 to the array
            
    zomatoDF["rate"].update(SplitedRate)                                    # update 'rate' with the new values
    zomatoDF["rate"] = zomatoDF["rate"].astype(float)                       # convert the array to float

    
    ### Add a new column to seperate new and old restaurants by their rating value.
    ### 0 rating equals to a new unrated restaurant

    def assign(x):
        if x > 0:
            return 1
        else:
            return 0
        
    zomatoDF['rated'] = zomatoDF['rate'].apply(assign)
    
    
    ### Removal of irrelevant text from the reviews

    cleanReviews= []
    for i in range(0,len(zomatoDF)):                                         # scanning the entire DF
        review = ''                                                     
        if zomatoDF['reviews_list'][i] != None: 
            review = zomatoDF['reviews_list'][i]                             # Retrive text from the cell and clean it
            review = review.lower()
            review = re.sub('[^a-zA-z]', ' ', review)
            review = re.sub('rated', ' ',review)
            review = re.sub('x', ' ',review)
            review = re.sub(' +', ' ',review)
            
            cleanReviews.append(str(review))                                # Append clean text into a new cell of process array of strings
            
        else:
            cleanReviews.append(None) 
            
    zomatoDF['reviews_list'].update(cleanReviews)                           # update 'reviews_list' with the new values



    return zomatoDF


### Define and organize existing and deducable features for better ML processing
# split the data to two categories: 
# new restaurant - 0 rate
# old restaurants with rating different then 0 for the trainning models 
def zomataDFReorganizing(zomatoDF, thresholdRating):

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
    
    reducedTrainTestRestaurantsDF.dropna(how='any',inplace=True)
    
    return reducedTrainTestRestaurantsDF





