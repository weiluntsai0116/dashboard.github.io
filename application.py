# -*- coding: utf-8 -*-
import os
import pymysql
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
from pandas import DataFrame
from datetime import datetime
import flask
import re
import csv
import boto3
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import jwt
from cryptography.fernet import Fernet, InvalidToken  # new
import apps.db_access as db_access
import apps.test_and_upload as app_upload
import apps.security as security
import plotly.express as px
from io import StringIO
# import logging
#
# logging.basicConfig(filename="dashboard_service.log",
#                     filemode='a',
#                     format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
#                     datefmt='%H:%M:%S',
#                     level=logging.DEBUG)
# logging.getLogger()
# logging.error("Starting Dashboard Service")

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server

app.title = 'Dashboard Page'
app.layout = html.Div([

    dcc.Location(id='dashboard_url', refresh=False),
    html.Div(id='error_redirect_page'),

    dbc.Row([
        dbc.Col(dbc.Button("Login Page", color="link", id='button_login', n_clicks=0), width=2),
        dbc.Col(dbc.Button('Catalog Page', color="link", id='button_catalog', n_clicks=0), width=2),
        dbc.Col(dbc.Button("Alert Page", color="link", id='button_alert', n_clicks=0), width=2),
        dbc.Col(dbc.Button("User Page", color="link", id='button_user', n_clicks=0), width=2),
    ], justify="center"),

    html.H1(
        children='Dashboard',
        style={
            'textAlign': 'center',
            'color': '#000000'
        }),

    html.Br(),
    dbc.Row([
        dbc.Col(html.Div(id='username-output'), width=2),
        # dbc.Col(html.Div(["User ID:   ", dcc.Input(id='user_id-state', placeholder="0", type='text', value='')]),
        #         width=2),
        dbc.Col(html.Div(["Signal ID (Read/Modify/Delete only): ",
                          dcc.Input(id='signal_id-state', placeholder="0", type='text', value='')]),
                width=2),
        # dbc.Col(html.Div(
        #     ["Signal name: ", dcc.Input(id='signal_name-state', placeholder="SignalName", type='text', value='')]),
        #     width=2)
    ], justify="center"),

    html.Br(),
    dbc.Row([
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("S3 filename", addon_type="prepend"),
                dbc.Input(id='s3-state',
                          placeholder="your-signal-data.csv"),
            ],
            className="mb-3", style={'width': 800, 'align': 'center'}
        )
    ], justify="center"),
    dbc.Row([
        dbc.InputGroup(
            [
                dbc.InputGroupAddon("Description", addon_type="prepend"),
                dbc.Textarea(id='description-state', placeholder="signal name or any comments")
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
        dbc.Col(html.Div(id='signalid-output'), width=2),
        dbc.Col(html.Div(id='description-output', style={'whiteSpace': 'pre-line'}), width=2),
        dbc.Col(html.Div(id='s3-output', style={'whiteSpace': 'pre-line'}), width=2),
    ], justify="center"),

    html.Br(),
    dbc.Row([
        dbc.Col(html.Div(id='create-output'), width=2),
        dbc.Col(html.Div(id='readit-output'), width=2),
        dbc.Col(html.Div(id='modify-output'), width=2),
        dbc.Col(html.Div(id='delete-output'), width=2)
    ], justify="center"),

    dcc.ConfirmDialog(
        id='delete-confirm',
        message='Danger danger! Your just press the \'Delete\' button. \nAre you sure you want to continue?',
    ),

    # dbc.Button("Modal with scrollable body", id="open"),
    # dbc.Modal(
    #     [
    #         dbc.ModalHeader("Error"),
    #         dbc.ModalBody("Test result: Fail."),
    #         dbc.ModalBody("Please check with the tech support team."),
    #         dbc.ModalFooter(
    #             dbc.Button(
    #                 "Close", id="close", className="ml-auto"
    #             )
    #         ),
    #     ],
    #     id="modal",
    #     scrollable=True,
    # ),

    html.Br(),
    dbc.Row([
        html.Div(id='dash-output'),

    ], justify="center"),

    # html.Button('Login Page', id='button_login', n_clicks=0),
    # html.Button('Catalog Page', id='button_catalog', n_clicks=0),
    # html.Button('Alert Page', id='button_alert', n_clicks=0),
    html.Div(id='login_redirect'),
    html.Div(id='catalog_redirect'),
    html.Div(id='alert_redirect'),
    html.Div(id='user_redirect'),

    # session div for global vars. meant to be hidden.
    html.Div(id='user_id-state', style={'display': 'none'}),
    # html.Div(id='test_out'),
])


@app.callback(Output('login_redirect', 'children'),
              Input('button_login', 'n_clicks'),
              Input('dashboard_url', 'href'))
def login_redirect(click, pathname):
    if click != 0:
        return dcc.Location(href=security.login_url, id="any")


@app.callback(Output('catalog_redirect', 'children'),
              Input('button_catalog', 'n_clicks'),
              Input('dashboard_url', 'href'))
def catalog_redirect(click, pathname):
    path_info = pathname.split("?token=")
    if len(path_info) != 2:
        return dcc.Location(href=security.login_url, id="any")
    if click != 0:
        signed_token = path_info[1]
        return dcc.Location(href=f"{security.catalog_url}?token={signed_token}", id="any")


@app.callback(Output('alert_redirect', 'children'),
              Input('button_alert', 'n_clicks'),
              Input('dashboard_url', 'href'))
def alert_redirect(click, pathname):
    path_info = pathname.split("?token=")
    if len(path_info) != 2:
        return dcc.Location(href=security.login_url, id="any")
    if click != 0:
        signed_token = path_info[1]
        return dcc.Location(href=f"{security.alert_url}?token={signed_token}", id="any")


@app.callback(Output('user_redirect', 'children'),
              Input('button_user', 'n_clicks'),
              Input('dashboard_url', 'href'))
def user_redirect(click, pathname):
    path_info = pathname.split("?token=")
    if len(path_info) != 2:
        return dcc.Location(href=security.login_url, id="any")
    if click != 0:
        signed_token = path_info[1]
        return dcc.Location(href=f"{security.user_url}?token={signed_token}", id="any")


@app.callback(Output('error_redirect_page', 'children'),
              Output('user_id-state', 'children'),
              Output('username-output', 'children'),
              [Input('dashboard_url', 'href')])
def check_token(pathname):
    # URL format: http://xxx/xxxx?token=iamatoken

    path_info = pathname.split("?token=")
    print("pathname = ", pathname, "path_info = ", path_info)
    if len(path_info) != 2:  # check if token exist
        return dcc.Location(href=security.login_url, id="any"), "", ""

    signed_token = path_info[1]

    # dev_mode:
    # True: always authorized; user_id = 11;
    # False: token is needed; user_id = 2;
    if signed_token == "demo":
        dev_mode = True
    else:
        dev_mode = False

    if dev_mode:
        user_id = 11
        print("User Name: ", db_access.get_user_name_by_user_id(user_id))
        return '', user_id, u'''User Name: {}'''.format(db_access.get_user_name_by_user_id(user_id))
    else:
        f = Fernet(security.fernet_secret)
        try:
            jwt_token = f.decrypt(signed_token.encode("utf-8")).decode("utf-8")
        except (InvalidToken, TypeError):
            print("exception 1: ", InvalidToken, "; fernet_secret: ", security.fernet_secret)
            return dcc.Location(href=security.login_url, id="any"), "", ""
        # print("jwt_token = ", jwt_token)
        # flask.session['token'] = jwt_token
        # print("session token = ", flask.session['token'])

        if jwt_token.startswith("Bearer "):
            jwt_token = jwt_token[7:]
        try:
            payload = jwt.decode(jwt_token, security.jwt_secret,
                                 algorithms=[security.jwt_algo])
            # payload = {
            #     "user_id": user["user_id"],
            #     "role": user["role"],
            #     "email": user["email"],
            #     "exp": datetime.utcnow() + timedelta(seconds=jwt_exp_delta_sec)
            # }

            if payload["role"] not in {"support", "ip"}:
                print("exception 2")
                return dcc.Location(href=security.login_url,
                                    id="any"), "", ""  # ["Permission Denied", 403] # ["Not authenticated", 400]
            else:
                print("user_id = ", payload['user_id'], u'''User ID: {} User Name: '''.format(payload['user_id']),
                      db_access.get_user_name_by_user_id(payload['user_id']))
                return "", payload['user_id'], u'''User Name: {}'''.format(
                    db_access.get_user_name_by_user_id(payload['user_id']))  # everything's good
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            print("exception 3")
            return dcc.Location(href=security.login_url, id="any"), "", ""  # ["Token is invalid", 401]
        return dcc.Location(href=security.login_url, id="any"), "", ""  # something unexpected happened


# @app.callback(Output('test_out', 'children'),
#               Input('user_id', 'children'))
# def get_user_id(user_id):
#     print("user_id = ", user_id)
#     return user_id


@app.callback(Output('delete-confirm', 'displayed'),
              Input('delete-button', 'n_clicks'))
def delete_confirm(n_clicks):
    if n_clicks:
        return True
    return False


@app.callback([
    Output('signalid-output', 'children'),
    Output('description-output', 'children'),
    Output('s3-output', 'children')],
    [Input('delete-confirm', 'submit_n_clicks'),
     Input('modify-button', 'n_clicks'),
     Input('create-button', 'n_clicks'),
     Input('readit-button', 'n_clicks')],
    [State('user_id-state', 'children'),
     State('signal_id-state', 'value'),
     State('description-state', 'value'),
     State('s3-state', 'value')])
def info_disp(delete_n_clicks, modify_n_clicks, create_n_clicks, readit_n_clicks,
              user_id, signal_id, description, s3):
    user_id = u'''User ID   : {}'''.format(user_id)
    signal_id = u'''Signal ID: {}'''.format(signal_id)
    description = u'''Description: {}'''.format(description)
    s3 = u'''S3 link: {}'''.format(s3)
    return signal_id, description, s3


@app.callback(
    Output('create-output', 'children'),
    [Input('create-button', 'n_clicks')],
    [State('user_id-state', 'children'),
     State('signal_id-state', 'value'),
     State('description-state', 'value'),
     State('s3-state', 'value')])
def create_dash(create_n_clicks, user_id, signal_id, signal_description, s3):
    if create_n_clicks != 0:
        if s3 is None:
            create = u'''Create: Fail! Lack of S3 filename'''
        elif '.csv' not in s3:
            create = u'''Create: Fail! S3 filename format should be *.csv'''
        else:
            signal_id_list = db_access.get_all_signal_id()
            signal_id = db_access.first_missing_positive(signal_id_list)
            if user_id == "" or signal_id == "":
                create = u'''Create: Fail! Lack of Signal ID'''
            elif type(signal_id) != int:
                create = u'''Create: Fail! Invalid signal ID'''
            elif db_access.is_signal_exist(user_id, signal_id):
                create = u'''Create: Fail! (User ID, Signal ID) is 'duplicate'''
            else:
                try:
                    client = boto3.client('s3', aws_access_key_id=security.aws_id,
                                          aws_secret_access_key=security.aws_secret)

                    csv_obj = client.get_object(Bucket='user-signal-data', Key=s3)
                    db_access.insert_signal(user_id, signal_id, signal_description, s3)
                    create = 'Create: Pass!'
                except Exception as e:
                    create = u'''Create: Fail! S3 file \"{}\" is not exist: {}'''.format(s3, e)
    else:
        create = 'Create: 0 times'
    return create


@app.callback(
    Output('modify-output', 'children'),
    [Input('modify-button', 'n_clicks')],
    [State('user_id-state', 'children'),
     State('signal_id-state', 'value'),
     State('description-state', 'value'),
     State('s3-state', 'value')])
def modify_dash(modify_n_clicks, user_id, signal_id, signal_description, s3):
    if modify_n_clicks != 0:
        if user_id == "" or signal_id == "":
            modify = u'''Modify: Fail! Lack of User ID, Signal ID'''
        elif s3 is not None and s3 != "" and ('.csv' not in s3):
            modify = u'''Create: Fail! S3 filename format should be *.csv'''
        elif not re.search('^\d*$', signal_id):
            modify = u'''Modify: Fail! Invalid signal ID'''
        elif not db_access.is_signal_exist(user_id, signal_id):
            modify = u'''Modify: Fail! (User ID, Signal ID) is not exist'''
        else:
            if s3 is not None and s3 != "":
                try:
                    client = boto3.client('s3', aws_access_key_id=security.aws_id,
                                          aws_secret_access_key=security.aws_secret)

                    csv_obj = client.get_object(Bucket='user-signal-data', Key=s3)
                    db_access.update_signal(user_id, signal_id, signal_description, s3)
                    modify = 'Modify: Pass!'  # u'''Modify: {} times'''.format(modify_n_clicks)
                except Exception as e:
                    modify = u'''Create: Fail! S3 file \"{}\" is not exist: {}'''.format(s3, e)
            else:
                db_access.update_signal(user_id, signal_id, signal_description, s3)
                modify = 'Modify: Pass!'  # u'''Modify: {} times'''.format(modify_n_clicks)
    else:
        modify = 'Modify: 0 times'
    return modify


@app.callback(
    [Output('readit-output', 'children'),
     Output('dash-output', 'children')],
    [Input('readit-button', 'n_clicks')],
    [State('user_id-state', 'children'),
     State('signal_id-state', 'value')])
def read_dash(readit_n_clicks,
              user_id, signal_id):
    s3_df, cols = None, None
    if readit_n_clicks != 0:
        if user_id == "" or signal_id == "":
            read = u'''Read: Fail! Lack of User ID or Signal ID'''
        elif not re.search('^\d*$', signal_id):
            read = u'''Create: Fail! Invalid signal ID'''
        elif not db_access.is_signal_exist(user_id, signal_id):
            read = u'''Read: Fail! (User ID, Signal ID) is not exist'''
        else:
            s3_filename = db_access.read_signal(user_id, signal_id)
            print("user_id = ", user_id, "signal_id = ", signal_id)
            print("s3_filename = ", s3_filename)

            client = boto3.client('s3', aws_access_key_id=security.aws_id,
                                  aws_secret_access_key=security.aws_secret)

            csv_obj = client.get_object(Bucket='user-signal-data', Key=s3_filename)
            body = csv_obj['Body']
            csv_string = body.read().decode('utf-8')
            s3_df = pd.read_csv(StringIO(csv_string))

            # for local test :
            # s3_df = pd.read_csv(s3_filename)

            print("s3_df = ", s3_df)
            cols = list(s3_df.columns)

            if len(cols) < 2:
                read = "Data has less than 2 columns "
            else:
                read = u'''Read: Pass!'''
    else:
        read = 'Read: 0 times'
    iframe = html.Iframe(
        src=f'https://weiluntsai0116.github.io/dashboard.github.io/user{user_id}_signal{signal_id}.html',
        height=500, width=1000)

    if read != u'''Read: Pass!''':
        return read, None

    # this fig must be plot outside otherwise it won't show
    fig = px.line(s3_df, x=cols[0], y=cols[1])
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    return read, html.Div(dcc.Graph(figure=fig))


@app.callback(
    Output('delete-output', 'children'),
    [Input('delete-confirm', 'submit_n_clicks')],
    [State('user_id-state', 'children'),
     State('signal_id-state', 'value'),
     State('description-state', 'value')])
def delete_dash(delete_n_clicks, user_id, signal_id, signal_description):
    if delete_n_clicks is not None:
        if user_id == "" or signal_id == "":
            delete = u'''Delete: Fail! Lack of User ID or Signal ID'''
        elif not re.search('^\d*$', signal_id):
            delete = u'''Create: Fail! Invalid signal ID'''
        elif not db_access.is_signal_exist(user_id, signal_id):
            delete = u'''Delete: Fail! (User ID, Signal ID) is not exist'''
        else:
            s3_filename = db_access.read_signal(user_id, signal_id)
            db_access.delete_signal(user_id, signal_id)
            myresult = db_access.is_csv_needed(s3_filename)
            if not myresult:
                s3_rsc = boto3.resource(u's3')
                bucket = s3_rsc.Bucket(u'user-signal-data')
                bucket.Object(key=s3_filename).delete()
            # print("myresult =", myresult)
            delete = u'''Delete: Pass!'''
    else:
        delete = u'''Delete: 0 times'''
    return delete


# @app.callback(
#     Output("modal", "is_open"),
#     [
#         Input("open", "n_clicks"),
#         Input("close", "n_clicks"),
#     ],
#     [State("modal", "is_open")],
# )
# def toggle_modal(n1, n2, is_open):
#     if n1 or n2:
#         return not is_open
#     return is_open

if __name__ == '__main__':
    application.run(debug=True, port=8080)
