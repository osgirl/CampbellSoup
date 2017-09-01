# (c) 2017 Julian Gonggrijp

import pyparsing as pp

from .parsers import *


def test_to_int():
    string = '999 bananas'
    parser1 = pp.Word(pp.nums) + pp.Word(pp.alphas)
    result1 = parser1.parseString(string)
    assert result1[0] == '999'
    parser2 = parser1.setParseAction(to_int)
    result2 = parser2.parseString(string)
    assert result2[0] == 999
    parser3 = parser2.addParseAction(to_int)
    result3 = parser3.parseString(string)
    assert result3[0] == 999


def test_integer():
    assert integer.parseString('123')[0] == 123
    assert integer.parseString('123.456')[0] == 123
    assert not integer.matches('.456')
    assert not integer.matches('abc')
    assert not integer.matches('')


def test_floating():
    assert floating.parseString('123')[0] == 123.0
    assert floating.parseString('123.456')[0] == 123.456
    assert floating.parseString('.456')[0] == .456
    assert not floating.matches('abc')
    assert not floating.matches('')


def test_line_start():
    parser1 = integer + line_start
    parser2 = integer + pp.lineEnd + line_start
    assert not parser1.matches('123\n ')
    assert parser2.matches('123\n ')


def test_line_end():
    assert len(line_end.parseString('')) == 0
    assert len(line_end.parseString(' ')) == 0
    assert len(line_end.parseString('\n')) == 0
    assert not (line_end + ' ').matches(' ')


def test_empty_line():
    assert len(empty_line.parseString('')) == 0
    assert empty_line.parseString('\n')[0] == '\n'
    assert len(empty_line.parseString(' ')) == 0
    assert empty_line.parseString(' \n')[0] == '\n'
    assert empty_line.parseString(' \n\n')[0] == '\n'
    assert empty_line.parseString(' \nabc')[0] == '\n'
    for head in 'a1.':
        for tail in ('', '\n', '\n\n'):
            assert not empty_line.matches(head + tail)


def test_twoOrMore():
    assert not twoOrMore(integer).matches('')
    assert not twoOrMore(integer).matches('123')
    assert len(twoOrMore(integer).parseString('123 456')) == 2
    assert len(twoOrMore(integer).parseString('123 456 789')) == 3


def test_m_keywords():
    parser1 = m_colon + m_comma + m_dash + m_quote + m_titel + m_plat
    assert len(parser1.parseString(':,-"titel plat')) == 0
    assert len((m_titel * 4).parseString('titel TITEL TiTeL tItEl')) == 0
    assert len((m_plat * 4).parseString('PLAT plat plAT PLat')) == 0
    assert len((m_toetsjaar * 2).parseString('toetsJAAR TOETSjaar')) == 0
    assert len((m_auteur * 4).parseString('auteuR AUTEUr AUTEUR auTeuR')) == 0
    assert len((m_deelvragen * 2).parseString(' deElvrageN deElvRagEn')) == 0
    assert len((m_antwoord * 3).parseString('ANTWOORD anTwoOrd Antwoord')) == 0
    assert len((m_herbruik * 3).parseString('herbruik HERBRUIK hErBruIk')) == 0
    assert len(m_puntenverdeling.parseString('pUnteNverDELiNg')) == 0
    assert len((m_afbeeldingen*2).parseString('aFbeeldingen afbeeldINgen')) == 0
    for parser in (
        m_colon, m_comma, m_dash, m_quote, m_titel, m_plat, m_toetsjaar,
        m_auteur, m_deelvragen, m_antwoord, m_herbruik, m_puntenverdeling,
        m_afbeeldingen,
    ):
        for invalid in ('', '.', 'a', '1'):
            assert not parser.matches(invalid)


def test_v_keywords():
    assert len((v_onbekend * 3).parseString('onbekend ONBEKEND oNbEkEnD')) == 0
    assert len((v_geen * 4).parseString('GeeN gEeN GEEN geen')) == 0
    assert len((v_nee * 4).parseString('NEE nee NeE nEe')) == 0
    for parser in (v_onbekend, v_geen, v_nee):
        for invalid in ('', '.', 'a', '1'):
            assert not parser.matches(invalid)


def test_v_year():
    assert v_year.parseString('2004')[0] == 2004
    assert v_year.parseString('2010')[0] == 2010
    assert v_year.parseString('2092')[0] == 2092
    assert not v_year.matches('a')
    assert not v_year.matches('123')
    assert not v_year.matches('2003')
    assert not v_year.matches('2100')


def test_v_question_number():
    assert v_question_number.parseString('1')[0] == 1
    assert v_question_number.parseString('5')[0] == 5
    assert v_question_number.parseString('99')[0] == 99
    assert not v_question_number.matches('')
    assert not v_question_number.matches('100')
    assert not v_question_number.matches('a')


def test_v_author():
    assert v_author.parseString('  banananana2')[0] == '  banananana2'
    assert v_author.parseString('Banana Nanana')[0] == 'Banana Nanana'
    assert v_author.parseString('Banana,Nanana')[0] == 'Banana'
    assert v_author.parseString('Banana\nNanana')[0] == 'Banana'
    assert not v_author.matches('')


def test_l_keywords():
    assert len(((l_pipe & l_bang)* 4).parseString('|!!|!||!')) == 0
    assert len(l_figure.parseString('figure')) == 0
    assert len(l_answer.parseString('answer')) == 0
    assert len(l_comment.parseString('comment')) == 0
    assert len(l_points.parseString('points')) == 0
    assert len(l_type.parseString('type')) == 0
    assert len(l_choose.parseString('choose')) == 0
    assert len(l_drawbox.parseString('drawbox')) == 0
    assert len(l_table.parseString('table')) == 0
    assert len(l_answerfigure.parseString('answerfigure')) == 0
    assert len(l_complete_text.parseString('complete_text')) == 0
    assert len(l_dont_randomize.parseString('dont_randomize')) == 0
    assert len(l_subquestions.parseString('subquestions')) == 0
    assert len(l_answerblock.parseString('answerblock')) == 0
    for parser in (
        l_pipe, l_bang, l_figure, l_answer, l_comment, l_points, l_type,
        l_choose, l_drawbox, l_table, l_answerfigure, l_complete_text,
        l_dont_randomize, l_subquestions, l_answerblock, 
    ):
        for invalid in ('', '.', 'a', '1'):
            assert not parser.matches(invalid)


def test_t_keywords():
    assert t_whichof2.parseString('whichof2')[0] == 'whichof2'
    assert t_mc.parseString('mc')[0] == 'mc'
    assert t_open.parseString('open')[0] == 'open'
    assert t_truefalse.parseString('truefalse')[0] == 'truefalse'
    assert t_truefalse.parseString('plusmin')[0] == 'truefalse'
    for parser in (t_whichof2, t_mc, t_open, t_truefalse):
        for invalid in ('', '.', 'a', '1'):
            assert not parser.matches(invalid)


def test_w_tables():
    cell = 'abc 123;!'
    row = 'abc|123|...'
    table = 'a|b|c||1|2|3||.|.|.'
    results = [[parser.parseString(string) for parser in (
        w_table_cell,
        w_table_row,
        w_table,
    )] for string in (cell, row, table)]
    # parse cell as w_cell
    assert results[0][0][0] == 'abc 123;!'
    # parse cell as w_row
    assert results[0][1][0].asList() == ['abc 123;!']
    # parse cell as w_table
    assert results[0][2].asList() == [['abc 123;!']]
    # parse row as w_cell
    assert results[1][0][0] == 'abc'
    # parse row as w_row
    assert results[1][1][0].asList() == ['abc', '123', '...']
    # parse row as w_table
    assert results[1][2].asList() == [['abc', '123', '...']]
    # parse table as w_cell
    assert results[2][0][0] == 'a'
    # parse table as w_row
    assert results[2][1][0].asList() == ['a', 'b', 'c']
    # parse table as w_table
    assert results[2][2].asList() == [
        ['a', 'b', 'c'],
        ['1', '2', '3'],
        ['.', '.', '.'],
    ]


def test_w_args():
    int_arg = '!123'
    float_arg = '!123.456'
    text_arg = '!12ab'
    table_arg = '!1a|2b||3c|4d'
    assert w_integer_arg.parseString(int_arg).asList() == [123]
    assert w_integer_arg.parseString(float_arg).asList() == [123]
    assert w_integer_arg.parseString(text_arg).asList() == [12]
    assert w_integer_arg.parseString(table_arg).asList() == [1]
    assert w_floating_arg.parseString(int_arg).asList() == [123]
    assert w_floating_arg.parseString(float_arg).asList() == [123.456]
    assert w_floating_arg.parseString(text_arg).asList() == [12]
    assert w_floating_arg.parseString(table_arg).asList() == [1]
    assert w_table_arg.parseString(int_arg).asList() == [['123']]
    assert w_table_arg.parseString(float_arg).asList() == [['123.456']]
    assert w_table_arg.parseString(text_arg).asList() == [['12ab']]
    assert w_table_arg.parseString(table_arg).asList() == [
        ['1a', '2b'],
        ['3c', '4d'],
    ]
    assert w_generic_arg.parseString(int_arg).asList() == ['123']
    assert w_generic_arg.parseString(float_arg).asList() == ['123.456']
    assert w_generic_arg.parseString(text_arg).asList() == ['12ab']
    assert w_generic_arg.parseString(table_arg).asList() == ['1a|2b||3c|4d']


def test_w_command_start():
    assert w_command_start.matches('!')
    assert (pp.lineEnd + w_command_start).matches('\n!')


def test_w_figure_com():
    assert w_figure_com.parseString('figure!banana.png').asDict() == {
        'figure': ['banana.png'],
    }
    assert w_figure_com.parseString('figure!banana.png!0.3').asDict() == {
        'figure': ['banana.png', 0.3],
    }
    assert not w_figure_com.matches('figure!banana.png!banana.png')
    assert not w_figure_com.matches('figure')


def test_w_subquestions_com():
    assert w_subquestions_com.parseString('subquestions!10').asDict() == {
        'subquestions': [10],
    }
    assert not w_subquestions_com.matches('subquestions!10.5')
    assert not w_subquestions_com.matches('subquestions!10!5')
    assert not w_subquestions_com.matches('subquestions')


def test_w_table_com():
    assert w_table_com.parseString('table!ab|cd||12|34').asDict() == {'table': [
        ['ab', 'cd'], ['12', '34'],
    ]}
    assert not w_table_com.matches('table')


def test_w_points_com():
    assert w_points_com.parseString('points!10').asDict() == {
        'points': [10.0],
    }
    # assert w_points_com.parseString('points!10(3:4:3)').asDict() == {
    #     'points': [10.0, [3.0, 4.0, 3.0]],
    # }
    assert not w_points_com.matches('points!10!4')
    assert not w_points_com.matches('points')


def test_w_comment_com():
    assert w_comment_com.parseString('comment!bla!123!abc|||!').asDict() == {
        'comments': [['bla', '123!abc|||!']],
    }
    parser = pp.OneOrMore(w_comment_com)
    assert parser.parseString('comment!bla!123\ncomment!yada!456').asDict() == {
        'comments': [['bla', '123'], ['yada', '456']],
    }
    assert not w_comment_com.matches('comment')


def test_w_answer_com():
    assert w_answer_com.parseString('answer!bla!123!abc|||!').asDict() == {
        'answer': ['bla!123!abc|||!'],
    }
    assert not w_answer_com.matches('answer')


def test_w_command_line():
    assert w_command_line.parseString('!dont_randomize').asDict() == {
        'dontRandomize': True,
    }
    for valid in (
        'figure!banana.png!0.3', 'subquestions!10', 'table!ab|cd||12|34',
        'points!10', 'comment!bla!123!abc|||!', 'answer!bla!123!abc|||!',
    ):
        assert not w_command_line.matches(valid)
        assert len(w_command_line.parseString('!' + valid).asDict()) == 1
        assert w_command_line.matches('!' + valid + '\n')
    for invalid in (
        'dont_randomize!1', 'figure!banana.png!banana.png', 'anything'
        'subquestions!10.5', 'table', 'points!10!4', 'comment', 'answer',
    ):
        assert not w_command_line.matches(invalid)
        assert not w_command_line.matches('!' + invalid)
        assert not w_command_line.matches('!' + invalid + '\n')


def test_w_type_start():
    assert w_type_start.matches('!type!')
    assert w_type_start.matches('  !type!')
    assert not w_type_start.matches('type!')
    assert not w_type_start.matches('!type')
    assert not w_type_start.matches('')


def test_w_mc_decl():
    assert w_mc_decl.matches('mc')
    assert w_mc_decl.parseString('mc!4').asList() == ['mc', 4]
    assert not w_mc_decl.matches('mc!4.5')
    assert not w_mc_decl.matches('mc!4!5')
    assert not w_mc_decl.matches('mc!ab')


def test_w_open_decl():
    assert w_open_decl.parseString('open!2').asList() == ['open', 2]
    assert w_open_decl.matches('open!34')
    assert w_open_decl.matches('open!567')
    assert not w_open_decl.matches('open!4.5')
    assert not w_open_decl.matches('open!ab')
    assert not w_open_decl.matches('open')


def test_w_truefalse_decl():
    assert w_truefalse_decl.matches('truefalse')
    assert w_truefalse_decl.matches('truefalse!6')
    assert w_truefalse_decl.matches('plusmin')
    assert w_truefalse_decl.parseString('plusmin!6').asList() == [
        'truefalse',
        6,
    ]
    assert not w_truefalse_decl.matches('truefalse!ab')
    assert not w_truefalse_decl.matches('truefalse!1.2')
    assert not w_truefalse_decl.matches('plusmin!ab')
    assert not w_truefalse_decl.matches('plusmin!1.2')


def test_w_type_line():
    assert w_type_line.parseString('!type!whichof2').asDict() == {
        'type': ['whichof2'],
    }
    for valid in ('mc!4', 'open!4', 'truefalse!4', 'plusmin!4'):
        result = w_type_line.parseString('!type!' + valid).asDict()
        assert len(result) == 1
        assert 'type' in result
        assert len(result['type']) == 2
        assert type(result['type'][0]) == str
        assert result['type'][1] == 4
        assert w_type_line.matches('!type!' + valid + '\n')
    for invalid in ('whichof2!1', 'mc!ab', 'open', 'truefalse!1.2'):
        assert not w_type_line.matches(invalid)
        assert not w_type_line.matches('!type!' + invalid)
        assert not w_type_line.matches('!type!' + invalid + '\n')


def test_w_normal_line():
    assert w_normal_line.parseString('bananas bananas').asList() == [
        'bananas bananas',
    ]
    assert w_normal_line.parseString('bananas!bananas').asList() == [
        'bananas!bananas',
    ]
    assert w_normal_line.parseString('bananas\nbananas').asList() == ['bananas']
    assert not w_normal_line.matches('')
    assert not w_normal_line.matches(' \n')
    assert not w_normal_line.matches('!bananas\n')


def test_w_drawbox_line():
    assert w_drawbox_line.parseString('!drawbox!10.8\n').asDict() == {
        'drawbox': [10.8],
    }
    assert not w_drawbox_line.matches('!drawbox!ab\n')
    assert not w_drawbox_line.matches('!drawbox\n')


def test_w_answerfigure_line():
    assert w_answerfigure_line.parseString(
        '!answerfigure!banana.png\n',
    ).asDict() == {'answerfigure': ['banana.png']}
    assert w_answerfigure_line.parseString(
        '!answerfigure!banana.png!4.5',
    ).asDict() == {'answerfigure': ['banana.png', 4.5]}
    assert not w_answerfigure_line.matches('!answerfigure!banana.png!bla')
    assert not w_answerfigure_line.matches('!answerfigure\n')


def test_w_answerblock_line():
    assert w_answerblock_line.parseString('!answerblock!2!3\n').asDict() == {
        'answerblock': [2, 3],
    }
    assert not w_answerblock_line.matches('!answerblock!2!3.5\n')
    assert not w_answerblock_line.matches('!answerblock!2.5!3\n')
    assert not w_answerblock_line.matches('!answerblock!2\n')
    assert not w_answerblock_line.matches('!answerblock\n')


def test_w_command_line_x():
    assert w_command_line_x.matches('!figure!banana.png!0.3')
    assert w_command_line_x.matches('!answerblock!2!3\n')
    assert w_command_line_x.matches('!drawbox!10.8\n')
    assert w_command_line_x.matches('!type!open!4')
    assert w_command_line_x.matches('!answerfigure!banana.png\n')
    assert not w_command_line_x.matches('!type!complete_text')
    assert not w_command_line_x.matches('!choose!abc!def\n')
    assert not w_command_line_x.matches('banana bananas')


def test_w_complete_text_line():
    assert w_complete_text_line.parseString('!type!complete_text').asDict() == {
        'complete_text': [],
    }
    assert not w_complete_text_line.matches('!type!complete_text!1')
    assert not w_complete_text_line.matches('!type')


def test_addCondition():
    """ Check the behaviour of pyparsing.ParserElement.addCondition. """
    parser1 = w_drawbox_line.copy().addCondition(lambda toks: 'drawbox' in toks)
    assert parser1.matches('!drawbox!1\n')
    parser2 = w_type_line.copy().addCondition(
        lambda toks: hasattr(toks, 'type')
    )
    assert parser2.matches('!type!open!1\n')


def test_w_is_typed():
    text1 = '!comment!someone!whatever\n'
    text2 = '!type!open!2\n'
    text3 = text1 + text2
    text4 = text1 + text1
    assert w_comment_line.matches(text1)
    parser1 = w_comment_line.copy().addCondition(w_is_typed)
    assert not parser1.matches(text1)
    assert w_type_line.matches(text2)
    parser2 = w_type_line.copy().addCondition(w_is_typed)
    assert parser2.matches(text2)
    parser3 = pp.OneOrMore(w_command_line_x)
    assert parser3.matches(text3)
    parser4 = parser3.copy().addCondition(w_is_typed)
    assert parser4.matches(text3)
    assert parser3.matches(text4)
    parser5 = parser3.copy().addCondition(w_is_typed)
    assert not parser5.matches(text4)


def test_regressions():
    for parser, example, result in EXAMPLES:  # bottom of file
        if isinstance(result, dict):
            assert parser.parseString(example, parseAll=True).asDict() == result
        else:
            assert parser.parseString(example, parseAll=True).asList() == result


# The examples below are based on real question files. They were
# bananafied in order to keep confidential information confidential.

EXAMPLES = [(document, '''Toetsjaar: 2090
Auteur: onbekend
Titel:"Banana banana banana"
Deelvragen:3
Plat:
"Banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana: banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana. 
banana. Banana banana (banana banana banana) banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana.

	banana				banana








Banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana.(Banana banana, banana banana banana (banana banana))

	banana	banana









**$$**
Banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana, banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana. 

banana. Banana banana banana banana banana banana banana banana banana banana banana banana?
*

*


**$$**
banana.    Banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana-banana banana. Banana banana banana banana banana banana banana banana banana banana banana banana. (Banana banana banana banana banana banana banana banana banana banana banana)
Banana banana banana banana banana banana banana banana banana banana banana? 
banana: Banana banana: banana banana banana banana
     Banana banana: banana banana banana banana
banana: Banana banana: banana banana banana banana
     Banana banana: banana banana banana banana"

Antwoord:Onbekend
Puntenverdeling:Onbekend
Afbeeldingen:Geen
Herbruik:Nee
''', {
    'answer': [None],
    'authors': [None],
    'contentPlain': [
        'Banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana: banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana. \nbanana. Banana banana (banana banana banana) banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana.\n\n        banana                          banana\n\n\n\n\n\n\n\n\nBanana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana.(Banana banana, banana banana banana (banana banana))\n\n        banana  banana\n\n\n\n\n\n\n\n\n\n',
        'Banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana, banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana. \n\nbanana. Banana banana banana banana banana banana banana banana banana banana banana banana?\n*\n\n*\n\n\n',
        'banana.    Banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana-banana banana. Banana banana banana banana banana banana banana banana banana banana banana banana. (Banana banana banana banana banana banana banana banana banana banana banana)\nBanana banana banana banana banana banana banana banana banana banana banana? \nbanana: Banana banana: banana banana banana banana\n     Banana banana: banana banana banana banana\nbanana: Banana banana: banana banana banana banana\n     Banana banana: banana banana banana banana',
    ],
    'images': [None],
    'points': [None],
    'questionCount': [3],
    'reuse': [None],
    'title': ['Banana banana banana'],
    'year': [2090],
}), (document, '''Auteur: Banana Banana
Herbruik:nee
Banana

Banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana, banana banana banana Banana banana (\\'{a}\\'{a}nana Banana) banana Banana banana (Banana) banana banana banana. Banana banana banana banana banana banana Banana-banana, banana banana banana banana banana Banana-banana banana.

Banana banana banana banana banana banana banana (banana-banana) banana banana banana banana banana Banana banana banana. Banana banana banana banana banana banana banana banana.
!answerfigure!banana.png
!points!1
!answer!Banana banana banana.

Banana banana banana banana banana banana banana banana banana banana banana banana banana.
!type!open!3
!points!2
!answer!banana Banana

Banana Banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana Banana, Banana$_1$ banana Banana$_2$ banana banana banana~Banana banana Banana-banana banana banana banana banana banana banana banana banana Banana-banana banana banana banana banana Banana-banana banana banana banana banana banana banana banana banana banana banana \\'{a}\\'{a}nana banana banana banana banana.\\\\Banana banana banana banana banana banana banana Banana~banana banana banana Banana~banana banana banana banana banana Banana banana, banana banana banana banana banana \\ldots
\\ldots banana banana banana banana banana banana banana.
\\ldots banana banana banana Banana banana banana banana, banana banana banana banana banana.
!subquestions!2
!type!open!1
!points!2
!answer!banana banana banana
!comment!answer!40 banana banana
''', {
    'authors': [' Banana Banana'],
    'contentLW': [{
        'title': 'Banana',
    }, {
        'title': "Banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana, banana banana banana Banana banana (\\'{a}\\'{a}nana Banana) banana Banana banana (Banana) banana banana banana. Banana banana banana banana banana banana Banana-banana, banana banana banana banana banana Banana-banana banana.",
    }, {
        'answer': ['Banana banana banana.'],
        'answerfigure': ['banana.png'],
        'points': [1.0],
        'question': 'Banana banana banana banana banana banana banana (banana-banana) banana banana banana banana banana Banana banana banana. Banana banana banana banana banana banana banana banana.\n',
    }, {
        'answer': ['banana Banana'],
        'points': [2.0],
        'question': 'Banana banana banana banana banana banana banana banana banana banana banana banana banana.\n',
        'type': ['open', 3],
    }, {
        'answer': ['banana banana banana'],
        'comments': [['answer', '40 banana banana']],
        'points': [2.0],
        'question': "Banana Banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana Banana, Banana$_1$ banana Banana$_2$ banana banana banana~Banana banana Banana-banana banana banana banana banana banana banana banana banana Banana-banana banana banana banana banana Banana-banana banana banana banana banana banana banana banana banana banana banana \\'{a}\\'{a}nana banana banana banana banana.\\\\Banana banana banana banana banana banana banana Banana~banana banana banana Banana~banana banana banana banana banana Banana banana, banana banana banana banana banana \\ldots\n\\ldots banana banana banana banana banana banana banana.\n\\ldots banana banana banana Banana banana banana banana, banana banana banana banana banana.\n",
        'subquestions': [2],
        'type': ['open', 1],
    }],
    'reuse': [None],
}), (pp.ZeroOrMore(g_meta_field), '''Afbeeldingen:"6.png"
Herbruik:Nee
''', {
    'images': ['6.png'],
    'reuse': [None],
}), (pp.ZeroOrMore(g_meta_field), '''Afbeeldingen:"2a.png", "2b.png", "2c.png", "2d.png", "2e.png", "2f.png"
Herbruik:Nee
''', {
    'images': ['2a.png', '2b.png', '2c.png', '2d.png', '2e.png', '2f.png'],
    'reuse': [None],
}), (g_plaintext_field, r'''Plat:"Banana banana banana banana’banana banana banana banana. Banana banana banana banana banana banana banana Banana’banana bana¨na banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana?

A. Banana ban\"ana banana banana banana banana banana banana banana banana ban\"ana banana banana.
B. Banana banana banana banana banana banana, banana banana banana banana banana banana banana
banana banana banana banana–Banana.
C. Banana bana¨na banana banana banana banana banana–Banana banana banana banana banana banana banana banana.
D. Banana bana¨na banana banana banana banana banana banana banana banana banana banana banana.
E. Banana banana banana banana banana banana banana banana banana banana banana."''', {
    'contentPlain': ['''Banana banana banana banana’banana banana banana banana. Banana banana banana banana banana banana banana Banana’banana bana¨na banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana?

A. Banana ban\"ana banana banana banana banana banana banana banana banana ban\"ana banana banana.
B. Banana banana banana banana banana banana, banana banana banana banana banana banana banana
banana banana banana banana–Banana.
C. Banana bana¨na banana banana banana banana banana–Banana banana banana banana banana banana banana banana.
D. Banana bana¨na banana banana banana banana banana banana banana banana banana banana banana.
E. Banana banana banana banana banana banana banana banana banana banana banana.'''],
}), (w_question_group, '''Banana banana banana banana
Banana banana [i]Banana banana[/i] banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana (-- banana banana banana banana banana banana ``banana banana banana\'\' banana). Banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana, banana banana banana banana banana. \\newline Banana banana banana banana banana banana banana banana. Banana banana banana banana, banana banana banana banana banana, banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana. 
!figure!Banana.png
!comment!Banana!banana banana banana banana banana.


Banana + banana banana banana banana banana banana banana: banana banana banana banana banana (banana-) banana. Banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana ($\\alpha$- en $\\beta$- banana banana, banana banana banana banana banana banana) banana banana banana banana $2\\cdot 10^{8}$kg banana. Banana banana banana banana banana banana banana banana banana. \\newline Banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana. Banana banana banana banana banana banana 4 $\\cdot 10^{X}$L banana banana banana banana 5 $\\cdot 10^{X}$L. Banana banana.
!type!open!1
!answer!100
!points!1
!comment!Banana!http://www.banana.com/ - banana banana banana banana (B. banana) = 25 mg/ml (A+B banana) - banana: banana = 600 g/L
''', {'contentLW': [{
    'title': 'Banana banana banana banana',
    'intro': 'Banana banana [i]Banana banana[/i] banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana (-- banana banana banana banana banana banana ``banana banana banana\'\' banana). Banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana, banana banana banana banana banana. \\newline Banana banana banana banana banana banana banana banana. Banana banana banana banana, banana banana banana banana banana, banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana. ',
    'figure': ['Banana.png'],
    'comments': [['Banana', 'banana banana banana banana banana.']],
}, {
    'question': '''Banana + banana banana banana banana banana banana banana: banana banana banana banana banana (banana-) banana. Banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana ($\\alpha$- en $\\beta$- banana banana, banana banana banana banana banana banana) banana banana banana banana $2\\cdot 10^{8}$kg banana. Banana banana banana banana banana banana banana banana banana. \\newline Banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana. Banana banana banana banana banana banana 4 $\\cdot 10^{X}$L banana banana banana banana 5 $\\cdot 10^{X}$L. Banana banana.
''',
    'type': ['open', 1],
    'answer': ['100'],
    'points': [1.0],
    'comments': [['Banana', 'http://www.banana.com/ - banana banana banana banana (B. banana) = 25 mg/ml (A+B banana) - banana: banana = 600 g/L']]
}]}), (w_question_group_sources, r'''Banana banana banana banana
Banana banana [i]Banana banana[/i] banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana (-- banana banana banana banana banana banana ``banana banana banana'' banana). Banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana, banana banana banana banana banana. \newline Banana banana banana banana banana banana banana banana. Banana banana banana banana, banana banana banana banana banana, banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana. 
!figure!Banana.png
!comment!Banana!banana banana banana banana banana.


Banana + banana banana banana banana banana banana banana: banana banana banana banana banana (banana-) banana. Banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana ($\alpha$- en $\beta$- banana banana, banana banana banana banana banana banana) banana banana banana banana $2\cdot 10^{8}$kg banana. Banana banana banana banana banana banana banana banana banana. \newline Banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana. Banana banana banana banana banana banana 4 $\cdot 10^{X}$L banana banana banana banana 5 $\cdot 10^{X}$L. Banana banana.
!type!open!1
!answer!100
!points!1
!comment!Banana!http://www.banana.com/ - banana banana banana banana (B. banana) = 25 mg/ml (A+B banana) - banana: banana = 600 g/L
''', [
    r'''Banana banana banana banana
Banana banana [i]Banana banana[/i] banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana (-- banana banana banana banana banana banana ``banana banana banana'' banana). Banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana, banana banana banana banana banana. \newline Banana banana banana banana banana banana banana banana. Banana banana banana banana, banana banana banana banana banana, banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana. 
!figure!Banana.png
!comment!Banana!banana banana banana banana banana.
''',
    r'''Banana + banana banana banana banana banana banana banana: banana banana banana banana banana (banana-) banana. Banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana banana ($\alpha$- en $\beta$- banana banana, banana banana banana banana banana banana) banana banana banana banana $2\cdot 10^{8}$kg banana. Banana banana banana banana banana banana banana banana banana. \newline Banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana. Banana banana banana banana banana banana 4 $\cdot 10^{X}$L banana banana banana banana 5 $\cdot 10^{X}$L. Banana banana.
!type!open!1
!answer!100
!points!1
!comment!Banana!http://www.banana.com/ - banana banana banana banana (B. banana) = 25 mg/ml (A+B banana) - banana: banana = 600 g/L
'''
]), (w_atleast3commands, r'''!points!3
!drawbox!1.5
!answer!banana banana banana banana banana banana banana banana banana
!comment!banana1!banana banana, banana banana banana banana banana banana?
!comment!banana2!banana banana banana banana banana banana, banana banana. banana banana banana banana banana banana, banana banana banana banana. banana banana banana banana banana banana.''', {
    'points': [3.0],
    'drawbox': [1.5],
    'answer': [
        'banana banana banana banana banana banana banana banana banana'
    ],
    'comments': [[
        'banana1',
        'banana banana, banana banana banana banana banana banana?',
    ], [
        'banana2',
        'banana banana banana banana banana banana, banana banana. banana banana banana banana banana banana, banana banana banana banana. banana banana banana banana banana banana.',
    ]],
})]
