from search import keyword_to_titles, title_to_info, search, article_length,key_by_author, filter_to_author, filter_out, articles_from_year
from search_tests_helper import get_print, print_basic, print_advanced, print_advanced_option
from wiki import article_metadata
from unittest.mock import patch
from unittest import TestCase, main

class TestSearch(TestCase):

    ##############
    # UNIT TESTS #
    ##############

    def test_example_unit_test(self):
        dummy_keyword_dict = {
            'cat': ['title1', 'title2', 'title3'],
            'dog': ['title3', 'title4']
        }
        expected_search_results = ['title3', 'title4']
        self.assertEqual(search('dog', dummy_keyword_dict), expected_search_results)

    def test_keyword_to_titles(self):
        test_info_1 = [['Machala','Wizkid',6493733893,3000,['a','c','C','A']],
                        ['OBO','Davido',664738637322,1000,['g','f']],
                        ['Odogwu','Burna Boy',758567484,2000,['h','g','c']]
        ]
        keywords_1 = {'a':['Machala'],
                      'c': ['Machala','Odogwu'],
                      'C': ['Machala'],
                      'A':['Machala'],
                      'g':['OBO','Odogwu'],
                      'f':['OBO'],
                      'h':['Odogwu']

        }
        test_info_2 =[['kcee', 'Mela', 753665222, 8000, ['trainer', 'qdot', 'lamba']],
                     ['slim tensim', 'Jackie Mars', 6492457426,527427, ['qdot', 'lamba']],
                     ['Godzilla', 'Falony', 1112343560, 7462012, ['trainer', 'qdot', 'lamba']]
        ]
        keywords_2 = {'trainer': ['kcee', 'Godzilla'],
                      'qdot': ['kcee', 'slim tensim', 'Godzilla'],
                      'lamba': ['kcee', 'slim tensim', 'Godzilla'],
        }
        self.assertEqual(keyword_to_titles(test_info_1), keywords_1)
        self.assertEqual(keyword_to_titles(test_info_2), keywords_2)
        self.assertEqual(keyword_to_titles([]), {})


    def test_title_to_info(self):
        test_info_1 = [['Machala','Wizkid',6493733893,3000,['a','c','C','A']],
                        ['OBO','Davido',664738637322,1000,['g','f']],
                        ['Odogwu','Burna Boy',758567484,2000,['h','g','c']]
        ]
        mapped_titles_1 = {'Machala': {'author': 'Wizkid', 'timestamp': 6493733893, 'length': 3000}, 
                           'OBO': {'author': 'Davido', 'timestamp': 664738637322, 'length': 1000},
                           'Odogwu': {'author': 'Burna Boy', 'timestamp': 758567484, 'length': 2000}
        }
        test_info_2 =[['kcee', 'Mela', 753665222, 8000, ['trainer', 'qdot', 'lamba']],
                     ['slim tensim', 'Jackie Mars', 6492457426,527427, ['qdot', 'lamba']],
                     ['Godzilla', 'Falony', 1112343560, 7462012, ['trainer', 'qdot', 'lamba']]
        ]
        mapped_titles_2 = {'kcee': {'author': 'Mela', 'timestamp': 753665222, 'length': 8000},
                           'slim tensim': {'author': 'Jackie Mars', 'timestamp': 6492457426, 'length': 527427},
                           'Godzilla': {'author': 'Falony', 'timestamp': 1112343560, 'length': 7462012}
        }
        test_info_3 = [['DC vs Marvel', 'Stan Lee', 75605632, 73973, ['Super Woman']]]
        mapped_title_3 = {'DC vs Marvel': {'author': 'Stan Lee', 'timestamp': 75605632, 'length': 73973}}
        self.assertEqual(title_to_info(test_info_1), mapped_titles_1)
        self.assertEqual(title_to_info(test_info_2), mapped_titles_2)
        self.assertEqual(title_to_info(test_info_3), mapped_title_3)
        self.assertEqual(title_to_info([]), {})


    def test_search(self):
        keyword_dictionary = {'a':['Machala'],
                              'A':['Machala'],
                              'c': ['Machala','Odogwu'],
                              'C': ['Machala'],
                              'g':['OBO','Odogwu'],
                              'f':['OBO'],
                              'h':['Odogwu']
        }
        expected_g_search = ['OBO','Odogwu']
        self.assertEqual(search('A', keyword_dictionary), ['Machala'])
        self.assertEqual(search('c', keyword_dictionary), ['Machala','Odogwu'])
        self.assertEqual(search('C', keyword_dictionary), ['Machala'])
        self.assertEqual(search('g', keyword_dictionary), expected_g_search)
        self.assertEqual(search('G', keyword_dictionary), [])
        self.assertEqual(search('', keyword_dictionary), [])
        self.assertEqual(search('absent', keyword_dictionary), [])

    def test_article_length(self):
        mapped_titles = {'Master Shifu': {'author': 'Donatel', 'timestamp': 6258422, 'length': 3000},
                         'Panda po': {'author': 'Jett Finderson', 'timestamp': 69274794, 'length': 2100},
                         'Derek Patterson': {'author': 'Faderon', 'timestamp': 82729742, 'length': 434},
                         'Enduring': {'author': 'Matterson', 'timestamp': 7429646, 'length': 500300}
        }
        search_results = ['Master Shifu', 'Panda po', 'Derek Patterson', 'Enduring']
        self.assertEqual(article_length(0, search_results, mapped_titles), [])
        self.assertEqual(article_length(200, search_results, mapped_titles), [])
        self.assertEqual(article_length(433, search_results, mapped_titles), [])
        self.assertEqual(article_length(434, search_results, mapped_titles), ['Derek Patterson'])
        self.assertEqual(article_length(540, search_results, mapped_titles), ['Derek Patterson'])
        self.assertEqual(article_length(4000, search_results, mapped_titles), ['Master Shifu', 'Panda po', 'Derek Patterson'])
        self.assertEqual(article_length(500300, search_results, mapped_titles), ['Master Shifu', 'Panda po', 'Derek Patterson', 'Enduring'])
        self.assertEqual(article_length(500301, search_results, mapped_titles), ['Master Shifu', 'Panda po', 'Derek Patterson', 'Enduring'])
        self.assertEqual(article_length(599080, search_results, mapped_titles), ['Master Shifu', 'Panda po', 'Derek Patterson', 'Enduring'])
    
    def test_key_by_author(self):
        mapped_titles_1 = {'Master Shifu': {'author': 'Falony', 'timestamp': 6258422, 'length': 3000},
                         'Panda po': {'author': 'Matterson', 'timestamp': 69274794, 'length': 2100},
                         'Derek Patterson': {'author': 'Faderon', 'timestamp': 82729742, 'length': 434},
                         'Enduring': {'author': 'Matterson', 'timestamp': 7429646, 'length': 500300},
                         'Godzilla': {'author': 'Falony', 'timestamp': 1112343560, 'length': 7462012}
        }
        mapped_titles_2 = {'Master Shifu': {'author': 'Donatel', 'timestamp': 6258422, 'length': 3000},
                         'Panda po': {'author': 'Jett Finderson', 'timestamp': 69274794, 'length': 2100},
                         'Derek Patterson': {'author': 'Faderon', 'timestamp': 82729742, 'length': 434},
                         'Enduring': {'author': 'Matterson', 'timestamp': 7429646, 'length': 500300},
                         'Godzilla': {'author': 'Falony', 'timestamp': 1112343560, 'length': 7462012}
        }
        search_results = ['Master Shifu', 'Panda po', 'Derek Patterson', 'Enduring','Godzilla']
        mapped_authors_1 = {'Falony': ['Master Shifu', 'Godzilla'],
                          'Matterson': ['Panda po','Enduring'],
                          'Faderon': ['Derek Patterson']
        }
        mapped_authors_2 = {'Donatel': ['Master Shifu'],
                            'Jett Finderson': ['Panda po'], 
                            'Faderon': ['Derek Patterson'],
                            'Matterson': ['Enduring'],
                            'Falony': ['Godzilla']
                            
        }
        self.assertEqual(key_by_author(search_results, mapped_titles_1), mapped_authors_1)
        self.assertEqual(key_by_author(search_results, mapped_titles_2), mapped_authors_2)
        self.assertEqual(key_by_author([], mapped_titles_1), {})
    
    def test_filter_to_author(self):
        mapped_titles = {'Master Shifu': {'author': 'Donatel', 'timestamp': 6258422, 'length': 3000},
                         'Panda po': {'author': 'Jett Finderson', 'timestamp': 69274794, 'length': 2100},
                         'Derek Patterson': {'author': 'Donatel', 'timestamp': 82729742, 'length': 434},
                         'Enduring': {'author': 'Matterson', 'timestamp': 7429646, 'length': 500300}
        }
        holder_search_results = ['Master Shifu', 'Panda po', 'Enduring']
        hold_search_results = ['Derek Patterson','Panda po']
        self.assertEqual(filter_to_author('Donatel', holder_search_results, mapped_titles), ['Master Shifu'])
        self.assertEqual(filter_to_author('DONATEL', holder_search_results, mapped_titles), [])
        self.assertEqual(filter_to_author('Donatel', hold_search_results, mapped_titles), ['Derek Patterson'])
        self.assertEqual(filter_to_author('donatel', hold_search_results, mapped_titles), [])
        self.assertEqual(filter_to_author('', hold_search_results, mapped_titles), [])
        self.assertEqual(filter_to_author('Matterson', hold_search_results, mapped_titles), [])
    
    def test_filter_out(self):
        mapped_keywords = {
                           'fan': ['Wizkidayo'],
                           'monkey' : ['Dance Monkey'],
                           'spider': ['King Kong', 'Godzilla'],
                           'computer': ['kettle','fadeso','killa'],
                           'samba': ['King Kong', 'Jon Frederick', 'Godzilla'],
                           'patter': ['Jon Frederick']
                           
        }
        search_man_results = ['King Kong', 'Jon Frederick', 'Godzilla']
        search_two_results = ['Wizkidayo', 'Machala']
        self.assertEqual(filter_out('spider', search_man_results, mapped_keywords), ['Jon Frederick'])
        self.assertEqual(filter_out('fan', search_two_results, mapped_keywords), ['Machala'])
        self.assertEqual(filter_out('', search_two_results, mapped_keywords), search_two_results)
        self.assertEqual(filter_out('samba', search_man_results, mapped_keywords), [])
        self.assertEqual(filter_out('patter', search_man_results, mapped_keywords), ['King Kong', 'Godzilla'])
        self.assertEqual(filter_out('computer', [], mapped_keywords), [])
    
    def test_articles_from_year(self):
        mapped_titles = {'Master Shifu': {'author': 'Donatel', 'timestamp':132415200, 'length': 3000},
                         'Panda po': {'author': 'Jett Finderson', 'timestamp': 132501600, 'length': 2100},
                         'Derek Patterson': {'author': 'Donatel', 'timestamp': 1079269200, 'length': 434},
                         'Enduring': {'author': 'Matterson', 'timestamp': 1110805200, 'length': 69496229},
                         'Projecture': {'author': 'Rickerson', 'timestamp': 1110978000, 'length': 629742},
                         'Falacy': {'author': 'Johnson', 'timestamp': 1110891600, 'length': 72977913}
        }
        basic_searched_results = ['Master Shifu','Panda po','Derek Patterson','Enduring','Projecture','Falacy']
        self.assertEqual(articles_from_year(1974,basic_searched_results, mapped_titles), ['Master Shifu','Panda po'])
        self.assertEqual(articles_from_year(2004,basic_searched_results, mapped_titles), ['Derek Patterson'])
        self.assertEqual(articles_from_year(2005,basic_searched_results, mapped_titles), ['Enduring','Projecture','Falacy'])
        self.assertEqual(articles_from_year(2022,basic_searched_results, mapped_titles), [])

    #####################
    # INTEGRATION TESTS #
    #####################
   
    @patch('builtins.input')
    def test_example_integration_test(self, input_mock):
        keyword = 'soccer'
        advanced_option = 5
        advanced_response = 2009

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Spain national beach soccer team', 'Steven Cohen (soccer)']\n"

        self.assertEqual(output, expected)
    @patch('builtins.input')
    def test_advanced_option_6(self, input_mock):
        keyword = 'musician'
        advanced_option = 6
        advanced_response = ''

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\nHere are your articles: ['List of Canadian musicians', '1986 in music', '2009 in music', 'List of overtone musicians', '1996 in music', '2006 in music', '2007 in music', '2008 in music']\n"

        self.assertEqual(output, expected)
    @patch('builtins.input')
    def test_advanced_option_1(self, input_mock):
        keyword = 'musician'
        advanced_option = 1
        advanced_response = 76

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nNo articles found\n"

        self.assertEqual(output, expected)
    @patch('builtins.input')
    def test_advanced_option_2(self, input_mock):
        keyword = 'musician'
        advanced_option = 2
        advanced_response = ''

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\nHere are your articles: {'Jack Johnson': ['List of Canadian musicians', '2006 in music'], 'jack johnson': ['1986 in music'], 'RussBot': ['2009 in music'], 'Mack Johnson': ['List of overtone musicians'], 'Nihonjoe': ['1996 in music'], 'Bearcat': ['2007 in music'], 'Burna Boy': ['2008 in music']}\n"

        self.assertEqual(output, expected)
    @patch('builtins.input')
    def test_advanced_option_3(self, input_mock):
        keyword = 'music'
        advanced_option = 3
        advanced_response = 'Burna Boy'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['Lights (musician)', 'Indian classical music', 'Tony Kaye (musician)', '2008 in music']\n"

        self.assertEqual(output, expected)
    @patch('builtins.input')
    def test_advanced_option_4(self, input_mock):
        keyword = 'musician'
        advanced_option = 4
        advanced_response = 'canada'

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['1986 in music', '2009 in music', 'List of overtone musicians', '1996 in music', '2006 in music', '2007 in music', '2008 in music']\n"

        self.assertEqual(output, expected)
    @patch('builtins.input')
    def test_advanced_option_5(self, input_mock):
        keyword = 'musician'
        advanced_option = 5
        advanced_response = 2009

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\n\nHere are your articles: ['2009 in music']\n"

        self.assertEqual(output, expected)
    @patch('builtins.input')   
    def test_no_article_found(self, input_mock):
        keyword = 'MUSICIAN'
        advanced_option = 6
        advanced_response = ''

        output = get_print(input_mock, [keyword, advanced_option, advanced_response])
        expected = print_basic() + keyword + '\n' + print_advanced() + str(advanced_option) + '\n' + print_advanced_option(advanced_option) + str(advanced_response) + "\nNo articles found\n"

        self.assertEqual(output, expected)

# Write tests above this line. Do not remove.
if __name__ == "__main__":
    main()