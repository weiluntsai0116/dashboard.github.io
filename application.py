# -*- coding: utf-8 -*-
import os
import pymysql
# import pandas as pd
# from sqlalchemy import create_engine
# from pandas import DataFrame
# from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# # get date and time
# now = datetime.now()
# dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
# # print("date and time =", dt_string)
#
# # DB manipulation
# c_info = {
#     "host": os.getenv('USER_SERVICE_HOST'),
#     "user": os.getenv('USER_SERVICE_USER'),
#     "password": os.getenv("USER_SERVICE_PASSWORD"),
#     "port": int(os.getenv("USER_SERVICE_PORT")),
#     "cursorclass": pymysql.cursors.DictCursor,
# }
#
#
# def get_connection():
#     conn = pymysql.connect(**c_info)
#     return conn
#
#
# def read_signals(user_id):
#     conn = get_connection()
#     df = pd.read_sql(
#         f"select * "
#         f"from signals.signals "
#         f"where user_id = {user_id}",
#         conn
#     )
#     return df
#
#
# def write_signals():
#     conn = create_engine(
#         f'mysql+pymysql://{c_info["user"]}:{c_info["password"]}@{c_info["host"]}:{c_info["port"]}/signals?charset=utf8')
#
#     signals = {
#         'signal_id': ['signal_id_001'],
#         'signal_name': ['signal_name_001'],
#         'signal_description': ['signal_description_001'],
#         'user_id': ['user_id_001']
#     }
#     df = DataFrame(signals, columns=['signal_id', 'signal_name', 'signal_description', 'user_id'])
#     df.to_sql(name='signals', con=conn, if_exists='replace', index=False)


# df = read_signals(0)
# print(df)
# write_signals()

# dash app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

app.layout = html.Div([
    html.H3(
        children='Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Div(["User ID:   ",
              dcc.Input(id='user_id-state', type='text', value='user0')]),
    html.Div(["Signal ID: ",
              dcc.Input(id='signal_id-state', type='text', value='signal0')]),
    html.Div(["Description: ",
              dcc.Textarea(id='description-state', value='description', style={'width': '50%', 'height': 50})]),
    html.Br(),
    html.Button(id='create-button', n_clicks=0, children='Create'),
    html.Button(id='readit-button', n_clicks=0, children='Read'),
    html.Button(id='modify-button', n_clicks=0, children='Modify'),
    html.Button(id='delete-button', n_clicks=0, children='Delete'),
    html.Br(),
    html.Div(id='userid-output'),
    html.Div(id='signalid-output'),
    html.Div(id='description-output', style={'whiteSpace': 'pre-line'}),
    html.Div(id='create-output'),
    html.Div(id='readit-output'),
    html.Div(id='modify-output'),
    html.Div(id='delete-output'),
    html.Hr(),
    html.Div(id='dash-output'),
], style={'columnCount': 3, "height": "100vh"})


@app.callback([Output('create-output', 'children'),
               Output('readit-output', 'children'),
               Output('modify-output', 'children'),
               Output('delete-output', 'children'),
               Output('userid-output', 'children'),
               Output('signalid-output', 'children'),
               Output('description-output', 'children')],
              [Input('create-button', 'n_clicks'),
               Input('readit-button', 'n_clicks'),
               Input('modify-button', 'n_clicks'),
               Input('delete-button', 'n_clicks')],
              [State('user_id-state', 'value'),
               State('signal_id-state', 'value'),
               State('description-state', 'value')])
def info_disp(create_n_clicks, readit_n_clicks,
              modify_n_clicks, delete_n_clicks,
              user_id, signal_id, description):
    create = u'''Create: {} times'''.format(create_n_clicks)
    read = u'''Read  : {} times'''.format(readit_n_clicks)
    modify = u'''Modify: {} times'''.format(modify_n_clicks)
    delete = u'''Delete: {} times'''.format(delete_n_clicks)
    user_id = u'''Use ID   : {}'''.format(user_id)
    signal_id = u'''Signal ID: {}'''.format(signal_id)
    description = u'''Description: {}'''.format(description)
    return create, read, modify, delete, user_id, signal_id, description


@app.callback(
    Output('dash-output', 'children'),
    [Input('readit-button', 'n_clicks')],
    [State('user_id-state', 'value'),
     State('signal_id-state', 'value')])
def read_dash(readit_n_clicks,
              user_id, signal_id):
    iframe = html.Iframe(src=f'https://weiluntsai0116.github.io/dashboard.github.io/{user_id}_{signal_id}.html',
                         height=500, width=800)
    return iframe


'''
@app.callback()
def create_dash()
    return 
'''

'''
@app.callback()
def modify_dash()
    return 
'''

'''
@app.callback()
def delete_dash()
    return 
'''

if __name__ == '__main__':
    application.run(debug=True, port=8080)
