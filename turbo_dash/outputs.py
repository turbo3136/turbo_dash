import plotly.express as px
import dash
import dash_core_components as dcc

from .inputs import TurboInput


class TurboOutput:

    def __init__(
            self,
            output_component_id,
            output_component_property,
            output_type_string,
            df=None,
            x=None,
            y=None,
            z=None,
            color=None,
            size=None,
            hover_data=None,
            template=None,
            turbo_input_list=[],
            graph_input_list=[],
    ):
        """output object that will assemble the information we need

        :param output_component_id: component ID for the output, dash will use this in the callbacks
        :param output_component_property: property we want to update for the output, dash will use this in the callbacks
        :param output_type_string: string for the type of output we want to use,
            you might have to add functionality for your output if you're using a new one
        :param df: optional, dataframe we'll use to gather the output data
        :param x: optional, column we'll use for the x axis data
        :param y: optional, column we'll use for the y axis data
        :param z: optional, column we'll use for the z axis
        :param color: optional, plotly express color argument (column to color accordingly)
        :param size: optional, column we'll use for size
        :param hover_data: optional, column we'll use for the hover_data axis
        :param template: optional, plotly express template for the output
        :param turbo_input_list: optional, list of TurboInput objects that will affect this output
        :param graph_input_list: optional, list of strings corresponding to different inputs we want to apply
            directly to the graph. These are things like 'graph_type' for choosing what plot we want to use.
            'x' for choosing the x-axis, etc.
        """
        self.output_component_id = output_component_id
        self.output_component_property = output_component_property
        self.output_type_string = output_type_string
        self.df = df
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.size = size
        self.hover_data = hover_data
        self.template = template
        self.turbo_input_list = turbo_input_list
        self.graph_input_list = graph_input_list

        # create the turbo input objects from the graph_input_list strings
        self.graph_turbo_input_list = self._create_graph_turbo_input_list()

        # shove the two input lists together because all the values will apply to this output
        self.complete_turbo_input_list = self.turbo_input_list + self.graph_turbo_input_list

        # then we log off some important indices that we'll use to parse arguments in the callback
        self.turbo_input_list_start_index = self._get_input_list_index_dict()['turbo_start']
        self.turbo_input_list_stop_index = self._get_input_list_index_dict()['turbo_stop']
        self.graph_input_list_start_index = self._get_input_list_index_dict()['graph_start']
        self.graph_input_list_stop_index = self._get_input_list_index_dict()['graph_stop']

        # this is important! This is the dash output that the callback will update
        self.dash_dependencies_output = dash.dependencies.Output(
            component_id=self.output_component_id,
            component_property=self.output_component_property,
        )

        # this is also important! This is the list of dash inputs the callback will listen for
        # We need to flatten all the dash dependencies input lists for this output and grab the dependencies
        # this is using list comprehension, the expanded equivalent would be:
        # lst = []
        # for turbo_input in self.turbo_input_list:
        #     for item in turbo_input.dash_dependencies_input_list:
        #         lst.append(item)
        self.dash_dependencies_input_list = [
            inp for turbo_input in self.turbo_input_list for inp in turbo_input.dash_dependencies_input_list
        ]

        # yet again, this is important! This is the list of lambda functions we're going to filter the dataframe on
        self.lambda_function_list = [
            func for turbo_input in self.turbo_input_list for func in turbo_input.lambda_function_list
        ]

        self.html = dcc.Graph(id=self.output_component_id)  # set the html we'll use for the layout

    def _get_input_list_index_dict(self):
        """grab some important indices we'll use in the callback"""
        ret = {}

        if self.turbo_input_list:  # if we provided turbo inputs, log the indices
            ret['turbo_start'] = 0
            ret['turbo_stop'] = ret['turbo_start'] + len(self.turbo_input_list) - 1

            if self.graph_input_list:  # if we provided graph inputs, log the indices
                ret['graph_start'] = ret['turbo_stop'] + 1
                ret['graph_stop'] = ret['graph_start'] + len(self.graph_input_list) - 1
            else:
                ret['graph_start'] = None
                ret['graph_stop'] = None

        else:  # if we didn't provide turbo inputs, set the indices to None
            ret['turbo_start'] = None
            ret['turbo_stop'] = None

            if self.graph_input_list:  # if we provided graph inputs, log the indices
                ret['graph_start'] = 0
                ret['graph_stop'] = ret['graph_start'] + len(self.graph_input_list) - 1
            else:
                ret['graph_start'] = None
                ret['graph_stop'] = None

        return ret

    def _create_graph_turbo_input_list(self):
        """assemble the TurboInput objects based on the strings in graph_input_list"""
        return [self._create_graph_turbo_input(graph_input) for graph_input in self.graph_input_list]

    def _create_graph_turbo_input(self, graph_input):
        """create the TurboInput object for a graph input based on the provided string"""
        return TurboInput(
            output_id_list=[self.output_component_id],
            input_type=graph_input,
            df=self.df,
            value_column=graph_input,
            input_component_id='asdflkjasdlkj',
            filter_input_property_list=['value'],
        )

    def assemble_output_object(
            self,
            data_frame,
            output_type_string=None,
            x=None,
            y=None,
            z=None,
            color=None,
            template=None,
    ):
        """assemble the output object we want"""

        if self.output_type_string == 'bar':
            return px.bar(
                data_frame=data_frame,
                x=self.x,
                y=self.y,
                color=self.color,
                template=self.template,
            )

        elif self.output_type_string == 'scatter':
            return px.scatter(
                data_frame=data_frame,
                x=self.x,
                y=self.y,
                color=self.color,
                template=self.template,
            )

        elif self.output_type_string == 'line':
            return px.line(
                data_frame=data_frame,
                x=self.x,
                y=self.y,
                color=self.color,
                template=self.template,
            )

        elif self.output_type_string == 'violin':
            return px.violin(
                data_frame=data_frame,
                x=self.x,
                y=self.y,
                color=self.color,
                points='all',
            )

        # who are you? who who, who who
        else:
            raise ValueError(
                """I don't know what to do with a "{}" output type. Please add it to {}."""
                .format(self.output_type_string, __file__)
            )

    def filter_dataframe(self, args):
        """filter the dataframe based on the input values, columns, and operators provided"""
        filtered_df = self.df

        for index, input_filter_value in enumerate(args):  # args is a list of all the filter input values

            # if the value provided is None, we'll return the original df, otherwise we'll do the filtering
            if input_filter_value is not None:
                filtered_df = self.lambda_function_list[index](filtered_df, input_filter_value)

        return filtered_df

    def callback(self, app_to_callback):
        @app_to_callback.callback(
            output=self.dash_dependencies_output,
            inputs=self.dash_dependencies_input_list,
        )
        def filter_and_assemble_output(*input_values):
            """put everything together into one function where we filter and assemble the output"""
            filtered_df = self.filter_dataframe(input_values)

            # TODO: use indices from above and only use the turbo input values to filter, then the graph input values to update the graph in assemble_output_object

            return self.assemble_output_object(data_frame=filtered_df)
