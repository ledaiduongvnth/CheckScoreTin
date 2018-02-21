import numpy as np
import pandas as pd
import ast
from nltk import word_tokenize, pos_tag
from Dataset import *
from ProcessData import *
from TextPreprocessingFunctionalStyle import *
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm

def FirtsStepCategozineBySeaching(df):
    list_conditions = [lambda x: 'pronou' in x or 'pronunciation' in x, lambda x: 'stress' in x,
                       lambda x: 'read' in x and 'following' in x and 'correct' in x and 'answer' in x,
                       lambda x: 'need' in x and 'correct' in x, lambda x: 'word(s)' in x and 'closest' in x and 'meaning' in x,
                       lambda x: 'word(s)' in x and 'opposite' in x and 'meaning' in x,
                       lambda x: 'sentence' in x and ('combine' in x or ('closest' in x and 'meaning' in x)),
                       lambda x: 'response' in x]
    conditions = [df['header1'].apply(condition) for condition in list_conditions]
    choices = ['Pronunciation', 'Stress', 'Reading', 'Error_identification', 'Synonyms', 'Antonyms',
               'Sentence_transformation', 'Direct_indirect_sentence']
    df['Category'] = np.select(conditions, choices)
    return df[['options', 'Category']]

def ExtractFeaturesFromOptions(list_options):
    # Arguments list_options like ['yet', 'still' ,'untill', 'even']
    # Result list_numerical_lable like [19, 19, 19, 11]
    list_pos_tag = [pos_tag(word_tokenize(option)) for option in list_options]
    list_label = [option_and_pos_tag[1] for option in list_pos_tag for option_and_pos_tag in option]
    list_numerical_lable = sorted(list(LabelEncoderPosTag.transform(list_label)), key= int, reverse= True)
    return list_numerical_lable

def ConvertEnglishCategoryToNumber(lable):
    list_lable = [lable]
    list_numerical_lable = LabelEncoderEnglishCategory.transform(list_lable)
    number = list_numerical_lable[0]
    return number

def ConvertNumberToCategoricalData(number):
    list_number = [number]
    list_categorical_lable = LabelEncoderEnglishCategory.inverse_transform(list_number)
    category = list_categorical_lable[0]
    return category

def UniformFeature(feature, standart_length):
    length_intite = len(feature)
    uniformed_feature = np.zeros(standart_length)
    uniformed_feature[0:length_intite] = feature
    return uniformed_feature.tolist()

def CategorizeATest(text, Answers, k_neighbors, length_feature):
    # Convert raw text to DataFrame
    try:
        df = ConvertADictionaryToDataFrame(ExtractATestToDictionary(text, list_delimiters_0, get_head=False, get_tail=False))
    except KeyError:
        df = ConvertADictionaryToDataFrame(ExtractATestToDictionary(text, list_delimiters_0, get_head=True, get_tail=True))
    # Get Trainning Data and their lables from Database
    df_trainning = SubFunctions().ReadDataFrameFromMySQL('TrainningData')
    df_trainning['Feature'] = df_trainning['Feature'].apply(ast.literal_eval)
    data_trainning = np.array([UniformFeature(feature, length_feature) for feature in list(df_trainning['Feature'])])
    lables = list(df_trainning['Lable'])
    # PreCategorize test and built feature to storage
    df = FirtsStepCategozineBySeaching(df)
    df = df.reset_index().drop(columns='index')
    df['Index'] = list(df.index)
    df_unlabled = df[df['Category'] == '0']
    feature_to_storage = [ExtractFeaturesFromOptions(option) for option in list(df_unlabled['options'])]
    df_feature_to_storage = pd.DataFrame()
    df_feature_to_storage['Index'] = df_unlabled['Index']
    df_feature_to_storage['Feature'] = pd.Series(feature_to_storage,name = 'Feature', index= df_feature_to_storage.index)
    df_feature_to_storage['Feature'] = df_feature_to_storage['Feature'].apply(str)
    data_test = np.array([UniformFeature(feature, length_feature) for feature in feature_to_storage])
    #Test new data
    clf = KNeighborsClassifier(n_neighbors= k_neighbors)
    clf.fit(data_trainning, lables)
    numerical_lable = clf.predict(data_test)
    categorical_lable = list(LabelEncoderEnglishCategory.inverse_transform(numerical_lable))
    for lable, index in zip(categorical_lable, list(df_unlabled.index)):
        df.loc[index, 'Category'] = lable
    # Create final dataframe to display
    df_result = pd.DataFrame()
    df_result['Index'] = range(1, 51)
    df_result['Category'] = list(df['Category'])
    df_result['Answers'] = Answers
    return df_result, df_feature_to_storage
