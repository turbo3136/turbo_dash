from typing import List
import pandas as pd
import dash
import dash_html_components as html

from ._turbo_filter import turbo_filter
from ._turbo_output import turbo_output
from ._lookups import _template_lookup


class turbo_dashboard_page(object):
    """Class that helps us organize information and create a dashboard page.

    This class does most of the heavy lifting within turbo_dash. It creates all the html
    and all the callbacks that make the dashboard run.

    Methods:
        create_html: create the html for this page
        callback: create the callback for this page

    """

    _template_lookup_dict = _template_lookup

    def __init__(
            self,
            url: str = None,
            name: str = None,
            df: pd.DataFrame = None,
            menu_filter_list: List[turbo_filter] = (),
            output_list: List[turbo_output] = (),
            prebuilt_page: str = None,
            prebuilt_page_img_url: str = None,
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
            prebuilt_page_img_url (:obj: `str`, optional): default `None`, provides the source url for the image
                we'll use on the prebuilt page
        """
        self.url = url
        self.name = name
        self.df = df
        self.menu_filter_list = menu_filter_list
        self.output_list = output_list
        self.prebuilt_page = prebuilt_page
        self.prebuilt_page_img_url = prebuilt_page_img_url

    def create_html(
            self,
            template: str = None,
            header_html: html.Div = None,
    ) -> html.Div:
        """create the html for this page

        1. if we're using a prebuilt_page, return that page. Else:
        2. assemble the menu html
        3. assemble the content html
        4. wrap the menu and content html into one div and return

        Args:
            template (:obj: `str`, optional): layout template we want to use. Options include:
                ['default', 'turbo', 'turbo-dark']
            header_html (:obj: `html.Div`, optional): html for the header

        Returns:
            dash_html_components.Div
        """
        # 1
        if self.prebuilt_page:
            return self._prebuilt_page_html(
                template=template,
                prebuilt_page=self.prebuilt_page,
                header_html=header_html,
            )

        # 2
        menu_html = html.Div(
            className=self._template_lookup_dict[template]['menu_className'],
            children=[
                menu_filter.create_html(
                    template=template,
                    df=self.df,
                    location='menu',
                    template_lookup_dict=self._template_lookup_dict,
                ) for menu_filter in self.menu_filter_list
            ],
        )

        # 3
        content_html = html.Div(
            className=self._template_lookup_dict[template]['content_className'],
            children=[
                output.create_html(
                    template=template,
                    df=self.df,
                    location='content',
                    template_lookup_dict=self._template_lookup_dict,
                ) for output in self.output_list
            ],
        )

        # 4
        menu_and_content_html = html.Div(
            className=self._template_lookup_dict[template]['menu_and_content_className'],
            children=[menu_html, content_html],
        )
        return html.Div(children=[header_html, menu_and_content_html])

    def callbacks(
            self,
            app: dash.Dash,
            template: str,
    ) -> bool:
        """run all the callbacks for this page

        Args:
            app (dash.Dash): the dash.Dash app object
            template (:obj: `str`, optional): layout template we want to use. Options include:
                ['default', 'turbo', 'turbo-dark']

        Returns:
            bool: True if successful, raises errors otherwise
        """
        for output in self.output_list:
            output.callback(
                app=app,
                df=self.df,
                menu_filter_list=self.menu_filter_list,
                template=template,
            )

        return True

    """protected methods"""
    def _prebuilt_page_html(
            self,
            template: str,
            prebuilt_page: str,
            header_html: html.Div,
    ) -> html.Div:
        """create the html for the prebuilt page

        Args:
            template:
            prebuilt_page:
            header_html:

        Returns:
            html.Div
        """
        if prebuilt_page in ('homepage', '404'):
            return html.Div(
                children=[
                    header_html,
                    html.Div(
                        className=self._template_lookup_dict[template]['menu_and_content_className'],
                        style={'text-align': 'center', 'display': 'block'},
                        children=html.Img(src=self.prebuilt_page_img_url),
                    ),
                ],
            )

        else:
            raise ValueError(
                """Unknown prebuilt_page string: {}. Check file ({}) for details.""".format(prebuilt_page, __file__)
            )
