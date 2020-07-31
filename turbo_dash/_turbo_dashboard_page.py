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
            prebuilt_template: str = None,
    ):
        """

        Args:
            url (:obj: `str`, optional): default `None`, url for this page, applicable to multi-page dashboards
            name (:obj: `str`, optional): default `None`, name for this page, applicable to multi-page dashboards
            df (:obj: `pandas.DataFrame`, optional): default `None`, dataframe for this page
            menu_filter_list (:obj: `list`, optional): default `None`, list of turbo_filter objects
            output_list (:obj: `list`, optional): default `None`, list of turbo_output objects
            prebuilt_template (:obj: `str`, optional): default `None`, denotes a page that's a prebuilt template
                options include ['homepage', '404']
        """
        self.url = url
        self.name = name
        self.df = df
        self.menu_filter_list = menu_filter_list
        self.output_list = output_list
        self.prebuilt_template = prebuilt_template
