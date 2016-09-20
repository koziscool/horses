


import numpy as np
import pandas as pd
from  pandas import DataFrame
import datetime
import pandas.io.data 

pd.set_option( 'expand_frame_repr', False)

# horses_df = pd.read_csv('HR_short.csv', parse_dates = ['RACE', 'LATEST_EXECUTED_AT_PRICE'])
horses_df = pd.read_csv('March2015HR.csv',  parse_dates = ['RACE', 'LATEST_EXECUTED_AT_PRICE'])

# print horses_df.columns.values
print horses_df.dtypes
print horses_df.head()

bad_data = horses_df[ horses_df[ 'ODDS' ].isnull() ]
print bad_data.head()

bad_data_winner = horses_df[ horses_df[ 'HORSE_WON' ].isnull() | (horses_df.HORSE_WON != 0) & (horses_df.HORSE_WON != 1)]
print bad_data_winner.head()

bad_volume_data = horses_df[ horses_df[ 'VOLUME_EXECUTED' ].isnull() ]
print bad_volume_data.head()

bad_posttime_data = horses_df[ horses_df[ 'RACE' ].isnull() ]
print bad_posttime_data.head()

bad_bettime_data = horses_df[ horses_df[ 'LATEST_EXECUTED_AT_PRICE' ].isnull() ]
print bad_bettime_data.head()

print horses_df.describe()

