from sklearn.preprocessing import LabelEncoder


regime = 2

if regime == 3 :
    import sshtunnel
    sshtunnel.SSH_TIMEOUT = 5.0
    sshtunnel.TUNNEL_TIMEOUT = 5.0
    ssh = ('ssh.pythonanywhere.com');
    un = 'ledaiduongvnth';
    pwd = 'leduysao290893';
    lcad = ('localhost', 3333);
    rmad = ('ledaiduongvnth.mysql.pythonanywhere-services.com', 3306)



# English
EnglishCategory = ['Pronunciation', 'Stress',
                   'Noun', 'Adjective_Adverb','Conjunction', 'Articles_a_an_the',  'Prepositions', 'Phrasal_verb', 'Verb',
                   'Verb_tenses','Relative_clause',
                   'Direct_indirect_sentence','Comparison', 'Identify_formation_of_words',
                   'Synonyms', 'Antonyms',
                   'Error_identification', 'Sentence_transformation',
                   'Reading',
                   'Pronoun', 'Model_verb', 'Passive_voice','Conditinal','Gerund_infinitive_participle','Tag_Question','Inversion', 'Subject_verb_agreement']
# Math
MathCategory = ['Survey of variation and plot of functions',
                'Trigonometric equations',
                'Equation, unequation,system of equations',
                'Integral',
                'Geometry of space',
                'Inequalities, finding of max/min values',
                'Plane geometry',
                'Space analysis geometry',
                'Combination - Probability, Newtonian binary',
                'Complex numbers']
# Physics
PhysicsCategory = ['Mechanical oscillation',
                   'Mechanical waves',
                   'Alternating current',
                   'Oscillation and electromagnetic waves',
                   'Light waves',
                   'Quantum of light',
                   'Atomic nucleus']
Categories = {'English': EnglishCategory,
            'Math': MathCategory,
            'Physics': PhysicsCategory}
list_pos_tag = ['CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB']
LabelEncoderPosTag = LabelEncoder()
LabelEncoderPosTag.fit(list_pos_tag)
list(LabelEncoderPosTag.classes_)
LabelEncoderEnglishCategory = LabelEncoder()
LabelEncoderEnglishCategory.fit(EnglishCategory)
list(LabelEncoderEnglishCategory.classes_)
list_delimiters_0 = ['Mark the letter', 'Blacken the letter', 'Read the following', 'THE END', 'ĐÁP ÁN']
Subjects = ['English', 'Math','Physics']
Algorithm = ['K nearest neighbor', 'Support vector machine', 'Tree decision']
Options = ['A', 'B', 'C', 'D']






