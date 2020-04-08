import dash
import dash_core_components as dcc
import dash_html_components as html

from app import app
import app1
import app2

# this is just a loop to return the
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return html.Div('Hello World')
    elif pathname == '/app1':
        return app1.layout
    elif pathname == '/app2':
        return app2.layout
    # else:
    #     return fourohfour.layout


if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(debug=False)
