from typing import List, Dict, OrderedDict as ODict, Union, Tuple
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
            logo_img_url: str = 'https://raw.githubusercontent.com/turbo3136/turbo_dash_assets/master/turbo_logo.png',
            logo_width: str = '36px',
            homepage_img_url: str =
            'https://raw.githubusercontent.com/turbo3136/turbo_dash_assets/master/launch_risk.png',
            fourohfour_img_url: str =
            'https://raw.githubusercontent.com/turbo3136/turbo_dash_assets/master/not_available.png',
            external_stylesheets_tuple: Tuple[str, ...] = (
                'https://codepen.io/turbo3136/pen/BaKjLoL.css',  # stylesheet for 'turbo' template
                'https://codepen.io/turbo3136/pen/jOqqqgj.css',  # stylesheet for 'turbo-dark' template
            ),
            app_tab_title: str = 'Turbo Dash',
    ):
        """create a single or multi-page Plotly Dash dashboard

        Args:
            template (:obj: `str`, optional): layout template we want to use. Options include:
                ['default', 'turbo', 'turbo-dark']
            dashboard_page_list (:obj: `List[turbo_dashboard_page]`, optional): list of turbo_dashboard_page objects
            dashboard_wrapper_div_id (:obj: `str`, optional): default 'dashboard_wrapper_id`, div_id for the
                dashboard's wrapper
            logo_img_url (:obj: `str`, optional): url to use for the logo in the header,
                any public url should work
            logo_width (:obj: `str`, optional): logo width, usually something like '40px'
            homepage_img_url (:obj: `str`, optional): url to use for the img on the homepage,
                any public url should work
            fourohfour_img_url (:obj: `str`, optional): url to use for the img on the 404 page,
                any public url should work
            external_stylesheets_tuple (:obj: `Tuple[str, ...]`, optional): urls pointing to external CSS sources,
                github doesn't seem to work for some reason
            app_tab_title (:obj: `str`, optional): default `'Turbo Dash'`, the title given to the app's tab
                in your browser
        """
        self.template = template
        self.dashboard_page_list = dashboard_page_list
        self._original_dashboard_page_list = self.dashboard_page_list[:]  # create a copy of the dashboard page list
        self.dashboard_wrapper_div_id = dashboard_wrapper_div_id
        self.logo_img_url = logo_img_url
        self.logo_width = logo_width
        self.homepage_img_url = homepage_img_url
        self.fourohfour_img_url = fourohfour_img_url
        self.external_stylesheets_tuple = external_stylesheets_tuple
        self.external_stylesheets = list(self.external_stylesheets_tuple)
        self.app_tab_title = app_tab_title

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

        # if we're using a template that builds pages for us, like a homepage and 404 page, build and add them
        if self.template in ('turbo', 'turbo-dark'):
            self._homepage = turbo_dashboard_page(
                url=self._homepage_url,
                name=self._homepage_name,
                prebuilt_page=self._homepage_prebuilt_page_name,
                prebuilt_page_img_url=self.homepage_img_url,
            )
            self._fourohfour_page = turbo_dashboard_page(
                url=self._fourohfour_url,
                name=self._fourohfour_name,
                prebuilt_page=self._fourohfour_prebuilt_page_name,
                prebuilt_page_img_url=self.fourohfour_img_url,
            )
            self.dashboard_page_list.extend([self._homepage, self._fourohfour_page])  # add them to the dashboard list

    def run_dashboard(
            self,
            app_name: str,
            suppress_callback_exceptions: bool = True,
            debug: bool = False,
            is_in_production: bool = False,
    ) -> dash.Dash:
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
            dash.Dash
        """
        # create the app and initiate everything (layout, )
        app = self._initiate_app(
            app_name=app_name,
            suppress_callback_exceptions=suppress_callback_exceptions,
        )

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

        return app

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
        app = dash.Dash(
            name=app_name,
            suppress_callback_exceptions=suppress_callback_exceptions,
            external_stylesheets=self.external_stylesheets,
        )
        app.title = self.app_tab_title

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

            # if we didn't find anything, grab the 404 page if there is one, otherwise return an empty Div
            if urls_names_and_html.get(self._fourohfour_url):
                return urls_names_and_html[self._fourohfour_url][self._html_dict_key]
            else:
                return html.Div(children='404 - Make sure your browser\'s url matches one of the page urls')

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
            """If you\'re trying to run this on a production server, check out the "Deploying in Production" 
            section here: https://github.com/turbo3136/turbo_dash/blob/master/README.md"""
            pass

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
                src=self.logo_img_url,
                width=self.logo_width,
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
