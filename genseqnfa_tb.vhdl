library IEEE;
use IEEE.std_logic_1164.all;

entity genseqnfa_tb is
end genseqnfa_tb;

architecture behavioral of genseqnfa_tb is
  signal clck,m, reset, enable: std_logic;
  signal n: Character;
  constant req: Character := 'n';
begin

  nfa: entity work.seqex
    port map(
      n => n,
      clck => clck,
      m => m,
      reset => reset,
      enable => enable
      );

enable <= '1';

  test: process
  begin
    reset <= '1';
    wait for 20 ns;
    reset <= '0';
    n <= 'n';
    wait for 20 ns;
    n <= 'p';
    wait for 20 ns;
    n <= 'n';
    wait for 20 ns;
  end process;

  process
  begin
    clck <= '1';
    wait for 10 ns;
    clck <= '0';
    wait for 10 ns;
  end process;

end architecture;
