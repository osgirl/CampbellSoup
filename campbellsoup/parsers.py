# (c) 2017 Julian Gonggrijp

import pyparsing as pp

# General
integer = pp.Word(pp.nums)
floating = pp.Optional(integer) + '.' + integer | integer


def twoOrMore(parserElement):
    """ returns a parser that matches `parserElement` twice or more. """
    return parserElement + pp.OneOrMore(parserElement)


# Meta keywords
m_toetsjaar       = pp.CaselessKeyword('toetsjaar')
m_auteur          = pp.CaselessKeyword('auteur')
m_titel           = pp.CaselessKeyword('titel')
m_deelvragen      = pp.CaselessKeyword('deelvragen')
m_plat            = pp.CaselessKeyword('plat')
m_antwoord        = pp.CaselessKeyword('antwoord')
m_puntenverdeling = pp.CaselessKeyword('puntenverdeling')
m_afbeeldingen    = pp.CaselessKeyword('afbeeldingen')
m_herbruik        = pp.CaselessKeyword('herbruik')

# Meta values
v_onbekend        = pp.CaselessKeyword('onbekend')
v_geen            = pp.CaselessKeyword('geen')
v_nee             = pp.CaselessKeyword('nee')

# LaTeX-writer keywords
l_bang            = pp.Literal('!')
l_pipe            = pp.Literal('|')
l_figure          = pp.Keyword('figure')
l_answerfigure    = pp.Keyword('answerfigure')
l_answer          = pp.Keyword('answer')
l_comment         = pp.Keyword('comment')
l_points          = pp.Keyword('points')
l_type            = pp.Keyword('type')
l_complete_text   = pp.Keyword('complete_text')
l_dont_randomize  = pp.Keyword('dont_randomize')
l_subquestions    = pp.Keyword('subquestions')
l_answerblock     = pp.Keyword('answerblock')
l_choose          = pp.Keyword('choose')
l_drawbox         = pp.Keyword('drawbox')
l_table           = pp.Keyword('table')

# LaTeX-writer type values
t_whichof2        = pp.Keyword('whichof2')
t_mc              = pp.Keyword('mc')
t_open            = pp.Keyword('open')
t_truefalse       = pp.Keyword('truefalse') | pp.Keyword('plusmin')

# LaTeX-writer parts
w_table_cell        = pp.CharsNotIn('|')
w_table_row         = w_table_cell + pp.ZeroOrMore(l_pipe + w_table_cell)
w_table             = w_table_row + pp.ZeroOrMore(l_pipe * 2 + w_table_row)

w_integer_arg       = l_bang + integer
w_floating_arg      = l_bang + floating
w_table_arg         = l_bang + w_table
w_generic_arg       = l_bang + pp.CharsNotIn('!')

w_command_start     = pp.lineStart + l_bang
w_figure_com        = l_figure + w_generic_arg + pp.Optional(w_floating_arg)
w_subquestions_com  = l_subquestions + w_integer_arg
w_table_com         = l_table + w_table_arg
w_points_com        = l_points + w_floating_arg
w_comment_com       = l_comment + w_generic_arg + pp.restOfLine
w_answer_com        = l_answer + l_bang + pp.restOfLine
w_command_line      = w_command_start + (
    w_figure_com | l_dont_randomize | w_subquestions_com | w_table_com |
    w_points_com | w_comment_com | w_answer_com
) + pp.lineEnd

w_type_start        = w_command_start + l_type + l_bang
w_mc_decl           = t_mc + pp.Optional(w_integer_arg)
w_open_decl         = t_open + w_integer_arg
w_truefalse_decl    = t_truefalse + pp.Optional(w_integer_arg)
w_type_line         = w_type_start + (
    t_whichof2 | w_mc_decl | w_open_decl | w_truefalse_decl
) + pp.lineEnd

w_empty_line         = pp.lineStart + pp.lineEnd
w_normal_line        = (
    ~w_empty_line + pp.lineStart + ~l_bang + pp.restOfLine + pp.lineEnd
)
w_drawbox_line       = w_command_start + l_drawbox + w_floating_arg + pp.lineEnd
w_answerfigure_line  = (
    w_command_start + l_answerfigure + w_generic_arg +
    pp.Optional(w_floating_arg) + pp.lineEnd
)
w_answerblock_line   = (
    w_command_start + l_answerblock + w_integer_arg * 2 + pp.lineEnd
)
w_command_line_x     = w_command_line | w_answerblock_line
w_type_line_x        = (
    w_type_line | w_answerblock_line | w_drawbox_line | w_answerfigure_line
)
w_complete_text_line = w_type_start + l_complete_text + pp.lineEnd
w_choose_line        = (
    w_command_start + l_choose + twoOrMore(w_generic_arg) + pp.lineEnd
)
w_complete_text_duet = w_normal_line + w_choose_line

w_atleast1command    = (
    pp.ZeroOrMore(w_command_line_x) + w_type_line_x +
    pp.ZeroOrMore(w_command_line_x)
)
w_atleast2commands   = w_atleast1command & w_command_line_x
w_atleast3commands   = w_atleast2commands & w_command_line_x

w_intro_block        = (
    w_normal_line + pp.Optional(w_normal_line) + pp.Optional(w_command_line)
).leaveWhitespace()
w_standard_question_block = pp.OneOrMore(w_normal_line) + (
    w_normal_line * 2 + w_atleast1command  |
    w_normal_line     + w_atleast2commands | w_atleast3commands
).leaveWhitespace()
w_complete_text_block = (
    w_complete_text_line + pp.OneOrMore(w_complete_text_duet) +
    pp.Optional(w_normal_line) + pp.ZeroOrMore(w_command_line)
).leaveWhitespace()
w_block      = w_standard_question_block | w_intro_block | w_complete_text_block

w_question_group    = (
    w_block + pp.ZeroOrMore(w_empty_line + w_block)
).ignore(pp.pythonStyleComment + pp.lineEnd)
