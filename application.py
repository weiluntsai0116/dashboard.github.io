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
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State


# Date and time
def get_time():
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    print(" [DEVELOPMENT] date and time =", dt_string)
    return dt_string


get_time()

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
    # todo: exception handling
    mydb = mysql.connector.connect(
        host=c_info['host'],
        user=c_info['user'],
        password=c_info['password'],
        database="signals"
    )
    mycursor = mydb.cursor()
    print(" [DEVELOPMENT] connection established.")
    return (mydb, mycursor)


def insertTo_table(user_id, signal_id, signal_description, mydb, mycursor):
    sql = "INSERT INTO signals.signals (signal_id, signal_name, signal_description, user_id, datetime) \
    VALUES (%s, %s, %s, %s, %s)"
    dt_string = get_time()
    val = (signal_id, "signal_name_dummy", signal_description, user_id, dt_string)
    mycursor.execute(sql, val)
    mydb.commit()
    print(sql, val)
    print(mycursor.rowcount, "record inserted.")


def update_table(user_id, signal_id, signal_description, mydb, mycursor):
    sql = "UPDATE signals.signals SET signal_description = %s, datetime = %s where user_id = %s and signal_id =%s"
    dt_string = get_time()
    val = (signal_description, dt_string, user_id, signal_id)
    mycursor.execute(sql, val)
    mydb.commit()
    print(sql, val)
    print(mycursor.rowcount, "record updated")


def deleteFrom_table(user_id, signal_id, mydb, mycursor):
    sql = "DELETE FROM signals.signals WHERE user_id = %s and signal_id = %s"
    val = (user_id, signal_id)
    mycursor.execute(sql, val)
    mydb.commit()
    print(sql, val)
    print(mycursor.rowcount, "record deleted")


def selectFrom_table(user_id, signal_id, mydb, mycursor):
    sql = "SELECT * FROM signals.signals where user_id = %s and signal_id = %s"
    val = (user_id, signal_id)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)


(mydb, mycursor) = build_connection()
# insertTo_table('user51', 'signal0', 'signal_description', mydb, mycursor)
# selectFrom_table('user2', 'signal0', mydb, mycursor)
# update_table('user0', 'signal0', 'description', mydb, mycursor) # if it fails, run "SET SQL_SAFE_UPDATES=0;" in mysql workbench
# deleteFrom_table('user5', 'signal0', mydb, mycursor)

# Dash app
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

app.title = 'Dashboard Page'
app.layout = html.Div([

    html.H3(
        children='Dashboard',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }),

    html.Br(),
    dbc.Row([
        dbc.Col(html.Div(["User ID:   ", dcc.Input(id='user_id-state', placeholder="0", type='text', value='')]),
            width=2),
        dbc.Col(html.Div(["Signal ID: ", dcc.Input(id='signal_id-state', placeholder="0", type='text', value='')]),
            width=2),
        dbc.Col(html.Div(["Signal name: ", dcc.Input(id='signal_name-state', placeholder="SignalName", type='text', value='')]),
            width=2)
    ], justify="center"),

    html.Br(),
    dbc.Row([
        dbc.InputGroup(
            [  # todo: user input format tbd (github link or what?)
                dbc.InputGroupAddon("GitHub link", addon_type="prepend"),
                dbc.Input(id='github-state',
                          placeholder="https://weiluntsai0116.github.io/dashboard.github.io/user0_signal0.html"),
            ],
            className="mb-3", style={'width': 800, 'align': 'center'}
        )
    ], justify="center"),
    dbc.Row([
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Description", addon_type="prepend"),
                dbc.Textarea(id='description-state', placeholder="Any comments?")
            ],
            className="mb-3", style={'width': 800, 'align': 'center'}
        )
    ], justify="center"),

    dbc.Row([
        dbc.Col(dbc.Button("Create", color="success", className="mr-1", id='create-button', n_clicks=0), width=2),
        dbc.Col(dbc.Button('Read', color="primary", className="mr-1", id='readit-button', n_clicks=0), width=2),
        dbc.Col(dbc.Button('Modify', color="warning", className="mr-1", id='modify-button', n_clicks=0), width=2),
        dbc.Col(dbc.Button("Delete", color="danger", className="mr-1", id='delete-button', n_clicks=0), width=2)
    ], justify="center"),

    dbc.Tooltip("Create a signal", target="create-button", placement='left'),
    dbc.Tooltip("Read a signal", target="readit-button", placement='left'),
    dbc.Tooltip("Modify a signal", target="modify-button", placement='left'),
    dbc.Tooltip("Delete a signal", target="delete-button", placement='right'),

    html.Br(),
    dbc.Row([
        dbc.Col(html.Div(id='userid-output'), width=2),
        dbc.Col(html.Div(id='signalid-output'), width=2),
        dbc.Col(html.Div(id='description-output', style={'whiteSpace': 'pre-line'}), width=2),
    ], justify="center"),

    html.Br(),
    dbc.Row([
        dbc.Col(html.Div(id='create-output'), width=2),
        dbc.Col(html.Div(id='readit-output'), width=2),
        dbc.Col(html.Div(id='modify-output'), width=2),
        dbc.Col(html.Div(id='delete-output'), width=2)
    ], justify="center"),

    # dbc.Modal(
    #     [
    #         dbc.ModalHeader("Warning!"),
    #         dbc.ModalBody("Not yet completed!"),
    #         dbc.ModalFooter(
    #             dbc.Button("Close", id="close", className="ml-auto")
    #         ),
    #     ],
    #     id="modal",
    # ),
    dcc.ConfirmDialog(
        id='delete-confirm',
        message='Danger danger! Your just press the \'Delete\' button. \nAre you sure you want to continue?',
    ),

    html.Br(),
    dbc.Row([
        html.Div(id='dash-output')
    ], justify="center"),
])


@app.callback(Output('delete-confirm', 'displayed'),
              Input('delete-button', 'n_clicks'))
def display_confirm(n_clicks):
    if n_clicks:
        return True
    return False


# @app.callback(
#     Output("modal", "is_open"),
#     [Input('create-button', 'n_clicks'),
#      Input('modify-button', 'n_clicks'),
#      Input("delete-button", "n_clicks"),
#      Input("close", "n_clicks")],
#     [State("modal", "is_open")],
# )
# def toggle_modal(create_n_clicks, modify_n_clicks,
#                  delete_n_clicks, close_modal, is_open):
#     if delete_n_clicks or modify_n_clicks or delete_n_clicks or close_modal:
#         return not is_open
#     return is_open

@app.callback([Output('userid-output', 'children'),
               Output('signalid-output', 'children'),
               Output('description-output', 'children')],
              [Input('delete-confirm', 'submit_n_clicks'),
               Input('modify-button', 'n_clicks'),
               Input('create-button', 'n_clicks'),
               Input('readit-button', 'n_clicks')],
              [State('user_id-state', 'value'),
               State('signal_id-state', 'value'),
               State('description-state', 'value')])
def info_disp(delete_n_clicks, modify_n_clicks, create_n_clicks, readit_n_clicks,
              user_id, signal_id, description):
    user_id = u'''User ID   : {}'''.format(user_id)
    signal_id = u'''Signal ID: {}'''.format(signal_id)
    description = u'''Description: {}'''.format(description)
    return user_id, signal_id, description


@app.callback(
    Output('create-output', 'children'),
    [Input('create-button', 'n_clicks')],
    [State('user_id-state', 'value'),
     State('signal_id-state', 'value'),
     State('description-state', 'value')])
def create_dash(create_n_clicks, user_id, signal_id, signal_description):
    if user_id != "" and signal_id != "":
        insertTo_table(user_id, signal_id, signal_description, mydb, mycursor)
        # todo: 1. use regex will be better
        # todo: 2. should be implemented in def insertTo_table()
        # todo: 3. should use INSERT IGNORE INTO
    create = u'''Create: {} times'''.format(create_n_clicks)
    return create


@app.callback(
    Output('modify-output', 'children'),
    [Input('modify-button', 'n_clicks')],
    [State('user_id-state', 'value'),
     State('signal_id-state', 'value'),
     State('description-state', 'value')])
def modify_dash(modify_n_clicks, user_id, signal_id, signal_description):
    if user_id != "" and signal_id != "":  # todo: as mentioned in create_dash
        update_table(user_id, signal_id, signal_description, mydb, mycursor)
    modify = u'''Modify: {} times'''.format(modify_n_clicks)
    return modify


@app.callback(
    [Output('readit-output', 'children'),
     Output('dash-output', 'children')],
    [Input('readit-button', 'n_clicks')],
    [State('user_id-state', 'value'),
     State('signal_id-state', 'value')])
def read_dash(readit_n_clicks,
              user_id, signal_id):
    read = u'''Read  : {} times'''.format(readit_n_clicks)
    if user_id == "" and signal_id == "":
        user_id = "user0"
        signal_id = "signal0"
    iframe = html.Iframe(src=f'https://weiluntsai0116.github.io/dashboard.github.io/user{user_id}_signal{signal_id}.html',
                         height=500, width=1000)
    return read, iframe


@app.callback(
    Output('delete-output', 'children'),
    [Input('delete-confirm', 'submit_n_clicks')],
    [State('user_id-state', 'value'),
     State('signal_id-state', 'value'),
     State('description-state', 'value')])
def delete_dash(delete_n_clicks, user_id, signal_id, signal_description):
    if user_id != "" and signal_id != "":  # todo: as mentioned in create_dash
        deleteFrom_table(user_id, signal_id, mydb, mycursor)
    delete = u'''Delete: {} times'''.format(delete_n_clicks)
    return delete


if __name__ == '__main__':
    application.run(debug=True, port=8080)
