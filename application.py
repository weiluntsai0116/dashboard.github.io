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
import subprocess as cmd
import apps.db_access as db_access


external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server


app.title = 'Dashboard Page'
app.layout = html.Div([

    html.H3(
        children='Dashboard',
        style={
            'textAlign': 'center',
            'color': '#000000'
        }),

    html.Br(),
    dbc.Row([
        dbc.Col(html.Div(["User ID:   ", dcc.Input(id='user_id-state', placeholder="0", type='text', value='')]),
                width=2),
        dbc.Col(html.Div(["Signal ID: ", dcc.Input(id='signal_id-state', placeholder="0", type='text', value='')]),
                width=2),
        dbc.Col(html.Div(
            ["Signal name: ", dcc.Input(id='signal_name-state', placeholder="SignalName", type='text', value='')]),
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
        dbc.Col(html.Div(id='github-output', style={'whiteSpace': 'pre-line'}), width=2),
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
        html.Div(id='dash-output')
    ], justify="center"),
])


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


@app.callback(Output('delete-confirm', 'displayed'),
              Input('delete-button', 'n_clicks'))
def delete_confirm(n_clicks):
    if n_clicks:
        return True
    return False


@app.callback([Output('userid-output', 'children'),
               Output('signalid-output', 'children'),
               Output('description-output', 'children'),
               Output('github-output', 'children')],
              [Input('delete-confirm', 'submit_n_clicks'),
               Input('modify-button', 'n_clicks'),
               Input('create-button', 'n_clicks'),
               Input('readit-button', 'n_clicks')],
              [State('user_id-state', 'value'),
               State('signal_id-state', 'value'),
               State('description-state', 'value'),
               State('github-state', 'value')])
def info_disp(delete_n_clicks, modify_n_clicks, create_n_clicks, readit_n_clicks,
              user_id, signal_id, description, github):
    user_id = u'''User ID   : {}'''.format(user_id)
    signal_id = u'''Signal ID: {}'''.format(signal_id)
    description = u'''Description: {}'''.format(description)
    github = u'''Github link: {}'''.format(github)
    return user_id, signal_id, description, github


@app.callback(
    Output('create-output', 'children'),
    [Input('create-button', 'n_clicks')],
    [State('user_id-state', 'value'),
     State('signal_id-state', 'value'),
     State('description-state', 'value'),
     State('github-state', 'value')])
def create_dash(create_n_clicks, user_id, signal_id, signal_description, github):
    if (user_id == "" or signal_id == "" or github is None) and create_n_clicks != 0:
        create = u'''Create result: Fail! Lack of User ID, Signal ID, or GitHub link'''
    elif db_access.is_exist(user_id, signal_id) and create_n_clicks != 0:  # todo: as mentioned in create_dash
        create = u'''Create result: Fail! (User ID, Signal ID) is 'duplicate'''
    elif create_n_clicks != 0:
        # todo: 1. use regex will be better
        # todo: 2. should be implemented in def insertTo_table()
        # todo: 3. should use INSERT IGNORE INTO
        # -----------------------------------------------------------------------------
        # todo for Eric: Please insert your function call here. parameter you may need: user_id, signal_id, github.
        #                1. User's github link: {github}
        #                2. The naming format of the new html file should be:
        #                https://weiluntsai0116.github.io/dashboard.github.io/user{user_id}_signal{signal_id}.html
        #                3. Please test if it works by:
        #                   0) imagine you're an user.
        #                     - Use the dashcode template (.py) you wrote
        #                     - Generate .html
        #                     - Upload .html you wrote to your github.
        #                   1) create a new signal: fill out User ID, Signal ID, Github link, and press the Create button
        #                   2) wait for a while (DB update, html upload)
        #                   3) read back the signal: fill out the same User ID, Signal ID, and press the Read button
        #                   4) If the figure you expected appear below, then you complete the integration
        #                4. deployment error: 99% from the requirements.txt
        # -----------------------------------------------------------------------------

        # 0. Process link to be raw data link

        contents_list = github.split('/')
        raw_link = None
        if "github.com" not in contents_list or 'blob' not in contents_list:
            print("The provided github link is invalid. ")
            create = "The provided github link is invalid. "
        else:
            github_idx = contents_list.index("github.com")
            raw_lists = contents_list[github_idx + 1:]
            raw_lists.remove('blob')

            raw_lists.insert(0, "https://raw.githubusercontent.com")
            raw_link = "/".join(raw_lists)
            print(raw_link)
            db_access.insert_signal(user_id, signal_id, signal_description)
            create = 'Create result: Pass!'

        # 1. download from github link and modify the filename as we need
        try:
            cp = cmd.run(f"wget -O user{user_id}_signal{signal_id}.html {raw_link}", check=True, shell=True)
            print(cp)
        except:
            print("Download file failed.")

        # 3. upload to github
        try:
            cp = cmd.run("git add .", check=True, shell=True)
            print("Git add: ")
            print(cp)
            cp = cmd.run(f"git commit -m 'upload user file'", check=True, shell=True)
            print("Git commit: ")
            print(cp)

            cp = cmd.run("git push -u origin main -f", check=True, shell=True)
            print("Git push: ")
            print(cp)

        except:
            print("Didn't upload to github. ")
            # return False

        # u'''Create: {} times'''.format(create_n_clicks)
    elif create_n_clicks != 0:
        create = u'''Create result: Fail! Lack of User ID, Signal ID, or GitHub link'''
    else:
        create = 'Create: 0 times'
    return create


@app.callback(
    Output('modify-output', 'children'),
    [Input('modify-button', 'n_clicks')],
    [State('user_id-state', 'value'),
     State('signal_id-state', 'value'),
     State('description-state', 'value'),
     State('github-state', 'value')])
def modify_dash(modify_n_clicks, user_id, signal_id, signal_description, github):
    if (user_id == "" or signal_id == "") and modify_n_clicks != 0:
        modify = u'''Modify result: Fail! Lack of User ID, Signal ID, or GitHub link'''
    elif not db_access.is_exist(user_id, signal_id) and modify_n_clicks != 0:  # todo: as mentioned in create_dash
        modify = u'''Modify result: Fail! (User ID, Signal ID) is not exist'''
    elif modify_n_clicks != 0:
        db_access.update_signal(user_id, signal_id, signal_description)
        # -----------------------------------------------------------------------------
        # todo for Eric: Please insert your function call here. parameter you may need: user_id, signal_id, github.
        #                1. User's github link: {github}
        #                2. The naming format of the new html file should be:
        #                https://weiluntsai0116.github.io/dashboard.github.io/user{user_id}_signal{signal_id}.html
        #                3. Please test if it works by:
        #                   0) imagine you're an user.
        #                     - Use the dashcode template (.py) you wrote
        #                     - Generate .html
        #                     - Upload .html you wrote to your github.
        #                   1) create a new signal: fill out User ID, Signal ID, Github link, and press the Create button
        #                   2) wait for a while (DB update, html upload)
        #                   3) read back the signal: fill out the same User ID, Signal ID, and press the Read button
        #                   4) If the figure you expected appear below, then you complete the integration
        #                4. deployment error: 99% from the requirements.txt
        # -----------------------------------------------------------------------------

        # 1. download from github link and modify the filename as we need
        try:
            cp = cmd.run(f"wget -O user{user_id}_signal{signal_id}.html {github}", check=True, shell=True)
            print(cp)
        except:
            print("Download file failed.")

        # 2. Modify name to be user{user_id}_signal{signal_id}.html
        user_fn = github.split('/')[-1]
        try:
            cp = cmd.run(f"mv {user_fn} user{user_id}_signal{signal_id}.html", check=True, shell=True)
            print(cp)
        except:
            print("Change filename failed.")

        # 3. upload to github
        try:
            cp = cmd.run("git add .", check=True, shell=True)
            print("Git add: ")
            print(cp)
            cp = cmd.run(f"git commit -m 'update user file'", check=True, shell=True)
            print("Git commit: ")
            print(cp)

            cp = cmd.run("git push -u origin main -f", check=True, shell=True)
            print("Git push: ")
            print(cp)

        except:
            print("Didn't upload to github. ")
            # return False

        modify = 'Modify result: Pass!'  # u'''Modify: {} times'''.format(modify_n_clicks)
    else:
        modify = 'Modify: 0 times'
    return modify


@app.callback(
    [Output('readit-output', 'children'),
     Output('dash-output', 'children')],
    [Input('readit-button', 'n_clicks')],
    [State('user_id-state', 'value'),
     State('signal_id-state', 'value')])
def read_dash(readit_n_clicks,
              user_id, signal_id):
    if (user_id == "" or signal_id == "") and readit_n_clicks != 0:
        read = u'''Read result: Fail! Lack of User ID or Signal ID'''
    elif not db_access.is_exist(user_id, signal_id) and readit_n_clicks != 0:  # todo: as mentioned in create_dash
        read = u'''Read result: Fail! (User ID, Signal ID) is not exist'''
    elif readit_n_clicks != 0:
        read = u'''Read result: Pass!'''
    else:
        read = 'Read: 0 times'
    iframe = html.Iframe(
        src=f'https://weiluntsai0116.github.io/dashboard.github.io/user{user_id}_signal{signal_id}.html',
        height=500, width=1000)
    return read, iframe


@app.callback(
    Output('delete-output', 'children'),
    [Input('delete-confirm', 'submit_n_clicks')],
    [State('user_id-state', 'value'),
     State('signal_id-state', 'value'),
     State('description-state', 'value')])
def delete_dash(delete_n_clicks, user_id, signal_id, signal_description):
    if (user_id == "" or signal_id == "") and delete_n_clicks is not None:
        delete = u'''Delete result: Fail! Lack of User ID or Signal ID'''
    elif not db_access.is_exist(user_id, signal_id) and delete_n_clicks is not None:  # todo: as mentioned in create_dash
        delete = u'''Delete result: Fail! (User ID, Signal ID) is not exist'''
    elif delete_n_clicks is not None:
        db_access.delete_signal(user_id, signal_id)
        delete = u'''Delete result: Pass!'''
    else:
        delete = 'Delete: 0 times'
    return delete


if __name__ == '__main__':
    application.run(debug=True, port=8080)
