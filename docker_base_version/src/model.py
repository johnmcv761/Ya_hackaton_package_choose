import pickle
import pandas as pd
import numpy as np


import warnings
warnings.filterwarnings("ignore")


def req_to_df(req):
    # функция преобразования
    df_req = pd.json_normalize(req, record_path=['items'], meta=['orderId'])

    # создаем пустой датафрейм,дублируем строку столько раз, сколько указано в столбце "count" как в оригинальных данных
    new_df_req = pd.DataFrame()
    for _, row in df_req.iterrows():
        # получаем значение столбца "count"
        count = int(row['count'])
        for i in range(count):
            new_df_req = new_df_req.append(row, ignore_index=True)
    new_df_req = new_df_req.drop(['sku', 'type', 'orderId', 'count'], axis=1)


    def gen_geometry_feat(df, a, b, c):
        #генерим геометрические фичи a, b, c -- размеры
        df['dim_sum'] = df[[a, b, c]].sum(axis=1)
        df['vol'] = np.floor(df[[a, b, c]].prod(axis=1))
        df['dim_mean'] = np.floor(df[[a, b, c]].mean(axis=1))
        df['dim_median'] = np.floor(df[[a, b, c]].median(axis=1))
        df['prod_a_b'] = np.floor(df[[a, b]].prod(axis=1))
        df['prod_a_c'] = np.floor(df[[a, c]].prod(axis=1))
        df['prod_b_c'] = np.floor(df[[b, c]].prod(axis=1))
        df['prod_min'] = df[['prod_a_b', 'prod_a_c', 'prod_b_c']].min(axis=1)
        df['prod_mean'] = np.floor(df[['prod_a_b', 'prod_a_c', 'prod_b_c']].mean(axis=1))
        df['diag'] = round(np.sqrt(df[a] ** 2 + df[b] ** 2 + df[c] ** 2), 1)

        df = df.rename(columns={
            'weight': 'goods_wght',
            'vol': 'sku_vol',
            'a': 'sku_a',
            'b': 'sku_b',
            'c': 'sku_c'})
        return df

    df_req_geo = gen_geometry_feat(new_df_req, 'a', 'b', 'c')
    df_req_geo = df_req_geo.sum()
    return pd.DataFrame(df_req_geo).T

###предсказание  для запроса
def predict(x):
    # загрузка модели
    with open('tree_pipe.pkl', 'rb') as f:
        model = pickle.load(f)

    # преобразование
    y_test = req_to_df(x)
    # предсказание
    y_pr = model.predict(y_test).flatten()
    y_pr = y_pr[0]
    return str(y_pr)


# ####testing model
# data = {"orderId": "unique_order_id",
#  "items": [
#     {"sku": "unique_sku_1", "count": 1, "a": 20, "b": 30, "c": 5,
#      "weight": 7.34, "type": [2]},
#    ]
# }
# print(predict(data))


# ####testing request
# def predict(x):
#     return req_to_df(x)



