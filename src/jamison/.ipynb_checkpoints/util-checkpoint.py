import pandas as pd

def get_first_day_index(df, c_or_d):
    target_col = 'confirmed_1/22/20' if c_or_d == 0 else 'deaths_1/22/20'
    return list(df.columns).index(target_col)

def get_cases_from_start(state_df, diff=True):
    cols = filter(lambda x: 'confirmed' in x, state_df.columns)
    if diff == True: tmp = state_df[cols].diff(axis=1).round()
    else: tmp = state_df[cols]
    tmp['confirmed_1/22/20'] = 0
    return tmp

def get_deaths_from_start(state_df, diff=True):
    cols = filter(lambda x: 'deaths' in x, state_df.columns)
    if diff == True: tmp = state_df[cols].diff(axis=1).round()
    else: tmp = state_df[cols]
    tmp['deaths_1/22/20'] = 0
    return tmp

def get_cases(state_df, days_back=0, diff=True):
    if days_back == 0: return get_cases_from_start(state_df, diff)
    
    else:
        confirmed_cols = list(filter(lambda x: 'confirmed' in x, state_df.columns))
        confirmed_cols = confirmed_cols[-(days_back + 1):]
        if diff == True: df_confirmed = state_df[confirmed_cols].diff(axis=1)
        else: df_confirmed = state_df[confirmed_cols]
        df_confirmed.drop(columns = [confirmed_cols[0]], inplace=True)
    return df_confirmed
    
def get_deaths(state_df, days_back=0, diff=True):
    if days_back == 0: return get_deaths_from_start(state_df, diff)
    
    else:
        deaths_cols = list(filter(lambda x: 'deaths' in x, state_df.columns))
        deaths_cols = deaths_cols[-(days_back + 1):]
        if diff == True: df_deaths = state_df[deaths_cols].diff(axis=1)
        else: df_deaths = state_df[deaths_cols]
        df_deaths.drop(columns = [deaths_cols[0]], inplace=True)
    return df_deaths

def compare_states(df, list_of_states):
    cases = pd.DataFrame(columns = ['state', 'mean', 'median', 'mode'])
    deaths = pd.DataFrame(columns = ['state', 'mean', 'median', 'mode'])
    cases.set_index('state', inplace=True)
    deaths.set_index('state', inplace=True)
    
    for state in list_of_states:
        state_df = per_N(get_state(df, state), 1000000)
        c, d = get_weekly_stats(state_df)
        cases.loc[state] = c
        deaths.loc[state] = d
        
    return cases,deaths

def get_weekly_stats(state_df):
    confirmed = get_cases_past_week(state_df)
    deaths = get_deaths_past_week(state_df)
    return summary(confirmed), summary(deaths)
    
def summary(category):
    summary = pd.DataFrame(columns = ['mean', 'median', 'mode'])
    values = category.stack()
    mean = round(values.mean())
    median = round(values.median())
    mode = values.mode().iloc[0]
    return [mean, median, mode]

def scale(row, pop, n):
    factor = pop / n
#     print(row[:3])
    return  list(map(lambda x: x / factor, row))

def get_state(country_df, state):
    new_df = country_df.loc[country_df['State'] == state]
    new_df.drop(columns = ['State', 'stateFIPS'], inplace=True)
    return new_df

def per_N(state_df, n):
    state_df = state_df.copy()
    pop = state_df['population'].sum()
    state_df.drop(columns="population", inplace=True)
    cols = state_df.columns
    state_df = state_df.apply(scale, args=[pop, n], axis=1, result_type="expand")
    state_df.columns = cols
    return state_df.round()

def drop_zeros(df):
    return df.loc[df['population'] > 0]

def count(e, string):
    count = 0
    for i in string:
        if i == e: count +=1
    return count

def get_levels(df):
    levels = list(map(lambda x: count('!', x)/2 +1, df.columns))
    return levels

def get_levels0(x):
    return count('!', x)/2 + 1

def get_level_frames(category_df, level):
    level_cols = []
    for col in category_df.columns:
        if get_levels0(col) == level:
            level_cols.append(col)
    return category_df[level_cols]

def get_percents(df):
    pcols = list(filter(lambda x: 'Percent' in x, df.columns))
    percents = df[pcols[1:]]
    return percents

def get_totals(df):
    pcols = list(filter(lambda x: 'Percent' in x, df.columns))
    tcols = list(filter(lambda x: x not in pcols, list(df.columns)))
    totals = df[tcols]
    return totals

def trim_cols(df):
    frame = df.copy()
    frame = frame[filter(lambda x: "Margin" not in x, df.columns)]
    return frame

def rename_cols(df):
#     new_cols = [df.replace("HOUSEHOLDS BY TYPE!!Total households", "") for x in list(households.columns)]
    t1 = df.rename(columns = lambda x: x.replace("HOUSEHOLDS BY TYPE!!Total households", ""))
#     t1 = households
    t2 = df.rename(columns = lambda x: x.replace("Estimate!!", ""))
    t3 = t2.rename(columns = lambda x: x.replace("Percent ", ""))
    t4 = t3.rename(columns = lambda x: x.replace("HOUSEHOLDS BY TYPE!!", ""))
#     t5 = t4.rename(columns = lambda x: x.replace("Total households!!", ""))
    return t4

def pred_growth(row, model, num_days = 7):
    new_week = pd.Series(list(range(len(row), len(row) + num_days)))
    new_week.name = 'day'    
    known_total = row.sum()
    pred_week = poly_3.predict(new_week)
    pred_total = pred_week.sum()
    value = round(pred_total / known_total, 2)
    return value

def get_FID(row):
    for i in range(len(row.index)):
        if row[i] > 0:
            return i
        
def get_known_dfs(frame):
    cases = get_cases(frame, 0, True).sum().to_frame()
    deaths = get_deaths(frame, 0, True).sum().to_frame()
    cases.index = range(len(cases))
    deaths.index = range(len(deaths))
    cases.reset_index(inplace=True)
    deaths.reset_index(inplace=True)
    cases.rename(columns = {'index': 'day', 0: 'total'}, inplace=True)
    deaths.rename(columns = {'index': 'day', 0: 'total'}, inplace=True)
    return cases, deaths         
