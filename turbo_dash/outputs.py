import random
import string
from collections import OrderedDict
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

from .inputs import TurboInput


class TurboOutput:

    def __init__(
            self,
            output_component_id,
            output_component_property,
            output_type,
            df=None,
            x=None,
            y=None,
            z=None,
            color=None,
            size=None,
            hover_data=[],
            template=None,
            turbo_input_list=[],
            graph_input_list=[],
            wrapper_class_name=None,
    ):
        """output object that will assemble the information we need

        :param output_component_id: component ID for the output, dash will use this in the callbacks
        :param output_component_property: property we want to update for the output, dash will use this in the callbacks
        :param output_type: string for the type of output we want to use,
            you might have to add functionality for your output if you're using a new one
        :param df: optional, dataframe we'll use to gather the output data
        :param x: optional, column we'll use for the x axis data
        :param y: optional, column we'll use for the y axis data
        :param z: optional, column we'll use for the z axis
        :param color: optional, plotly express color argument (column to color accordingly)
        :param size: optional, column we'll use for size
        :param hover_data: optional, list of columns we'll use for the hover_data axis
        :param template: optional, plotly express template for the output
        :param turbo_input_list: optional, list of TurboInput objects that will affect this output
        :param graph_input_list: optional, list of strings corresponding to different inputs we want to apply
            directly to the graph. These are things like 'output_type' for choosing what plot we want to use.
            'x' for choosing the x-axis, etc.
        :param wrapper_class_name: optional, css class name to use for the wrapper around the output
        """
        self.output_component_id = output_component_id
        self.output_component_property = output_component_property
        self.output_type = output_type
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
        self.wrapper_class_name = wrapper_class_name

        self.default_kwargs = {
            'output_type': self.output_type,
            'data_frame': self.df,
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'color': self.color,
            'size': self.size,
            'hover_data': self.hover_data,
            'template': self.template,
        }

        # create the plotly express lookup object to grab useful chart information
        self._plotly_express_lookup_object = PlotlyExpressLookup()

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
            inp for turbo_input in self.complete_turbo_input_list for inp in turbo_input.dash_dependencies_input_list
        ]

        # yet again, this is important! This is the list of lambda functions we're going to filter the dataframe on
        self.lambda_function_list = [
            func for turbo_input in self.turbo_input_list for func in turbo_input.lambda_function_list
        ]

        self.html = self.assemble_output_html()

    def assemble_output_html(self):
        # grab the graph and graph_inputs html
        graph_inputs = self._create_graph_turbo_input_html_list()  # grab the html for each graph_input
        graph = [dcc.Graph(id=self.output_component_id)]  # set the html we'll use for the graph

        graph_and_inputs = graph_inputs + graph

        return html.Div(
            className=self.wrapper_class_name,
            children=graph_and_inputs,
        )

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

    def _create_graph_turbo_input_html_list(self):
        """grab the turbo input list and create a list of the html for each input"""
        return [turbo_input.html for turbo_input in self.graph_turbo_input_list]

    def _create_graph_turbo_input_list(self):
        """assemble the TurboInput objects based on the strings in graph_input_list"""
        return [self._create_graph_turbo_input(graph_input) for graph_input in self.graph_input_list]

    def _create_graph_turbo_input(self, graph_input):
        """create the TurboInput object for a graph input based on the provided string"""
        # first, generate a random ID we'll use for this input
        random_input_component_id = ''.join([random.choice(string.ascii_lowercase + string.digits) for n in range(32)])

        return TurboInput(
            output_id_list=[self.output_component_id],
            input_type=graph_input,
            df=self.df,
            value_column=graph_input,
            input_component_id=random_input_component_id,
            filter_input_property_list=['value'],
            plotly_express_lookup_object=self._plotly_express_lookup_object,
            default_value=self.default_kwargs.get(graph_input),
            wrapper_class_name='graph-input',
        )

    def _assemble_kwargs_dict(self, graph_input_args, default_data_frame, default_kwargs):
        """use any graph input filters to assemble the args we'll pass to self.assemble_output_object"""
        ret = default_kwargs
        ret['data_frame'] = default_data_frame

        # now we need to look at self.graph_input_list to see which dict keys we need to change
        # and update them with graph inputs provided
        if graph_input_args:
            for index, graph_input_key in enumerate(self.graph_input_list):
                ret[graph_input_key] = graph_input_args[index]

        return ret

    def _assemble_and_pop_kwargs(self, local_args_dict):
        """assemble the kwargs from the input, remove the self, and remove all kwargs that don't fit the object"""
        local_args_dict.pop('self')  # ego death

        # get a list of all kwargs that correspond to this object
        output_type_kwargs = self._plotly_express_lookup_object.get_chart_inputs(local_args_dict['output_type'])

        # remove any kwargs that don't go with this object
        return {key: local_args_dict[key] for key in output_type_kwargs}

    def assemble_output_object(
            self,
            data_frame=None,
            output_type=None,
            x=None,
            y=None,
            z=None,
            color=None,
            size=None,
            hover_data=None,
            template=None,
    ):
        """assemble the output object we want and return the plotly express object"""
        assembled_and_popped_kwargs = self._assemble_and_pop_kwargs(local_args_dict=locals())

        # here we're grabbed the plotly_express object
        return self._plotly_express_lookup_object.get_chart_object(chart_string=output_type)(
            **assembled_and_popped_kwargs  # here, we're filling in the arguments
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
            filtered_df = self.df

            # filter the dataframe based on the turbo inputs
            if self.turbo_input_list_start_index is not None:
                filtered_df = self.filter_dataframe(
                    # pass the inputs we'll use for filters, i.e. from the turbo_input_list
                    args=input_values[self.turbo_input_list_start_index:self.turbo_input_list_stop_index + 1],
                )

            # assemble the output depending on the graph_input_list
            if self.graph_input_list_start_index is not None:
                graph_input_args = input_values[self.graph_input_list_start_index:self.graph_input_list_stop_index + 1]
            else:
                graph_input_args = None

            kwargs_dict = self._assemble_kwargs_dict(
                # pass the inputs we'll use to assemble the output arguments
                graph_input_args=graph_input_args,
                default_data_frame=filtered_df,
                default_kwargs=self.default_kwargs,
            )

            return self.assemble_output_object(**kwargs_dict)


class PlotlyExpressLookup:

    def __init__(self):
        """look up information about plotly express objects"""

        self._chart_lookup_dict = OrderedDict([
            (
                'scatter', {
                    'object': px.scatter,
                    'inputs': ['data_frame', 'x', 'y', 'color', 'size', 'hover_data', 'template'],
                }
            ),
            (
                'line', {
                    'object': px.line,
                    'inputs': ['data_frame', 'x', 'y', 'color', 'hover_data', 'template'],
                }
            ),
            (
                'area', {
                    'object': px.area,
                    'inputs': ['data_frame', 'x', 'y', 'color', 'hover_data', 'template'],
                }
            ),
            (
                'bar', {
                    'object': px.bar,
                    'inputs': ['data_frame', 'x', 'y', 'color', 'hover_data', 'template'],
                }
            ),
            (
                'histogram', {
                    'object': px.histogram,
                    'inputs': ['data_frame', 'x', 'y', 'color', 'hover_data', 'template'],
                }
            ),
            (
                'violin', {
                    'object': px.violin,
                    'inputs': ['data_frame', 'x', 'y', 'color', 'hover_data', 'template'],
                }
            ),
            (
                'scatter3d', {
                    'object': px.scatter_3d,
                    'inputs': ['data_frame', 'x', 'y', 'z', 'color', 'size', 'hover_data', 'template'],
                }
            ),
        ])

        # not supported yet
        # density_contour
        # density_heatmap
        # box
        # strip
        # line_3d
        # scatter_ternary
        # line_ternary
        # scatter_polar
        # line_polar
        # bar_polar
        # choropleth
        # scatter_geo
        # line_geo
        # scatter_mapbox
        # choropleth_mapbox
        # density_mapbox
        # line_mapbox
        # scatter_matrix
        # parallel_coordinates
        # parallel_categories
        # pie
        # sunburst
        # treemap
        # funnel
        # funnel_area

        self.list_of_chart_strings = list(self._chart_lookup_dict.keys())

    def _get_chart_dict(self, chart_string):
        """return the dictionary for the specified plotly express chart"""
        ret_dict = self._chart_lookup_dict.get(chart_string)

        if ret_dict:
            return ret_dict
        else:
            raise ValueError(
                """I don't have a plotly object for "{}" output type. You might need to add it to {}."""
                .format(chart_string, __file__)
            )

    def _get_chart_dict_value(self, chart_string, key):
        """return a key from the dict corresponding to the chart_string"""
        return self._get_chart_dict(chart_string).get(key)

    def get_chart_object(self, chart_string):
        """return the plotly express object corresponding to the chart_string"""
        return self._get_chart_dict_value(chart_string, key='object')

    def get_chart_inputs(self, chart_string):
        """return the plotly express input arguments corresponding to the chart_string"""
        return self._get_chart_dict_value(chart_string, key='inputs')
