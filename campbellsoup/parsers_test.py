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


def test_document():
    for example, result in TEST_DOCUMENTS:  # bottom of file
        assert document.parseString(example, parseAll=True).asDict() == result


# The examples below are based on real question files. They were
# bananafied in order to keep confidential information confidential.

TEST_DOCUMENTS = [('''Toetsjaar: 2090
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
}), ('''Auteur: Banana Banana
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
})]
