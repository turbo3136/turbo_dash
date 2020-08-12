from typing import Dict, Any
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

from ._helpers import generate_random_string
from ._lookups import _filter_type_lookup, _list_of_chart_strings


class turbo_filter(object):
    """object to set defaults and organize data about the filter

    Methods:
        create_html: create the html for this filter
    """

    _filter_type_lookup_dict = _filter_type_lookup

    def __init__(
            self,
            filter_type: str = None,
            input_filter_type: str = None,
            column: str = None,
            label_column: str = None,
            default_value: Any = None,
    ):
        """

        Args:
            filter_type (:obj: `str`, optional): string representing the filter object. If filter_type
                is None, input_filter_type must be provided.
            input_filter_type (:obj: `str`, optional): string representing the input_filter we'll
                use to control the output. For example,
                'x' gives us a Dropdown filter with all the column names in our dataset,
                'output_type' gives us a Dropdown filter with all the chart types available to us.
            column (:obj: `str`, optional): string representing the column of the dataframe
                used for the values of this filter
            label_column (:obj: `str`, optional): string representing the column of the dataframe
                used for the labels of this filter
            default_value (:obj: `Any`, optional): default value for this filter
        """
        self.filter_type = filter_type
        self.input_filter_type = input_filter_type
        self.column = column
        self.label_column = label_column if label_column is not None else self.column
        self.default_value = default_value

        # grab some important data
        self.component_id = '{}-{} - {}'.format(self.filter_type, self.column, generate_random_string())
        self.persistence = True  # todo: do we want to allow different values for persistence and persistence_type?
        self.persistence_type = 'memory'

        # assemble the dash dependencies input list, this is an important part
        self.dash_dependencies_input_list = [  # comprehend the list of dash.dependencies.Input
            dash.dependencies.Input(component_id=self.component_id, component_property=input_property)
            for input_property in self._filter_input_property_list
        ]

    def create_html(
            self,
            template: str,
            df: pd.DataFrame,
            location: str,
            template_lookup_dict: Dict[str, Dict[str, str]],
    ) -> html.Div:
        """create the html for this filter

        Args:
            template (str): layout template we want to use. Options include:
                ['default', 'turbo', 'turbo-dark']
            df (pandas.DataFrame): dataframe for this filter
            location (str): location of this filter to help us determine attributes
                like the CSS class it should have
            template_lookup_dict (Dict[str, Dict[str, str]]): dict we'll use to lookup
                class names based on the template

        Returns:
            html.Div
        """
        class_name_prefix = '{}_filter'.format(location)
        class_name_suffix = 'className'
        wrapper_class_name_lookup = '{}_wrapper_{}'.format(class_name_prefix, class_name_suffix)
        label_class_name_lookup = '{}_label_{}'.format(class_name_prefix, class_name_suffix)
        filter_class_name_lookup = '{}_{}'.format(class_name_prefix, class_name_suffix)

        wrapper_class_name = template_lookup_dict[template][wrapper_class_name_lookup]
        label_class_name = template_lookup_dict[template][label_class_name_lookup]
        filter_class_name = template_lookup_dict[template][filter_class_name_lookup]

        # now we dive into specific filters
        if self.input_filter_type is None:  # if this isn't for an input filter, grab the html for a normal filter
            return self._assemble_html_for_filter(
                df=df,
                wrapper_class_name=wrapper_class_name,
                label_class_name=label_class_name,
                filter_class_name=filter_class_name,
            )
        else:  # if this is for an input filter, grab the html for an input filter
            return self._assemble_html_for_input_filter(
                df=df,
                wrapper_class_name=wrapper_class_name,
                label_class_name=label_class_name,
                filter_class_name=filter_class_name,
            )

    """protected methods"""
    @property
    def _filter_input_property_list(self):
        return self._filter_type_lookup_dict[self.filter_type]['input_property_list']

    def _assemble_html_for_filter(
            self,
            df: pd.DataFrame,
            wrapper_class_name: str,
            label_class_name: str,
            filter_class_name: str,
    ) -> html.Div:
        """assemble the html for a filter

        Args:
            df (pandas.DataFrame): dataframe this filter will use
            wrapper_class_name (str): CSS class name for the filter's wrapper
            label_class_name (str): CSS class name for the filter's label
            filter_class_name (str): CSS class name for the filter's filter

        Returns:
            html.Div
        """
        if self.filter_type == 'Dropdown':
            # if it's a Dropdown, we'll create a list of dicts that look like {'label': label, 'value': value}
            filter_options = [
                # groupby objects are cool, they create a list of grouped values and their dfs
                # since we're grouping by both label and value, we get a tuple returned with the df
                # note that we don't use the df
                {'label': label_value_tuple[0], 'value': label_value_tuple[1]}
                for label_value_tuple, label_value_df in df.groupby([self.label_column, self.column])
            ]

            return html.Div(
                className=wrapper_class_name,
                children=[
                    html.Div(
                        className=label_class_name,
                        children=self.label_column,
                    ),
                    dcc.Dropdown(
                        id=self.component_id,
                        className=filter_class_name,
                        options=filter_options,
                        value=self.default_value,
                        persistence=self.persistence,
                        persistence_type=self.persistence_type,
                    ),
                ],
            )

        if self.filter_type == 'Checklist':
            # if it's a Checklist, we'll create a list of dicts that look like {'label': label, 'value': value}
            filter_options = [
                # groupby objects are cool, they create a list of grouped values and their dfs
                # since we're grouping by both label and value, we get a tuple returned with the df
                # note that we don't use the df
                {'label': label_value_tuple[0], 'value': label_value_tuple[1]}
                for label_value_tuple, label_value_df in df.groupby([self.label_column, self.column])
            ]

            # for a Checklist, we need to change the default value to an empty list if it's None
            if self.default_value is None:
                self.default_value = []

            return html.Div(
                className=wrapper_class_name,
                children=[
                    html.Div(
                        className=label_class_name,
                        children=self.label_column,
                    ),
                    dcc.Checklist(
                        id=self.component_id,
                        className=filter_class_name,
                        options=filter_options,
                        value=self.default_value,
                        persistence=self.persistence,
                        persistence_type=self.persistence_type,
                    ),
                ],
            )

        if self.filter_type == 'RangeSlider':
            values = sorted(df[self.column].unique())  # grab the values in order
            minimum = min(values)
            maximum = max(values)
            # todo: support different columns for labels and values
            marks = {str(val): {'label': str(val), 'style': {'transform': 'rotate(45deg)'}} for val in values}

            return html.Div(
                className=wrapper_class_name,
                children=[
                    html.Div(
                        className=label_class_name,
                        children=self.label_column,
                    ),
                    dcc.RangeSlider(
                        id=self.component_id,
                        className=filter_class_name,
                        min=minimum,
                        max=maximum,
                        value=self.default_value if self.default_value is not None else [minimum, maximum],
                        marks=marks,
                        step=None,
                        persistence=self.persistence,
                        persistence_type=self.persistence_type,
                    ),
                ],
            )

        # who are you? who who, who who
        else:
            raise ValueError(
                """I don't know what to do with a "{}" filter_type. Please add it to {}."""
                .format(self.filter_type, __file__)
            )

    def _assemble_html_for_input_filter(
            self,
            df: pd.DataFrame,
            wrapper_class_name: str,
            label_class_name: str,
            filter_class_name: str,
    ) -> html.Div:
        """assemble the html for an input filter, not a normal filter

        Args:
            df (pandas.DataFrame): dataframe this filter will use
            wrapper_class_name (str): CSS class name for the filter's wrapper
            label_class_name (str): CSS class name for the filter's label
            filter_class_name (str): CSS class name for the filter's filter

        Returns:
            html.Div
        """
        if self.input_filter_type in ('x', 'y', 'z'):
            # for these input_filter_types we want a list of columns as the filter options
            filter_options = [{'label': col, 'value': col} for col in df.columns.values]

            return html.Div(
                className=wrapper_class_name,
                children=[
                    html.Div(
                        className=label_class_name,
                        children=self.label_column,
                    ),
                    dcc.Dropdown(
                        id=self.component_id,
                        className=filter_class_name,
                        options=filter_options,
                        value=self.default_value,
                        persistence=self.persistence,
                        persistence_type=self.persistence_type,
                    ),
                ],
            )

        if self.input_filter_type == 'output_type':
            # for this input_filter_type we want to grab a list of all supported chart options
            filter_options = [{'label': chart_string, 'value': chart_string} for chart_string in _list_of_chart_strings]

            return html.Div(
                className=wrapper_class_name,
                children=[
                    html.Div(
                        className=label_class_name,
                        children=self.label_column,
                    ),
                    dcc.Dropdown(
                        id=self.component_id,
                        className=filter_class_name,
                        options=filter_options,
                        value=self.default_value,
                        persistence=self.persistence,
                        persistence_type=self.persistence_type,
                    ),
                ],
            )

        # who are you? who who, who who
        else:
            raise ValueError(
                """I don't know what to do with a "{}" input_filter_type. Please add it to {}."""
                .format(self.input_filter_type, __file__)
            )
