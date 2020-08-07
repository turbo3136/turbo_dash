from collections import OrderedDict
import dash
import dash_core_components as dcc
import dash_html_components as html

from ._turbo_dashboard_page import turbo_dashboard_page


class turbo_dashboard(object):
    """Class that helps us organize information, create a dashboard, and deploy it.

    Methods:
        run_dashboard: create the app, manage the layouts, run the callbacks, start the server.
            Uses each of the protected methods below.

    Protected Methods:
        _initiate_app: initiate the app and layout
        _urls_names_and_html: grab the url, name, and html based on the provided template for every page
        _layouts_callback: run the layouts callback
        _callbacks: run the dash callbacks for the layouts and each page
        _run_server: run the server

    """

    def __init__(
            self,
            template: str = None,
            dashboard_page_list: list = None,
            dashboard_wrapper_div_id: str = 'dashboard_wrapper_div',
    ):
        """create a single or multi-page Plotly Dash dashboard

        Args:
            template (:obj: `str`, optional): layout template we want to use. Options include:
                ['default', 'turbo', 'turbo-dark']
            dashboard_page_list (:obj: `list`, optional): list of turbo_dashboard_page objects
        """
        self.template = template
        self.dashboard_page_list = dashboard_page_list
        self.dashboard_wrapper_div_id = dashboard_wrapper_div_id

        # set some internal variables
        self._pathname_prefix = '/'
        self._url_dict_key = 'url'
        self._url_name_dict_key = 'name'
        self._html_dict_key = 'html'
        self._url_component_id = 'url'
        self._url_component_property = 'pathname'
        self._homepage_url = ''
        self._homepage_name = 'homepage'
        self._homepage_template_name = 'homepage'
        self._fourohfour_url = '404'
        self._fourohfour_name = '404'
        self._fourohfour_template_name = '404'

        # if we're using a template that builds pages for us, like a homepage and 404 page, build and add them
        if self.template in ('turbo', 'turbo-dark'):
            self._homepage = turbo_dashboard_page(
                url=self._homepage_url,
                name=self._homepage_name,
                prebuilt_template=self._homepage_template_name,
            )
            self._fourohfour_page = turbo_dashboard_page(
                url=self._fourohfour_url,
                name=self._fourohfour_name,
                prebuilt_template=self._fourohfour_template_name,
            )
            self.dashboard_page_list.extend([self._homepage, self._fourohfour_page])  # add them to the dashboard list

    def run_dashboard(
            self,
            app_name: str = __name__,
            debug: bool = False,
            is_in_production: bool = False,
    ) -> bool:
        """create the app, manage the layouts, run the callbacks, start the server

        Args:
            app_name (:obj: `str`, optional): default `__name__`, the name flask will use for the app
            debug (:obj: `bool`, optional): default `False`, set flask debug mode
            is_in_production (:obj: `bool`, optional): default `False`, if it's in production, we'll
                have to do some special stuff with the server

        Returns:
            bool: True if successful
        """
        # create the app and initiate everything (layout, )
        app = self._initiate_app(app_name=app_name)

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
            is_in_production=is_in_production
        )

        return True

    def _initiate_app(
            self,
            app_name: str,
    ) -> dash.Dash:
        """initiate the app and layout

        Args:
            app_name (str): name we'll use for the app

        Returns:
            dash.Dash: the app object
        """
        # create the app
        app = dash.Dash(name=app_name)

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
    ) -> OrderedDict:
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
                        'html': dashboard_page.html(template=template),
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
                    self._html_dict_key: page.html(template=template),
                }
            ) for page in self.dashboard_page_list  # iterate over the dashboard page list
        ])

        return ret

    def _layouts_callback(
            self,
            app: dash.Dash,
            urls_names_and_html: OrderedDict,
    ) -> bool:
        """run the layouts callback

        Args:
            app (dash.Dash): the dash.Dash app object
            urls_names_and_html (list): the list of urls, names, and layouts we'll use that create each page

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
        def display_page(pathname: str):
            for url in urls_names_and_html:  # search through the page names in this dict
                if pathname == '{}{}'.format(self._pathname_prefix, url):  # for a url matching the pathname in the url
                    return urls_names_and_html[url][self._html_dict_key]  # if we find it, return the html for that url

            # if we didn't find anything, grab the 404 page
            return urls_names_and_html[self._fourohfour_url][self._html_dict_key]

        return True

    def _callbacks(
            self,
            app: dash.Dash,
            urls_names_and_html: OrderedDict,
    ) -> bool:
        """run the dash callbacks for the layouts and each page

        Args:
            app (dash.Dash): the dash.Dash app object
            urls_names_and_html (list): the list of urls, names, and layouts we'll use that create each page

        Returns:
            bool: True if successful, raises errors otherwise
        """
        # layouts callback
        self._layouts_callback(app=app, urls_names_and_html=urls_names_and_html)

        # callback for each page
        for page in self.dashboard_page_list:
            page.callback(app=app)

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
