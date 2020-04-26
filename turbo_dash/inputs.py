from collections import OrderedDict
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html


class TurboInput:
    def __init__(
            self,
            output_id_list,
            input_type,
            df,
            value_column,
            label_column=None,
            input_component_id=None,
            filter_input_property_list=None,
            lambda_function_list=None,
            wrapper_class_name=None,
            input_class_name=None,
            input_label=None,
            input_label_class_name=None,
    ):
        """input object that will assemble the information we need

        :param output_id_list: ID(s) for which outputs this input will affect
        :param input_type: string for the type of input we want to use,
            you might have to add functionality for your input if you're using a new one
        :param df: dataframe we'll use to gather the filter info
        :param value_column: column in the dataframe that contains the values
        :param label_column: optional, column in the dataframe that contains the labels, defaults to the value_column
        :param input_component_id: ID for the input, dash will use this in the callbacks
        :param filter_input_property_list: list of input strings that tell us what values to look for from each filter,
            e.g. ['value'] for Dropdown and RadioItems, ['start_date', 'end_date'] for DatePickerRange
        :param lambda_function_list: list of lambda functions we want to apply to each of the inputs, respectively
            these functions must take two arguments: a dataframe and the value to filter on
        :param wrapper_class_name: optional, css class name for the wrapper of the filter and label
        :param input_class_name: optional, css class name for the input object
        :param input_label: optional, text label for the input object
        :param input_label_class_name: optional, css class name for the label of the input object
        """
        self.output_id_list = output_id_list
        self.input_type = input_type
        self.df = df
        self.value_column = value_column
        if label_column is None:
            self.label_column = value_column
        else:
            self.label_column = label_column
        self.input_component_id = input_component_id
        self.filter_input_property_list = filter_input_property_list
        self.lambda_function_list = lambda_function_list
        self.wrapper_class_name = wrapper_class_name
        self.input_class_name = input_class_name
        if input_label is None:
            self.input_label = self.label_column
        else:
            self.input_label = input_label
        self.input_label_class_name = input_label_class_name

        # assemble the dash dependencies input list, this is an important part
        self.dash_dependencies_input_list = [  # comprehend the list of dash.dependencies.Input
            dash.dependencies.Input(component_id=self.input_component_id, component_property=input_property)
            for input_property in self.filter_input_property_list
        ]

        # object to look up information about the charts we're using
        self._plotly_express_lookup_object = PlotlyExpressLookup()

        self.html = self.assemble_input_html()

    def assemble_input_html(self):
        """assemble the input html we want and update a few variables relating to the input"""

        if self.input_type == 'Dropdown':
            filter_options = [
                # groupby objects are cool, they create a list of dfs and the grouped values
                # since we're grouping by both label and value, we get a tuple returned with the df
                {'label': i[0], 'value': i[1]} for i, i_df in self.df.groupby([self.label_column, self.value_column])
            ]

            return html.Div(
                className=self.wrapper_class_name,
                children=[
                    html.Div(
                        className=self.input_label_class_name,
                        children=self.input_label,
                    ),
                    dcc.Dropdown(
                        id=self.input_component_id,
                        className=self.input_class_name,
                        options=filter_options,
                    ),
                ]
            )

        if self.input_type == 'RangeSlider':
            values = self.df[self.value_column].unique()
            minimum = min(values)
            maximum = max(values)
            marks = {int(val): {'label': str(val), 'style': {'transform': 'rotate(45deg)'}} for val in values}

            return html.Div(
                children=[
                    html.Div(
                        className=self.input_label_class_name,
                        children=self.input_label,
                    ),
                    dcc.RangeSlider(
                        id=self.input_component_id,
                        className=self.input_class_name,
                        min=minimum,
                        max=maximum,
                        value=[minimum, maximum],
                        marks=marks,
                        step=None,
                    ),
                ]
            )

        """
        ## now we handle graph_input input types, i.e. inputs that directly affect the graph like the y axis
        """
        if self.input_type == 'graph_type':
            return html.Div(
                children=[
                    html.Div(
                        className=self.input_label_class_name,
                        children=self.input_label,
                    ),
                    dcc.Dropdown(
                        id=self.input_component_id,
                        className=self.input_class_name,
                        options=self._plotly_express_lookup_object.list_of_chart_strings,
                    ),
                ]
            )

        # who are you? who who, who who
        else:
            raise ValueError(
                """I don't know what to do with a "{}" input type. Please add it to {}."""
                .format(self.input_type, __file__)
            )


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

    def _get_chart_object(self, chart_string):
        """return the plotly express object corresponding to the chart_string"""
        return self._get_chart_dict_value(chart_string, key='object')

    def _get_chart_inputs(self, chart_string):
        """return the plotly express input arguments corresponding to the chart_string"""
        return self._get_chart_dict_value(chart_string, key='inputs')
