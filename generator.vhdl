
library IEEE;
use IEEE.std_logic_1164.all;

entity generator is
  port(
    n: in Character;
    clck, reset, enable: in std_logic;
    m: out std_logic
);
end entity;

architecture behavioral of generator is
    
        signal signal_0,signal_1,signal_2,signal_3,signal_4,signal_5: std_logic;
    
begin
    signal_0 <= enable;

    
instance_1: entity work.genseqnfa
    generic map(
        req => 'e'
    )
    port map(
        clck => clck,
        reset => reset,
        enable => signal_0,
        n => n,
        m => signal_1
    );


instance_2: entity work.genseqnfa
    generic map(
        req => 't'
    )
    port map(
        clck => clck,
        reset => reset,
        enable => signal_1,
        n => n,
        m => signal_2
    );


instance_3: entity work.genseqnfa
    generic map(
        req => 'e'
    )
    port map(
        clck => clck,
        reset => reset,
        enable => signal_2,
        n => n,
        m => signal_3
    );


instance_4: entity work.genseqnfa
    generic map(
        req => 's'
    )
    port map(
        clck => clck,
        reset => reset,
        enable => signal_3,
        n => n,
        m => signal_4
    );


signal_5 <= signal_1 or signal_4;


    m <= signal_5;
end architecture;
