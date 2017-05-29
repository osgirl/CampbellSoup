# (c) 2017 Julian Gonggrijp

import pyparsing as pp

# General

def to_int(toks):
    """ Parser action for converting strings of digits to int. """
    return int(toks[0])

integer    = pp.Word(pp.nums).setName('integer').setParseAction(to_int)

floating  = pp.Combine(
    pp.Optional(integer) + '.' + integer | integer
).setName('floating').setParseAction(lambda toks: float(toks[0]))

line_start = pp.lineStart.leaveWhitespace()
line_end   = pp.lineEnd.suppress()
empty_line = (line_start + pp.lineEnd).setName('empty_line')


def twoOrMore(parserElement):
    """ returns a parser that matches `parserElement` twice or more. """
    return parserElement + pp.OneOrMore(parserElement)


# Meta keywords

m_colon           = pp.Literal(':').setName('m_colon').suppress()
m_comma           = pp.Literal(',').setName('m_comma').suppress()
m_dash            = pp.Literal('-').setName('m_dash').suppress()
m_quote           = pp.Literal('"').setName('m_quote').suppress()
m_titel           = (pp.CaselessKeyword('titel')).setName('m_titel').suppress()
m_plat            = (pp.CaselessKeyword('plat')).setName('m_plat').suppress()

m_toetsjaar       = (
    pp.CaselessKeyword('toetsjaar')
).setName('m_toetsjaar').suppress()

m_auteur          = (
    pp.CaselessKeyword('auteur')
).setName('m_auteur').suppress()

m_deelvragen      = (
    pp.CaselessKeyword('deelvragen')
).setName('m_deelvragen').suppress()

m_antwoord        = (
    pp.CaselessKeyword('antwoord')
).setName('m_antwoord').suppress()

m_herbruik        = (
    pp.CaselessKeyword('herbruik')
).setName('m_herbruik').suppress()

m_puntenverdeling = (
    pp.CaselessKeyword('puntenverdeling')
).setName('m_puntenverdeling').suppress()

m_afbeeldingen    = (
    pp.CaselessKeyword('afbeeldingen')
).setName('m_afbeeldingen').suppress()

# Meta values

v_onbekend        = (
    pp.CaselessKeyword('onbekend')
).setName('v_onbekend').suppress()

v_geen            = (pp.CaselessKeyword('geen')).setName('v_geen').suppress()
v_nee             = (pp.CaselessKeyword('nee')).setName('v_nee').suppress()

v_year            = pp.Regex(
    '20(0[4-9]|[1-9]\d)',  # not century-proof
).setName('v_year').setParseAction(to_int)

v_question_number = pp.Word(
    pp.nums,
    min=1,
    max=2,
).setName('v_question_number').setParseAction(to_int)

v_author          = pp.CharsNotIn(',\r\n').setName('v_author')

# LaTeX-writer keywords

l_bang            = (pp.Literal('!')).setName('l_bang').suppress()
l_pipe            = (pp.Literal('|')).setName('l_pipe').suppress()
l_figure          = (pp.Keyword('figure')).setName('l_figure').suppress()
l_answer          = (pp.Keyword('answer')).setName('l_answer').suppress()
l_comment         = (pp.Keyword('comment')).setName('l_comment').suppress()
l_points          = (pp.Keyword('points')).setName('l_points').suppress()
l_type            = (pp.Keyword('type')).setName('l_type').suppress()
l_choose          = (pp.Keyword('choose')).setName('l_choose').suppress()
l_drawbox         = (pp.Keyword('drawbox')).setName('l_drawbox').suppress()
l_table           = (pp.Keyword('table')).setName('l_table').suppress()

l_answerfigure    = (
    pp.Keyword('answerfigure')
).setName('l_answerfigure').suppress()

l_complete_text   = (
    pp.Keyword('complete_text')
).setName('l_complete_text').suppress()

l_dont_randomize  = (
    pp.Keyword('dont_randomize')
).setName('l_dont_randomize').suppress()

l_subquestions    = (
    pp.Keyword('subquestions')
).setName('l_subquestions').suppress()

l_answerblock     = (
    pp.Keyword('answerblock')
).setName('l_answerblock').suppress()

# LaTeX-writer type values

t_whichof2        = (pp.Keyword('whichof2')).setName('t_whichof2')
t_mc              = (pp.Keyword('mc')).setName('t_mc')
t_open            = (pp.Keyword('open')).setName('t_open')

t_truefalse       = (
    pp.Keyword('truefalse') | pp.Keyword('plusmin')
).setName('t_truefalse').setParseAction(pp.replaceWith('truefalse'))

# LaTeX-writer parts

w_table_cell        = (pp.CharsNotIn('|\n\r')).setName('w_table_cell')

w_table_row         = pp.Group(pp.delimitedList(
    w_table_cell,
    l_pipe,
)).setName('w_table_row')

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
).setName('w_figure_com').setResultsName('figure')

w_subquestions_com  = (
    l_subquestions + w_integer_arg
).setName('w_subquestions_com').setResultsName('subquestions')

w_table_com         = (
    l_table + w_table_arg
).setName('w_table_com').setResultsName('table')

w_points_com        = (
    l_points + w_floating_arg
).setName('w_points_com').setResultsName('points')

w_comment_com       = (
    l_comment + w_generic_arg + l_bang + pp.restOfLine
).setName('w_comment_com').setResultsName('comments', True)

w_answer_com        = (
    l_answer + l_bang + pp.restOfLine
).setName('w_answer_com').setResultsName('answer')

w_command_line      = (w_command_start + (
    l_dont_randomize.copy().setParseAction(
        pp.replaceWith(True),
    ).setResultsName('dontRandomize') |
    w_figure_com | w_subquestions_com | w_table_com |
    w_points_com | w_comment_com | w_answer_com
) + line_end).setName('w_command_line')

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
) + line_end).setName('w_type_line').setResultsName('type')

w_normal_line        = pp.Combine(
    ~empty_line + line_start + ~l_bang + pp.restOfLine + line_end
).setName('w_normal_line')

w_drawbox_line       = (
    w_command_start + l_drawbox + w_floating_arg + line_end
).setName('w_drawbox_line').setResultsName('drawbox')

w_answerfigure_line  = (
    w_command_start + l_answerfigure + w_generic_arg +
    pp.Optional(w_floating_arg) + line_end
).setName('w_answerfigure_line').setResultsName('answerfigure')

w_answerblock_line   = (
    w_command_start + l_answerblock + w_integer_arg * 2 + line_end
).setName('w_answerblock_line').setResultsName('answerblock')

w_command_line_x     = (
    w_command_line | w_answerblock_line
).setName('w_command_line_x')

w_type_line_x        = (
    w_type_line | w_answerblock_line | w_drawbox_line | w_answerfigure_line
).setName('w_type_line_x')

w_complete_text_line = (
    w_type_start + l_complete_text + line_end
).setName('w_complete_text_line').setResultsName('complete_text')

w_choose_line        = pp.Group(
    w_command_start + l_choose + twoOrMore(w_generic_arg) + line_end
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
    w_normal_line.setResultsName('title') +
    pp.Optional(w_normal_line.setResultsName('intro')) +
    pp.Optional(w_command_line)
).leaveWhitespace().setName('w_intro_block')

w_standard_question_block = (
    pp.originalTextFor(
        w_normal_line
    ).setResultsName('question') + w_atleast3commands |
    pp.originalTextFor(
        w_normal_line * 2
    ).setResultsName('question') + w_atleast2commands |
    pp.originalTextFor(
        w_normal_line + twoOrMore(w_normal_line)
    ).setResultsName('question') + w_atleast1command
).leaveWhitespace().setName('w_standard_question_block')

w_complete_text_block = (
    w_complete_text_line + (
        pp.OneOrMore(w_complete_text_duet) +
        pp.Optional(w_normal_line)
    ).setResultsName('question') + pp.ZeroOrMore(w_command_line)
).leaveWhitespace().setName('w_complete_text_block')

w_block      = pp.Group(
    w_standard_question_block | w_intro_block | w_complete_text_block
).setName('w_block')

w_question_group    = pp.Group(pp.delimitedList(
    w_block, empty_line.suppress()
).ignore(
    pp.pythonStyleComment + pp.lineEnd
)).setName('w_question_group').setResultsName('contentLW')

w_question_group_sources = pp.delimitedList(
    pp.originalTextFor(w_block.copy().ignore(
        pp.pythonStyleComment + pp.lineEnd,
    )),
    empty_line.copy().ignore(pp.pythonStyleComment + pp.lineEnd).suppress(),
).setName('w_question_group_sources')

# Plaintext parts

p_separator   = (
    pp.Literal('**$$**').leaveWhitespace() + pp.lineEnd
).suppress().setName('p_separator')

p_block       = pp.originalTextFor(pp.OneOrMore(
    line_start + ~p_separator + pp.restOfLine + pp.lineEnd
)).setName('p_block')

p_question_group = pp.Group(
    pp.delimitedList(p_block, p_separator)
).setName('p_question_group').setResultsName('contentPlain')


def p_parse(toks):
    """ Parsing action for applying p_question_group to a nested token. """
    return p_question_group.parseString(toks[0])


# Global parts

g_null         = (
    v_nee | v_onbekend | v_geen
).setName('g_null').setParseAction(pp.replaceWith(None))

g_year_value   = (v_year | g_null).setName('g_year_value')
g_question_ref = (v_year + m_dash + v_question_number).setName('g_question_ref')
g_reuse_value  = (g_question_ref | g_null).setName('g_reuse_value')

g_authors_value = (
    g_null | pp.delimitedList(v_author, m_comma).leaveWhitespace()
).setName('g_authors_value')

g_text_value    = (
    g_null | pp.dblQuotedString.setParseAction(pp.removeQuotes) | pp.restOfLine
).setName('g_text_value')

g_points_value = (g_null | integer + pp.Optional(
    pp.nestedExpr(content=pp.delimitedList(integer, ':'))
).leaveWhitespace()).setName('g_points_value')

g_images_value = (g_null | pp.delimitedList(
    pp.dblQuotedString.setParseAction(pp.removeQuotes),
    pp.Regex(r', ?'),
).leaveWhitespace()).setName('g_images_value')

g_author_field  = (
    pp.lineStart + m_auteur + m_colon + g_authors_value + line_end
).setName('g_author_field').setResultsName('authors')

g_reuse_field   = (
    pp.lineStart + m_herbruik + m_colon + g_reuse_value + line_end
).setName('g_reuse_field').setResultsName('reuse')

g_year_field    = (
    pp.lineStart + m_toetsjaar + m_colon + g_year_value + line_end
).setName('g_year_field').setResultsName('year')

g_title_field   = (
    pp.lineStart + m_titel + m_colon + g_text_value + line_end
).setName('g_title_field').setResultsName('title')

g_questions_field = (
    pp.lineStart + m_deelvragen + m_colon + integer + line_end
).setName('g_questions_field').setResultsName('questionCount')

g_answer_field = (
    pp.lineStart + m_antwoord + m_colon + g_text_value + line_end
).setName('g_answer_field').setResultsName('answer')

g_points_field = (
    pp.lineStart + m_puntenverdeling + m_colon + g_points_value + line_end
).setName('g_points_field').setResultsName('points')

g_images_field = (
    pp.lineStart + m_afbeeldingen + m_colon + g_images_value + line_end
).setName('g_images_field').setResultsName('images')

g_meta_field    = (
    g_author_field | g_reuse_field | g_year_field | g_title_field |
    g_questions_field | g_answer_field | g_points_field | g_images_field
).setName('g_meta_field')

g_plaintext_field = (
    pp.lineStart + m_plat + m_colon +
    pp.QuotedString('"', multiline=True).setParseAction(p_parse) + line_end
).setName('g_plaintext_field')

# Full document parsing

latex_writer_header   = (
    g_author_field & g_reuse_field
).setName('latex_writer_header')

latex_writer_document = (
    latex_writer_header + w_question_group
).setName('latex_writer_document')

latex_writer_sources = (
    latex_writer_header.copy().suppress() + w_question_group_sources
).setName('latex_writer_sources')

plaintext_document = (
    pp.OneOrMore(g_meta_field) + g_plaintext_field + pp.ZeroOrMore(g_meta_field)
).setName('plaintext_document')

document = (latex_writer_document | plaintext_document).setName('document')

# File names

# Parses the proper name only, use os.path.splitext to remove the extension.
filename_parts = (
    pp.Optional(v_year + '-').suppress() +
    integer + pp.Optional(
        pp.Word(pp.alphas, exact=1) | pp.Literal('-').suppress() + integer
    )
).setName('filename_parts')


def debug_all():
    """ Helper function for the developer: call .setDebug() on all parsers. """
    import sys
    this_module = sys.modules[__name__]
    for name in dir(this_module):
        candidate = getattr(this_module, name)
        if isinstance(candidate, pp.ParserElement):
            candidate.setDebug()
