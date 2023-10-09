import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import pylab

import warnings
warnings.filterwarnings('ignore')

from scipy.stats import norm
from scipy import stats

from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder

from sklearn.cluster import KMeans
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.decomposition import PCA
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from joblib import dump, load
from statsmodels.tsa.seasonal import seasonal_decompose

import time
from tqdm.autonotebook import tqdm

import seaborn as sns

from lightgbm import LGBMRegressor
import lightgbm
from tslearn.clustering import TimeSeriesKMeans
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    make_scorer)
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from catboost import CatBoostRegressor
from datetime import datetime, timedelta

"""## Функции"""

# метрика для оценки работы модели
def wape(y_true: np.array, y_pred: np.array):
    return np.sum(np.abs(y_true-y_pred))/np.sum(np.abs(y_true))

# формируем временные ряды для среза магазин-товар
def  ts_st_sku(sales_df_train):
    st_id_unique = sales_df_train['st_id'].unique()
    sales_df_train['date'] = pd.to_datetime(sales_df_train['date'])
    #sales_df_train_2 = sales_df_train[sales_df_train['pr_sales_type_id'] ==0].copy()
    sales_df_train_2 = sales_df_train.copy()

    # смотрим только продажи без акций
    sales_df_train_2 = sales_df_train_2[sales_df_train_2['pr_sales_type_id'] == 0]


    sales_df_train_2 =sales_df_train_2[['st_id', 'pr_sku_id','date',  'pr_sales_in_units']]


    TimeSeries_df = pd.DataFrame( )
    data_time_series = []
    for i in st_id_unique:
        data = sales_df_train_2[sales_df_train_2['st_id'] ==i].copy()
        pr_sku_id_unique = data['pr_sku_id'].unique()
        for j in pr_sku_id_unique:
          data1 = data[data['pr_sku_id'] == j].copy()
          data1 = data1[['date', 'pr_sales_in_units']]
          data1.index =data1['date']
          data1.index = data1.index.copy()
          data1 = data1.resample('1D').first()
          data1 = data1.drop(columns = 'date', axis = 1)
          data2 = data1.T
          data2['st_id'] = i
          data2['pr_sku_id'] = j
          columns_df = data2.columns
          data2.index = data2['st_id'] + data2['pr_sku_id']
          data_time_series.append(data2)
          #TimeSeries_df = TimeSeries_df.append(data2)
          #TimeSeries_df = TimeSeries_df.append(data_time_series[len(data_time_series)-1])

    TimeSeries_df = pd.DataFrame( columns = columns_df )
    for i in range(len(data_time_series)):
        TimeSeries_df = TimeSeries_df.append(data_time_series[i])
        #imeSeries_df = pd.DataFrame(data_time_series, columns = columns )
        TimeSeries_df = TimeSeries_df.fillna(0)

    return TimeSeries_df

# для выбронного количества кластеров обучаем kmeans
def kmeans_st_pred(TimeSeries_df, k, metric_):
    n_clusters = k
    scaler = StandardScaler()
    TimeSeries_df = TimeSeries_df.drop(columns = ['st_id','pr_sku_id' ], axis = 1)
    tickers_scaled = scaler.fit_transform(TimeSeries_df)
    ts_kmeans = TimeSeriesKMeans(n_clusters=n_clusters, metric=metric_, n_jobs=3, max_iter=10, random_state = 1234)
    ts_kmeans.fit(tickers_scaled)
    TimeSeries_df_2 = TimeSeries_df.copy()
    TimeSeries_df['cluster'] = ts_kmeans.predict(tickers_scaled)
    #st_id = TimeSeries_df['st_id'].unique()
    #pr_sku_id = TimeSeries_df['pr_sku_id'].unique()
    data_cluster = pd.DataFrame(index = TimeSeries_df.index)
    data_cluster['cluster'] = ts_kmeans.predict(tickers_scaled)
    return data_cluster,ts_kmeans.cluster_centers_

# Формируем признаки даты: год, месяц, неделя, день (пункт 4.1)
def year_month_week(data):
    data['year'] = pd.to_datetime(data['date'], utc=True).dt.year
    data['month'] = pd.to_datetime(data['date'], utc=True).dt.month
    data['week'] = pd.to_datetime(data['date'], utc=True).dt.dayofweek
    data['day'] = pd.to_datetime(data['date'], utc=True).dt.day

    return data

# присваиваем номер кластера
def give_cluster_ts(x):
    #data_cluster = kmeans_st_pred(tickers_scaled, 6)
    try:
       cluster = list(data_cluster.loc[data_cluster.index == x, 'cluster'])[0]
    except:
       cluster = -1
    return cluster

# топ товаров и магазинов
def likvid(train):
  top_pr_sku_id = train.groupby(['pr_sku_id'])['date'].nunique().sort_values(ascending =False)
  top_st_revenue = train.groupby('st_id')['pr_sales_in_units'].sum().sort_values(ascending = False)
  return top_pr_sku_id, top_st_revenue

# формируем сдвиг и среднее
def make_features(data_):
    max_lag = 28
    rolling_mean_size = 28
    data = data_.copy()

    # проверка качества
    #data = data[data['pr_sales_type_id'] == 0]

    data = data.groupby('date')['pr_sales_in_units'].mean()

    data.sort_index(inplace=True)
    data = data.resample('1D').median()
    data = data.fillna(0)
    #data.index = pd.to_datetime(data.index)

    decomposed = seasonal_decompose(data)


    data_new = pd.DataFrame(data)

    for lag in range(1, max_lag + 1):
        data_new['lag_{}'.format(lag)] = data.shift(lag)
        #data_new['lag_{}'.format(lag)] = is_it_int_2(data_new['lag_{}'.format(lag)])

    data_new['rolling_mean'] = data.rolling(rolling_mean_size, closed = 'left').mean()
    data_new['trend']  =  decomposed.trend
    data_new['seasonal']  = decomposed.seasonal
    data_new = data_new.fillna(0)
    #data_new = is_it_int(data_new)
    return data_new

def mada_log(sales_df_train_10):
    sales_df_train_20 = sales_df_train_10.copy()
    data_all = []
    cluster_st = sales_df_train_20['cluster_st'].unique()

    for i in cluster_st:
        data = sales_df_train_20[sales_df_train_20['cluster_st'] == i]
        data_new = make_features(data)
        data_new = data_new.drop(columns = ['pr_sales_in_units'])
        #columns = data_new.columns

        sales_df_train_21 = pd.merge(data,  data_new, how='left', left_on='date', right_on='date')
        data_all.append(sales_df_train_21)

    columns_df =  data_all[0].columns
    data_all_df = pd.DataFrame( columns = columns_df )
    for i in range(len(cluster_st)):
            data_all_df = data_all_df.append(data_all[i])
            data_all_df = data_all_df.fillna(0)

    return data_all_df

# определяем фичи для трейна
def make_features_train(train,k, metric_, holidays_covid_calendar):
  train_ = train.copy()
  sales_df_train_neg_sales = sales_df_train[(sales_df_train['pr_sales_in_units'] <= 0) |
                           (sales_df_train['pr_sales_in_rub'] <= 0)]
  train_ = train_[~(train_.index.isin(sales_df_train_neg_sales.index))]
  train_ = train_.drop(columns = ['pr_promo_sales_in_units',	'pr_promo_sales_in_rub'], axis = 1)
  TimeSeries_df = ts_st_sku(train_)
  data_cluster, centers = kmeans_st_pred(TimeSeries_df, k, metric_)

  train_['date'] = pd.to_datetime(train_['date'])
  train_['st_id_pr_sku_id'] = train_['st_id']+train_['pr_sku_id']
  train_['cluster_st'] = train_['st_id_pr_sku_id'].apply(give_cluster_ts)

  # Вытащим день недели, год, месяц, день
  train_ = year_month_week(train_)
  #Добавим маркер праздника
  holidays_covid_calendar['date'] = pd.to_datetime(holidays_covid_calendar['date'])
  holidays_calendar = holidays_covid_calendar[holidays_covid_calendar['holiday'] ==1]
  train_['holiday'] = 0
  train_.loc[train_['date'].isin(list(holidays_calendar['date'])), 'holiday'] = 1
  # ликвидность
  top_pr_sku_id, top_st_revenue= likvid(train_)
  train_['liquidity'] = 0
  train_.loc[train_['pr_sku_id'].isin(list((top_pr_sku_id>350).index)), 'liquidity'] = 2
  train_.loc[train_['pr_sku_id'].isin(list((top_pr_sku_id>50).index)), 'liquidity'] = 1
  train_['top_st_revenue'] = 0
  train_.loc[train_['top_st_revenue'].isin(list((top_st_revenue>400000).index)), 'top_st_revenue'] = 2
  train_.loc[train_['top_st_revenue'].isin(list((top_st_revenue>100000).index)), 'top_st_revenue'] = 1
  train_ = mada_log(train_)
  #train_ = lag_mean_2(train_, TimeSeries_df)
  return train_, data_cluster

# определяем фичи для тест
def make_features_test(test, data_cluster, holidays_covid_calendar, train_):
  test_ = test.copy()
  test_['date'] = pd.to_datetime(test_['date'])
  test_['st_id_pr_sku_id'] = test_['st_id']+test_['pr_sku_id']

  test_ = year_month_week(test_)
  #Добавим маркер праздника
  holidays_covid_calendar['date'] = pd.to_datetime(holidays_covid_calendar['date'])
  holidays_calendar = holidays_covid_calendar[holidays_covid_calendar['holiday'] ==1]
  test_['holiday'] = 0
  test_.loc[test_['date'].isin(list(holidays_calendar['date'])), 'holiday'] = 1
  # ликвидность
  top_pr_sku_id, top_st_revenue= likvid(train_)
  test_['liquidity'] = 0
  test_.loc[test_['pr_sku_id'].isin(list((top_pr_sku_id>350).index)), 'liquidity'] = 2
  test_.loc[test_['pr_sku_id'].isin(list((top_pr_sku_id>50).index)), 'liquidity'] = 1
  test_['top_st_revenue'] = 0
  test_.loc[test_['top_st_revenue'].isin(list((top_st_revenue>400000).index)), 'top_st_revenue'] = 2
  test_.loc[test_['top_st_revenue'].isin(list((top_st_revenue>100000).index)), 'top_st_revenue'] = 1


  # Формируем сдвиг по кластеру
  # метка для разделения обучающего и тестовго набора
  test_['split'] = 'test'

  # обучающий набор
  train_['st_id_pr_sku_id'] = train_['st_id'] + train_['pr_sku_id']
  train_['cluster_st'] = train_['st_id_pr_sku_id'].apply(give_cluster_ts)
  train_ = train_.drop(columns = ['pr_promo_sales_in_units',	'pr_promo_sales_in_rub'], axis = 1)
  train_['split'] = 'train'
  train_['true_sku'] = 0

  test_2 = test_[test_['pr_sku_id'].isin(train_['pr_sku_id'].unique())]
  # метка для выделения товаров, которых нет в обучающих данных
  test_2['true_sku'] = -1

  # товары, информации по которым не было в трейне
  test_3 =test_[~(test_['pr_sku_id'].isin(train_['pr_sku_id'].unique()))]
  # test_[~(test_['st_id_pr_sku_id'].isin(data_cluster.index))]
  #test_3['cluster_st'] = -1
  new_pr_sku_id = test_without_sku(test_3, pr_df, train_)

  test_3 = pd.merge(test_3, new_pr_sku_id, how = 'left', left_on = 'st_id_pr_sku_id', right_on='st_id_pr_sku_id')
  test_3['true_sku'] = test_3['true_sku'].fillna(0)
  test_3['new_sku'] = test_3['new_sku'].fillna(0)
  test_3['pr_sku_id'] = test_3.apply(lambda  x: x.pr_sku_id if x.new_sku == 0 else x.new_sku, axis=1)
  test_3['st_id_pr_sku_id'] =  test_3['st_id']+test_3['pr_sku_id']
  test_3 = test_3.drop(columns = ['new_sku'], axis = 1)



  test_2= test_2.append(test_3, ignore_index = True)
  test_2['cluster_st'] = test_2['st_id_pr_sku_id'].apply(give_cluster_ts)

  train_2 =train_.append(test_2)

  train_2['date'] = pd.to_datetime(train_2['date'])

  train_2 = mada_log(train_2)
  test_2_ = train_2[train_2['split'] == 'test']
  test_2_ = test_2_.fillna(0)
  test_2_ = test_2_.drop(columns = 'split', axis = 1)
  return test_2_

def train_model_day(sales_df_train, st_df, pr_df,holidays_covid_calendar):
    # подготовка обучающего датасета
    train = pd.merge(sales_df_train, st_df, how='left', left_on='st_id', right_on='st_id')
    train_ = pd.merge(train, pr_df, how='left', left_on='pr_sku_id', right_on='pr_sku_id')
    train_, data_cluster = make_features_train(train_, 8, 'euclidean', holidays_covid_calendar)



     # разделение на таргет/фичу
    features = train_.drop(columns = ['pr_sales_in_units', 'pr_sales_in_rub',  'date',  'st_is_active'], axis = 1)
    target = train_['pr_sales_in_units']
    #  категориальные столбцы
    cat_features6 = features.select_dtypes(include='object').columns.to_list()+ ['cluster_st'] + ['year', 'month', 'week', 'day','holiday', 'liquidity', 'top_st_revenue']
    features[cat_features6] = features[cat_features6].astype('category')

    models_day = []
    wape_day = []

    for i in range(1, 15):
          day = train_['date'].max() + timedelta(days = i)

          #Каждая модель подавалась на гридсерч с кросс-валидацией 5 - лучшие параметры каждой модели learning_rate = 0.03, num_leaves =521, n_estimators =300
          model_day = LGBMRegressor(learning_rate = 0.03, num_leaves =521, n_estimators =300)

          features_day = features.copy()
          if i>1:
            for lag in range(1, i):
                    columns ='lag_{}'.format(lag)
                    features_day = features_day.drop(columns = columns, axis = 1)
          model_day.fit(features_day, target)
          predict = model_day.predict(features_day)
          w_day =wape(target, predict)
          models_day.append(model_day)
          wape_day.append(w_day)
          #filename = 'model_lgbm_{}.sav'.format(i)
          #model_day.booster_.save_model(filename)

    return models_day, wape_day, data_cluster

def test_without_sku(test_with_no_sku_, pr_df, train_):

    df_old_sku = test_with_no_sku_.groupby('st_id_pr_sku_id')['pr_sku_id', 'st_id'].agg('first')
    df_old_sku['st_id_pr_sku_id'] = df_old_sku.index
    df_old_sku = pd.merge(df_old_sku, pr_df, how='left', left_on='pr_sku_id', right_on='pr_sku_id')
    new_pr_sku_id = []
    for i, row in df_old_sku.iterrows():
        true_sku =row['pr_sku_id']
        sub = row['pr_subcat_id']
        cat = row['pr_cat_id']
        st =  row['st_id']
        group = row['pr_group_id']
        st_id_pr_sku_id = row['st_id_pr_sku_id']
        try:
            new_sku =  train_[(train_['st_id'] == st) & (train_['pr_subcat_id'] == sub)]['pr_sku_id'].value_counts().sort_values(ascending = False).index[0]
        except:
            try:
                new_sku =  train_[(train_['st_id'] == st) & (train_['pr_cat_id'] == cat)]['pr_sku_id'].value_counts().sort_values(ascending = False).index[0]
            except:
                new_sku =  train_[(train_['st_id'] == st) & (train_['pr_group_id'] == group)]['pr_sku_id'].value_counts().sort_values(ascending = False).index[0]
        new_pr_sku_id.append([true_sku,st_id_pr_sku_id,new_sku])



    new_pr_sku_id = pd.DataFrame(new_pr_sku_id, columns = ['true_sku', 'st_id_pr_sku_id', 'new_sku'])
    return new_pr_sku_id

def predict_days(model_best,data_cluster,sales_df_train,  sales_submission, st_df, pr_df,holidays_covid_calendar ):
    ## подготовка обучающего датасета
    train = pd.merge(sales_df_train, st_df, how='left', left_on='st_id', right_on='st_id')
    train['date'] = pd.to_datetime(train['date'])
    train_ = pd.merge(train, pr_df, how='left', left_on='pr_sku_id', right_on='pr_sku_id')
    #train_, data_cluster = make_features_train(train, 8, 'euclidean', holidays_covid_calendar)

    # подготовка тестовго датасета
    test_ = sales_submission.copy()
    test_.columns = test_.columns.str.replace('target', 'pr_sales_in_units')
    test_ = pd.merge(test_, st_df, how='left', left_on='st_id', right_on='st_id')
    test_ = pd.merge(test_, pr_df, how='left', left_on='pr_sku_id', right_on='pr_sku_id')
    test_ = make_features_test(test_, data_cluster, holidays_covid_calendar, train_)

    #  подготовка таблицы выходных данных
    sales_submission['date'] = pd.to_datetime(sales_submission['date'])

    #  категориальные столбцы

     # разделение на таргет/фичу
    #features = train_.drop(columns = ['pr_sales_in_units', 'pr_sales_in_rub',  'date',  'st_is_active'], axis = 1)
    #target = train_['pr_sales_in_units']
    #cat_features6 = features.select_dtypes(include='object').columns.to_list()+ ['cluster_st'] + ['year', 'month', 'week', 'day','holiday', 'liquidity', 'top_st_revenue']
    #features[cat_features6] = features[cat_features6].astype('category')



    features_test =  test_.drop(columns = ['pr_sales_in_units',  'date',  'st_is_active', 'true_sku',  'pr_sales_in_rub'], axis = 1)
    #features_test =features_test.drop(columns =['pr_group_id', 'pr_cat_id', 'pr_subcat_id',
    #   'pr_uom_id'])
    true_sku = test_['true_sku']
    cat_features6 = features_test.select_dtypes(include='object').columns.to_list()+ ['cluster_st'] + ['year', 'month', 'week', 'day','holiday', 'liquidity', 'top_st_revenue']
    target_test = test_['pr_sales_in_units']
    features_test[cat_features6] = features_test[cat_features6].astype('category')
    #print(features_test.columns)
    # подготовка таблицы выходных данных
    sales_columns = list(sales_submission.columns)
    sales_columns.append('true_sku')
    sales_submission_out = pd.DataFrame(columns = sales_columns)

    # перебор моделей
    columns = []
    for i in range(1, 15):
          model = model_best[i-1]
          day = train['date'].max() + timedelta(days = i)
          #features_day = features.copy()

          if i>1:
              for lag in range(1, i):
                      columns.append('lag_{}'.format(lag))
          #features_day = features_day.drop(columns = columns, axis = 1)
          features_test_day = features_test.drop(columns = columns, axis = 1)
          #print(features_test_day.columns)
          #model.fit(features_day, target)
          sales_submission_day = pd.DataFrame()
          features_test_day = features_test_day[test_['date'] == day]
          sales_submission_day['pr_sku_id'] = list(features_test_day['pr_sku_id'])
          sales_submission_day['st_id'] = list(features_test_day['st_id'])
          sales_submission_day['date'] = day
          true_sku_day = true_sku.loc[test_['date'] == day]
          sales_submission_day['target'] = model.predict(features_test_day)
          sales_submission_day['true_sku'] = list(true_sku_day)
          sales_submission_out = sales_submission_out.append(sales_submission_day)
    sales_submission_out['target'] = sales_submission_out['target'].round()
    sales_submission_out['target'] = sales_submission_out['target'].where(sales_submission_out['target']>0, 0)
    sales_submission_out['target'] = sales_submission_out['target'].astype('int')
    #sales_submission_out['true_sku'] = true_sku
    sales_submission_out['pr_sku_id'] = sales_submission_out.apply(lambda  x: x.pr_sku_id if x.true_sku == -1 else x.true_sku, axis=1)
    sales_submission_out = sales_submission_out.drop(columns = ['true_sku'])
    return sales_submission_out

def make_submission_file(sales_df_train):
    sales_submission_our = pd.DataFrame(columns = ['st_id', 'pr_sku_id', 'date', 'target'])
    train = sales_df_train.copy()
    train['st_id_pr_sku_id'] = train['st_id'] +  train['pr_sku_id']
    st_id_pr_sku_id =train.groupby('st_id_pr_sku_id')['st_id', 'pr_sku_id'].first()
    day_max =pd.to_datetime(train['date']).max()
    for i in range(1, 15):
      sales_submission_day = pd.DataFrame()
      sales_submission_day['st_id'] = st_id_pr_sku_id['st_id']
      sales_submission_day['pr_sku_id'] = st_id_pr_sku_id['pr_sku_id']
      sales_submission_day['date'] = [day_max + timedelta(days = i)]*len(st_id_pr_sku_id)
      sales_submission_day['target'] = 0
      sales_submission_our = sales_submission_our.append(sales_submission_day)
    sales_submission_our.reset_index(drop= True , inplace= True )
    return sales_submission_our

"""# MAIN"""

#Загружаем данные
pr_df = pd.read_csv('ds\data\pr_df.csv')
sales_df_train = pd.read_csv('ds\data\sales_df_train.csv')
sales_submission = pd.read_csv('ds\data\sales_submission.csv')
st_df = pd.read_csv('ds\data\st_df.csv')
holidays_covid_calendar = pd.read_csv('ds\data\holidays_covid_calendar.csv')

# Обучаем модель
models_day, wape_day, data_cluster = train_model_day(sales_df_train, st_df, pr_df,holidays_covid_calendar)

# Получаем предсказания для всех товаров-магазинов, которые есть в обучающем наборе
sales_submission_our = make_submission_file(sales_df_train)

sales_submission_out = predict_days(models_day, data_cluster,sales_df_train,  sales_submission_our, st_df, pr_df,holidays_covid_calendar)

# sales_submission_out.to_csv('ds\sales_submission_out.csv')
