import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def get_similair_clients(client):

    clients_df = pd.read_csv('clients.csv')
    
    #print(clients_df.head())
    
    # Check for missing values
    #print("Missing values:",clients_df.isnull().values.any())
    
    # Create a function to combine the values of the columns into a single string
    def get_features(data):
        features=[]
        for i in range(0,data.shape[0]):
            features.append(data['Username'][i]+' '+data['Birthday'][i]+' '+str(data['Strength'][i])+' '+str(data['Endurance'][i])+' '+str(data['Mobility'][i])+' '+str(data['Combat-Sports'][i])+' '+str(data['Balance'][i])+' '+str(data['Weight-Loss'][i])+' '+str(data['Weight-Gain'][i]))
        
        return features
    
    clients_df['features_concat']=get_features(clients_df)
    
    #print(clients_df.head())
    
    # Convert Text Into Matrix
    cm = CountVectorizer().fit_transform(clients_df['features_concat'])
    
    # Get the cosine similarity
    cs = cosine_similarity(cm)
    #print(cs)
    
    #print(cs.shape)
    
    # Get the username of a username that the client likes
    client_uname = client
    
    # Get index of trainer
    client_index = clients_df[clients_df.Username == client_uname].index[0]
    #print(trainer_index)
    
    # Create list of enums for the similarities score
    scores = list(enumerate(cs[client_index]))
    
    # Sort the list
    sorted_scores = sorted(scores, key = lambda x:x[1], reverse = True)
    sorted_scores = sorted_scores[1:]
    
    #print(sorted_scores)
    similar_clients = []

    # return the top 3 trainers with a high recommendation
    i = 0

    for client in sorted_scores:
        similar_clients.append(clients_df.iloc[client[0]]['Username'])
        i += 1
        if i>3:
            break

    return similar_clients
