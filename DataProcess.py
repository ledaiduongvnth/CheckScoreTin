import numpy as np
import pandas as pd
from pathlib import Path
import warnings;warnings.filterwarnings('ignore')
from DatasetPython import *

class SubFunctions:
    def __init__(self):pass
    def PrintDataFrame(self, path):
        df = pd.read_excel(path)
        print(df)
    def AddSeriesOrListToRowOfDataFrameByIndexEqualLength(self,path,series_or_list):
        series = pd.Series(series_or_list)
        df_origin = pd.read_excel(path)
        df_update = pd.DataFrame(index= ['0'], columns= df_origin.columns )
        len_series = len(series.index.tolist())
        len_columns_data_frame = len(df_update.columns)
        if len_series == len_columns_data_frame:
            for index in np.arange(0, len_series): df_update.set_value('0', df_update.columns[index], series[index])
            df_origin = df_origin.append(df_update, ignore_index=True)
            writer = pd.ExcelWriter(path);df_origin.to_excel(writer);writer.save()
        else:
            raise ValueError('columns length of dataframe not equal length of series')
    def AddSeriesOrListToRowOfDataFrameByIndexNotEqualLength(self,path,series_or_list):
        series = pd.Series(series_or_list)
        df_origin = pd.read_excel(path)
        df_update = pd.DataFrame(index= ['0'], columns= df_origin.columns )
        len_series = len(series.index.tolist())
        len_columns_data_frame = len(df_update.columns)
        if len_series < len_columns_data_frame:
            for index in np.arange(0, len_series): df_update.set_value('0', df_update.columns[index], series[index])
            df_origin = df_origin.append(df_update, ignore_index=True)
            writer = pd.ExcelWriter(path);df_origin.to_excel(writer);writer.save()
        else:
            raise ValueError('columns length of dataframe is less then length of series')
    def AddSeriesToRowOfDataFrameByName(self,path,series):
        df_origin = pd.read_excel(path)
        df_update = pd.DataFrame(index= ['0'], columns= df_origin.columns )
        for index in series.index.tolist(): df_update.set_value('0', index, series[index])
        df_origin = df_origin.append(df_update, ignore_index=True)
        writer = pd.ExcelWriter(path);df_origin.to_excel(writer);writer.save()
    def RemoveRows(self, path, list_of_rows):
        df = pd.read_excel(path)
        df = df.drop(list_of_rows)
        writer = pd.ExcelWriter(path); df.to_excel(writer); writer.save()
    def RemoveAllRows(self, path):
        df = pd.read_excel(path)
        df = df.drop(df.index.tolist())
        writer = pd.ExcelWriter(path); df.to_excel(writer); writer.save()
    def RemoveColumns(self, path, list_of_columns):
        df = pd.read_excel(path)
        df = df.drop(columns = list_of_columns)
        writer = pd.ExcelWriter(path); df.to_excel(writer); writer.save()

class Person(SubFunctions):
    def __init__(self, file_raw_data, tab, number_rows_of_one_test ):
        SubFunctions.__init__(self)
        self.tab = tab
        self.file_raw_data = file_raw_data
        self.number_rows_of_one_test = number_rows_of_one_test
    def CheckComponentsToGetRawData(self, role_and_subject, test_number, complete_confirm):
        if role_and_subject == None or len(role_and_subject) != 2  : return '..........Status: Role and subject is wrong'
        tab_choosen = role_and_subject[0].upper() + ' ' + role_and_subject[1].upper() == self.tab.upper()
        if tab_choosen is False: return '..........Status: Role and subject is wrong'
        check_test_number = str(int(len(pd.read_excel(self.file_raw_data)) / self.number_rows_of_one_test) + 1) == test_number
        if check_test_number is False: return '..........Status: Test number is wrong'
        completed = complete_confirm == 'I have done'
        if completed is False: return '..........Status: You do not complete your test'

class Subject(SubFunctions):
    def __init__(self, file_preprocessed_data, file_raw_data_student, file_raw_data_teacher,
                 number_rows_of_one_test_subject):
        self.file_preprocessed_data = file_preprocessed_data
        self.file_raw_data_student = file_raw_data_student
        self.file_raw_data_teacher = file_raw_data_teacher
        self.number_rows_of_one_test = number_rows_of_one_test_subject
        SubFunctions.__init__(self)
    def CheckAllNewTests(self):
        number_scaned_tests = len(pd.read_excel(self.file_preprocessed_data).index)
        number_student_tests = len(pd.read_excel(self.file_raw_data_student).index)
        number_teacher_tests = int(len(pd.read_excel(self.file_raw_data_teacher).index)/self.number_rows_of_one_test)
        tests_ready_to_scan = list(range(number_scaned_tests+1, min(number_student_tests, number_teacher_tests) + 1))
        return tests_ready_to_scan
    def ProcessATest(self, df_raw_data_teacher, df_raw_data_student, test_oder, handle_value=1):
        df = pd.DataFrame()
        df_result = pd.DataFrame()
        df['Categories'] = list(df_raw_data_teacher.loc[test_oder * self.number_rows_of_one_test - handle_value, :])
        df['AnwersCorrect'] = list(
            df_raw_data_teacher.loc[test_oder * self.number_rows_of_one_test - self.number_rows_of_one_test, :])
        df['AnwersUser'] = list(df_raw_data_student.loc[test_oder - 1, :])
        df['Score'] = np.where(df.AnwersUser == df.AnwersCorrect, 1, 0)
        df_result['Percentage'] = 100 * df.groupby('Categories').sum()['Score'] / df.groupby('Categories').count()[
            'Score']
        score = 10 * df['Score'].sum() / df['Score'].count()
        return [df_result, score]
    def UpdateATest(self, test_oder, type_extra=False):
        df_raw_data_teacher = pd.read_excel(self.file_raw_data_teacher)
        df_raw_data_student = pd.read_excel(self.file_raw_data_student)
        if type_extra == False:
            [df_type, score] = self.ProcessATest(df_raw_data_teacher, df_raw_data_student, test_oder)
            df_score = pd.DataFrame(data=[[score]], index=['Score'], columns=['Percentage'])
            df_result = pd.concat([df_score, df_type], axis=0)
            self.AddSeriesToRowOfDataFrameByName(self.file_preprocessed_data, df_result['Percentage'])
        elif type_extra == True:
            [df_type1, score1] = self.ProcessATest(df_raw_data_teacher, df_raw_data_student, test_oder)
            [df_type2, score2] = self.ProcessATest(df_raw_data_teacher, df_raw_data_student, test_oder, handle_value= 2)
            df_score = pd.DataFrame(data=[[score1]], index=['Score'], columns=['Percentage'])
            df_result = pd.concat([df_score, df_type1, df_type2], axis=0)
            self.AddSeriesToRowOfDataFrameByName(self.file_preprocessed_data, df_result['Percentage'])

class Teacher(Person):
    def __init__(self, file_raw_data, tab, number_rows_of_one_test):
        Person.__init__(self,file_raw_data= file_raw_data, tab= tab, number_rows_of_one_test= number_rows_of_one_test)
    def UpdateRawDataForClass(self, list_options):
        list_anwers = []
        list_categories = []
        for option in list_options:
            if option == None or len(option) != 2: return '..........Status: Anwers form is wrong'
            list_anwers.append(option[0])
            list_categories.append(option[1])
        self.AddSeriesOrListToRowOfDataFrameByIndexEqualLength(self.file_raw_data, list_anwers)
        self.AddSeriesOrListToRowOfDataFrameByIndexEqualLength(self.file_raw_data, list_categories)
        return '..........Status: Your test is sent successfully'

class Student(Person):
    def __init__(self, file_raw_data, tab, number_rows_of_one_test_student):
        Person.__init__(self,file_raw_data= file_raw_data, tab= tab, number_rows_of_one_test= number_rows_of_one_test_student)
    def UpdateRawDataForClass(self, list_options):
        self.AddSeriesOrListToRowOfDataFrameByIndexEqualLength(self.file_raw_data, list_options)
        return '..........Status: Your test is sent successfully'
    def GetDataForGraphForClass(self, type_to_plot, storage_types, file_preprocessed_data):
        df = pd.read_excel(file_preprocessed_data)
        data = [
            {
                'x': df.index,
                'y': df[category],
                'name': category,
                'marker': {'color': 'rgb(55, 83, 109)'},
            } for category in storage_types[type_to_plot]]
        return data
class EnglishTeacher(Teacher):
    def __init__(self):
        self.tab = 'English teacher'
        self.file_raw_data = 'dataset/EnglishTeacherCategories.xlsx'
        self.number_rows_of_one_test = 3
        Teacher.__init__(self, file_raw_data= self.file_raw_data,
                         tab= self.tab, number_rows_of_one_test=
                         self.number_rows_of_one_test)
    def UpdateRawDataForObject(self, list_options):
        if self.UpdateRawDataForClass(list_options) == '..........Status: Anwers form is wrong':
            return '..........Status: Anwers form is wrong'
        list_categories_extra = []
        for option in list_options:
            for Category in list(EnglishCategory.keys()):
                if option[1] in EnglishCategory[Category]: list_categories_extra.append(Category)
        self.AddSeriesOrListToRowOfDataFrameByIndexEqualLength(self.file_raw_data, list_categories_extra)
        return '..........Status: Your test is sent successfully'

class EnglishStudent(Student, Subject):
    def __init__(self):
        self.number_rows_of_one_test = 3
        self.tab = 'English student'
        self.file_raw_data_student = 'dataset/EnglishStudentAnwers.xlsx'
        self.file_raw_data_teacher = 'dataset/EnglishTeacherCategories.xlsx'
        self.file_preprocessed_data = 'dataset/EnglishPreprocessedData.xlsx'
        Student.__init__(self, file_raw_data= self.file_raw_data_student, tab= self.tab,
                          number_rows_of_one_test_student= self.number_rows_of_one_test)
        Subject.__init__(self, file_preprocessed_data=self.file_preprocessed_data,
                         file_raw_data_student= self.file_raw_data_student,
                         file_raw_data_teacher= self.file_raw_data_teacher,
                         number_rows_of_one_test_subject= self.number_rows_of_one_test)
    def UpdateRawDataForObject(self, list_options):
        return self.UpdateRawDataForClass(list_options)
    def UpdateAllTest(self):
        tests_ready_to_scan = self.CheckAllNewTests()
        if len(tests_ready_to_scan) > 0:
            for test in tests_ready_to_scan:
                self.UpdateATest(test, type_extra=True)
    def GetDataForGraphForObject(self, type_to_plot):
        return self.GetDataForGraphForClass(type_to_plot, EnglishTypesToPlot, self.file_preprocessed_data)


