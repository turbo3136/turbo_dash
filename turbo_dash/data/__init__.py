# built-in datasets for examples and testing


def gapminder():
    """function to grab the gapminder dataframe

    :return: pandas df with columns [
        'country', 'continent', 'year', 'lifeExp', 'pop', 'gdpPercap', 'iso_alpha', 'iso_num'
    ]
    """
    return _get_df('gapminder')


def _get_df(df_name):
    """function to grab a dataframe from the `./package_data/datasets/` directory

    :param df_name: string of the dataframe filename
    :return: pandas df
    """
    import pandas as pd
    import os
    from config import DATASETS_DIR

    return pd.read_csv(
        os.path.join(
            DATASETS_DIR,
            '{}.csv.gz'.format(df_name),
        )
    )
