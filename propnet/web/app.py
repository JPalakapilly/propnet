import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
from propnet import log_stream
from propnet.web.app_graph import graph_component
from propnet.web.app_model import model_layout, list_models
from propnet.web.app_property import property_layout, list_properties
from propnet.models import all_model_names
from propnet.properties import all_property_names

app = dash.Dash()
server = app.server
app.config.supress_callback_exceptions = True

d3 = "https://d3js.org/d3.v4.min.js"
app.scripts.append_script({"external_url": d3})

# home page
index = html.Div([
    graph_component,
    html.Br(),
    dcc.Markdown('''
Propnet is a knowledge graph for materials science. It is under active
development and not for public release yet.
    '''),
    dcc.Link('All Properties', href='/property'),
    html.Br(),
    dcc.Link('All Models', href='/model'),
    html.Br(),
    dcc.Markdown('''
```
Propnet initialization log:
{}
```'''.format(log_stream.getvalue()))
])

# header
app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Img(src='https://raw.githubusercontent.com/materialsintelligence/'
                 'propnet/master/docs/images/propnet_logo.png', style={'width': 350}),
    html.Br(),
    html.Div(id='page-content')
], style={'marginLeft': 200, 'marginRight': 200, 'marginTop': 50})

# standard Dash css, fork this for a custom theme
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

# routing, current routes defined are:
# / for home page
# /model for model summary
# /model/model_name for information on that model
# /property for property summary
# /property/property_name for information on that property
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/' or pathname is None:
        return index
    elif pathname == '/model':
        return list_models
    elif pathname.startswith('/model'):
        for model in all_model_names:
            if pathname == ('/model/{}'.format(model)):
                return model_layout(model)
    elif pathname == '/property':
        return list_properties
    elif pathname.startswith('/property'):
        for property in all_property_names:
            if pathname == ('/property/{}'.format(property)):
                return property_layout(property)
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=False)