from datetime import datetime
import pandas as pd
import plotly.express as px

from app import app
from turbo_dash import turbo_dash
from turbo_dash.inputs import TurboInput
from turbo_dash.outputs import TurboOutput

from config import LOGO_PATH

# ['country', 'continent', 'year', 'lifeExp', 'pop', 'gdpPercap', 'iso_alpha', 'iso_num']
df = px.data.gapminder()
df['datetime'] = pd.to_datetime(df['year'], format='%Y')  # create a datetime column for our DatePicker examples


list_of_inputs = [
    TurboInput(
        output_id_list=['test_output'],
        input_type='Dropdown',
        df=df,
        value_column='country',
        input_component_id='test_input',
        filter_input_property_list=['value'],
        lambda_function_list=[
            lambda dataframe, value: dataframe[dataframe['country'] == value]
        ],
        input_label_class_name='sidebar-label',
    ),
    TurboInput(
        output_id_list=['test_output'],
        input_type='RangeSlider',
        df=df,
        value_column='year',
        input_component_id='test_input1',
        filter_input_property_list=['value'],
        lambda_function_list=[
            lambda dataframe, value: dataframe[(dataframe['year'] >= value[0]) & (dataframe['year'] <= value[1])]
        ],
        input_label_class_name='sidebar-label',
    ),
    TurboInput(
        output_id_list=['test_output'],
        input_type='Checklist',
        df=df,
        value_column='continent',
        input_component_id='test_input2',
        filter_input_property_list=['value'],
        lambda_function_list=[
            lambda dataframe, value: dataframe[dataframe['continent'].isin(value)]
        ],
        input_label_class_name='sidebar-label',
    ),
    TurboInput(
        output_id_list=['test_output'],
        input_type='RadioItems',
        df=df,
        value_column='continent',
        input_component_id='test_input3',
        filter_input_property_list=['value'],
        lambda_function_list=[
            lambda dataframe, value: dataframe[dataframe['continent'] == value]
        ],
        input_label_class_name='sidebar-label',
    ),
    TurboInput(
        output_id_list=['test_output'],
        input_type='Slider',
        df=df,
        value_column='year',
        input_component_id='test_input4',
        filter_input_property_list=['value'],
        lambda_function_list=[
            lambda dataframe, value: dataframe[dataframe['year'] == value]
        ],
        input_label_class_name='sidebar-label',
    ),
    TurboInput(
        output_id_list=['test_output'],
        input_type='DatePickerSingle',
        df=df,
        value_column='datetime',
        input_component_id='test_input5',
        filter_input_property_list=['date'],
        lambda_function_list=[
            lambda dataframe, date: dataframe[dataframe['datetime'] == date]
        ],
        input_label_class_name='sidebar-label',
    ),
    TurboInput(
        output_id_list=['test_output'],
        input_type='DatePickerRange',
        df=df,
        value_column='datetime',
        input_component_id='test_input6',
        filter_input_property_list=['start_date', 'end_date'],
        lambda_function_list=[
            lambda dataframe, start_date: dataframe[dataframe['datetime'] >= start_date],
            lambda dataframe, end_date: dataframe[dataframe['datetime'] <= end_date],
        ],
        input_label_class_name='sidebar-label',
        default_value=[datetime(1952, 1, 1), datetime(2007, 1, 1)]
    ),
]

list_of_outputs = [
    TurboOutput(
        output_component_id='test_output',
        output_component_property='figure',
        output_type='bar',
        df=df,
        x='year',
        y='pop',
        color='country',
        template='seaborn',
        turbo_input_list=list_of_inputs,
        graph_input_list=[
            'output_type',
            'x',
            'y',
            'z',
            'color',
            'size',
            'hover_data',
            'locations',
            'locationmode',
            'projection'
        ],
        wrapper_class_name='output',
    )
]


td = turbo_dash(
    app_to_callback=app,
    list_of_inputs=list_of_inputs,
    list_of_outputs=list_of_outputs,
    layout_template='turbo',
    turbo_header_logo_file_path=LOGO_PATH,
    turbo_header_links_list=[
        {'href': '/app1', 'text': 'app1', 'link_class_name': 'header-link-current'},
        {'href': '/app2', 'text': 'app2'},
    ],
)

layout = td.layout
td.callbacks
