library IEEE;
use IEEE.std_logic_1164.all;

entity genseqnfa_tb is
end genseqnfa_tb;

architecture behavioral of genseqnfa_tb is
  signal clck,m, reset, enable: std_logic;
  signal n: Character;
  constant req: Character := 'n';
  constant T: time := 20 ns;
  constant tested: String := "test";
begin

  nfa: entity work.generator
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
    wait for T;
    reset <= '0';
    for i in 0 to 3 loop
      n <= tested(i+1);
      wait for T;
    end loop;
  end process;

  process
  begin
    clck <= '1';
    wait for T/2;
    clck <= '0';
    wait for T/2;
  end process;

end architecture;
