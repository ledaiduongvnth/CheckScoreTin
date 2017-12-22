Tabs = ['English teacher', 'Math teacher','Physics teacher', 'English student', 'Math student', 'Physics student']
Options = ['A', 'B', 'C', 'D']
NumberQuestions = {'English': 50, 'Math': 50, 'Physics':40}
# English
EnglishCategory = {'Phonetics':['Pronunciation', 'Stress'],
                   'Grammar': ['Verb Tenses', 'Subject- Verb agreement', 'Gerund- infinitive- participle', 'Noun', 'Pronoun - Determine', 'Adjective - Adverb', 'Articles A an the', 'Comparision', 'Prepsitions', 'Model Verb','Passive Voice', 'Conditinal', 'Sentence Structure', 'Phrasal verb- idiom', 'Tag - Question', 'Inversion', 'Relative clause', 'Direct- Indirect sentence'],
                   'Vocabulary': ['Word Formation', 'Word Choice'],
                   'Use english': ['Error identification', 'Sentence Building', 'Sentence Transformation'],
                   'Reading Type1': ['Reading Type2']
                   }
EnglishCategoryType2 = []
for i in list(EnglishCategory.values()):
    for ii in i: EnglishCategoryType2.append(ii)
EnglishCategoryType1 = list(EnglishCategory.keys())
EnglishTypesToPlot = {'Type1': EnglishCategoryType1, 'Type2': EnglishCategoryType2, 'Score': ['Score']}
# Math
MathCategory = ['1', '2', '3']
# Physics
PhysicsCategory = ['4', '5', '6']

Files = {'English teacher': ['dataset/EnglishTeacherCategories.xlsx','dataset/EnglishStudentAnwers.xlsx'],
        'Math teacher': ['dataset/MathTeacherCategories.xlsx','dataset/MathStudentAnwers.xlsx'],
        'Physics teacher': ['dataset/PhysicsTeacherCategories.xlsx','dataset/PhysicsStudentAnwers.xlsx'],
        'English student': ['dataset/EnglishStudentAnwers.xlsx','dataset/EnglishTeacherCategories.xlsx'],
        'Math student': ['dataset/MathStudentAnwers.xlsx','dataset/MathTeacherCategories.xlsx'],
        'Physics student': ['dataset/PhysicsStudentAnwers.xlsx','dataset/PhysicsTeacherCategories.xlsx']}
Categories = {'English teacher': Options + EnglishCategoryType2,
            'Math teacher': Options + MathCategory,
            'Physics teacher': Options + PhysicsCategory,
            'English student': Options,
            'Math student': Options,
            'Physics student': Options}
NumberRowsForOneTest = {'English teacher': 3,
                        'Math teacher': 2,
                        'Physics teacher': 2,
                        'English student': 1,
                        'Math student': 1,
                        'Physics student': 1}
def WhetherOrNotCategories (tab):
    if tab in Tabs[0:3]: return True
    if tab in Tabs[3:6]: return False
