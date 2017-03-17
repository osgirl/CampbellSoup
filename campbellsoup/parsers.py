# (c) 2017 Julian Gonggrijp

import pyparsing as pp

# General

integer = (pp.Word(pp.nums)).setName('integer')
floating = (pp.Optional(integer) + '.' + integer | integer).setName('floating')
line_start = pp.lineStart.leaveWhitespace()
empty_line = (line_start + pp.lineEnd).setName('empty_line')


def twoOrMore(parserElement):
    """ returns a parser that matches `parserElement` twice or more. """
    return parserElement + pp.OneOrMore(parserElement)


# Meta keywords

m_colon           = pp.Literal(':').setName('m_colon')
m_comma           = pp.Literal(',').setName('m_comma')
m_dash            = pp.Literal('-').setName('m_dash')
m_quote           = pp.Literal('"').setName('m_quote')
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
v_year            = pp.Regex('20(0[4-9]|[1-9]\d)').setName('v_year')
                             # ^ not century-proof
v_question_number = pp.Word(pp.nums, min=1, max=2).setName('v_question_number')
v_author          = pp.CharsNotIn(',\r\n').setName('v_author')

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

w_table_row         = pp.delimitedList(
    w_table_cell,
    l_pipe,
).setName('w_table_row')

w_table             = pp.delimitedList(
    w_table_row,
    l_pipe * 2,
).setName('w_table')

w_integer_arg       = (l_bang + integer).setName('w_integer_arg')
w_floating_arg      = (l_bang + floating).setName('w_floating_arg')
w_table_arg         = (l_bang + w_table).setName('w_table_arg')
w_generic_arg       = (l_bang + pp.CharsNotIn('!\r\n')).setName('w_generic_arg')

w_command_start     = (line_start + l_bang).setName('w_command_start')

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

w_normal_line        = (
    ~empty_line + line_start + ~l_bang + pp.restOfLine + pp.lineEnd
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

w_question_group    = pp.delimitedList(w_block, empty_line).ignore(
    pp.pythonStyleComment + pp.lineEnd
).setName('w_question_group')

# Plaintext parts

p_separator   = (pp.Literal('**$$**') + pp.lineEnd).setName('p_separator')

p_block       = pp.OneOrMore(
    line_start + ~p_separator + pp.restOfLine + pp.lineEnd
).setName('p_block')

p_question_group = (
    pp.delimitedList(p_block, p_separator)
).setName('p_question_group')


def p_parse(toks):
    """ Parsing action for applying p_question_group to a nested token. """
    return p_question_group.parseString(toks[0])


# Global parts

g_null         = (v_nee | v_onbekend | v_geen).setName('g_null')
g_year_value   = (v_year | g_null).setName('g_year_value')
g_question_ref = (v_year + m_dash + v_question_number).setName('g_question_ref')
g_reuse_value  = (g_question_ref | g_null).setName('g_reuse_value')

g_authors_value = (
    g_null | pp.delimitedList(v_author, m_comma).leaveWhitespace()
).setName('g_authors_value')

g_text_value    = (
    g_null | pp.dblQuotedString | pp.restOfLine
).setName('g_text_value')

g_points_value = (g_null | integer + pp.Optional(
    pp.nestedExpr(content=pp.delimitedList(integer, ':'))
).leaveWhitespace()).setName('g_points_value')

g_images_value = (
    g_null | pp.delimitedList(pp.dblQuotedString)
).setName('g_images_value')

g_author_field  = (
    pp.lineStart + m_auteur + m_colon + g_authors_value + pp.lineEnd
).setName('g_author_field')

g_reuse_field   = (
    pp.lineStart + m_herbruik + m_colon + g_reuse_value + pp.lineEnd
).setName('g_reuse_field')

g_year_field    = (
    pp.lineStart + m_toetsjaar + m_colon + g_year_value + pp.lineEnd
).setName('g_year_field')

g_title_field   = (
    pp.lineStart + m_titel + m_colon + g_text_value + pp.lineEnd
).setName('g_title_field')

g_questions_field = (
    pp.lineStart + m_deelvragen + m_colon + integer + pp.lineEnd
).setName('g_questions_field')

g_answer_field = (
    pp.lineStart + m_antwoord + m_colon + g_text_value + pp.lineEnd
).setName('g_answer_field')

g_points_field = (
    pp.lineStart + m_puntenverdeling + m_colon + g_points_value + pp.lineEnd
).setName('g_points_field')

g_images_field = (
    pp.lineStart + m_afbeeldingen + m_colon + g_images_value + pp.lineEnd
).setName('g_images_field')

g_meta_field    = (
    g_author_field | g_reuse_field | g_year_field | g_title_field |
    g_questions_field | g_answer_field | g_points_field | g_images_field
).setName('g_meta_field')

g_plaintext_field = (
    pp.lineStart + m_plat + m_colon +
    pp.QuotedString('"', multiline=True).setParseAction(p_parse) + pp.lineEnd
).setName('g_plaintext_field')

# Full document parsing

latex_writer_header   = (
    g_author_field & g_reuse_field
).setName('latex_writer_header')

latex_writer_document = (
    latex_writer_header + w_question_group
).setName('latex_writer_document')

plaintext_document = (
    pp.OneOrMore(g_meta_field) + g_plaintext_field + pp.ZeroOrMore(g_meta_field)
).setName('plaintext_document')

document = (latex_writer_document | plaintext_document).setName('document')


def debug_all():
    """ Helper function for the developer: call .setDebug() on all parsers. """
    import sys
    this_module = sys.modules[__name__]
    for name in dir(this_module):
        candidate = getattr(this_module, name)
        if isinstance(candidate, pp.ParserElement):
            candidate.setDebug()
