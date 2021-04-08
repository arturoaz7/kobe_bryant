
if __name__=="__main__":

    import pandas as pd
    import pandasql as ps
    import numpy as np
    kb = pd.read_csv('kobe_shots.csv', parse_dates=['game_date']).drop(columns=['game_id', 'team_id', 'team_name'])
    
    kb.loc[kb['shot_distance'] > 24, 'shot_type']='3PT Field Goal' #fixing wrong values, every shot taken from 24 feet or more is a 3-pointer
    
    kb = ps.sqldf('''
        select *
        from kb
        order by 
            game_date asc, 
            period asc, 
            minutes_remaining desc,
            seconds_remaining''') #sorting Dataframe in chronological order
    
    kb['month'] = kb['game_date'].str[5:7] #extracting month from date feature
    kb['month'].replace(kb['month'].unique(), np.arange(len(kb['month'].unique())), inplace=True) 
    kb.drop(columns = 'game_date', inplace=True) #dropping game_date column
    
    #time features
#     kb['time_remaining'] = (kb['minutes_remaining']*60) + kb['seconds_remaining'] #creating the time_remaining feature
#     kb['time_remaining'] = pd.cut(kb['time_remaining'], 30, labels=range(30)) #binning time_remaining
#     kb.drop(columns=['minutes_remaining', 'seconds_remaining'], inplace=True) #dropping the minutes_remaining and seconds_remaining columns
    
    kb['shot_distance'] = pd.cut(kb['shot_distance'], 20, labels=range(20)) #binning shot_distance
    
    kb.loc[kb.groupby('action_type').action_type.transform('count').lt(120), 'action_type'] = 'Other' #replacing every value that occurs less than 120 times with the value 'Other'
    
    #home feature
    kb.loc[kb['matchup'].str.contains('@'), 'home'] = 0 #when the matchup value contains a @ the value will be 0. This means Lakers did not play as home-club
    kb.loc[kb['matchup'].str.contains('vs.'), 'home'] = 1 #when the matchup value contains a vs. the value will be 1. This Means Lakers did play as home-club
    kb['home'] = kb['home'].astype('int32')
    kb.drop(columns='matchup', inplace=True) #drop the matchup column
    
    #season feature
    season_keys = kb['season'].value_counts().sort_index().index.tolist() #creating a list with each season kobe played
    season_values = [i for i in range(20)] #creating a list from 0 to 19
    season_map = {key:val for key, val in zip(season_keys, season_values)} #zipping the lists created above into a dictionary

    kb['season'] = kb['season'].map(season_map) #mapping old values with new ones using the dictionary created above
    kb['season'] = kb['season'].astype('int32') #casting the new column to integer type
    
    kb['angle'] = np.arctan(kb.loc_x/kb.loc_y)
    kb['angle'].fillna(0, inplace=True) #creating an angle column with loc_x and loc_y
    
    asteps = 5
    kb['angle_bin'] = pd.cut(kb.angle, asteps, labels=np.arange(asteps) - asteps//2)
    kb.drop(columns='angle', inplace=True) #creating bins out of the angle cloumn and dropping the angle column

    angle_map={
    -2:'Left',
    -1:'Left-Center',
    0:'Center',
    1:'Right-Center',
    2:'Right'}
    
    kb.loc[kb['period'] > 4, 'period'] = 5 #combining overtime values into a single value
    
    kb['angle_bin'] = kb['angle_bin'].map(angle_map) # replacing original values mapping a dictionary
    
    sorted_features = ['shot_id', 'season', 'month', 'playoffs', 'home', 'period',\
                     'shot_distance', 'combined_shot_type', 'action_type','shot_type',\
                     'shot_zone_basic', 'shot_zone_area', 'shot_zone_range', 'angle_bin','shot_made_flag'] #reorder columns 
    
   
    kb = kb[sorted_features]
