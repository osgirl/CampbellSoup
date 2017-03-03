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
l_figure          = pp.Keyword('figure')
l_answerfigure    = pp.Keyword('answerfigure')
l_comment         = pp.Keyword('comment')
l_points          = pp.Keyword('points')
l_type            = pp.Keyword('type')
l_complete_text   = pp.Keyword('complete_text')
l_answerblock     = pp.Keyword('answerblock')
l_dont_randomize  = pp.Keyword('dont_randomize')
l_subquestions    = pp.Keyword('subquestions')
l_answerblock     = pp.Keyword('answerblock')
l_choose          = pp.Keyword('choose')
l_drawbox         = pp.Keyword('drawbox')

# LaTeX-writer type values
t_whichof2        = pp.Keyword('whichof2')
t_complete_text   = pp.Keyword('complete_text')
t_mc              = pp.Keyword('mc')
t_open            = pp.Keyword('open')
t_truefalse       = pp.Keyword('truefalse') | pp.Keyword('plusmin')

# LaTeX-writer parts
w_command_start    = pp.lineStart + bang
w_integer_arg      = bang + integer
w_floating_arg     = bang + floating
w_generic_arg      = bang + pp.CharsNotIn('!')
w_figure_com       = figure + generic_arg + pp.Optional(floating_arg)
w_subquestions_com = subquestions + integer_arg
w_command_line     = command_start + (
    figure_com | dont_randomize | subquestions_com
) + pp.lineEnd

w_type_start       = command_start + type + bang
w_mc_decl          = mc + pp.Optional(integer_arg)
w_open_declaration = open + integer_arg
w_truefalse_decl   = truefalse + pp.Optional(integer_arg)
w_type_line        = type_start + (
    whichof2 | mc_decl | open_decl | truefalse_decl
) + pp.lineEnd

w_normal_line       = pp.lineStart + ~bang + pp.restOfLine + pp.lineEnd
w_empty_line        = pp.lineStart + pp.lineEnd
w_drawbox_line      = command_start + drawbox + floating_arg + pp.lineEnd
w_answerblock_line  = command_start + answerblock + integer_arg * 2 + pp.lineEnd
w_command_line_x    = command_line | answerblock_line
w_type_line_x       = type_line | answerblock_line | drawbox_line
w_complete_text_line = type_start + complete_text + pp.lineEnd
w_choose_line     = command_start + choose + twoOrMore(generic_arg) + pp.lineEnd
w_complete_text_duet = normal_line + choose_line

w_atleast1command  = (
    pp.ZeroOrMore(command_line_x) + type_line_x + pp.ZeroOrMore(command_line_x)
)
w_atleast2commands = atleast1command & command_line_x
w_atleast3commands = atleast2commands & command_line_x

w_intro_block = (
    normal_line + pp.Optional(normal_line) + pp.Optional(figure_command)
).leaveWhitespace()
w_standard_question_block = pp.OneOrMore(normal_line) + (
    normal_line * 2 + atleast1command  |
    normal_line     + atleast2commands | atleast3commands
).leaveWhitespace()
w_complete_text_block = (
    complete_text_line + pp.OneOrMore(complete_text_duet) +
    pp.Optional(normal_line) + pp.ZeroOrMore(command_line)
).leaveWhitespace()
w_block = intro_block | standard_question_block | complete_text_block

w_question_group = (
    block + pp.ZeroOrMore(empty_line + block)
).ignore(pp.pythonStyleComment + pp.lineEnd)
