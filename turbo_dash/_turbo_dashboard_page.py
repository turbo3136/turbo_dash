import pandas as pd


class turbo_dashboard_page(object):
    """

    """

    def __init__(
            self,
            url: str = None,
            name: str = None,
            df: pd.DataFrame = None,
            menu_filter_list: list = None,
            output_list: list = None,
    ):
        """

        Args:
            url (:obj: `str`, optional): default `None`, url for this page, applicable to multi-page dashboards
            name (:obj: `str`, optional): default `None`, name for this page, applicable to multi-page dashboards
            df (:obj: `pandas.DataFrame`, optional): default `None`, dataframe for this page
            menu_filter_list (:obj: `list`, optional): default `None`, list of turbo_filter objects
            output_list (:obj: `list`, optional): default `None`, list of turbo_output objects
        """
        self.url = url
        self.name = name
        self.df = df
        self.menu_filter_list = menu_filter_list
        self.output_list = output_list