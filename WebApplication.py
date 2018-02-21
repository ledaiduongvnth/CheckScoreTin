from NatureLanguageProcessing import *
from LayoutWebApplication import *
from LayoutListTests import *
from Dataset import *
import plotly.graph_objs as go
app = dash.Dash();app.layout = layout_teacher
from dash.dependencies import Input, Output, State
import pandas as pd

print(dcc.__version__) # 0.6.0 or above is required
app = dash.Dash()
app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page_content'),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'})])
# Update the homepage
@app.callback(Output('page_content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page_teacher':
        return layout_teacher
    elif pathname == '/page_student':
        return layout_student
    elif pathname == '/page_list_test':
        return layout_list_test
    else:
        return layout_home_page
# You could also return a 404 "URL not found" page here
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})
# /////////////////////////////////////////////////////////////////CallBack for home page/////////////////////////////////////////////////////////////////////////
# @app.callback(Output('graphs','children'),[Input('subject_plot', 'value')])
# def UpdateDataAndPlotGraphSecond(tab):
#     obj = EnglishStudent() if tab == Subjects[0] else (MathStudent() if tab == Subjects[1] else PhysicsStudent())
#     obj.UpdateAllTest()
#     graph = [dcc.Graph(id='g',figure= {'data': obj.GetDataForGraphForClass(obj.file_preprocessed_data), 'layout': go.Layout(
#                 title = 'PRESENTATION OF SCORES AND EFFECTIONCIES',
#                 yaxis={'range': [0, 10]},
#                 margin={'l': 20, 'b': 20, 't': 70, 'r': 20},
#                 legend={'x': 1, 'y': 1},
#             )})]
#     data = obj.GetDataForGraphForClassSecond(obj.file_preprocessed_data, Categories[tab])
#     graphs = [dcc.Graph(id= id,figure= {'data': data_i, 'layout': go.Layout(
#                 title= id,
#                 yaxis={'range': [0, 100]},
#                 margin={'l': 20, 'b': 20, 't': 70, 'r': 20},
#                 legend={'x': 1, 'y': 1},
#             )})
#               for id, data_i in zip(Categories[tab], data)]
#     return graph + graphs
# //////////////////////////////////////////////////////////////////CallBack for teacher page//////////////////////////////////////////////////////////////////////
# Give user the his or her state to fill number of next test
@app.callback(Output('state_teacher', 'children'),[Input('subject_teacher', 'value')])
def GetState(subject):
    try:
        number_done_test_your = int(len(SubFunctions().ReadDataFrameFromMySQL(FilesStudent[subject])) / NumberRowsOfOwnDataForOneTestStudent[subject])
    except KeyError:
        return 'You need to select subject in above dropdown'
    return u'In this subject you have done {} test next be {}'.format(number_done_test_your,number_done_test_your+1)

@app.callback(Output('table_teacher', 'rows'), [Input('text_area_exam_teacher', 'value'), Input('text_area_answers_teacher', 'value'), Input('K_neighbors_teacher', 'value')])
def CategorizeQuestions(text_exam, text_answers, k_neighbors ):
    df_result = pd.DataFrame()
    try:
        Answers = ExtractAnswersFromText(text_answers)
        df_result, df_feature_to_storage = CategorizeATest(text_exam, Answers, k_neighbors, 50)
        SubFunctions().WriteDataFrimeToSQLDatabase(df_feature_to_storage, 'FeatureToStore')
    except():
        #TypeError, AttributeError , IndexError, ValueError, KeyError
        pass
    return df_result.to_dict('records')

@app.callback(  Output('status_teacher', 'children'),[Input('submit_button_teacher', 'n_clicks'), Input('table_teacher', 'rows')],
                state=[State('subject_teacher', 'value'),State('test_number_teacher', 'value'),State('complete_confirm_teacher', 'value'),])
def UpdateDataToDatabase(n_clicks, rows, subject, test_number, complete_confirm):
    if n_clicks != None:
        obj = EnglishTeacher() if subject == Subjects[0] else (MathTeacher() if subject == Subjects[1] else PhysicsTeacher())
        state = obj.CheckComponentsToGetRawData(test_number, complete_confirm)
        if state is not None: return state
        df = pd.DataFrame(rows)
        Categories = list(df['Category'])
        Answers = list(df['Answers'])
        return obj.UpdateRawDataForObject(Answers, Categories)
    return 'Status: You can start'
#////////////////////////////////////////////////////////////////////////////////////////CallBacks for student/////////////////////////////////////////////////////
@app.callback(Output('state_student', 'children'),[Input('subject_student', 'value')])
def GetState(subject):
    try:
        number_done_test_your = int(len(SubFunctions().ReadDataFrameFromMySQL(FilesStudent[subject])) / NumberRowsOfOwnDataForOneTestStudent[subject])
    except KeyError:
        return 'You need to select subject in above dropdown'
    return u'In this subject you have done {} test next be {}'.format(number_done_test_your,number_done_test_your+1)
@app.callback(  Output('status', 'children'),[Input('submit_button_student', 'n_clicks')],state=[
State('subject_student', 'value'),
State('test_number_student', 'value'),
State('input1', 'value'),
State('input2', 'value'),
State('input3', 'value'),
State('input4', 'value'),
State('input5', 'value'),
State('input6', 'value'),
State('input7', 'value'),
State('input8', 'value'),
State('input9', 'value'),
State('input10', 'value'),
State('input11', 'value'),
State('input12', 'value'),
State('input13', 'value'),
State('input14', 'value'),
State('input15', 'value'),
State('input16', 'value'),
State('input17', 'value'),
State('input18', 'value'),
State('input19', 'value'),
State('input20', 'value'),
State('input21', 'value'),
State('input22', 'value'),
State('input23', 'value'),
State('input24', 'value'),
State('input25', 'value'),
State('input26', 'value'),
State('input27', 'value'),
State('input28', 'value'),
State('input29', 'value'),
State('input30', 'value'),
State('input31', 'value'),
State('input32', 'value'),
State('input33', 'value'),
State('input34', 'value'),
State('input35', 'value'),
State('input36', 'value'),
State('input37', 'value'),
State('input38', 'value'),
State('input39', 'value'),
State('input40', 'value'),
State('input41', 'value'),
State('input42', 'value'),
State('input43', 'value'),
State('input44', 'value'),
State('input45', 'value'),
State('input46', 'value'),
State('input47', 'value'),
State('input48', 'value'),
State('input49', 'value'),
State('input50', 'value'),
State('complete_confirm_student', 'value'),])
def update_output(n_clicks, tab, test_number,
                  input1, input2, input3, input4, input5, input6, input7, input8, input9, input10,
                  input11, input12, input13, input14, input15, input16, input17, input18, input19, input20,
                  input21, input22, input23, input24, input25, input26, input27, input28, input29, input30,
                  input31, input32, input33, input34, input35, input36, input37, input38, input39, input40,
                  input41, input42, input43, input44, input45, input46, input47, input48, input49, input50, complete_confirm):
    if n_clicks != None:
        obj = EnglishStudent() if tab == Subjects[0] else (MathStudent() if tab == Subjects[1] else PhysicsStudent())
        state = obj.CheckComponentsToGetRawData(test_number, complete_confirm)
        if state is not None: return state
        list_options = [input1, input2, input3, input4, input5, input6, input7, input8, input9, input10,
                        input11, input12, input13, input14, input15, input16, input17, input18, input19, input20,
                        input21, input22, input23, input24, input25, input26, input27, input28, input29, input30,
                        input31, input32, input33, input34, input35, input36, input37, input38, input39, input40,
                        input41, input42, input43, input44, input45, input46, input47, input48, input49, input50]
        return obj.UpdateRawDataForObject(list_options)
    return 'Status: You can start'
if __name__ == '__main__':
    app.run_server()