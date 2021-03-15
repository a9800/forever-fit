#Content-Based Recommender System
import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def content_based_recommendation(liked_trainer):

    trainers_df = pd.read_csv('trainers.csv')
    
    #print(trainers_df.head())
    
    # Check for missing values
    #print("Missing values:",trainers_df.isnull().values.any())
    
    # Create a function to combine the values of the columns into a single string
    def get_features(data):
        features=[]
        for i in range(0,data.shape[0]):
            features.append(data['Username'][i]+' '+data['Birthday'][i]+' '+str(data['Strength'][i])+' '+str(data['Endurance'][i])+' '+str(data['Mobility'][i])+' '+str(data['Combat-Sports'][i])+' '+str(data['Balance'][i])+' '+str(data['Weight-Loss'][i])+' '+str(data['Weight-Gain'][i]))
        
        return features
    
    trainers_df['features_concat']=get_features(trainers_df)
    
    #print(trainers_df.head())
    
    # Convert Text Into Matrix
    cm = CountVectorizer().fit_transform(trainers_df['features_concat'])
    
    # Get the cosine similarity
    cs = cosine_similarity(cm)
    #print(cs)
    
    #print(cs.shape)
    
    # Get the username of a username that the client likes
    trainer_uname = liked_trainer
    
    # Get index of trainer
    trainer_index = trainers_df[trainers_df.Username == trainer_uname].index[0]
    #print(trainer_index)
    
    # Create list of enums for the similarities score
    scores = list(enumerate(cs[trainer_index]))
    
    # Sort the list
    sorted_scores = sorted(scores, key = lambda x:x[1], reverse = True)
    sorted_scores = sorted_scores[1:]
    
    print(sorted_scores)
    recommended_trainers = []

    # return the top 3 trainers with a high recommendation
    i = 0

    for trainer in sorted_scores:
        recommended_trainers.append(trainers_df.iloc[trainer[0]]['Username'])
        i += 1
        if i>2:
            break

    return recommended_trainers
