

class turbo_filter(object):
    """object to set defaults and organize data about the filter

    Attributes:

    """

    def __init__(
            self,
            filter_type: str,
            column: str = None,
    ):
        """

        Args:
            filter_type (str): string representing the filter object
            column (:obj: `str`, optional): string representing the column of the dataframe used for this filter
        """
        self.filter_type = filter_type
        self.column = column
