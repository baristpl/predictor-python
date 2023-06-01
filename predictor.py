import pandas as pd
from joblib import load

max = 4999000
min = 60000

def predicate(price, seri, model, araba_yasi, kilometre, yillik_mtv, motor_gucu, vites_tipi_Düz, vites_tipi_Otomatik,
            garanti_durumu) -> int:
    data = {
        'price': price,
        'seri': seri,
        'model': model,
        'araba_yasi': araba_yasi,
        'kilometre': kilometre,
        'yillik_mtv': yillik_mtv,
        'motor_gucu': motor_gucu,
        'vites_tipi_Düz': vites_tipi_Düz,
        'vites_tipi_Otomatik': vites_tipi_Otomatik,
        'garanti_durumu': garanti_durumu
    }

    rf = load('random_forest_regressor.joblib')

    standardization_scaler = load('std_scaler.joblib')
    normalization_scaler = load('norm_scaler.joblib')
    target_encoder = load('target_encoder.joblib')

    new_data = pd.DataFrame(data)

    new_data = target_encoder.transform(new_data)

    standardization_columns = ['kilometre', 'araba_yasi']
    new_data[standardization_columns] = standardization_scaler.transform(new_data[standardization_columns])

    normalization_columns = ['price', 'motor_gucu', 'yillik_mtv']
    new_data_copy = new_data.copy()
    new_data_copy[normalization_columns] = normalization_scaler.transform(new_data_copy[normalization_columns])
    normalization_columns.remove('price')
    new_data[normalization_columns] = new_data_copy[normalization_columns]

    new_data.drop('price', inplace=True, axis=1)
    pred = rf.predict(new_data)

    original_value = (pred * (max - min)) + min
    return original_value
