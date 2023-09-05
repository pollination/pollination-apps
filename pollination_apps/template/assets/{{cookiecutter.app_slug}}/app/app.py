{%- if cookiecutter.sdk == "streamlit" -%}
import streamlit as st

st.write("Welcome! Start writing your Pollination app here.")

{%- elif cookiecutter.sdk == "dash" -%}
from dash import Dash, html

app = Dash(__name__)
app.title = "Hello Pollination"

server = app.server

app.layout = html.Div([
    html.Div(children='Welcome! Start writing your Pollination app here.')
])

if __name__ == '__main__':
    app.run_server(debug=True)
{% endif %}
