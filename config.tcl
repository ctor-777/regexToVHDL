
set signals [list]
lappend signals "top.genseqnfa_tb.clck"
lappend signals "top.genseqnfa_tb.enable"
lappend signals "top.genseqnfa_tb.reset"
lappend signals "top.genseqnfa_tb.n"
lappend signals "top.genseqnfa_tb.m"

set added_signals [ gtkwave::addSignalsFromList $signals ]

gtkwave::/Time/Zoom/Zoom_Full
