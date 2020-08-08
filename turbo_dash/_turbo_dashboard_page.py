from typing import List
import pandas as pd

from ._turbo_filter import turbo_filter
from ._turbo_output import turbo_output


class turbo_dashboard_page(object):
    """Class that helps us organize information so we can create a dashboard page.

    This class is a glorified dictionary. It helps the user understand different argument
    options in a more digestible way than a dictionary.
    """

    def __init__(
            self,
            url: str = None,
            name: str = None,
            df: pd.DataFrame = None,
            menu_filter_list: List[turbo_filter] = None,
            output_list: List[turbo_output] = None,
            prebuilt_page: str = None,
    ):
        """Gather info for a Plotly Dash page.

        Args:
            url (:obj: `str`, optional): default `None`, url for this page, applicable to multi-page dashboards
            name (:obj: `str`, optional): default `None`, name for this page, applicable to multi-page dashboards
            df (:obj: `pandas.DataFrame`, optional): default `None`, dataframe for this page
            menu_filter_list (:obj: `list`, optional): default `None`, list of turbo_filter objects
            output_list (:obj: `list`, optional): default `None`, list of turbo_output objects
            prebuilt_page (:obj: `str`, optional): default `None`, denotes a page that's prebuilt for us
                options include ['homepage', '404']
        """
        self.url = url
        self.name = name
        self.df = df
        self.menu_filter_list = menu_filter_list
        self.output_list = output_list
        self.prebuilt_page = prebuilt_page
