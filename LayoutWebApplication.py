import dash
import dash_core_components as dcc
import dash_html_components as html
from DatasetPython import *
layout = html.Div([
    dcc.Tabs(
        tabs=[{'label': i, 'value': i} for i in Tabs],
        value='English student',
        id='tabs',
        style={
        'width': '80%',
        'fontFamily': 'Sans-Serif',
        'margin-left': 'auto',
        'margin-right': 'auto'}),

    dcc.Dropdown(
        id = 'type_to_plot',
        options=[
        {'label': 'Score', 'value': 'Score'},
        {'label': 'Type1', 'value': 'Type1'},
        {'label': 'Type2', 'value': 'Type2'}],
        value="Score"),

    dcc.Graph(id='graph'),

    html.H1('Your state'),
    html.Div(id='state'),
    html.H1('Choose role and subject'),
    dcc.Dropdown(
        id = 'role_and_subject',
        options=[
        {'label': 'None', 'value': 'None'},
        {'label': 'Student', 'value': 'Student'},
        {'label': 'Teacher', 'value': 'Teacher'},
        {'label': 'English', 'value': 'English'},
        {'label': 'Math', 'value': 'Math'},
        {'label': 'Physics', 'value': 'Physics'}],
        multi=True,
        value="None"),
    html.H1('Choose test number'),
    dcc.Input(id='test_number', value='Test number', type= 'number'),
    html.H1('Choose your anwers'),
    # The firts 25 questions here
    html.Div([dcc.Dropdown(id='input'+str(i), placeholder = "Question " + str(i)) for i in range(1, 26)], style = {'width': '38%','display': 'inline-block'}),
    # The second 25 questions here
    html.Div([dcc.Dropdown(id='input'+str(i), placeholder = "Question " + str(i)) for i in range(26, 51)],style = {'width': '38%','float': 'right','display': 'inline-block'}),
    html.H1('Submit your anwers and see the sending status'),
        dcc.RadioItems(
            id='complete_confirm',
            options=[{'label': 'I have done', 'value':'I have done'}, {'label':'I have not done.............', 'value': 'I have not done' }],
            value= 'I have not done',
            style={'display': 'inline-block'}),
    html.Button(id='submit_button',type='n-clicks', children='Submit', style = {'display': 'inline-block'}),
    html.Div(id='status', style = {'display': 'inline-block'})
    ])
