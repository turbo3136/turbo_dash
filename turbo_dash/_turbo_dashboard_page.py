from typing import List
import pandas as pd
import dash
import dash_html_components as html

from ._turbo_filter import turbo_filter
from ._turbo_output import turbo_output


class turbo_dashboard_page(object):
    """Class that helps us organize information and create a dashboard page.

    This class does most of the heavy lifting within turbo_dash. It creates all the html
    and all the callbacks that make the dashboard run.

    Methods:
        html: create the html for this page
        callback: create the callback for this page

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
        """Create a Plotly Dash page.

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

    def html(
            self,
            template: str,
    ) -> html.Div:
        """create the html for this page

        Args:
            template (:obj: `str`, optional): layout template we want to use. Options include:
                ['default', 'turbo', 'turbo-dark']

        Returns:
            dash_html_components.Div
        """
        pass

    def callback(
            self,
            app: dash.Dash,
    ) -> bool:
        """run the callback for this page

        Args:
            app (dash.Dash): the dash.Dash app object

        Returns:
            bool: True if successful, raises errors otherwise
        """
        pass
