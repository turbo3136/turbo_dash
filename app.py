import dash

app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True

# now we load all our data
import plotly.express as px
app1_df = px.data.gapminder()
app2_df = px.data.gapminder()

# let's also set the ID of our app's main wrapper div
wrapper_div_id = 'page-content'
