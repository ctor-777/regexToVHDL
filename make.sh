
ghdl -a genseqnfa.vhdl quanex.vhdl genseqnfa_tb.vhdl;
ghdl -e genseqnfa_tb;
ghdl -r genseqnfa_tb --wave=wave.ghw --stop-time=1us;
