
ghdl -a genseqnfa.vhdl generator.vhdl genseqnfa_tb.vhdl;
ghdl -e genseqnfa_tb;
ghdl -r genseqnfa_tb --wave=wave.ghw --stop-time=500ns;
gtkwave wave.ghw  -S config.tcl
