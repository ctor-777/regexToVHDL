
library IEEE;
use IEEE.std_logic_1164.all;

entity seqex is
  port(
    n: in Character;
    clck, reset, enable: in std_logic;
    m: out std_logic
);
end entity;

architecture bahavioral of seqex is
  constant char_n : Character := 'n';
  constant char_p: Character := 'p';
  signal s0tos1, s1tos2: std_logic;
begin

  s0tos1_entity: entity work.genseqnfa
    generic map(
      req => char_n
      )
    port map(
      clck => clck,
      reset => reset,
      enable => enable,
      n => n,
      m => s0tos1
      );
  s1tos2_entity: entity work.genseqnfa
    generic map(
      req => char_p
      )
    port map(
      clck => clck,
      reset => reset,
      enable => s0tos1,
      n => n,
      m => s1tos2
      );
 s2tos3_entity: entity work.genseqnfa
    generic map(
      req => char_n
      )
    port map(
      clck => clck,
      reset => reset,
      enable => s1tos2,
      n => n,
      m => m
      );

 
end architecture;
