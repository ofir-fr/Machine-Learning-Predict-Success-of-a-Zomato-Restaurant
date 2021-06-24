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






## tbc
