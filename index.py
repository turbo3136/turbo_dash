import dash
import dash_core_components as dcc
import dash_html_components as html

from app import app, wrapper_div_id
import app1
import app2
import homepage
import fourohfour

# this initial layout is an empty div with our wrapper_div_id from the app
# also notice the dcc.Location object. This tracks what page we're on.
# We can also use it to do fancy stuff like track filter values if we want.
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id=wrapper_div_id)
])


@app.callback(
    dash.dependencies.Output(wrapper_div_id, 'children'),
    [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return homepage.layout
    elif pathname == '/app1':
        return app1.layout
    elif pathname == '/app2':
        return app2.layout
    else:
        return fourohfour.layout


if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(debug=False)
