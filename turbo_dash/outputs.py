import plotly.express as px
import dash
import dash_core_components as dcc

from collections import OrderedDict
from .inputs import TurboInput, TurboFilter


class TurboOutput:

    def __init__(
            self,
            output_component_id,
            output_component_property,
            output_type,
            df=None,
            x=None,
            y=None,
            color=None,
            template=None,
            turbo_input_list=[],
            graph_inputs_list=[],
    ):
        """output object that will assemble the information we need

        :param output_component_id: component ID for the output, dash will use this in the callbacks
        :param output_component_property: property we want to update for the output, dash will use this in the callbacks
        :param output_type: string for the type of output we want to use,
            you might have to add functionality for your output if you're using a new one
        :param df: optional, dataframe we'll use to gather the output data
        :param x: optional, column we'll use for the x axis data
        :param y: optional, column we'll use for the y axis data
        :param color: optional, plotly express color argument (column to color accordingly)
        :param template: optional, plotly express template for the output
        :param turbo_input_list: optional, list of TurboInput objects that will affect this output
        :param graph_inputs_list: optional, list of strings corresponding to different inputs we want to apply
            directly to the graph. These are things like 'plot_type' for choosing what plot we want to use.
            'x' for choosing the x-axis, etc.
        """
        self.output_component_id = output_component_id
        self.output_component_property = output_component_property
        self.output_type = output_type
        self.df = df
        self.x = x
        self.y = y
        self.color = color
        self.template = template
        self.turbo_input_list = turbo_input_list
        self.graph_inputs_list = graph_inputs_list

        # object to look up information about the charts we're using
        self._plotly_express_lookup_object = PlotlyExpressLookup()

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

    def assemble_output_object(self, filtered_df):
        """assemble the output object we want"""

        if self.output_type == 'bar':
            return px.bar(
                data_frame=filtered_df,
                x=self.x,
                y=self.y,
                color=self.color,
                template=self.template,
            )

        elif self.output_type == 'scatter':
            return px.scatter(
                data_frame=filtered_df,
                x=self.x,
                y=self.y,
                color=self.color,
                template=self.template,
            )

        elif self.output_type == 'line':
            return px.line(
                data_frame=filtered_df,
                x=self.x,
                y=self.y,
                color=self.color,
                template=self.template,
            )

        elif self.output_type == 'violin':
            return px.violin(
                data_frame=filtered_df,
                x=self.x,
                y=self.y,
                color=self.color,
                points='all',
            )

        # who are you? who who, who who
        else:
            raise ValueError(
                """I don't know what to do with a "{}" output type. Please add it to {}."""
                .format(self.output_type, __file__)
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
            return self.assemble_output_object(filtered_df=filtered_df)


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

        self._list_of_chart_strings = list(self._chart_lookup_dict.keys())

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

    def _get_chart_object(self, chart_string):
        """return the plotly express object corresponding to the chart_string"""
        return self._get_chart_dict_value(chart_string, key='object')

    def _get_chart_inputs(self, chart_string):
        """return the plotly express input arguments corresponding to the chart_string"""
        return self._get_chart_dict_value(chart_string, key='inputs')
