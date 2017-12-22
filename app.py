from dash.dependencies import Input, Output, State
from DataProcess import *
from LayoutWebApplication import *
from DatasetPython import *
app = dash.Dash();app.layout = layout

def Gettab(tab):
    if tab == Tabs[0]: return EnglishTeacher()
    if tab == Tabs[3]: return EnglishStudent()


@app.callback(Output('graph', 'figure'),[Input('tabs', 'value'), Input('type_to_plot', 'value')])
def UpdateDataAndPlotGraph(tab, type_to_plot):
    graph = None
    if tab in Tabs[3:6]:
        obj = Gettab(tab)
        obj.UpdateAllTest()
        data = obj.GetDataForGraphForObject(type_to_plot)
        graph = {'data': data,
                'layout': {
                'margin': {'l': 30,'r': 0,'b': 30,'t': 0},
                'legend': {'x': 0, 'y': 1}}}
    return graph
@app.callback(Output('state', 'children'),[Input('tabs', 'value')])
def GetState(tab):
    number_done_test_your = int(len(pd.read_excel(Files[tab][0])) / NumberRowsForOneTest[tab])
    return u'In this subject you have done {} test next be {}'.format(number_done_test_your,number_done_test_your+1)
for i in range(1, 51):
    @app.callback(Output('input' + str(i), 'options'), [Input('tabs', 'value')])
    def TakeOptions(tab): return [{'label': Option, 'value': Option} for Option in Categories[tab]]
for i in range(1, 51):
    @app.callback(Output('input' + str(i), 'multi'),[Input('tabs', 'value')])
    def TakeMulti(tab): return WhetherOrNotCategories(tab)
@app.callback(  Output('status', 'children'),[Input('submit_button', 'n_clicks')],state=[
State('tabs', 'value'),
State('test_number', 'value'),
State('role_and_subject', 'value'),
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
State('complete_confirm', 'value'),])
def update_output(n_clicks, tabs, test_number, role_and_subject,
                  input1, input2, input3, input4, input5, input6, input7, input8, input9, input10,
                  input11, input12, input13, input14, input15, input16, input17, input18, input19, input20,
                  input21, input22, input23, input24, input25, input26, input27, input28, input29, input30,
                  input31, input32, input33, input34, input35, input36, input37, input38, input39, input40,
                  input41, input42, input43, input44, input45, input46, input47, input48, input49, input50, complete_confirm):
    if n_clicks != None:
        obj = Gettab(tabs)
        state = obj.CheckComponentsToGetRawData(role_and_subject, test_number, complete_confirm)
        if state is not None: return state
        list_options = [input1, input2, input3, input4, input5, input6, input7, input8, input9, input10,
                        input11, input12, input13, input14, input15, input16, input17, input18, input19, input20,
                        input21, input22, input23, input24, input25, input26, input27, input28, input29, input30,
                        input31, input32, input33, input34, input35, input36, input37, input38, input39, input40,
                        input41, input42, input43, input44, input45, input46, input47, input48, input49, input50]
        return obj.UpdateRawDataForObject(list_options)
    return '..........Status: Data form is wrong'


if __name__ == '__main__':
    app.run_server(debug=True)


