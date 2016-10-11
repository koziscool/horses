
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

# print horses_df.dtypes
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
odds_post_agg_results =  odds_and_post_groups.apply( weight_ave, 'DOLLAR_RETURN', 'VOLUME_EXECUTED' )

# print odds_post_agg_results.head()
# odds_post_agg_results.reset_index()


print odds_post_agg_results.head()
print odds_post_agg_results.index.nlevels
print odds_post_agg_results.index.levels[0]
print odds_post_agg_results.index.levels[1]

# print odds_post_agg_results.index
# print odds_post_agg_results.index.shape

# print odds_post_agg_results[1:2]
# odds_post_agg_results_resize = 

print odds_post_agg_results.dtypes

print '------'
# results_matrix = odds_post_agg_results.EXPECTED_EQUITY.as_matrix()
# print results_matrix

# np.resize( results_matrix, (10, 10) )
# print results_matrix.shape
# print odds_post_agg_results.EXPECTED_EQUITY
print '------'



# plot heatmap
# ax = sns.heatmap(results_matrix)

# # turn the axis label
# for item in ax.get_yticklabels():
#     item.set_rotation(0)

# for item in ax.get_xticklabels():
#     item.set_rotation(90)

# # save figure
# plt.savefig('odds_post_heatmap.png', dpi=100)
# plt.show()


def add_tags( s, t_list):
    if isinstance( t_list, list ):
        for t in t_list:
            s.add( t )
    return s 

all_tags = reduce( add_tags, horses_df['RACE_DATA'], set() )
# print len(all_tags), all_tags

# unique_race_tuples  = np.unique( horses_df[['COUNTRY', 'COURSE', 'RACE']] )
# print unique_race_tuples
# print len(unique_race_tuples)

# horses_df['RACE_TUPLE'] = ( horses_df['COUNTRY'], horses_df['COURSE'],  horses_df['RACE'] )

# def race_tuples( s, bet_record ):
#     print 'koz', bet_record
#     record_tuple = ( bet_record['COUNTRY'], bet_record['COURSE'], bet_record['RACE'], )
#     s.add( record_tuple )
#     return s 

# all_race_tuples = reduce( race_tuples, horses_df['COUNTRY', 'COURSE', 'RACE'], set() )
# print len(all_race_tuples)

# horses_df['RACE_TYPE'] = horses_df['RACE_TYPE'].str.split()

print horses_df['DISTANCE'].unique()
# print horses_df['RACE_DATA']

print( horses_df[['MINUTES_TILL_POST','HORSE_WON']].corr())

# print horses_df[:20]
# print horses_df.describe()

# print pd.crosstab( horses_df.HORSE_WON, horses_df.MINUTES_TILL_POST_DECILE, margins=True )
print pd.crosstab( horses_df.HORSE_WON, horses_df.MINUTES_TILL_POST_DECILE, margins=False )
