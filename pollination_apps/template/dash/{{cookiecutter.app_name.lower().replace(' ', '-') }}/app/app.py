import os
import pollination_dash_io
import dash
from dash import html
from dash.dependencies import Input, Output
import dash_renderjson

base_path = os.getenv('POLLINATION_API_URL', 'https://api.pollination.cloud')

app = dash.Dash(__name__)
server = app.server

api_key = pollination_dash_io.ApiKey()


app.layout = html.Div([
    api_key.component,
    html.Div(children='Welcome! Start writing your Pollination app here.'),
    pollination_dash_io.AuthUser(id='auth-user', basePath=base_path),
    pollination_dash_io.SelectProject(id='po-select-project',
                                      projectOwner='antoinedao',
                                      basePath=base_path),
    html.Div(id='output-form')
])

api_key.create_api_key_callback(app=app, component_ids=['auth-user', 'po-select-project'])

@app.callback(
    Output(component_id='output-form',
      component_property='children'),
    Input(component_id='po-select-project',
      component_property='project')
)
def get_value_from_recipe_form(data):
    return dash_renderjson.DashRenderjson(id='json-out',
                                          data={ 'project': data })

if __name__ == '__main__':
    app.run_server(debug=True)
