from typing import List, Dict, Any, Callable, Tuple
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

from ._turbo_filter import turbo_filter
from ._helpers import generate_random_string
from ._lookups import _template_lookup


class turbo_output(object):
    """Class that helps us organize information so we can create an output.

    Methods:
        create_html: create the html for this output
        callback: create the callback for this output
    """

    _template_lookup_dict = _template_lookup

    def __init__(
            self,
            output_type: str,
            x: str = None,
            y: str = None,
            z: str = None,
            color: str = None,
            size: str = None,
            hover_data: List[str] = (),
            locations: str = None,
            locationmode: str = None,
            projection: str = None,
            chart_input_list: List[str] = (),
            output_component_property: str = 'figure',
    ):
        """

        Args:
            output_type (str): string representing the output object
            x (:obj: `str`, optional): default `None`, string representing the x-axis of the output
            y (:obj: `str`, optional): default `None`, string representing the y-axis of the output
            z (:obj: `str`, optional): default `None`, string representing the z-axis of the output
            color (:obj: `str`, optional): default `None`, string representing the color of the output
            size (:obj: `str`, optional): default `None`, string representing the size of the output
            hover_data (:obj: `str`, optional): default `()`, list representing the hover_data of the output
            locations (:obj: `str`, optional): default `None`, string representing the locations of the output
            locationmode (:obj: `str`, optional): default `None`, string representing the locationmode of the output
            projection (:obj: `str`, optional): default `None`, string representing the projection of the output
            chart_input_list (:obj: `List[str]`, optional): default `()`, list of inputs we want to include
                that will update this output
            output_component_property (:obj: `str`, optional): default `'figure'`, the property of the
                output we want the callback to update. Generally, we want the inputs to update the
                'figure' property of our dcc.Graph object.
        """
        self.output_type = output_type
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.size = size
        self.hover_data = hover_data
        self.locations = locations
        self.locationmode = locationmode
        self.projection = projection
        self.chart_input_list = chart_input_list
        self.output_component_property = output_component_property

        # create a dictionary so we know which input string corresponds to which instance variable
        self._chart_input_string_default_value_dict = {
            'output_type': self.output_type,
            'x': self.x,
            'y': self.y,
            'z': self.z,
            'color': self.color,
            'size': self.size,
            'hover_data': self.hover_data,
            'locations': self.locations,
            'locationmode': self.locationmode,
            'projection': self.projection,
        }

        # create actual turbo_filter objects from the list of input strings
        self.chart_input_turbo_filter_list = self._create_chart_input_turbo_filter_list_from_chart_input_list()

        # grab some important data
        self.component_id = '{} - {}'.format(self.output_type, generate_random_string())
        self.persistence = True  # todo: do we want to allow different values for persistence and persistence_type?
        self.persistence_type = 'memory'

        # this is important! This is the dash output that the callback will update
        self.dash_dependencies_output = dash.dependencies.Output(
            component_id=self.component_id,
            component_property=self.output_component_property,
        )

    def create_html(
            self,
            template: str,
            df: pd.DataFrame,
            location: str,
            template_lookup_dict: Dict[str, Dict[str, str]],
    ) -> html.Div:
        wrapper_class_name = '{}_output_and_filter_wrapper_className'.format(location)

        input_turbo_filter_html_list = [
            input_turbo_filter.create_html(
                template=template,
                df=df,
                location=location,
                template_lookup_dict=template_lookup_dict,
            ) for input_turbo_filter in self.chart_input_turbo_filter_list
        ]
        output_html_list = [self._create_output_html(
            template=template,
            location=location,
            template_lookup_dict=template_lookup_dict,
        )]

        return html.Div(
            className=template_lookup_dict[template][wrapper_class_name],
            children=input_turbo_filter_html_list + output_html_list,
        )

    def callback(
            self,
            app: dash.Dash,
            df: pd.DataFrame = None,
            menu_filter_list: List[turbo_filter] = (),
            template: str = None,
    ) -> bool:
        """the dash callback for this output

        1. do the fancy dash decorator and create a function within this function
        2. filter the df based on the menu_filter_list, if necessary
        3. assemble and return the chart object based on the original inputs and/or the chart inputs

        Args:
            app (dash.Dash): the dash.Dash app object
            df (:obj: `pandas.DataFrame`, optional): default `None`, dataframe we want to use in the callback
            menu_filter_list (:obj: `list`, optional): default `()`, list of turbo_filter objects
            template (:obj: `str`, optional): layout template we want to use. Options include:
                ['default', 'turbo', 'turbo-dark']

        Returns:
            bool: True if successful, raises errors otherwise
        """
        @app.callback(
            output=self.dash_dependencies_output,
            inputs=self._dash_dependencies_input_list(menu_filter_list=menu_filter_list),
        )
        def callback_function(*dash_input_values_list: Any):
            """filter the df and create the chart object we want to display in the output"""
            filtered_df = df  # we need this reference so we don't filter a df that's already been filtered

            # 2
            df_filter_start_index = 0  # we can assume the dataframe filter values start at 0
            # and there are len([list of lambda functions]) values to filter on
            df_filter_stop_index = len([func for tf in menu_filter_list for func in tf.filter_input_lambda_function_list])
            filtered_df = self._filter_dataframe_from_turbo_filter_list(
                df=filtered_df,
                filter_column_list=self._filter_column_list(menu_filter_list=menu_filter_list),
                filter_lambda_function_list=self._filter_lambda_function_list(menu_filter_list=menu_filter_list),
                filter_value_list=dash_input_values_list[df_filter_start_index:df_filter_stop_index],
            )

            # 3
            chart_input_start_index = df_filter_stop_index
            chart_input_stop_index = len(dash_input_values_list)
            return self._assemble_chart_object_from_filtered_df_and_chart_input_list(
                df=filtered_df,
                chart_input_values_list=dash_input_values_list[chart_input_start_index:chart_input_stop_index],
                template=template,
            )

        return True

    """protected methods"""
    def _create_chart_input_turbo_filter_list_from_chart_input_list(self) -> List[turbo_filter]:
        return [
            turbo_filter(
                chart_input_filter_type=chart_input_string,
                default_value=self._get_default_value_from_chart_input_string(chart_input_string=chart_input_string),
            ) for chart_input_string in self.chart_input_list
        ]

    def _get_default_value_from_chart_input_string(
            self,
            chart_input_string: str,
    ) -> Any:
        return self._chart_input_string_default_value_dict[chart_input_string]

    def _create_output_html(
            self,
            template: str,
            location: str,
            template_lookup_dict: Dict[str, Dict[str, str]],
    ) -> html.Div:
        class_name_prefix = '{}_output'.format(location)
        class_name_suffix = 'className'
        wrapper_class_name = '{}_wrapper_{}'.format(class_name_prefix, class_name_suffix)
        label_class_name = '{}_label_{}'.format(class_name_prefix, class_name_suffix)
        output_class_name = '{}_{}'.format(class_name_prefix, class_name_suffix)

        return html.Div(
            className=template_lookup_dict[template][wrapper_class_name],
            children=[
                html.Div(
                    className=template_lookup_dict[template][label_class_name],
                    children='Ahoy hoy!',  # todo: yeah, this needs to be a real label
                ),
                html.Div(
                    className=template_lookup_dict[template][output_class_name],
                    children=dcc.Graph(id=self.component_id),  # here's the actual output graph
                ),
            ],
        )

    def _complete_turbo_filter_list(
            self,
            menu_filter_list: List[turbo_filter],
    ) -> List[turbo_filter]:
        """concatenate the menu filter list and input filter list together to get turbo_filter objects"""
        return list(menu_filter_list) + list(self.chart_input_turbo_filter_list)

    def _dash_dependencies_input_list(
            self,
            menu_filter_list: List[turbo_filter],
    ) -> List[dash.dependencies.Input]:
        """grab the full list of dash dependencies inputs this output will listen to

        this is important! This is the list of dash inputs the callback will listen for
        We need to flatten all the dash dependencies input lists for this output and grab the dependencies
        this is using list comprehension, the expanded equivalent would be:
        ret = []
        for tf in self._complete_turbo_filter_list(menu_filter_list=menu_filter_list):
            for dash_dependencies_input in tf.dash_dependencies_input_list:
                ret.append(dash_dependencies_input)

        Args:
            menu_filter_list (List[turbo_dash.turbo_filter]): list of turbo_filter objects

        Returns:
            List[dash.dependencies.Input]
        """
        return [
            dash_dependencies_input
            for tf in self._complete_turbo_filter_list(menu_filter_list=menu_filter_list)
            for dash_dependencies_input in tf.dash_dependencies_input_list
        ]

    @staticmethod
    def _filter_column_list(menu_filter_list: List[turbo_filter]) -> List[str]:
        """grab the list of column names for each of our filters"""
        # this is more than just grabbing the column for each menu filter
        # each menu filter can have 1 or more input properties associated with it
        # (e.g. DatePickerRange has [start_date, end_date])
        # so we have to loop through two lists instead of just the top-level list
        return [tf.column for tf in menu_filter_list for dummy in tf.dash_dependencies_input_list]

    @staticmethod
    def _filter_lambda_function_list(
            menu_filter_list: List[turbo_filter]
    ) -> List[Callable[[pd.DataFrame, str, Any], pd.DataFrame]]:
        """grab the list of lambda functions for each of our filters"""
        # this is more than just grabbing the lambda function for each menu filter
        # each menu filter can have 1 or more input properties associated with it
        # (e.g. DatePickerRange has [start_date, end_date])
        # so we have to loop through the functions for each of those properties instead of just the top-level list
        return [lambda_func for tf in menu_filter_list for lambda_func in tf.filter_input_lambda_function_list]

    @staticmethod
    def _filter_dataframe_from_turbo_filter_list(
            df: pd.DataFrame,
            filter_column_list: List[str],
            filter_lambda_function_list: List[Callable[[pd.DataFrame, str, Any], pd.DataFrame]],
            filter_value_list: Tuple[Any],
    ) -> pd.DataFrame:
        """filter a dataframe based on a list of values and turbo_filters

        Args:
            df (pandas.DataFrame): dataframe we want to filter
            filter_column_list (List[Any]):
            filter_lambda_function_list (List[Callable[[pd.DataFrame, str, Any], pd.DataFrame]]): if the typing doesn't
                help, this is a list of lambda functions that takes three arguments. The lambdas look like:
                lambda dataframe (pd.DataFrame), column (str), value (Any): return_value (pd.DataFrame)
            filter_value_list (List[Any]): list of values we'll filter the df on

        Returns:
            pandas.DataFrame

        Raises:
            ValueError if filter_value_list and turbo_filter_list are not the same length
        """
        if len(filter_value_list) != len(filter_column_list) \
                or len(filter_value_list) != len(filter_lambda_function_list):
            raise ValueError(
                '''filter_value_list ({}) and filter_column_list ({}) and filter_lambda_function_list ({}) 
                must be the same size'''.format(filter_value_list, filter_column_list, filter_lambda_function_list)
            )

        ret = df

        # loop through the list of filter values and apply the lambda function for each value
        for index, filter_value in enumerate(filter_value_list):
            ret = filter_lambda_function_list[index](ret, filter_column_list[index], filter_value)
            # remember, these lambda functions look like:
            #   lambda dataframe (pd.DataFrame), column (str), value (Any): return_value (pd.DataFrame)

        return ret

    def _assemble_chart_object_from_filtered_df_and_chart_input_list(
            self,
            df: pd.DataFrame,
            chart_input_values_list: Tuple[Any],
            template: str = None,
    ) -> Any:
        """take a dataframe and a list of chart input values from the dash callback, produce a plotly figure

        1. create a dict with all the original (default) values and updated values (from the chart inputs)
        2. create and return the figure based on that data

        Args:
            df (pandas.DataFrame): dataframe we want to filter
            chart_input_values_list (Tuple[Any]): list of values we'll use to update the chart
            template (:obj: `str`, optional): layout template we want to use. Options include:
                ['default', 'turbo', 'turbo-dark']

        Returns:
            plotly.graph_objs._figure.Figure (plotly.express.bar, line, etc)

        Raises:
            ValueError if chart_input_values_list doesn't have the same length as self.chart_input_list
        """
        if len(chart_input_values_list) != len(self.chart_input_list):
            raise ValueError(
                '''chart_input_values_list ({}) and chart_input_list ({}) must have the same length'''
                .format(chart_input_values_list, self.chart_input_list)
            )

        # 1
        figure_values_dict = dict(self._chart_input_string_default_value_dict)
        for index, chart_input_value in enumerate(chart_input_values_list):
            figure_values_dict[self.chart_input_list[index]] = chart_input_value

        # 2
        if figure_values_dict['output_type'] == 'scatter':
            return px.scatter(
                data_frame=df,
                x=figure_values_dict['x'],
                y=figure_values_dict['y'],
                color=figure_values_dict['color'],
                size=figure_values_dict['size'],
                hover_data=figure_values_dict['hover_data'],
                template=self._template_lookup_dict[template]['chart_template'],
            )

        if figure_values_dict['output_type'] == 'line':
            return px.line(
                data_frame=df,
                x=figure_values_dict['x'],
                y=figure_values_dict['y'],
                color=figure_values_dict['color'],
                hover_data=figure_values_dict['hover_data'],
                template=self._template_lookup_dict[template]['chart_template'],
            )

        if figure_values_dict['output_type'] == 'area':
            return px.area(
                data_frame=df,
                x=figure_values_dict['x'],
                y=figure_values_dict['y'],
                color=figure_values_dict['color'],
                hover_data=figure_values_dict['hover_data'],
                template=self._template_lookup_dict[template]['chart_template'],
            )

        if figure_values_dict['output_type'] == 'bar':
            return px.bar(
                data_frame=df,
                x=figure_values_dict['x'],
                y=figure_values_dict['y'],
                color=figure_values_dict['color'],
                hover_data=figure_values_dict['hover_data'],
                template=self._template_lookup_dict[template]['chart_template'],
            )

        if figure_values_dict['output_type'] == 'violin':
            return px.violin(
                data_frame=df,
                x=figure_values_dict['x'],
                y=figure_values_dict['y'],
                color=figure_values_dict['color'],
                hover_data=figure_values_dict['hover_data'],
                points='all',
                template=self._template_lookup_dict[template]['chart_template'],
            )

        if figure_values_dict['output_type'] == 'scatter_3d':
            return px.scatter_3d(
                data_frame=df,
                x=figure_values_dict['x'],
                y=figure_values_dict['y'],
                z=figure_values_dict['z'],
                color=figure_values_dict['color'],
                hover_data=figure_values_dict['hover_data'],
                template=self._template_lookup_dict[template]['chart_template'],
            )

        if figure_values_dict['output_type'] == 'scatter_geo':
            return px.scatter_geo(
                data_frame=df,
                locations=figure_values_dict['locations'],
                locationmode=figure_values_dict['location_mode'],
                projection=figure_values_dict['projection'],
                color=figure_values_dict['color'],
                size=figure_values_dict['size'],
                hover_data=figure_values_dict['hover_data'],
                template=self._template_lookup_dict[template]['chart_template'],
            )

        if figure_values_dict['output_type'] == 'choropleth':
            return px.choropleth(
                data_frame=df,
                locations=figure_values_dict['locations'],
                locationmode=figure_values_dict['location_mode'],
                projection=figure_values_dict['projection'],
                color=figure_values_dict['color'],
                hover_data=figure_values_dict['hover_data'],
                template=self._template_lookup_dict[template]['chart_template'],
            )

        # who are you? who who, who who
        else:
            raise ValueError(
                """I don't know what to do with a "{}" output_type. Please add it to {}."""
                .format(figure_values_dict['output_type'], __file__)
            )

