import pandas as pd

def check_nan(df):
    '''
    A function that takes a dataframe as input, and prints the percentage of missing values for each column.

    Args:
    df: The dataframe you want to check for missing values
    '''
    print(f'Percentage of missing values:\n\n{round(df.isnull().sum().sort_values(ascending=False) / len(df.index) * 100, 2)}')

def get_recommendations(anime, num_recs=5, threshold=0.2, type=True):
    '''
    This function will take an anime title as input, and print the top animes with the highest cosine similarity value, as well as the percentage of similarity.

    Args:
    anime: The anime title you want to get recommendations for.
    num_recs: The number of recommendations you want to get (default=5).
    threshold: The threshold for the cosine similarity value (default=0.2).
    type: If True, you'll only get recommendations of a similar type, e.g. TV, Movie, OVA, Special, etc. (default=True).

    Example:
    >>>Input: get_recommendations('Dragon Ball Z')
    >>>Output: 
        Since you watched Dragon Ball Z, we recommend:
        
            #1 - Dragon Ball (79.32% match)
            #2 - Fullmetal Alchemist (42.81% match)
            #3 - Death Note (42.6% match)
            #4 - Code Geass: Hangyaku no Lelouch (37.64% match)
            #5 - Yuu☆Yuu☆Hakusho (37.39% match)
    '''
    # Read in relevant data
    print('Calibrating, please wait...')
    features, similarities = pd.read_csv('src/features.csv', low_memory=False), pd.read_csv('src/similarities.csv', low_memory=False)
    # Check if the given input is valid
    if anime in similarities:
        print('Fetching recommendations...')
        if type:
            # Look up the type of input from feature_df (TV, Movie, OVA, etc.)
            type = features.loc[features['name'] == anime, 'type'].iloc[0]
            # Create a new dataframe with titles that have the same type as the input
            type = features[features['type'] == type]
        else:
            # If the type is not specified, just use the full features dataframe
            type = features
        # Sort results_df by similarity scores to the input
        results = similarities.sort_values(by=anime, ascending=False)
        # Instantiate two lists containing titles and similarity scores, respectively, where we reject titles that have similarity scores below the given threshold
        titles = [results[anime].index[i] for i, j in enumerate(results[anime]) if j >= threshold]
        scores = [j for i, j in enumerate(results[anime]) if j >= threshold]
        # Remove the original input from the lists 
        titles.pop(0)
        scores.pop(0)
        # Print the results
        if len(titles) == 0:
            print(f'No recommendations found for {anime} with a similarity score of {threshold} or greater.')
        else:
            print(f'Since you watched {anime}, we recommend:')
            index, count = 0, 1
            while count <= num_recs:
                if index == len(titles):
                    print(f'\nNo more recommendations found.')
                    break
                elif titles[index] in type['name'].values:
                    print(f'\t #{count} - {titles[index]} ({scores[index] * 100:.2f}% match)')
                    count += 1
                index += 1
    # If input it invalid, print error message
    else:
        print('Anime title not found. Please check for typos, or perhaps try using the anime\'s original (phonetic Japanese) name.')


if __name__ == '__main__':
    # Function test
    get_recommendations('Dragon Ball Z')