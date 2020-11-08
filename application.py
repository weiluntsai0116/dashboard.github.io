# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
application = app.server

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}

embeds = {
    'user_0': {'signal_0': 'user0_signal0.html'},
    'user_1': {'signal_0': 'user1_signal0.html'}
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
    html.Br(),
    html.Button(id='create-button1-state', n_clicks=0, children='Create'),
    html.Button(id='readit-button2-state', n_clicks=0, children='Read'),
    html.Button(id='modify-button3-state', n_clicks=0, children='Modify'),
    html.Button(id='delete-button4-state', n_clicks=0, children='Delete'),
    html.Div(id='create-output-state1'),
    html.Div(id='readit-output-state2'),
    html.Div(id='modify-output-state3'),
    html.Div(id='delete-output-state4'),
    html.Br(),
    html.Div(id='userid-output-state5'),
    html.Div(id='sigid-output-state6'),
    html.Hr(),
    html.Div(id='dash-output-state1'),
])


@app.callback([Output('create-output-state1', 'children'),
               Output('readit-output-state2', 'children'),
               Output('modify-output-state3', 'children'),
               Output('delete-output-state4', 'children'),
               Output('userid-output-state5', 'children'),
               Output('sigid-output-state6', 'children')],
              [Input('create-button1-state', 'n_clicks'),
               Input('readit-button2-state', 'n_clicks'),
               Input('modify-button3-state', 'n_clicks'),
               Input('delete-button4-state', 'n_clicks')],
              [State('user_id-state', 'value'),
               State('signal_id-state', 'value')])
def info_disp(create_n_clicks, readit_n_clicks,
                  modify_n_clicks, delete_n_clicks,
                  input1, input2):
    create    = u'''Create: {} times'''.format(create_n_clicks)
    read      = u'''Read  : {} times'''.format(readit_n_clicks)
    modify    = u'''Modify: {} times'''.format(modify_n_clicks)
    delete    = u'''Delete: {} times'''.format(delete_n_clicks)
    user_id   = u'''Use ID   : {}'''.format(input1)
    signal_id = u'''Signal ID: {}'''.format(input2)
    return create, read, modify, delete, user_id, signal_id

@app.callback(
              Output('dash-output-state1', 'children'),
              [Input('readit-button2-state', 'n_clicks')],
              [State('user_id-state', 'value'),
               State('signal_id-state', 'value')])
def read_dash(readit_n_clicks,
              input1, input2):
    iframe = html.Iframe(src=f'https://weiluntsai0116.github.io/dashboard.github.io/{input1}_{input2}.html',
                         height=500, width=1500)
    return iframe


if __name__ == '__main__':
    application.run(debug=True, port=8080)
