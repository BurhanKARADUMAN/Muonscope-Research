* LM358 macromodel provided by the user; original Schmitt and AND models unchanged.
.include LM358.lib
.include SN74LVC2G17.cir
.include SN74LVC1G08.cir

* Original approximate diode cards.
.model BAS70_REVU D(IS=2e-8 N=1.07 RS=5 CJO=1.5p M=0.33 TT=0.1n BV=70 IBV=1u)
.model BAT54_APPROX D(IS=2e-7 N=1.08 RS=4 CJO=8p M=0.35 TT=0.1n BV=30 IBV=5u)
