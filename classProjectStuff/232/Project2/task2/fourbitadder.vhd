-- Adds two 4 bit inputs, produces 5 bit output
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all; 

entity fourbitadder is

    port (
    A, B: in UNSIGNED (3 downto 0);
    subt: in std_logic;
    answer: out UNSIGNED (4 downto 0)
    );

end fourbitadder;

architecture behavior of fourbitadder is
  signal tempA : UNSIGNED(0 downto 0);

 begin   

    answer <= ('0' & A) - ('0' & B) when subt = '1' else ('0' & A) + ('0' & B);    

end behavior;