import pickle
import joblib
import json
import numpy as np
import pandas as pd

__Province = None
__column=None
__model = None

def get_predict_price(area, Bathroom, Bedroom, Province):
    
    new_sample = [[area, Bathroom, Bedroom, Province]]
    x = pd.DataFrame(new_sample)
    x.columns = __column

    predict = str(__model.predict(x)[0])
    return predict

def load_save_predict():
    print('Loading saved predict...')
    global __Province
    global __column

    with open("C:/Users/DELL/PTDLBPY/Practice_crawl/predict_web/Province_value.json", "r") as f:
        __Province=json.load(f)['Province_value']
 

    global __model
    if __model is None:
        with open("C:/Users/DELL/PTDLBPY/Practice_crawl/predict_web/model_HR.sav", 'rb') as f:
            __model = joblib.load(f)
    print("Loading saved artifacts...done")


if __name__=='__main__':
    load_save_predict()


