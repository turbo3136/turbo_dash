"""built-in datasets for examples and testing"""
import pandas as pd


def gapminder() -> pd.DataFrame:
    """function to grab the gapminder dataframe

    Returns:
        pandas.DataFrame: columns [
            'country', 'continent', 'year', 'lifeExp', 'pop', 'gdpPercap', 'iso_alpha', 'iso_num'
        ]
    """
    return _get_df('gapminder')


def _get_df(df_name: str) -> pd.DataFrame:
    """get a dataframe from the file's name in the datasets directory

    Args:
        df_name (str): string of the dataframe filename in the datasets directory

    Returns:
        pandas.DataFrame
    """
    import os

    return pd.read_csv(
        os.path.join(  # get the path to the dataset by
            os.path.dirname(os.path.dirname(__file__)),  # finding the dirname for this file (i.e. the turbo_dash dir)
            'package_data',  # move into package_data/
            'datasets',  # then into datasets/
            '{}.csv.gz'.format(df_name),  # finally grab the .csv.gz we're looking for
        )
    )
