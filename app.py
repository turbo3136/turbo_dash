import dash

# do some Dash stuff
app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True

# let's also set the ID of our app's main wrapper div
wrapper_div_id = 'page-content'
