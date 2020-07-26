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
    from config import DATASETS_DIR

    return pd.read_csv(
        os.path.join(
            DATASETS_DIR,
            '{}.csv.gz'.format(df_name),
        )
    )
