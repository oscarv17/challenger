import sys
sys.path.append('../dataPreparation')
sys.path.append('../getData')
from dataPreparation import user_item
import pandas as pd
import numpy as np
from sklearn.model_selection import RepeatedKFold,train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import precision_score, mean_squared_error
from scipy.sparse import csr_matrix
from math import sqrt

# split data
train_set, test_set = train_test_split(user_item, test_size=0.30, random_state=100)

train_set_aux=csr_matrix(train_set.values)
train_set_aux

#model 1


similarity=cosine_similarity(train_set_aux)

def prediction(users, similarity):
    pred = similarity.dot(users) / np.array([np.abs(similarity).sum(axis=1)]).T
    return pred


recommendations=prediction(train_set.values, similarity)


print(recommendations)

pd.DataFrame(recommendations).head()

#Eval 1
def calculate_target_set(val_set):
    target = np.zeros(val_set.shape)
    val_set_aux = val_set.copy()
    for user in range(val_set.shape[0]):
        if(len(val_set[user, :].nonzero()[0]) > 1):
            rats = np.random.choice(val_set[user, :].nonzero()[0], replace=False)
            val_set_aux[user, rats] = 0.
            target[user, rats] = val_set[user, rats]
    return val_set_aux, target

test_set_b, target_set = calculate_target_set(test_set.values)

test_set_aux=csr_matrix(test_set_b)
test_set_aux

similarity_val=cosine_similarity(test_set_aux)

recommendations_val=prediction(test_set_b, similarity_val)

sqrt(mean_squared_error(target_set[target_set.nonzero()], recommendations_val[target_set.nonzero()]))

mean_squared_error(target_set[target_set.nonzero()], recommendations_val[target_set.nonzero()])

# split data
train_set, test_set = train_test_split(user_item, test_size=0.30, random_state=2000)

train_set_aux=csr_matrix(train_set.values)
train_set_aux

similarity_2=cosine_similarity(train_set_aux)

def prediction_general(user, similarity):
    rating_means = user.mean(axis=1)
    mean_diff = (user - rating_means[:,np.newaxis])
    pred = rating_means[:,np.newaxis] + similarity.dot(mean_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
    return pred

recommendations_2 = prediction_general(train_set.values, similarity_2)

pd.DataFrame(recommendations_2)


# Eval 2

test_set_c, target_set = calculate_target_set(test_set.values)

test_set_aux=csr_matrix(test_set_c)
test_set_aux

similarity_eval_2=cosine_similarity(test_set_aux)

recommendations_eval_2=prediction_general(test_set_b, similarity_eval_2)

sqrt(mean_squared_error(target_set[target_set.nonzero()], recommendations_eval_2[target_set.nonzero()]))

mean_squared_error(target_set[target_set.nonzero()], recommendations_eval_2[target_set.nonzero()])

