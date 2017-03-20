# (c) 2017 Julian Gonggrijp

from .parsers import document


def test_document():
    for example, result in TEST_DOCUMENTS:
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
