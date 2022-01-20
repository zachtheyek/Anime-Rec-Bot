def check_nan(df):
    '''
    A function that takes a dataframe as input, and prints the percentage of missing values for each column.

    Args:
    df: The dataframe you want to check for missing values
    '''
    print(f'Percentage of missing values:\n\n{round(df.isnull().sum().sort_values(ascending=False) / len(df.index), 5) * 100}')