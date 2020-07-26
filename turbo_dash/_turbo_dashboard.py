

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
        # maybe do some stuff, maybe don't, not sure

    def run_dashboard(
            self,
            debug: bool = False,
            name: str = __name__,
            is_in_production: bool = False,
    ):
        """

        Args:
            debug (:obj: `bool`, optional):
            name (:obj: `str`, optional):
            is_in_production (:obj: `bool`, optional):

        Returns:

        """
        # create the app, run the callbacks, etc

    # find all the pages and do the index.py thing
    # gather the callbacks
    # do the filtering
    # do all the app stuff
