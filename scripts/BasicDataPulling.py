"""""""""""
Zomata Project

"""""""""""

"""""""""""
Basic Data Pulling

"""""""""""



### Top 5 most votes restaurantes
### Top 5 least voted restaurantes
def topFive(popularity):
    
    topVotes = popularity.sort_values(by='total_votes', ascending=False).head(5)
    leastVote = popularity.sort_values(by='total_votes', ascending=False).query('total_votes > 0').tail(5)
    
    return topVotes, leastVote






## tbc