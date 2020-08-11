from typing import Dict, Any
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html

from ._helpers import generate_random_string


class turbo_filter(object):
    """object to set defaults and organize data about the filter

    Methods:
        create_html: create the html for this filter
    """

    def __init__(
            self,
            filter_type: str = None,
            column: str = None,
            label_column: str = None,
            default_value: Any = None,
    ):
        """

        Args:
            filter_type (:obj: `str`, optional): string representing the filter object or the
                string representing the input_filter we'll use to control the output. For example,
                'x' gives us a Dropdown filter with all the column names in our dataset,
                'output_type' gives us a Dropdown filter with all the chart types available to us.
            column (:obj: `str`, optional): string representing the column of the dataframe
                used for the values of this filter
            label_column (:obj: `str`, optional): string representing the column of the dataframe
                used for the labels of this filter
            default_value (:obj: `Any`, optional): default value for this filter
        """
        self.filter_type = filter_type
        self.column = column
        self.label_column = label_column if label_column is not None else self.column
        self.default_value = default_value

        # grab some important data
        self.component_id = '{}-{} - {}'.format(self.filter_type, self.column, generate_random_string())
        self.persistence = True  # todo: do we want to allow different values for persistence and persistence_type?
        self.persistence_type = 'memory'

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
        wrapper_class_name = '{}_wrapper_{}'.format(class_name_prefix, class_name_suffix)
        label_class_name = '{}_label_{}'.format(class_name_prefix, class_name_suffix)
        filter_class_name = '{}_{}'.format(class_name_prefix, class_name_suffix)

        # now we dive into specific filters
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
                className=template_lookup_dict[template][wrapper_class_name],
                children=[
                    html.Div(
                        className=template_lookup_dict[template][label_class_name],
                        children=self.label_column,
                    ),
                    dcc.Dropdown(
                        id=self.component_id,
                        className=template_lookup_dict[template][filter_class_name],
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
                className=template_lookup_dict[template][wrapper_class_name],
                children=[
                    html.Div(
                        className=template_lookup_dict[template][label_class_name],
                        children=self.label_column,
                    ),
                    dcc.Checklist(
                        id=self.component_id,
                        className=template_lookup_dict[template][filter_class_name],
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
                className=template_lookup_dict[template][wrapper_class_name],
                children=[
                    html.Div(
                        className=template_lookup_dict[template][label_class_name],
                        children=self.label_column,
                    ),
                    dcc.RangeSlider(
                        id=self.component_id,
                        className=template_lookup_dict[template][filter_class_name],
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
