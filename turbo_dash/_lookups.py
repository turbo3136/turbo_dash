from collections import OrderedDict
import plotly.express as px

"""templates"""
_template_lookup = {
    'turbo': {
        # chart template
        'chart_template': 'seaborn',

        # header
        'header_className': 'header',
        'header_logo_className': 'logo',
        'header_links_className': 'header-links',
        'header_link_className': 'header-link',
        'header_link_current_className': 'header-link-current',

        # menu and content
        'menu_and_content_className': 'menu-and-content',

        # menu
        'menu_className': 'menu',
        'menu_filter_wrapper_className': 'menu-filter-wrapper',
        'menu_filter_label_className': 'menu-filter-label',
        'menu_filter_className': 'menu-filter',

        # content
        'content_className': 'content',
        'content_output_and_filter_wrapper_className': 'content-output-and-filter-wrapper',
        'content_filter_wrapper_className': 'content-filter-wrapper',
        'content_filter_label_className': 'content-filter-label',
        'content_filter_className': 'content-filter',
        'content_output_wrapper_className': 'content-output-wrapper',
        'content_output_label_className': 'content-output-label',
        'content_output_className': 'content-output',

    },

    'turbo-dark': {
        # chart template
        'chart_template': 'plotly_dark',

        # header
        'header_className': 'header-dark',
        'header_logo_className': 'logo-dark',
        'header_links_className': 'header-links-dark',
        'header_link_className': 'header-link-dark',
        'header_link_current_className': 'header-link-current-dark',

        # menu and content
        'menu_and_content_className': 'menu-and-content-dark',

        # menu
        'menu_className': 'menu-dark',
        'menu_filter_wrapper_className': 'menu-filter-wrapper-dark',
        'menu_filter_label_className': 'menu-filter-label-dark',
        'menu_filter_className': 'menu-filter-dark',

        # content
        'content_className': 'content-dark',
        'content_output_and_filter_wrapper_className': 'content-output-and-filter-wrapper-dark',
        'content_filter_wrapper_className': 'content-filter-wrapper-dark',
        'content_filter_label_className': 'content-filter-label-dark',
        'content_filter_className': 'content-filter-dark',
        'content_output_wrapper_className': 'content-output-wrapper-dark',
        'content_output_label_className': 'content-output-label-dark',
        'content_output_className': 'content-output-dark',

    },
}

"""filters"""
_filter_type_lookup = {
    'Checklist': {
        'input_property_list': ['value'],
        'lambda_function_list': [
            lambda dataframe, column, value: dataframe[dataframe[column].isin(value)] if value else dataframe,
        ],
    },

    'DatePickerRange': {
        'input_property_list': ['start_date', 'end_date'],
        'lambda_function_list': [
            lambda dataframe, column, value: dataframe[dataframe[column] >= value] if value else dataframe,  # start
            lambda dataframe, column, value: dataframe[dataframe[column] <= value] if value else dataframe,  # end
        ],
    },

    'DatePickerSingle': {
        'input_property_list': ['date'],
        'lambda_function_list': [
            lambda dataframe, column, value: dataframe[dataframe[column] == value] if value else dataframe,
        ],
    },

    'Dropdown': {
        'input_property_list': ['value'],
        'lambda_function_list': [
            lambda dataframe, column, value: dataframe[dataframe[column] == value] if value else dataframe,
        ],
    },

    'Dropdown-multi': {
        'input_property_list': ['value'],
        'lambda_function_list': [
            lambda dataframe, column, value: dataframe[dataframe[column].isin(value)] if value else dataframe,
        ],
    },

    'RadioItems': {
        'input_property_list': ['value'],
        'lambda_function_list': [
            lambda dataframe, column, value: dataframe[dataframe[column] == value] if value else dataframe,
        ],
    },

    'RangeSlider': {
        'input_property_list': ['value'],
        'lambda_function_list': [
            lambda dataframe, column, value:
            dataframe[(dataframe[column] >= value[0]) & (dataframe[column] <= value[1])],
        ],
    },

    'Slider': {
        'input_property_list': ['value'],
        'lambda_function_list': [
            lambda dataframe, column, value: dataframe[dataframe[column] == value] if value else dataframe,
        ],
    },

}

"""filter type from chart input type"""
_chart_input_to_filter_type_lookup = {
    'output_type': 'Dropdown',
    'x': 'Dropdown',
    'y': 'Dropdown-multi',
    'z': 'Dropdown',
    'color': 'Dropdown',
    'size': 'Dropdown',
    'hover_name': 'Dropdown',
    'hover_data': 'Dropdown-multi',
    'locations': 'Dropdown',
    'locationmode': 'Dropdown',
    'projection': 'Dropdown',
}

"""plotly objects"""
_chart_lookup_dict = OrderedDict([
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
        'violin', {
            'object': px.violin,
            'inputs': ['data_frame', 'x', 'y', 'color', 'hover_data', 'template'],
        }
    ),
    (
        'scatter_3d', {
            'object': px.scatter_3d,
            'inputs': ['data_frame', 'x', 'y', 'z', 'color', 'size', 'hover_data', 'template'],
        }
    ),
    (
        'scatter_geo', {
            'object': px.scatter_geo,
            'inputs': [
                'data_frame',
                'locations',
                'locationmode',
                'color',
                'size',
                'hover_data',
                'template',
                'projection',
            ],
        }
    ),
    (
        'choropleth', {
            'object': px.choropleth,
            'inputs': [
                'data_frame',
                'locations',
                'locationmode',
                'color',
                'hover_data',
                'template',
                'projection',
            ],
        }
    ),
])

# not supported yet
# histogram
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

_list_of_chart_strings = list(_chart_lookup_dict.keys())

_arg_options_lookup_dict = OrderedDict([
    (
        'projection', [  # projection arg, used by scatter_geo
            'equirectangular',
            'mercator',
            'orthographic',
            'natural earth',
            'kavrayskiy7',
            'miller',
            'robinson',
            'eckert4',
            'azimuthal equal area',
            'azimuthal equidistant',
            'conic equal area',
            'conic conformal',
            'conic equidistant',
            'gnomonic',
            'stereographic',
            'mollweide',
            'hammer',
            'transverse mercator',
            'albers usa',
            'winkel tripel',
            'aitoff',
            'sinusoidal'
        ]
    ),
    (
        'locationmode', [
            'ISO-3',
            'USA-states',
            'country names',
        ]
    ),
])


def _get_chart_dict(chart_string):
    """return the dictionary for the specified plotly express chart"""
    ret_dict = _chart_lookup_dict.get(chart_string)

    if ret_dict:
        return ret_dict
    else:
        raise ValueError(
            """I don't have a plotly object for "{}" output type. You might need to add it to {}."""
            .format(chart_string, __file__)
        )


def _get_chart_dict_value(chart_string, key):
    """return a key from the dict corresponding to the chart_string"""
    return _get_chart_dict(chart_string).get(key)


def get_chart_object(chart_string):
    """return the plotly express object corresponding to the chart_string"""
    return _get_chart_dict_value(chart_string, key='object')


def get_chart_inputs(chart_string):
    """return the plotly express input arguments corresponding to the chart_string"""
    return _get_chart_dict_value(chart_string, key='inputs')


def get_arg_options(arg_string):
    """return a list of argument options corresponding to the arg_string"""
    return _arg_options_lookup_dict.get(arg_string)
