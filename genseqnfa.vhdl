
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
  type state_type is (s0, s1);
  signal state: state_type := s0;
begin
  match:process(clck)
  begin
    if enable='1' and clck'event and clck='1' then
      if reset/= '1' then
        case state is
          when s0 =>m <= '0';
                    if n=req then
                      state <= s1;
                    else
                      state <= s0;
                    end if;
          when s1 =>m <= '1';
                    if n/=req then
                      state <= s0;
                    end if;
        end case;
      else
        state <= s0;
        m <= '0';
      end if;
    end if;
  end process;
end architecture;
