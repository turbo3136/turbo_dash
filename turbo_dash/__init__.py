import dash_core_components as dcc
import dash_html_components as html

from config import LOGO_PATH
from app import wrapper_div_id


class turbo_dash:

    def __init__(
            self,
            app_to_callback,
            list_of_inputs,
            list_of_outputs,
            header_object=None,
            layout_template=None,
            inputs_class_name=None,
            outputs_class_name=None,
    ):
        """quickly create a dashboard by providing a list of inputs and outputs

        :param app_to_callback: dash app we want to make reactive (i.e. call back)
        :param list_of_inputs: list of TurboInput objects to use in our dashboard
        :param list_of_outputs: list of TurboOutput objects to use in our dashboard
        :param header_object: optional, TurboHeader object to display
        :param layout_template: optional, template to use for the layout
        :param inputs_class_name: optional, css class name for the inputs div
        :param outputs_class_name: optional, css class name for the outputs div
        """
        self.app_to_callback = app_to_callback
        self.list_of_inputs = list_of_inputs
        self.list_of_outputs = list_of_outputs
        self.header_object = header_object
        self.layout_template = layout_template
        self.inputs_class_name = inputs_class_name
        self.outputs_class_name = outputs_class_name

        # if we provided a header object, grab the html
        if self.header_object is None:
            self.header_html = None
        else:
            self.header_html = self.header_object.html

        self.layout = self.create_layout()

    @property
    def callbacks(self):
        for o in self.list_of_outputs:
            o.callback(app_to_callback=self.app_to_callback)

        return True

    def create_layout(self):
        if self.layout_template is None or self.layout_template == 'default':
            # default layout, no divs or classes
            return html.Div(
                children=[
                    self.header_html,
                    html.Div(
                        className=self.inputs_class_name,
                        children=[i.html for i in self.list_of_inputs]
                    ),
                    html.Div(
                        className=self.outputs_class_name,
                        children=[o.html for o in self.list_of_outputs]
                    ),
                ],
            )

        elif self.layout_template == 'turbo':
            return html.Div(
                children=[
                    self.header_html,  # /header
                    html.Div(  # sidebar-and-content
                        className='sidebar-and-content',
                        children=[
                            html.Div(  # sidebar
                                className='sidebar',
                                children=[i.html for i in self.list_of_inputs]
                            ),  # /sidebar
                            html.Div(  # content
                                className='content',
                                children=[o.html for o in self.list_of_outputs]
                            ),  # /sidebar
                        ]
                    ),  # /sidebar-and-content
                ],
            )

        # who are you? who who, who who
        else:
            raise ValueError(
                """I don't know what to do with a "{}" layout template. Please add it to {}."""
                .format(self.layout_template, __file__)
            )
