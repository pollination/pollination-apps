import streamlit as st

st.set_page_config(
    page_title='Hello Pollination <> Streamlit', layout='wide',
    page_icon='https://app.pollination.cloud/favicon.ico'
)

# branding, api-key and url
# we should wrap this up as part of the pollination-streamlit library
st.sidebar.image(
    'https://uploads-ssl.webflow.com/6035339e9bb6445b8e5f77d7/616da00b76225ec0e4d975ba_pollination_brandmark-p-500.png',
    use_column_width=True
)

api_key = st.sidebar.text_input(
    'Enter Pollination APIKEY', type='password',
    help=':bulb: You only need an API Key to access private projects. '
    'If you do not have a key already go to the settings tab under your profile to '
    'generate one.'
) or None

query_params = st.experimental_get_query_params()
defult_url = query_params['url'][0] if 'url' in query_params else \
    'https://app.pollination.cloud/projects/chriswmackey/demo/jobs/' \
    '9f7360bd-704c-49ae-8c29-f600f43c9b2b'
