import dash
import dash_core_components as dcc
import dash_html_components as html


layout_list_test = html.Div([dcc.Link('<-HOME', href='/'),html.Br(),
                            dcc.Link('TEACHER PAGE', href='/page_teacher'),html.Br(),
                            dcc.Link('STUDENT PAGE', href='/page_student'),html.Br(),


                            html.H1('ENGLISH TESTS:'),
                            dcc.Markdown('''[1](https://drive.google.com/file/d/12kOWFOOaZomWf_7QYgadyD0KUxO_vxwk/view?usp=sharing)>>>>>>>>>
                            [2](https://drive.google.com/file/d/18Ph6O-7UYGkQl0CR_PLVnNmy0n0lXdyd/view?usp=sharing)>>>>>>>>>
                            [3](https://docs.google.com/document/d/1e_DPHeGwgKjHNjV2mkOjnBM25OVhlUMpaMgWp1lx5_s/edit?usp=sharing)>>>>>>>>>
                            [4](https://docs.google.com/document/d/1pTMPclfrd7oAT_JFQKmvHruWdRL_kK8aEg68y6cvEwk/edit?usp=sharing)>>>>>>>>>
                            [5](https://docs.google.com/document/d/1KiAz_aDbkKE1AFWoJ1QZhQ8hkTff9VZI6A5rb9yP910/edit?usp=sharing)>>>>>>>>>
                            [6](https://docs.google.com/document/d/1E4ip6TToMErX7JtHlQc1FzyxCBN-w-5j_zajSNCYUW8/edit?usp=sharing)>>>>>>>>>


                            '''),




                            html.H1('MATH TESTS:'),


                            html.H1('PHYSICS TESTS:')])