library IEEE;
use IEEE.std_logic_1164.all;

entity genseqnfa_tb is
end genseqnfa_tb;

architecture behavioral of genseqnfa_tb is
  signal clck,m, enable: std_logic;
  signal n: Character;
  constant req: Character := 'n';
begin

  nfa: entity work.genseqnfa
    generic map(
      req => req
      )
    port map(
      n => n,
      clck => clck,
      m => m,
      enable => enable
      );

  enable <= '1';

  process
  begin
    clck <= '1';
    wait for 20 ns;
    clck <= '0';
    wait for 20 ns;
  end process;

  process
  begin
    n <= 'n';
    wait for 40 ns;
    n <= 'p';
    wait for 40 ns;
  end process;


end architecture;
