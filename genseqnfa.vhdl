
library IEEE;
use IEEE.std_logic_1164.all;

entity genseqnfa is
  generic(
    req: Character
    );
  port(
    n: in Character;
    clck, reset, enable: in std_logic;
    m: out std_logic
    );
end entity;

architecture bahavioral of genseqnfa is
begin
  match:process(clck)
  begin
    if clck'event and clck='1' then
      if reset/= '1' and enable= '1' then
        if n=req then
          m <= '1';
        else
          m <= '0';
        end if;
      else
        m <= '0';
      end if;
    end if;
  end process;
end architecture;
