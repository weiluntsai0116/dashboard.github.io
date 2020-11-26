# -*- coding: utf-8 -*-
import os
import pymysql
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from pandas import DataFrame
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# get date and time
now = datetime.now()
dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
# print("date and time =", dt_string)

# DB manipulation
c_info = {
    "host": os.getenv('USER_SERVICE_HOST'),
    "user": os.getenv('USER_SERVICE_USER'),
    "password": os.getenv("USER_SERVICE_PASSWORD"),
    "port": int(os.getenv("USER_SERVICE_PORT")),
    "cursorclass": pymysql.cursors.DictCursor,
}


def get_connection():
    conn = pymysql.connect(**c_info)
    return conn


def read_signals(user_id):
    conn = get_connection()
    df = pd.read_sql(
        f"select * "
        f"from signals.signals "
        f"where user_id = {user_id}",
        conn
    )
    return df


def write_signals():
    conn = create_engine(
        f'mysql+pymysql://{c_info["user"]}:{c_info["password"]}@{c_info["host"]}:{c_info["port"]}/signals?charset=utf8')

    signals = {
        'signal_id': ['signal_id_003'],
        'signal_name': ['signal_name_003'],
        'signal_description': ['signal_description_003'],
        'user_id': ['user_id_003']
    }
    df = DataFrame(signals, columns=['signal_id', 'signal_name', 'signal_description', 'user_id'])
    df.to_sql(name='signals', con=conn, if_exists='append', index=False)


def build_connection():
    mydb = mysql.connector.connect(
        host=c_info['host'],
        user=c_info['user'],
        password=c_info['password'],
        database="signals"
    )
    mycursor = mydb.cursor()
    return (mydb, mycursor)


def insertTo_table(mydb, mycursor):
    sql = "INSERT INTO signals.signals (signal_id, signal_name, signal_description, user_id) VALUES (%s, %s, %s, %s)"
    val = ("signal_id_004", "signal_name_004", "signal_description_004", "user_id_004")
    mycursor.execute(sql, val)
    mydb.commit()
    # print(mycursor.rowcount, "record inserted.")


def update_table(mydb, mycursor):
    sql = "UPDATE signals.signals SET signal_description = %s where user_id = %s;"
    val = ("modified 2!", "user_id_001")
    mycursor.execute(sql, val)
    mydb.commit()
    # print(mycursor.rowcount, "record updated")


def deleteFrom_table(mydb, mycursor):
    sql = "DELETE FROM signals.signals WHERE user_id = %s and signal_id = %s"
    val = ("user_id_002", "signal_id_002")
    mycursor.execute(sql, val)
    mydb.commit()
    # print(mycursor.rowcount, "record deleted")


def selectFrom_table(mydb, mycursor):
    sql = "SELECT * FROM signals.signals where user_id = %s and signal_id = %s"
    val = ("user_id_003", "signal_id_003")
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


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
