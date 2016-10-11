

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from  pandas import DataFrame
import datetime
import pandas.io.data 

# import seaborn as sns

def weight_ave( group, num_name, denom_name ):
    try:
        return group[num_name].sum() / group[ denom_name ].sum()
    except ZeroDivisionError:
        return NaN


pd.set_option( 'expand_frame_repr', False)

# horses_df = pd.read_csv('HR_short.csv', parse_dates = ['RACE', 'LATEST_EXECUTED_AT_PRICE'])
horses_df = pd.read_csv('March2015HR.csv',  parse_dates = ['RACE', 'LATEST_EXECUTED_AT_PRICE'])



horses_df['MINUTES_TILL_POST'] = (horses_df['RACE'] - horses_df['LATEST_EXECUTED_AT_PRICE']) / np.timedelta64(60, 's')
horses_df['MINUTES_TILL_POST_DECILE'] = pd.qcut( horses_df.MINUTES_TILL_POST, 10 )

horses_df['ODDS_DECILE'] = pd.qcut( horses_df.ODDS, 10 )

horses_df['DOLLAR_RETURN'] = horses_df['HORSE_WON'] * horses_df['VOLUME_EXECUTED'] * horses_df['ODDS'] 
horses_df['DISTANCE'] = horses_df['RACE_TYPE'].str.split().str.get(0)
horses_df['RACE_DATA'] = horses_df['RACE_TYPE'].str.split().str[1:]


print horses_df.head()

aggregations = {
    'DOLLAR_RETURN' : {
        'TOTAL_RETURN': 'sum'
    },
    'VOLUME_EXECUTED': {
        'TOTAL_EXECUTED': 'sum'
    }
}

post_groups = horses_df.groupby( 'MINUTES_TILL_POST_DECILE' )
post_agg_results = post_groups.agg( aggregations )
post_agg_results['EXPECTED_EQUITY'] =  post_groups.apply( weight_ave, 'DOLLAR_RETURN', 'VOLUME_EXECUTED' )
# post_agg_results =  post_groups.apply( weight_ave, 'DOLLAR_RETURN', 'VOLUME_EXECUTED' )
# print post_dframe.dtypes
print post_agg_results

odds_and_post_groups = horses_df.groupby( ['MINUTES_TILL_POST_DECILE', 'ODDS_DECILE']  )
odds_post_agg_results = odds_and_post_groups.agg( aggregations )
odds_post_agg_results['EXPECTED_EQUITY'] =  odds_and_post_groups.apply( weight_ave, 'DOLLAR_RETURN', 'VOLUME_EXECUTED' )
# odds_post_agg_results =  odds_and_post_groups.apply( weight_ave, 'DOLLAR_RETURN', 'VOLUME_EXECUTED' )

print odds_post_agg_results
