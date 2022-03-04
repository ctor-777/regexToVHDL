

library IEEE;
use IEEE.std_logic_1164.all;

entity altex is
  port(
    n: in Character;
    clck, reset, enable: in std_logic;
    m: out std_logic
);
end entity;

architecture behavioral of altex is
  constant char1 : Character := 'n';
  constant char2 : Character := 'p';
  signal inter_1, inter_2: std_logic;
begin

  alt1_1: entity work.genseqnfa
    generic map(
      req => char1
      )
    port map(
      clck => clck,
      reset => reset,
      enable => enable,
      n => n,
      m => inter_1
      );

  alt1_2: entity work.genseqnfa
    generic map(
      req => char2
      )
    port map(
      clck => clck,
      reset => reset,
      enable => enable,
      n => n,
      m => inter_2
      );

  m <= inter_1 or inter_2;
end architecture;
