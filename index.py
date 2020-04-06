import operator
import plotly.express as px

from app import app
from turbo_dash import turbo_dash
from turbo_dash.inputs import TurboInput, TurboFilter
from turbo_dash.outputs import TurboOutput


# ['country', 'continent', 'year', 'lifeExp', 'pop', 'gdpPercap', 'iso_alpha', 'iso_num']
df = px.data.gapminder()


list_of_inputs = [
    TurboInput(
        output_id_list=['test_output'],
        input_type='Dropdown',
        df=df,
        value_column='country',
        label_column='country',
        turbo_filter_object=TurboFilter(
            input_component_id='test_input',
            filter_input_property_list=['value'],
            input_operator_list=[operator.eq],
        ),
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
    )
]

td = turbo_dash(
    app_to_callback=app,
    list_of_inputs=list_of_inputs,
    list_of_outputs=list_of_outputs,
    layout_template='turbo',
)

app.layout = td.layout
td.callbacks


if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(debug=False)
