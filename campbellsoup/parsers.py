# (c) 2017 Julian Gonggrijp

import pyparsing as pp

toetsjaar       = pp.CaselessKeyword('toetsjaar')
auteur          = pp.CaselessKeyword('auteur')
titel           = pp.CaselessKeyword('titel')
deelvragen      = pp.CaselessKeyword('deelvragen')
plat            = pp.CaselessKeyword('plat')
antwoord        = pp.CaselessKeyword('antwoord')
puntenverdeling = pp.CaselessKeyword('puntenverdeling')
afbeeldingen    = pp.CaselessKeyword('afbeeldingen')
herbruik        = pp.CaselessKeyword('herbruik')
onbekend        = pp.CaselessKeyword('onbekend')
geen            = pp.CaselessKeyword('geen')
nee             = pp.CaselessKeyword('nee')

meta_key = pp.Or([
    toetsjaar,
    auteur,
    titel,
    deelvragen,
    antwoord,
    puntenverdeling,
    afbeeldingen,
    herbruik,
])
