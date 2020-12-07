
def get_confirmed_deaths_tuple_df(super_covid_df):

    #calculate need cols and dates for confirmed df
    confirmed_cases_cols = ["countyFIPS", "County Name", "State", "stateFIPS" ] + [col for col in super_covid_df.columns if col.startswith("confirmed_")]
    
    #Get new dataframe from team file with needed cols
    confirmed_cases = super_covid_df[confirmed_cases_cols].copy()

    #rename date cols to remove confirmed title
    confirmed_cases.columns = [col.replace("confirmed_","") if col.startswith("confirmed_") else col for col in confirmed_cases.columns]

    #calculate need cols and dates for deaths df
    deaths_cols = ["countyFIPS", "County Name", "State", "stateFIPS" ] + [col for col in super_covid_df.columns if col.startswith("deaths_")]

    #Get new dataframe from team file with needed cols
    deaths = super_covid_df[deaths_cols].copy()

    #rename date cols to remove deaths title
    deaths.columns = [col.replace("deaths_","") if col.startswith("deaths_") else col for col in deaths.columns]

    return confirmed_cases, deaths

def get_confirmed_deaths_tuple_df_with_population(super_covid_df):

    #calculate need cols and dates for confirmed df
    confirmed_cases_cols = ["countyFIPS", "County Name", "State", "stateFIPS", "population" ] + [col for col in super_covid_df.columns if col.startswith("confirmed_")]
    
    #Get new dataframe from team file with needed cols
    confirmed_cases = super_covid_df[confirmed_cases_cols].copy()

    #rename date cols to remove confirmed title
    confirmed_cases.columns = [col.replace("confirmed_","") if col.startswith("confirmed_") else col for col in confirmed_cases.columns]

    #calculate need cols and dates for deaths df
    deaths_cols = ["countyFIPS", "County Name", "State", "stateFIPS", "population" ] + [col for col in super_covid_df.columns if col.startswith("deaths_")]

    #Get new dataframe from team file with needed cols
    deaths = super_covid_df[deaths_cols].copy()

    #rename date cols to remove deaths title
    deaths.columns = [col.replace("deaths_","") if col.startswith("deaths_") else col for col in deaths.columns]

    return confirmed_cases, deaths