from datetime import datetime
import pandas as pd


def get_data(symbol='HDFCBANKEQ', filename="OptionsData.xlsx"):
    df = pd.read_excel(filename)

    for symbol in set(df['SYMBOL']):
        print(symbol + ': ' + str(df[(df['SYMBOL'] == symbol) & (df['VOLUME'] > 0) & (df['OPTION TYPE'] == 'CE')].size))

    data_date = datetime(year=2023, month=8, day=19)
    df = df[(df['SYMBOL'] == symbol) & (df['VOLUME'] > 0) & (df['OPTION TYPE'] == 'CE')]

    # USE ONY HDFCBANKEQ data

    df['SYMBOL'].astype(str)
    df['EXPIRY'] =\
    df['EXPIRY'].transform(lambda expiry: (datetime.strptime(expiry, '%d/%m/%Y') - data_date).days).astype(int)
    df['STRIKE'] = df['STRIKE'].transform(lambda strike: float(strike.replace(',', ''))).astype(float)
    df['OPEN'] = df['OPEN'].transform(lambda strike: float(strike.replace(',', ''))).astype(float)
    df['SETTLE PRICE'] = df['SETTLE PRICE'].transform(lambda strike: float(strike.replace(',', ''))).astype(float)
    df['CLOSE'] = df['CLOSE'].transform(lambda strike: float(strike.replace(',', ''))).astype(float)

    return df