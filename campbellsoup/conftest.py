# (c) 2017 Julian Gonggrijp

import pytest

from .parsers import *

# The examples below are based on real question files. They were
# bananafied in order to keep confidential information confidential.

REGRESSION_CASES = {'full_document_plain': (document, '''Toetsjaar: 2090
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
}), 'full_document_LW': (document, '''Auteur: Banana Banana
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
}), 'single_image_lf': (pp.ZeroOrMore(g_meta_field), '''Afbeeldingen:"6.png"
Herbruik:Nee
''', {
    'images': ['6.png'],
    'reuse': [None],
}), 'multi_image_lf': (pp.ZeroOrMore(g_meta_field), '''Afbeeldingen:"2a.png", "2b.png", "2c.png", "2d.png", "2e.png", "2f.png"
Herbruik:Nee
''', {
    'images': ['2a.png', '2b.png', '2c.png', '2d.png', '2e.png', '2f.png'],
    'reuse': [None],
}), 'escaped_quotes': (g_plaintext_field, r'''Plat:"Banana banana banana banana’banana banana banana banana. Banana banana banana banana banana banana banana Banana’banana bana¨na banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana banana. Banana banana banana banana banana banana?

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
}), 'multi_blank_structured': (w_question_group, '''Banana banana banana banana
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
}]}), 'multi_blank_raw': (w_question_group_sources, r'''Banana banana banana banana
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
]), 'type_command_ordering': (w_atleast3commands, r'''!points!3
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
})}


@pytest.fixture(
    params=REGRESSION_CASES.values(),
    ids=list(REGRESSION_CASES.keys()),
)
def regressions_fix(request):
    return request.param
