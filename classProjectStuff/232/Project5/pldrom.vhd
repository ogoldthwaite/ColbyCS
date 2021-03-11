-- Owen Goldthwaite
-- CS232

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity pldrom is
  port 
  (
    addr  : in std_logic_vector (3 downto 0);
    data  : out std_logic_vector (9 downto 0)
  );

end entity;

architecture rtl of pldrom is
  -- definitions go here

begin
-- Given Test 1
--   data <= 
--     "0001100000" when addr = "0000" else -- move 0s to LR   00000000/00000000
--     "0001110000" when addr = "0001" else -- move 1s to LR   11111111/00000000
--     "0001101010" when addr = "0010" else -- move 1010 to LR 11111010/00000000
--     "0010101000" when addr = "0011" else -- move 8 to ACC   11111010/00001000
--     "0101001100" when addr = "0100" else -- shift LR left   
--     "0100011000" when addr = "0101" else -- add -1 to ACC  
--     "1100001000" when addr = "0110" else -- branch if  zero  
--     "1000000100" when addr = "0111" else -- branch  
--     "0001110000" when addr = "1000" else -- set LR to 1s    11111111/00000000
--     "1000000000" when addr = "1001" else -- branch to zero  11111111/00000000
--     "0101010101" when addr = "1010" else -- garbage
--     "1010101010" when addr = "1011" else -- garbage
--     "1100110011" when addr = "1100" else -- garbage
--     "0011001100" when addr = "1101" else -- garbage
--     "0000000000" when addr = "1110" else -- garbage
--     "1111111111";                        -- garbage

-- -- Given Test 2, operator test
-- data <= 
-- "0001110000" when addr = "0000" else -- move 11111111 to the LR    
-- "0011100000" when addr = "0001" else -- move 0000 from the IR to the high 4 bits of the ACC
-- "0010100010" when addr = "0010" else -- move 0010 from the IR to the low 4 bits of the ACC
-- "0100000100" when addr = "0011" else -- Add ACC to LR and put it back into the LR
-- "0100000100" when addr = "0100" else -- Add ACC to LR and put it back into the LR
-- "0100100100" when addr = "0101" else -- Subtract ACC from LR and put it back into the LR
-- "0101001100" when addr = "0110" else -- Shift the LR left and write it back to the LR
-- "0101101100" when addr = "0111" else -- Shift the LR right and write it back to the LR
-- "0111101100" when addr = "1000" else -- Rotate the LR right and write it back to the LR
-- "0101101100" when addr = "1001" else -- Shift the LR right and write it back to the LR
-- "0110011100" when addr = "1010" else -- XOR the LR with all 1s and write it back to the LR (bit inversion)
-- "0110110101" when addr = "1011" else -- AND the LR with 01 (sign-extended)
-- "0100010110" when addr = "1100" else -- ADD the LR with 10 (sign-extended)
-- "1111111111";                        -- garbage

-- Third instruction set, counting down and flash thing
-- data <= 
-- "0011100001" when addr = "0000" else -- ACC gets 0001 in 4 high bits 00000000 / 00010000
-- "0001000000" when addr = "0001" else -- LR gets ACC value            00010000 / 00010000
-- "0011100000" when addr = "0010" else -- ACC high bits get 0000       00010000 / 00000000
-- "0010100001" when addr = "0011" else -- ACC low bits get 0001        00010000 / 00000001
-- "0100100100" when addr = "0100" else -- LR gets LR - ACC (ACC = 1)   00001111 / 00000001
-- "1110000111" when addr = "0101" else -- Branch to 0111 if LR is 0, break from loop
-- "1000000100" when addr = "0110" else -- Branch to 0100 to continue loop 
-- "0010100001" when addr = "0111" else -- ACC low bits get 0001        00000000 / 00000001
-- "0001110000" when addr = "1000" else -- Set LR to all 1s             11111111 / 00000001
-- "0001100000" when addr = "1001" else -- Set LR to all 0s             00000000 / 00000001
-- "0101000000" when addr = "1010" else -- Shift ACC left by one bit    00000000 / 00000010
-- "1100001101" when addr = "1011" else -- Branch to 1101 if ACC is 0, break from loop
-- "1000001000" when addr = "1100" else -- Branch to 1000 to continue loop 
-- "1000000000" when addr = "1101" else -- Branch to 0000 to restart 
-- "1111111111";                        -- TRASH

-- -- Fourth cucstom instruction set
data <= 
"0010100001" when addr = "0000" else -- ACC gets 0001 in 4 low  bits 00000000 / 00000001
"0100000100" when addr = "0001" else -- LR gets LR + ACC             00000001 / 00000001
"1111000100" when addr = "0010" else -- Branch to 0100 if LR = 8, break from loop
"1000000001" when addr = "0011" else -- Branch to 0001, loop               
"0001110000" when addr = "0100" else -- LR gets all 1s               11111111 / 00000001
"0101101100" when addr = "0101" else -- Shift LR right by one bit    01111111 / 00000001
"0101101100" when addr = "0110" else -- Shift LR right by one bit    00111111 / 00000001
"0101101100" when addr = "0111" else -- Shift LR right by one bit    00011111 / 00000001
"0100100100" when addr = "1000" else -- LR gets LR - ACC (ACC = 1)   11111110 / 00000001
"1111001011" when addr = "1001" else -- Branch to 1011 if LR = 8, break from loop
"1000001000" when addr = "1010" else -- Branch to 1000, loop  
"0001100000" when addr = "1011" else -- Set LR to all 0s             00000000 / 00000001
"1000000000" when addr = "1100" else -- Branch to 0000 to restart 
"1111111111";                        -- TRASH






end rtl;
