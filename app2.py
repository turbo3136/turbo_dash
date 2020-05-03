from collections import OrderedDict
import plotly.express as px

from app import app
from turbo_dash import turbo_dash
from turbo_dash.inputs import TurboInput
from turbo_dash.outputs import TurboOutput

from config import LOGO_PATH


# ['country', 'continent', 'year', 'lifeExp', 'pop', 'gdpPercap', 'iso_alpha', 'iso_num']
df = px.data.gapminder()


list_of_inputs = [
    TurboInput(
        output_id_list=['app2_test_output'],
        input_type='Dropdown',
        df=df,
        value_column='country',
        input_component_id='app2_test_input',
        filter_input_property_list=['value'],
        lambda_function_list=[
            lambda dataframe, value: dataframe[dataframe['country'] == value]
        ],
        input_label_class_name='sidebar-label',
    ),
    TurboInput(
        output_id_list=['app2_test_output'],
        input_type='RangeSlider',
        df=df,
        value_column='year',
        input_component_id='app2_test_input1',
        filter_input_property_list=['value'],
        lambda_function_list=[
            lambda dataframe, value: dataframe[(dataframe['year'] >= value[0]) & (dataframe['year'] <= value[1])]
        ],
        input_label_class_name='sidebar-label',
    ),
]

list_of_tab1_outputs = [
    TurboOutput(
        output_component_id='app2_test_output',
        output_component_property='figure',
        output_type='line',
        df=df,
        x='year',
        y='lifeExp',
        color='country',
        template='seaborn',
        turbo_input_list=list_of_inputs,
    ),
]
list_of_tab2_outputs = [
    TurboOutput(
        output_component_id='app2_test_output1',
        output_component_property='figure',
        output_type='line',
        df=df,
        x='year',
        y='lifeExp',
        color='country',
        template='seaborn',
        turbo_input_list=list_of_inputs,
    ),
    TurboOutput(
        output_component_id='app2_test_output2',
        output_component_property='figure',
        output_type='line',
        df=df,
        x='year',
        y='gdpPercap',
        color='country',
        template='seaborn',
        turbo_input_list=list_of_inputs,
    ),
]

td = turbo_dash(
    app_to_callback=app,
    list_of_inputs=list_of_inputs,
    dict_of_tab_outputs=OrderedDict([
        ('tab1', list_of_tab1_outputs),
        ('tab2', list_of_tab2_outputs),
    ]),
    layout_template='turbo',
    turbo_header_logo_file_path=LOGO_PATH,
    turbo_header_links_list=[
        {'href': '/app1', 'text': 'app1'},
        {'href': '/app2', 'text': 'app2', 'link_class_name': 'header-link-current'},
    ],
)

layout = td.layout
td.callbacks
