import numpy as np
import pandas as pd

def get_collaborative_recommendations(uname):
    print(uname)

    ratings = pd.read_csv('ratings.csv')

    print(ratings.head())

    trainers = pd.read_csv('trainers.csv')

    print(trainers.head())

    df = pd.merge(ratings,trainers,on="Username")

    print(df.head())

    ratings = pd.DataFrame(df.groupby('Username')['rating'].mean())

    ratings['num_ratings'] = pd.DataFrame(df.groupby('Username')['rating'].count())

    print('ratings')
    print(ratings.head())
    print('')

    matrix = df.pivot_table(index='client',columns=['Username'],values='rating')
    matrix.replace(np.nan,0)

    print('matrix')
    print(matrix.head())
    print('')

    ratings.sort_values('num_ratings',ascending=False).head()

    trainer_rating = matrix[uname]

    print('trainer_rating')
    print(trainer_rating.head())
    print('')

    similar_to_trainer = matrix.corrwith(trainer_rating)

    print('similar to trainer')
    print(similar_to_trainer.head())
    print('')

    corr_trainer = pd.DataFrame(similar_to_trainer,columns=['Correlations'])
    corr_trainer.dropna(inplace=True)

    print('corr_trainer')
    print(corr_trainer.head())
    print('')

    corr_trainer = corr_trainer.join(ratings['num_ratings'])

    corr_trainer = corr_trainer[corr_trainer['num_ratings']>1].sort_values('Correlations',ascending=False).head()

    recommended_trainers = []

    i = 0

    for index, row in corr_trainer.iterrows():
        recommended_trainers.append(index)
        i += 1
        if i>2:
            break

    print(' ')
    print(recommended_trainers)
    print(' ')
    return recommended_trainers
