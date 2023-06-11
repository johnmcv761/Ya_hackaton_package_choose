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

def recomend_wraper(x):
    stretch_dict = {
        'Пузырчатая пленка': [40,50,80,81,200,210,220,230,310,315,640,641,960,],
        'Стрейтч пленка': [160,350,360,],
        'Пакет': [10,120,130,140,320,330,440,441,450,460,470,480,485,490,500,520,600,601,610,611,620,621,622,623,700,
                  710,720,750,751,752,760,770,780,790,799,801,900,901,905,907,908,910,920,930,931,950,955,970
                  #               400, # опасный
                  #               410, # опасный Авиа
                  #               420, # оружие и взрывчатые вещества
                  ],
        'NONPACK': [0,20,100,110,340,510,670,671,672,673,980,985,990,1010,1300,291,292,300,301,302,303,305,800
                    #                 690, # цена низкая
                    #                 691, # цена средняя
                    #                 692, # цена высокая
                    #                 1200, # малый аксессуар
                    #                 150, # малогабаритный товар
                    #                 290, # Склад МГТ (малогабаритный товар)
                    ]
    }
    # функция преобразования
    df_wrap = pd.json_normalize(x, record_path=['items'], meta=['orderId'])
    # инициализация списка для хранения результатов
    result_list = []

    # итерация по строкам датафрейма
    for index, row in df_wrap.iterrows():
        # проверка наличия типа упаковки в словаре stretch_dict
        for wrapper_type, skus in stretch_dict.items():
            if any(sku in row['type'] for sku in skus):
                # добавление результата в список
                result_list.append({"sku": row['sku'], "wrapper": wrapper_type})
                break

    return result_list


####testing model
data = {"orderId": "unique_order_id",
 "items": [
    {"sku": "unique_sku_1", "count": 1, "a": 2, "b": 3, "c": 5,
     "weight": 0.34, "type": [20, 960]},
    {"sku": "unique_sku_2", "count": 3, "a": 20, "b": 30, "c": 5,
    "weight": 7.34, "type": [320, 440]},
    {"sku": "unique_sku_3", "count": 2, "a": 20, "b": 30, "c": 5,
    "weight": 7.34, "type": [160, 100]},
    {"sku": "unique_sku_4", "count": 6, "a": 20, "b": 30, "c": 5,
    "weight": 7.34, "type": [40]},
   ]
}
print(predict(data))
print(recomend_wraper(data))


# ####testing request
# def predict(x):
#     return req_to_df(x)



