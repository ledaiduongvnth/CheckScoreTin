import numpy as np
import pandas as pd
import warnings;warnings.filterwarnings('ignore')
from Dataset import *
from TextPreprocessingFunctionalStyle import DeleteWhiteSpaceInFrontAndBack
from sqlalchemy import create_engine
from datetime import datetime

regime = 3

if regime == 3 :
    import sshtunnel
    sshtunnel.SSH_TIMEOUT = 5.0
    sshtunnel.TUNNEL_TIMEOUT = 5.0
    ssh = ('ssh.pythonanywhere.com');
    un = 'ledaiduongvnth';
    pwd = 'leduysao290893';
    lcad = ('localhost', 3333);
    rmad = ('ledaiduongvnth.mysql.pythonanywhere-services.com', 3306)

class SubFunctions:
    def __init__(self):pass

    def CreateEngineToConnectToMySQLServer(self,regime, server = None):
        if regime == 1:
            # Create engine in server cloud pythonanywhere
            engine = create_engine(
                'mysql+mysqldb://ledaiduongvnth:leduysao290893@ledaiduongvnth.mysql.pythonanywhere-services.com/ledaiduongvnth$CheckScoreTin1')
        elif regime == 2:
            # Create engine in local machine
            engine = create_engine('mysql+mysqldb://d:d@localhost/CheckScoreTin')
        elif regime == 3:
            # Create engine to access to MySQL server from local machine
            engine = create_engine('mysql+mysqldb://ledaiduongvnth:leduysao290893@127.0.0.1:%s/ledaiduongvnth$CheckScoreTin1' % server.local_bind_port)
        return engine

    def ReadDataFrameFromMySQL(self, path):
        if regime == 3:
            with sshtunnel.SSHTunnelForwarder(ssh, ssh_username=un, ssh_password=pwd, local_bind_address=lcad,
                                              remote_bind_address=rmad) as server:
                engine = self.CreateEngineToConnectToMySQLServer(regime ,server=server)
                with engine.connect() as conn, conn.begin():
                    df = pd.read_sql_table(path, conn)
                server.close()
        else:
            engine = self.CreateEngineToConnectToMySQLServer(regime)
            with engine.connect() as conn, conn.begin():
                df = pd.read_sql_table(path, conn)
        return df

    def WriteDataFrimeToSQLDatabase(self, df, table):
        if regime == 3 :
            with sshtunnel.SSHTunnelForwarder((ssh), ssh_username=un, ssh_password=pwd, local_bind_address=lcad,
                                              remote_bind_address=rmad) as server:
                engine = self.CreateEngineToConnectToMySQLServer(regime, server=server)
                with engine.connect() as conn, conn.begin():
                    df.to_sql(table, engine, if_exists='replace', index=False)
                server.close()
        else :
            engine = self.CreateEngineToConnectToMySQLServer(regime)
            df.to_sql(table, engine, if_exists='replace', index=False)

    def AddSeriesOrListToRowOfDataFrameByIndexEqualLength(self,path,series_or_list):
        series = pd.Series(series_or_list)
        df_origin = self.ReadDataFrameFromMySQL(path)
        df_update = pd.DataFrame(index= ['0'], columns= df_origin.columns )
        len_series = len(series.index.tolist())
        len_columns_data_frame = len(df_update.columns)
        if len_series == len_columns_data_frame:
            for index in np.arange(0, len_series): df_update.set_value('0', df_update.columns[index], series[index])
            df_origin = df_origin.append(df_update, ignore_index=True)
            self.WriteDataFrimeToSQLDatabase(df_origin, path)
        else: raise ValueError('columns length of dataframe not equal length of series')

    def AddSeriesToRowOfDataFrameByName(self,path,series):
        df_origin = self.ReadDataFrameFromMySQL(path)
        df_update = pd.DataFrame(index= ['0'], columns= df_origin.columns )
        for index in series.index.tolist(): df_update.set_value('0', index, series[index])
        df_origin = df_origin.append(df_update, ignore_index=True)
        self.WriteDataFrimeToSQLDatabase(df_origin, path)

    def RemoveRows(self, path, list_of_rows):
        df = self.ReadDataFrameFromMySQL(path)
        df = df.drop(list_of_rows)
        self.WriteDataFrimeToSQLDatabase(df, path)

    def RemoveAllRows(self, path):
        df = self.ReadDataFrameFromMySQL(path)
        df = df.drop(df.index.tolist())
        self.WriteDataFrimeToSQLDatabase(df, path)

    def RemoveColumns(self, path, list_of_columns):
        df = self.ReadDataFrameFromMySQL(path)
        df = df.drop(columns=list_of_columns)
        self.WriteDataFrimeToSQLDatabase(df, path)

    def WriteToExcel(self, df, path):
        writer = pd.ExcelWriter(path)
        df.to_excel(writer)
        writer.save()

class Person(SubFunctions):
    def __init__(self, file_raw_data, tab, number_rows_of_own_one_test ):
        SubFunctions.__init__(self)
        self.tab = tab
        self.file_raw_data = file_raw_data
        self.number_rows_of_own_one_test = number_rows_of_own_one_test

    def CheckComponentsToGetRawData(self, test_number, complete_confirm):
        df_file_raw_data = self.ReadDataFrameFromMySQL(self.file_raw_data)
        check_test_number = str(int(len(df_file_raw_data) / self.number_rows_of_own_one_test) + 1) == test_number
        if check_test_number is False: return 'Status: Test number is wrong, you need to choose your right test number'
        completed = complete_confirm == 'I have done'
        if completed is False: return 'Status: You do not complete your test, click to <I have done> to confirm your completion'

class Subject(SubFunctions):
    def __init__(self, file_preprocessed_data, file_raw_data_student, file_raw_data_teacher,
                 number_rows_of_one_test_of_teacher):
        self.file_preprocessed_data = file_preprocessed_data
        self.file_raw_data_student = file_raw_data_student
        self.file_raw_data_teacher = file_raw_data_teacher
        self.number_rows_of_one_test_of_teacher = number_rows_of_one_test_of_teacher
        SubFunctions.__init__(self)

    def CheckAllNewTests(self):
        df_file_preprocessed_data = self.ReadDataFrameFromMySQL(self.file_preprocessed_data)
        df_file_raw_data_student = self.ReadDataFrameFromMySQL(self.file_raw_data_student)
        df_file_raw_data_teacher = self.ReadDataFrameFromMySQL(self.file_raw_data_teacher)
        number_scaned_tests = len(df_file_preprocessed_data.index)
        number_student_tests = len(df_file_raw_data_student.index)
        number_teacher_tests = int(len(df_file_raw_data_teacher.index) / self.number_rows_of_one_test_of_teacher)
        tests_ready_to_scan = list(range(number_scaned_tests+1, min(number_student_tests, number_teacher_tests) + 1))
        return tests_ready_to_scan

    def ProcessATest(self, categories, anwrers_correct, list_anwers_user):
        df = pd.DataFrame()
        df_result = pd.DataFrame()
        df['Categories'] = categories
        df['AnwersCorrect'] = anwrers_correct
        Datetime = list_anwers_user.pop(0)
        df['AnwersUser'] = list_anwers_user
        df['Score'] = np.where(df.AnwersUser == df.AnwersCorrect, 1, 0)
        df_result['Percentage'] = 100 * df.groupby('Categories').sum()['Score'] / df.groupby('Categories').count()['Score']
        score = 10 * df['Score'].sum() / df['Score'].count()
        effectioncy = 10 * len([answer for answer in list_anwers_user if answer != None])/df['Score'].count()
        return [df_result,Datetime, score, effectioncy]

    def UpdateATest(self, test_oder):
        categories = list(self.ReadDataFrameFromMySQL(self.file_raw_data_teacher).loc[test_oder * self.number_rows_of_one_test_of_teacher - 1, :])
        anwrers_correct = list(self.ReadDataFrameFromMySQL(self.file_raw_data_teacher).loc[test_oder * self.number_rows_of_one_test_of_teacher - self.number_rows_of_one_test_of_teacher, :])
        list_anwers_user = list(self.ReadDataFrameFromMySQL(self.file_raw_data_student).loc[test_oder - 1, :])
        [df_type, Datetime, score, effectioncy] = self.ProcessATest(categories, anwrers_correct, list_anwers_user)
        df_score = pd.DataFrame(data=[[score]], index=['Score'], columns=['Percentage'])
        df_effectioncy = pd.DataFrame(data=[[effectioncy]], index=['Effectioncy'], columns=['Percentage'])
        df_date_time = pd.DataFrame(data=[[Datetime]], index=['Datetime'], columns=['Percentage'])
        df_result = pd.concat([df_date_time, df_score, df_effectioncy, df_type], axis=0)
        self.AddSeriesToRowOfDataFrameByName(self.file_preprocessed_data, df_result['Percentage'])

class Teacher(Person):
    def __init__(self, file_raw_data, tab, number_rows_of_own_one_test, categories_of_subject, number_questions_of_subject):
        self.categories_of_subject = categories_of_subject
        self.number_questions_of_subject = number_questions_of_subject
        Person.__init__(self,file_raw_data= file_raw_data, tab= tab, number_rows_of_own_one_test = number_rows_of_own_one_test)
    def UpdateRawDataForClass(self, Answers, Categories):
        Answers = Answers[0:self.number_questions_of_subject]
        Categories = Categories[0:self.number_questions_of_subject]
        for option in zip(Answers, Categories):
            if option == None or len(option) != 2 :
                return 'Status: Anwers form is wrong, you need to repair your anwers'
            elif option[0] not in Options or option[1] not in self.categories_of_subject:
                return 'Status: Anwers form is wrong, you need to repair your anwers'
        self.AddSeriesOrListToRowOfDataFrameByIndexEqualLength(self.file_raw_data, Answers)
        self.AddSeriesOrListToRowOfDataFrameByIndexEqualLength(self.file_raw_data, Categories)
        return 'Status: Your test is sent successfully, if you want to do next test you must click round button in top left conner to reload webpage'


class Student(Person):
    def __init__(self, file_raw_data, tab, number_rows_of_own_one_test, number_questions_of_subject):
        self.number_questions_of_subject = number_questions_of_subject
        Person.__init__(self,file_raw_data= file_raw_data, tab= tab, number_rows_of_own_one_test= number_rows_of_own_one_test)
    def UpdateRawDataForClass(self, list_options):
        for option in list_options:
            if option != None:
                if option not in Options or len(option) != 1:
                    return 'Status: You need to click round button in top left conner to reload webpage'
        list_options = list_options[0: self.number_questions_of_subject]
        now = datetime.now()
        list_options = [now] + list_options
        self.AddSeriesOrListToRowOfDataFrameByIndexEqualLength(self.file_raw_data, list_options)
        return 'Status: Your test is sent successfully, if you want to do next test you must click round button in top left conner to reload webpage'
    def GetDataForGraphForClass(self, file_preprocessed_data):
        df = self.ReadDataFrameFromMySQL(file_preprocessed_data)
        data = [
            {
                'x': df['Datetime'],
                'y': df['Score'],
                'name': 'Score',
                'marker': {'color': 'rgb(255, 0, 0)'},
            },
            {
                'x': df['Datetime'],
                'y': df['Effectioncy'],
                'name': 'Effectioncy',
                'marker': {'color': 'rgb(0, 213, 255)'},
            }]
        return data

    def GetDataForGraphForClassSecond(self, file_preprocessed_data, categories):
        df = self.ReadDataFrameFromMySQL(file_preprocessed_data)
        def EsarerToSee (x):
            if x == 0: return 2.222222222
            else:return x
        data = [
            {
                'x': list(range(1, df['Datetime'].count() + 1)),
                'y': [EsarerToSee(x) for x in list(df[category])],
                'name': category,
                'type': 'bar',
                'marker': { 'color': 'rgb(0,213,255)'}
            }for category in categories]
        return [[data_i] for data_i in data]

class EnglishTeacher(Teacher):
    def __init__(self):
        self.tab = 'English teacher'
        self.file_raw_data = 'EnglishTeacherCategories'
        self.number_rows_of_own_one_test = 2
        self.categories_of_subject = EnglishCategory
        self.number_questions_of_subject = 50
        Teacher.__init__(self, file_raw_data= self.file_raw_data,
                         tab= self.tab, number_rows_of_own_one_test=
                         self.number_rows_of_own_one_test,
                         categories_of_subject= self.categories_of_subject,
                         number_questions_of_subject= self.number_questions_of_subject)
    def UpdateRawDataForObject(self, Answers, Categories):
        Categories = [DeleteWhiteSpaceInFrontAndBack(category) for category in Categories]
        Answers = [DeleteWhiteSpaceInFrontAndBack(ans) for ans in Answers]
        if self.UpdateRawDataForClass(Answers, Categories) == 'Status: Anwers form is wrong, you need to repair your anwers':
            return 'Status: Anwers form is wrong, you need to repair your anwers'
        df_feature_to_storage = self.ReadDataFrameFromMySQL('FeatureToStore')
        Categories_to_storage = [Categories[i] for i in list(df_feature_to_storage['Index'])]
        df_feature_to_storage['Lable'] = list(LabelEncoderEnglishCategory.transform(Categories_to_storage))
        df_trainning_data = self.ReadDataFrameFromMySQL('TrainningData')
        df_trainning_data_new = pd.concat([df_trainning_data, df_feature_to_storage.drop(columns=['Index'])], axis=0, ignore_index= True)
        self.WriteDataFrimeToSQLDatabase(df_trainning_data_new, 'TrainningData')
        return 'Status: Your test is sent successfully, if you want to do next test you must click round button in top left conner to reload webpage'
class EnglishStudent(Student, Subject):
    def __init__(self):
        self.tab = 'English student'
        self.number_rows_of_own_one_test = 1
        self.number_rows_of_one_test_of_teacher = 2
        self.file_raw_data_student = 'EnglishStudentAnwers'
        self.file_raw_data_teacher = 'EnglishTeacherCategories'
        self.file_preprocessed_data = 'EnglishPreprocessedData'
        self.number_questions_of_subject = 50
        Student.__init__(self, file_raw_data= self.file_raw_data_student, tab= self.tab,
                         number_rows_of_own_one_test= self.number_rows_of_own_one_test,
                         number_questions_of_subject= self.number_questions_of_subject)
        Subject.__init__(self, file_preprocessed_data=self.file_preprocessed_data,
                         file_raw_data_student= self.file_raw_data_student,
                         file_raw_data_teacher= self.file_raw_data_teacher,
                         number_rows_of_one_test_of_teacher= self.number_rows_of_one_test_of_teacher)
    def UpdateRawDataForObject(self, list_options):
        return self.UpdateRawDataForClass(list_options)
    def UpdateAllTest(self):
        tests_ready_to_scan = self.CheckAllNewTests()
        if len(tests_ready_to_scan) > 0:
            for test in tests_ready_to_scan:
                self.UpdateATest(test)

class MathTeacher(Teacher):
    def __init__(self):
        self.tab = 'Math teacher'
        self.file_raw_data = 'MathTeacherCategories'
        self.number_rows_of_own_one_test = 2
        self.categories_of_subject = MathCategory
        self.number_questions_of_subject = 50
        Teacher.__init__(self, file_raw_data= self.file_raw_data,
                         tab= self.tab, number_rows_of_own_one_test=
                         self.number_rows_of_own_one_test,
                         categories_of_subject= self.categories_of_subject,
                         number_questions_of_subject= self.number_questions_of_subject)
    def UpdateRawDataForObject(self, list_options):
        if self.UpdateRawDataForClass(list_options) == 'Status: Anwers form is wrong, you need to repair your anwers':
            return 'Status: Anwers form is wrong, you need to repair your anwers'
        return 'Status: Your test is sent successfully, if you want to do next test you must click round button in top left conner to reload webpage'
class MathStudent(Student, Subject):
    def __init__(self):
        self.tab = 'Math student'
        self.number_rows_of_own_one_test = 1
        self.number_rows_of_one_test_of_teacher = 2
        self.file_raw_data_student = 'MathStudentAnwers'
        self.file_raw_data_teacher = 'MathTeacherCategories'
        self.file_preprocessed_data = 'MathPreprocessedData'
        self.number_questions_of_subject = 50
        Student.__init__(self, file_raw_data= self.file_raw_data_student, tab= self.tab,
                          number_rows_of_own_one_test= self.number_rows_of_own_one_test,
                         number_questions_of_subject= self.number_questions_of_subject)
        Subject.__init__(self, file_preprocessed_data=self.file_preprocessed_data,
                         file_raw_data_student= self.file_raw_data_student,
                         file_raw_data_teacher= self.file_raw_data_teacher,
                         number_rows_of_one_test_of_teacher= self.number_rows_of_one_test_of_teacher)
    def UpdateRawDataForObject(self, list_options):
        return self.UpdateRawDataForClass(list_options)
    def UpdateAllTest(self):
        tests_ready_to_scan = self.CheckAllNewTests()
        if len(tests_ready_to_scan) > 0:
            for test in tests_ready_to_scan:
                self.UpdateATest(test)

class PhysicsTeacher(Teacher):
    def __init__(self):
        self.tab = 'Physics teacher'
        self.file_raw_data = 'PhysicsTeacherCategories'
        self.number_rows_of_own_one_test = 2
        self.categories_of_subject = PhysicsCategory
        self.number_questions_of_subject = 40
        Teacher.__init__(self, file_raw_data= self.file_raw_data,
                         tab= self.tab, number_rows_of_own_one_test=
                         self.number_rows_of_own_one_test,
                         categories_of_subject= self.categories_of_subject,
                         number_questions_of_subject= self.number_questions_of_subject)
    def UpdateRawDataForObject(self, list_options):
        if self.UpdateRawDataForClass(list_options) == 'Status: Anwers form is wrong, you need to repair your anwers':
            return 'Status: Anwers form is wrong, you need to repair your anwers'
        return 'Status: Your test is sent successfully, if you want to do next test you must click round button in top left conner to reload webpage'
class PhysicsStudent(Student, Subject):
    def __init__(self):
        self.tab = 'Physics student'
        self.number_rows_of_own_one_test = 1
        self.number_rows_of_one_test_of_teacher = 2
        self.file_raw_data_student = 'PhysicsStudentAnwers'
        self.file_raw_data_teacher = 'PhysicsTeacherCategories'
        self.file_preprocessed_data = 'PhysicsPreprocessedData'
        self.number_questions_of_subject = 40
        Student.__init__(self, file_raw_data= self.file_raw_data_student, tab= self.tab,
                         number_rows_of_own_one_test= self.number_rows_of_own_one_test,
                         number_questions_of_subject= self.number_questions_of_subject)
        Subject.__init__(self, file_preprocessed_data=self.file_preprocessed_data,
                         file_raw_data_student= self.file_raw_data_student,
                         file_raw_data_teacher= self.file_raw_data_teacher,
                         number_rows_of_one_test_of_teacher= self.number_rows_of_one_test_of_teacher)
    def UpdateRawDataForObject(self, list_options):
        return self.UpdateRawDataForClass(list_options)
    def UpdateAllTest(self):
        tests_ready_to_scan = self.CheckAllNewTests()
        if len(tests_ready_to_scan) > 0:
            for test in tests_ready_to_scan:
                self.UpdateATest(test)
