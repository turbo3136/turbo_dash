import dash

app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True

# now we load all our data
# import plotly.express as px
# df = px.data.gapminder()
