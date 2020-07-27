

class turbo_output(object):
    """

    """

    def __init__(
            self,
            output_type: str,
            x: str = None,
            y: str = None,
            z: str = None,
            input_list: list = None,
    ):
        """

        Args:
            output_type (str): string representing the output object
            x (:obj: `str`, optional): default `None`, string representing the x-axis of the output
            y (:obj: `str`, optional): default `None`, string representing the y-axis of the output
            z (:obj: `str`, optional): default `None`, string representing the z-axis of the output
            input_list (:obj: `list`, optional): default `None`, list of inputs we want to include
                that will update this output
        """
        self.output_type = output_type
        self.x = x
        self.y = y
        self.z = z
        self.input_list = input_list
