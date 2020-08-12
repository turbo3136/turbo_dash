import string
import random
from typing import List, Dict, Union
from typing import OrderedDict as ODict
from collections import OrderedDict
import dash
import dash_core_components as dcc
import dash_html_components as html

from ._turbo_dashboard_page import turbo_dashboard_page
from ._lookups import _template_lookup
from ._helpers import generate_random_string


class turbo_dashboard(object):
    """Class that helps us organize information, create a dashboard, and deploy it.

    Methods:
        run_dashboard: create the app, manage the layouts, run the callbacks, start the server
        _initiate_app: initiate the app and layout
        _header_html: create the html we'll use for the header
        _urls_names_and_html: grab the url, name, and html based on the provided template for every page
        _layouts_callback: run the layouts callback
        _callbacks: run the dash callbacks for the layouts and each page
        _run_server: run the server

    """

    _template_lookup_dict = _template_lookup

    def __init__(
            self,
            template: str = None,
            dashboard_page_list: List[turbo_dashboard_page] = (),
            dashboard_wrapper_div_id: str = 'dashboard_wrapper_div',
    ):
        """create a single or multi-page Plotly Dash dashboard

        Args:
            template (:obj: `str`, optional): layout template we want to use. Options include:
                ['default', 'turbo', 'turbo-dark']
            dashboard_page_list (:obj: `List[turbo_dashboard_page]`, optional): list of turbo_dashboard_page objects
            dashboard_wrapper_div_id (:obj: `str`, optional): default 'dashboard_wrapper_id`, div_id for the
                dashboard's wrapper
        """
        self.template = template
        self.dashboard_page_list = dashboard_page_list
        self._original_dashboard_page_list = self.dashboard_page_list[:]  # create a copy of the dashboard page list
        self.dashboard_wrapper_div_id = dashboard_wrapper_div_id

        # set some internal variables
        self._pathname_prefix = '/'  # prefix we need for Dash's pathname property
        self._url_dict_key = 'url'  # string we'll use for the key of the url in _urls_names_and_html
        self._url_name_dict_key = 'name'  # string we'll use for the key of the name in _urls_names_and_html
        self._html_dict_key = 'html'  # string we'll use for the key of the html in _urls_names_and_html
        self._url_component_id = 'url'  # Dash component ID for the url
        self._url_component_property = 'pathname'  # Dash component property for the url

        # prebuilt page info
        self._homepage_url = '/'
        self._homepage_name = 'homepage'
        self._homepage_prebuilt_page_name = 'homepage'
        self._fourohfour_url = '404'
        self._fourohfour_name = '404'
        self._fourohfour_prebuilt_page_name = '404'

        # some layout stuff
        # @todo update this stuff, it should be an argument. We also want an external reference to these options
        self._logo_filepath = '/static/turbo_logo.png'
        self._logo_width = '36px'

        # if we're using a template that builds pages for us, like a homepage and 404 page, build and add them
        if self.template in ('turbo', 'turbo-dark'):
            self._homepage = turbo_dashboard_page(
                url=self._homepage_url,
                name=self._homepage_name,
                prebuilt_page=self._homepage_prebuilt_page_name,
            )
            self._fourohfour_page = turbo_dashboard_page(
                url=self._fourohfour_url,
                name=self._fourohfour_name,
                prebuilt_page=self._fourohfour_prebuilt_page_name,
            )
            self.dashboard_page_list.extend([self._homepage, self._fourohfour_page])  # add them to the dashboard list

    def run_dashboard(
            self,
            app_name: str,
            suppress_callback_exceptions: bool = True,
            debug: bool = False,
            is_in_production: bool = False,
    ) -> bool:
        """create the app, manage the layouts, run the callbacks, start the server

        Args:
            app_name (str): the name flask will use for the app, it should usually be set to '__name__'
            suppress_callback_exceptions (:obj: `bool`, optional): default `True`, dash arg for whether to
                suppress callback exceptions when dash is creating the callback map. Must be `True` for
                multi-page dashboards.
            debug (:obj: `bool`, optional): default `False`, set flask debug mode
            is_in_production (:obj: `bool`, optional): default `False`, if it's in production, we'll
                have to do some special stuff with the server

        Returns:
            bool: True if successful
        """
        # create the app and initiate everything (layout, )
        app = self._initiate_app(app_name=app_name, suppress_callback_exceptions=suppress_callback_exceptions)

        # gather all the layouts into an OrderedDict of dicts
        urls_names_and_html = self._urls_names_and_html(
            template=self.template,
        )

        # run the callbacks
        self._callbacks(
            app=app,
            urls_names_and_html=urls_names_and_html,
        )

        # run the server
        self._run_server(
            app=app,
            debug=debug,
            is_in_production=is_in_production,
        )

        return True

    def _initiate_app(
            self,
            app_name: str,
            suppress_callback_exceptions: bool,
    ) -> dash.Dash:
        """initiate the app and layout

        Args:
            app_name (str): name we'll use for the app
            suppress_callback_exceptions (:obj: `bool`, optional): default `True`, dash arg for whether to
                suppress callback exceptions when dash is creating the callback map. Must be `True` for
                multi-page dashboards.

        Returns:
            dash.Dash: the app object
        """
        # create the app
        app = dash.Dash(name=app_name)

        # suppress callback exceptions
        app.config.suppress_callback_exceptions = suppress_callback_exceptions

        # initiate the layout
        #    we need an empty Div that our callbacks will update based on the Location i.e. url
        app.layout = html.Div(
            children=[
                dcc.Location(id=self._url_component_id, refresh=False),
                html.Div(id=self.dashboard_wrapper_div_id)
            ],
        )
        return app

    def _urls_names_and_html(
            self,
            template: str,
    ) -> ODict[str, Dict[str, Union[str, str, html.Div]]]:
        """grab the url, name, and html based on the provided template for every page

        Args:
            template (str): the template for the layouts

        Returns:
            OrderedDict: OrderedDict of dicts with url, name, and html info in the order provided

            The return value looks like:
            OrderedDict([
                (
                    dashboard_page.url,
                    {
                        'url': dashboard_page.url,
                        'name': dashboard_page.name,
                        'html': dashboard_page.create_html(template=template),
                    }
                ),
                ...
            ])

            This gives us all the information we need to structure the app and create the layouts callback

        """
        ret = OrderedDict([  # list comprehension on the dashboard page list
            (  # to create an OrderedDict of
                page.url,  # page url keys
                {  # connected to dictionaries with page url, name, html
                    self._url_dict_key: page.url,
                    self._url_name_dict_key: page.name,
                    self._html_dict_key: page.create_html(
                        template=template,
                        header_html=self._header_html(current_page_url=page.url),
                    ),
                }
            ) for page in self.dashboard_page_list  # iterate over the dashboard page list
        ])

        return ret

    def _layouts_callback(
            self,
            app: dash.Dash,
            urls_names_and_html: ODict[str, Dict[str, Union[str, str, html.Div]]],
    ) -> bool:
        """run the layouts callback

        Args:
            app (dash.Dash): the dash.Dash app object
            urls_names_and_html (OrderedDict): an OrderedDict of urls, names, and layouts we'll use
                that create each page

        Returns:
            bool: True if successful, raises errors otherwise
        """
        @app.callback(
            dash.dependencies.Output(component_id=self.dashboard_wrapper_div_id, component_property='children'),
            [
                dash.dependencies.Input(
                    component_id=self._url_component_id,
                    component_property=self._url_component_property,
                ),
            ],
        )
        def display_page(pathname: str) -> html.Div:
            for url in urls_names_and_html:  # search through the page names in this dict
                if pathname == '{}'.format(url):  # for a url matching the pathname in the url
                    return urls_names_and_html[url][self._html_dict_key]  # if we find it, return the html for that url

            # if we didn't find anything, grab the 404 page
            return urls_names_and_html[self._fourohfour_url][self._html_dict_key]

        return True

    def _callbacks(
            self,
            app: dash.Dash,
            urls_names_and_html: ODict[str, Dict[str, Union[str, str, html.Div]]],
    ) -> bool:
        """run the dash callbacks for the layouts and each page

        Args:
            app (dash.Dash): the dash.Dash app object
            urls_names_and_html (OrderedDict): an OrderedDict of urls, names, and layouts we'll use
                that create each page

        Returns:
            bool: True if successful, raises errors otherwise
        """
        # layouts callback
        self._layouts_callback(app=app, urls_names_and_html=urls_names_and_html)

        # callback for each page
        for page in self.dashboard_page_list:
            page.callbacks(app=app, template=self.template)

        return True

    def _run_server(
            self,
            app: dash.Dash,
            debug: bool,
            is_in_production: bool,
    ) -> bool:
        """run the server

        Args:
            app (dash.Dash): the dash.Dash app object
            debug (bool): run the app in debug mode
            is_in_production: run the app in production

        Returns:
            bool: True if successful, raises errors otherwise
        """
        if is_in_production is True:
            raise NotImplementedError('Whoops, looks like turbo didn\'t productionize this yet!')
        else:
            app.run_server(debug=debug)

        return True

    """Beware the depths below. Here lies the real code."""
    def _header_html(
            self,
            current_page_url: str = None,
    ) -> html.Div:
        """create the header for the given page

        Args:
            current_page_url: what's the url for the current header so we can set that link's class

        Returns:
            dash_html_components.Div
        """
        # gather all the pages in this dashboard, ignore the 404 and homepage
        # create a logo and add each page's name with a link to the page
        # do we want to support tabs? maybe add a dropdown of the individual tabs?

        # 1. create the logo's html
        logo_html = html.A(
            id='{} logo - {}'.format(self._homepage_url, generate_random_string()),
            className=self._template_lookup_dict[self.template]['header_logo_className'],
            href='{}'.format(self._homepage_url),
            children=html.Img(
                src=self._logo_filepath,
                width=self._logo_width,
            )
        )

        # 2. gather all the pages in this dashboard and create the header links
        header_page_list = [
            {self._url_dict_key: page.url, self._url_name_dict_key: page.name}
            for page in self._original_dashboard_page_list
        ]

        links_html = html.Div(
            className=self._template_lookup_dict[self.template]['header_links_className'],
            children=[
                dcc.Link(
                    id='{} header-link - {}'.format(page_dict[self._url_dict_key], generate_random_string()),
                    href=page_dict[self._url_dict_key],
                    children=[
                        html.Div(
                            className=self._template_lookup_dict[self.template][
                                # if this link is not for the current page, use the regular class
                                # else use the class for the current link
                                'header_link_className'
                                if current_page_url != page_dict[self._url_dict_key]
                                else 'header_link_current_className'
                            ],
                            children=page_dict[self._url_name_dict_key],
                        ),
                    ]
                ) for page_dict in header_page_list
            ]
        )

        # return the assembled html
        return html.Div(
            className=self._template_lookup_dict[self.template]['header_className'],
            children=[logo_html, links_html],
        )
