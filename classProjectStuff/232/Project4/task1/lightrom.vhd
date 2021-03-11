-- Owen Goldthwaite
-- CS232

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity lightrom is
  port 
  (
    addr  : in std_logic_vector (4 downto 0);
    data  : out std_logic_vector (3 downto 0)
  );

end entity;

architecture rtl of lightrom is
  -- definitions go here

begin

    -- Given instructions
    -- data <= 
    -- "0000" when addr = "00000" else -- move 0s to LR  00000000
    -- "0101" when addr = "00001" else -- bit invert LR  11111111
    -- "0101" when addr = "00010" else -- bit invert LR  00000000
    -- "0101" when addr = "00011" else -- bit invert LR  11111111
    -- "0001" when addr = "00100" else -- shift LR right 01111111
    -- "0001" when addr = "00101" else -- shift LR right 00111111
    -- "0111" when addr = "00110" else -- rotate LR left 01111110
    -- "0111" when addr = "00111" else -- rotate LR left 11111100
    -- "0111" when addr = "01000" else -- rotate LR left 11111001
    -- "0111" when addr = "01001" else -- rotate LR left 11110011
    -- "0010" when addr = "01010" else -- shift LR left  11100110
    -- "0010" when addr = "01011" else -- shift LR left  11001100
    -- "0011" when addr = "01100" else -- add 1 to LR    11001101
    -- "0100" when addr = "01101" else -- sub 1 from LR  11001100
    -- "0101" when addr = "01110" else -- bit invert LR  00110011
    -- "0011";                        -- add 1 to LR    0011010

    -- Custom instructions 1
    -- data <= 
    -- "0000" when addr = "00000" else -- move 0s to LR  00000000
    -- "0011" when addr = "00001" else -- add 1          00000001        
    -- "0111" when addr = "00010" else -- rotate left    00000010
    -- "0111" when addr = "00011" else -- rotate left    00000100
    -- "0111" when addr = "00100" else -- rotate left    00001000
    -- "0111" when addr = "00101" else -- rotate left    00010000
    -- "0111" when addr = "00110" else -- rotate LR left 00100000
    -- "0111" when addr = "00111" else -- rotate LR left 01000000
    -- "0111" when addr = "01000" else -- rotate LR left 10000000
    -- "0101" when addr = "01001" else -- invert bits    01111111
    -- "0001" when addr = "01010" else -- shift LR right 00111111
    -- "0001" when addr = "01011" else -- shift LR right 00011111
    -- "0001" when addr = "01100" else -- shift LR right 00001111
    -- "0101" when addr = "01101" else -- invert         11110000
    -- "0101" when addr = "01110" else -- bit invert LR  00001111
    -- "0000"; 

    -- Custom Instructions 2
    -- data <= 
    -- "0000" when addr = "00000" else -- move 0s to LR  00000000
    -- "0011" when addr = "00001" else -- add 1          00000001        
    -- "0011" when addr = "00010" else -- add 1          00000010
    -- "0011" when addr = "00011" else -- add 1          00000011
    -- "0011" when addr = "00100" else -- add 1          00000100
    -- "0101" when addr = "00101" else -- invert         11111011
    -- "0111" when addr = "00110" else -- rotate LR left 11110111
    -- "0100" when addr = "00111" else -- subtract 1     11110110
    -- "0101" when addr = "01000" else -- invert         00001001
    -- "0111" when addr = "01001" else -- shift left     00010010
    -- "0111" when addr = "01010" else -- shift LR left  00100100
    -- "0101" when addr = "01011" else -- invert         11011011
    -- "0101" when addr = "01100" else -- invert         00100100
    -- "0101" when addr = "01101" else -- invert         11011011
    -- "0101" when addr = "01110" else -- bit invert LR  00100100
    -- "0000"; 

    -- Custom Instructions 3 EXTENDED
    data <= 
    "0000" when addr = "00000" else -- move 0s to LR  00000000
    "0011" when addr = "00001" else -- add 1          00000001        
    "0111" when addr = "00010" else -- rotate left    00000010
    "0111" when addr = "00011" else -- rotate left    00000100
    "0111" when addr = "00100" else -- rotate left    00001000
    "0111" when addr = "00101" else -- rotate left    00010000
    "0111" when addr = "00110" else -- rotate LR left 00100000
    "0111" when addr = "00111" else -- rotate LR left 01000000
    "0111" when addr = "01000" else -- rotate LR left 10000000
    "0101" when addr = "01001" else -- invert bits    01111111
    "0001" when addr = "01010" else -- shift LR right 00111111
    "0001" when addr = "01011" else -- shift LR right 00011111
    "0001" when addr = "01100" else -- shift LR right 00001111
    "0101" when addr = "01101" else -- invert         11110000
    "0101" when addr = "01110" else -- bit invert LR  00001111
    "1101" when addr = "01111" else -- load alternate 10101010
    "0011" when addr = "10000" else -- add 1          10101011
    "1111" when addr = "10001" else -- rotate left 2  10101110
    "1111" when addr = "10010" else -- rotate left 2  10111010
    "1111" when addr = "10011" else -- rotate left 2  11101010
    "1000" when addr = "10100" else -- load full      11111111
    "1001" when addr = "10101" else -- shift right 2  00111111
    "1001" when addr = "10110" else -- shift right 2  00001111
    "1001" when addr = "10111" else -- shift right 2  00000011
    "0101" when addr = "11000" else -- invert         11111100
    "1100" when addr = "11001" else -- sub 2          11111010
    "1100" when addr = "11010" else -- sub 2          11111000
    "1100" when addr = "11011" else -- sub 2          11011000
    "1010" when addr = "11100" else -- shift left 2   11011000
    "1010" when addr = "11101" else -- shift left 2   01100000
    "0011" when addr = "11110" else -- add 1          10000001
    "0101"; 


end rtl;
