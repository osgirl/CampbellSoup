# (c) 2017 Julian Gonggrijp

import pyparsing as pp

# General

integer = (pp.Word(pp.nums)).setName('integer')
floating = (pp.Optional(integer) + '.' + integer | integer).setName('floating')


def twoOrMore(parserElement):
    """ returns a parser that matches `parserElement` twice or more. """
    return parserElement + pp.OneOrMore(parserElement)


# Meta keywords

m_toetsjaar       = (pp.CaselessKeyword('toetsjaar')).setName('m_toetsjaar')
m_auteur          = (pp.CaselessKeyword('auteur')).setName('m_auteur')
m_titel           = (pp.CaselessKeyword('titel')).setName('m_titel')
m_deelvragen      = (pp.CaselessKeyword('deelvragen')).setName('m_deelvragen')
m_plat            = (pp.CaselessKeyword('plat')).setName('m_plat')
m_antwoord        = (pp.CaselessKeyword('antwoord')).setName('m_antwoord')
m_herbruik        = (pp.CaselessKeyword('herbruik')).setName('m_herbruik')

m_puntenverdeling = (
    pp.CaselessKeyword('puntenverdeling')
).setName('m_puntenverdeling')

m_afbeeldingen    = (
    pp.CaselessKeyword('afbeeldingen')
).setName('m_afbeeldingen')

# Meta values

v_onbekend        = (pp.CaselessKeyword('onbekend')).setName('v_onbekend')
v_geen            = (pp.CaselessKeyword('geen')).setName('v_geen')
v_nee             = (pp.CaselessKeyword('nee')).setName('v_nee')

# LaTeX-writer keywords

l_bang            = (pp.Literal('!')).setName('l_bang')
l_pipe            = (pp.Literal('|')).setName('l_pipe')
l_figure          = (pp.Keyword('figure')).setName('l_figure')
l_answerfigure    = (pp.Keyword('answerfigure')).setName('l_answerfigure')
l_answer          = (pp.Keyword('answer')).setName('l_answer')
l_comment         = (pp.Keyword('comment')).setName('l_comment')
l_points          = (pp.Keyword('points')).setName('l_points')
l_type            = (pp.Keyword('type')).setName('l_type')
l_complete_text   = (pp.Keyword('complete_text')).setName('l_complete_text')
l_dont_randomize  = (pp.Keyword('dont_randomize')).setName('l_dont_randomize')
l_subquestions    = (pp.Keyword('subquestions')).setName('l_subquestions')
l_answerblock     = (pp.Keyword('answerblock')).setName('l_answerblock')
l_choose          = (pp.Keyword('choose')).setName('l_choose')
l_drawbox         = (pp.Keyword('drawbox')).setName('l_drawbox')
l_table           = (pp.Keyword('table')).setName('l_table')

# LaTeX-writer type values

t_whichof2        = (pp.Keyword('whichof2')).setName('t_whichof2')
t_mc              = (pp.Keyword('mc')).setName('t_mc')
t_open            = (pp.Keyword('open')).setName('t_open')

t_truefalse       = (
    pp.Keyword('truefalse') | pp.Keyword('plusmin')
).setName('t_truefalse')

# LaTeX-writer parts

w_table_cell        = (pp.CharsNotIn('|\n\r')).setName('w_table_cell')

w_table_row         = (
    w_table_cell + pp.ZeroOrMore(l_pipe + w_table_cell)
).setName('w_table_row')

w_table             = (
    w_table_row + pp.ZeroOrMore(l_pipe * 2 + w_table_row)
).setName('w_table')

w_integer_arg       = (l_bang + integer).setName('w_integer_arg')
w_floating_arg      = (l_bang + floating).setName('w_floating_arg')
w_table_arg         = (l_bang + w_table).setName('w_table_arg')
w_generic_arg       = (l_bang + pp.CharsNotIn('!\r\n')).setName('w_generic_arg')

w_command_start     = (pp.lineStart + l_bang).setName('w_command_start')

w_figure_com        = (
    l_figure + w_generic_arg + pp.Optional(w_floating_arg)
).setName('w_figure_com')

w_subquestions_com  = (
    l_subquestions + w_integer_arg
).setName('w_subquestions_com')

w_table_com         = (l_table + w_table_arg).setName('w_table_com')
w_points_com        = (l_points + w_floating_arg).setName('w_points_com')

w_comment_com       = (
    l_comment + w_generic_arg + pp.restOfLine
).setName('w_comment_com')

w_answer_com        = (
    l_answer + l_bang + pp.restOfLine
).setName('w_answer_com')

w_command_line      = (w_command_start + (
    w_figure_com | l_dont_randomize | w_subquestions_com | w_table_com |
    w_points_com | w_comment_com | w_answer_com
) + pp.lineEnd).setName('w_command_line')

w_type_start        = (
    w_command_start + l_type + l_bang
).setName('w_type_start')

w_mc_decl           = (t_mc + pp.Optional(w_integer_arg)).setName('w_mc_decl')
w_open_decl         = (t_open + w_integer_arg).setName('w_open_decl')

w_truefalse_decl    = (
    t_truefalse + pp.Optional(w_integer_arg)
).setName('w_truefalse_decl')

w_type_line         = (w_type_start + (
    t_whichof2 | w_mc_decl | w_open_decl | w_truefalse_decl
) + pp.lineEnd).setName('w_type_line')

w_empty_line         = (
    pp.lineStart + pp.lineEnd
).leaveWhitespace().setName('w_empty_line')

w_normal_line        = (
    ~w_empty_line + pp.lineStart + ~l_bang + pp.restOfLine + pp.lineEnd
).setName('w_normal_line')

w_drawbox_line       = (
    w_command_start + l_drawbox + w_floating_arg + pp.lineEnd
).setName('w_drawbox_line')

w_answerfigure_line  = (
    w_command_start + l_answerfigure + w_generic_arg +
    pp.Optional(w_floating_arg) + pp.lineEnd
).setName('w_answerfigure_line')

w_answerblock_line   = (
    w_command_start + l_answerblock + w_integer_arg * 2 + pp.lineEnd
).setName('w_answerblock_line')

w_command_line_x     = (
    w_command_line | w_answerblock_line
).setName('w_command_line_x')

w_type_line_x        = (
    w_type_line | w_answerblock_line | w_drawbox_line | w_answerfigure_line
).setName('w_type_line_x')

w_complete_text_line = (
    w_type_start + l_complete_text + pp.lineEnd
).setName('w_complete_text_line')

w_choose_line        = (
    w_command_start + l_choose + twoOrMore(w_generic_arg) + pp.lineEnd
).setName('w_choose_line')

w_complete_text_duet = (
    w_normal_line + w_choose_line
).setName('w_complete_text_duet')

w_atleast1command    = (
    pp.ZeroOrMore(w_command_line_x) + w_type_line_x +
    pp.ZeroOrMore(w_command_line_x)
).setName('w_atleast1command')

w_atleast2commands   = (
    w_type_line_x & w_command_line_x & pp.ZeroOrMore(w_command_line_x)
).setName('w_atleast2commands')

w_atleast3commands   = (
    w_type_line_x & w_command_line_x & pp.OneOrMore(w_command_line_x)
).setName('w_atleast3commands')

w_intro_block        = (
    w_normal_line + pp.Optional(w_normal_line) + pp.Optional(w_command_line)
).leaveWhitespace().setName('w_intro_block')

w_standard_question_block = (w_normal_line + (
    w_atleast3commands | w_normal_line + w_atleast2commands |
    twoOrMore(w_normal_line) + w_atleast1command
)).leaveWhitespace().setName('w_standard_question_block')

w_complete_text_block = (
    w_complete_text_line + pp.OneOrMore(w_complete_text_duet) +
    pp.Optional(w_normal_line) + pp.ZeroOrMore(w_command_line)
).leaveWhitespace().setName('w_complete_text_block')

w_block      = (
    w_standard_question_block | w_intro_block | w_complete_text_block
).setName('w_block')

w_question_group    = (
    w_block + pp.ZeroOrMore(w_empty_line + w_block)
).ignore(pp.pythonStyleComment + pp.lineEnd).setName('w_question_group')
