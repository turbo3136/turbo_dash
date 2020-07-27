

class turbo_dashboard(object):
    """

    """

    def __init__(
            self,
            template: str = None,
            dashboard_page_list: list = None,
    ):
        """create a single or multi-page Plotly Dash dashboard

        Args:
            template (:obj: `str`, optional): layout template we want to use. Options include:
                ['default', 'turbo', 'turbo-dark']
            dashboard_page_list (:obj: `list`, optional): list of turbo_dashboard_page objects
        """
        self.template = template
        self.dashboard_page_list = dashboard_page_list

    def run_dashboard(
            self,
            debug: bool = False,
            name: str = __name__,
            is_in_production: bool = False,
    ):
        """start the server, create the layouts, run the callbacks

        Args:
            debug (:obj: `bool`, optional): default `False`, set flask debug mode
            name (:obj: `str`, optional): default `__name__`, the name flask will use for the app
            is_in_production (:obj: `bool`, optional): default `False`, if it's in production, we'll
                have to do some special stuff with the server

        Returns:

        """
        # maybe do some stuff

    # find all the pages and do the index.py thing
    # gather the callbacks
    # do the filtering
    # do all the app stuff
