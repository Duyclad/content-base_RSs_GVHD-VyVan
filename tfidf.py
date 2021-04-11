import pandas as pd 
# Reading user file:
u_cols =  ['user_id', 'age', 'sex', 'occupation', 'zip_code']
users = pd.read_csv('ml-100k/u.user', sep='|', names=u_cols,
 encoding='latin-1')

n_users = users.shape[0]
print ('Number of users:', n_users)
# users.head() #uncomment this to see some few examples



#Reading ratings file:
r_cols = ['user_id', 'movie_id', 'rating', 'unix_timestamp']

ratings_base = pd.read_csv('ml-100k/ua.base', sep='\t', names=r_cols, encoding='latin-1')
ratings_test = pd.read_csv('ml-100k/ua.test', sep='\t', names=r_cols, encoding='latin-1')

rate_train = ratings_base.to_numpy()
rate_test = ratings_test.to_numpy()

print ('Number of train rates:', rate_train.shape[0])
print ('Number of test rates:', rate_test.shape[0])



#Reading items file:
i_cols = ['movie id', 'movie title' ,'release date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
 'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

items = pd.read_csv('ml-100k/u.item', sep='|', names=i_cols,
 encoding='latin-1')

n_items = items.shape[0]


print ('Number of items:', n_items)



X0 = items.to_numpy()
X_train_counts = X0[:, -19:]
# print X0



#tfidf
from sklearn.feature_extraction.text import TfidfTransformer
transformer = TfidfTransformer(smooth_idf=True, norm ='l2')
tfidf = transformer.fit_transform(X_train_counts.tolist()).toarray()
"print (tfidf.shape)"




import numpy as np 
def get_items_rated_by_user(rate_matrix, user_id):
    """
    return (item_ids, scores)
    """
    y = rate_matrix[:,0] # all users
    # item indices rated by user_id
    # we need to +1 to user_id since in the rate_matrix, id starts from 1 
    # but id in python starts from 0
    ids = np.where(y == user_id +1)[0] 
    item_ids = rate_matrix[ids, 1] - 1 # index starts from 0 
    scores = rate_matrix[ids, 2]
    return (item_ids, scores)




from sklearn.linear_model import Ridge
from sklearn import linear_model

d = tfidf.shape[1] # data dimension
W = np.zeros((d, n_users))
b = np.zeros((1, n_users))
for n in range(n_users):    
    ids, scores = get_items_rated_by_user(rate_train, n)
    clf = Ridge(alpha=0.01, fit_intercept  = True)
    Xhat = tfidf[ids, :]
    
    clf.fit(Xhat, scores) 
    W[:, n] = clf.coef_
    b[0, n] = clf.intercept_




# predicted scores
Yhat = tfidf.dot(W) + b




"n = 100"
print('\nNhap id user can xem: ')
n = int(input())
np.set_printoptions(precision=2) # 2 digits after
ids, scores = get_items_rated_by_user(rate_test, n)
ids_t, scores_t = get_items_rated_by_user(rate_train, n)
"Yhat[n, ids]"
print ('\nRated movies ids - train:', ids_t) 
print ('\nRatings - train:', scores_t)
print ('\nRated movies ids - test:', ids)
print ('\nPredicted ratings:', Yhat[ids,n])
print ('\nTrue ratings - test:', scores)







from math import sqrt
def evaluate(Yhat, rates, W, b):
    se = 0
    cnt = 0
    for n in range(n_users):
        ids, scores_truth = get_items_rated_by_user(rates, n)
        scores_pred = Yhat[ids, n]
        e = scores_truth - scores_pred 
        se += (e*e).sum(axis = 0)
        cnt += e.size 
    return sqrt(se/cnt)

print ('\nRMSE for training:', evaluate(Yhat, rate_train, W, b))
print ('RMSE for test    :', evaluate(Yhat, rate_test, W, b))

input()
