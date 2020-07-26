import pandas as pd


class turbo_dashboard_page(object):
    """

    """

    def __init__(
            self,
            url: str,
            name: str,
            df: pd.DataFrame = None,
            menu_filter_list: list = None,
            output_list: list = None,
    ):
        """

        Args:
            url (str):
            name (str):
            df (:obj: `pandas.DataFrame`, optional):
            menu_filter_list (:obj: `list`, optional):
            output_list (:obj: `list`, optional):
        """
