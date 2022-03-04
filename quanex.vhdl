

library IEEE;
use IEEE.std_logic_1164.all;

entity quanex is
  port(
    n: in Character;
    clck, reset, enable: in std_logic;
    m: out std_logic
);
end entity;

architecture behavioral of quanex is
  constant char1: Character := 'n';
  signal inter_1, inter_2: std_logic;
begin

  inter_1 <= enable or inter_2;
  m <= inter_2;
  quan1_1: entity work.genseqnfa
    generic map(
      req => char1
      )
    port map(
      clck => clck,
      reset => reset,
      enable => inter_1,
      n => n,
      m => inter_2
      );
end architecture;
