-- Owen Goldthwaite
-- CS 232 Spring 2020
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- The alu circuit implements the specified operation on alu_srcA and alu_srcB, putting
-- the result in dest and setting the appropriate condition flags.

-- The opcode meanings are shown in the case statement below

-- condition outputs
-- cr(0) <= '1' if the result of the operation is 0
-- cr(1) <= '1' if there is a 2's complement overflow
-- cr(2) <= '1' if the result of the operation is negative
-- cr(3) <= '1' if the operation generated a carry of '1'

-- Note that the and/or/xor operations are defined on std_logic_vectors, so you
-- may have to convert the alu_srcA and alu_srcB signals to std_logic_vectors, execute
-- the operation, and then convert the result back to an unsigned.  You can do
-- this all within a single expression.


entity alu is
  
  port (
    alu_srcA : in  unsigned(15 downto 0);         -- input A
    alu_srcB : in  unsigned(15 downto 0);         -- input B
    op   : in  std_logic_vector(2 downto 0);  -- operation
    cr   : out std_logic_vector(3 downto 0);  -- condition outputs
    dest : out unsigned(15 downto 0));        -- output value

end alu;

architecture test of alu is

  -- The signal tdest is an intermediate signal to hold the result and
  -- catch the carry bit in location 16.
  signal tdest : unsigned(16 downto 0);  
  
  -- Note that you should always put the carry bit into index 16, even if the
  -- carry is shifted out the right side of the number (into position -1) in
  -- the case of a shift or rotate operation.  This makes it easy to set the
  -- condition flag in the case of a carry out.

begin  -- test
  process (alu_srcA, alu_srcB, op)
  begin  -- process
    case op is
      when "000" =>        -- addition     tdest = alu_srcA + alu_srcB
        tdest <= ('0' & alu_srcA) + ('0' & alu_srcB);
      when "001" =>        -- subtraction  tdest = alu_srcA - alu_srcB
        tdest <= ('0' & alu_srcA) - ('0' & alu_srcB);
      when "010" =>        -- and          tdest = alu_srcA and alu_srcB
        tdest(15 downto 0) <= unsigned(std_logic_vector(alu_srcA) and std_logic_vector(alu_srcB));
        tdest(16) <= '0';
      when "011" =>        -- or           tdest = alu_srcA or alu_srcB
        tdest(15 downto 0) <= unsigned(std_logic_vector(alu_srcA) or std_logic_vector(alu_srcB));
        tdest(16) <= '0';
      when "100" =>        -- xor          tdest = alu_srcA xor alu_srcB
        tdest(15 downto 0) <= unsigned(std_logic_vector(alu_srcA) xor std_logic_vector(alu_srcB));
        tdest(16) <= '0';
      when "101" =>        -- shift        tdest = alu_srcA shifted left arithmetic by one if alu_srcB(0) is 0, otherwise right
        if(alu_srcB(0) = '0') then
            tdest(15 downto 0) <= unsigned(shift_left(signed(alu_srcA),1));

            if(alu_srcA(15) = '1') then -- Checking for carry
                tdest(16) <= '1';
            else
                tdest(16) <= '0';
            end if;
        else
            tdest(15 downto 0) <= unsigned(shift_right(signed(alu_srcA),1));

            if(alu_srcA(0) = '1') then -- Checking for carry
                tdest(16) <= '1';
            else
                tdest(16) <= '0';
            end if;
        end if;
      when "110" =>        -- rotate       tdest = alu_srcA rotated left by one if alu_srcB(0) is 0, otherwise right
        if(alu_srcB(0) = '0') then
          tdest(15 downto 0) <= rotate_left(alu_srcA,1);

            if(alu_srcA(15) = '1') then -- Checking for carry
                tdest(16) <= '1';
            else
                tdest(16) <= '0';
            end if;
        else
          tdest(15 downto 0) <= rotate_right(alu_srcA,1);

            if(alu_srcA(0) = '1') then -- Checking for carry
                tdest(16) <= '1';
            else
                tdest(16) <= '0';
            end if;
        end if;
      when "111" =>        -- pass         tdest = alu_srcA
        tdest(15 downto 0) <= alu_srcA;
      when others =>
        null;
    end case;
  end process;

  -- connect the low 16 bits of tdest to dest here
  dest <= tdest(15 downto 0);

  -- If result is 0
  cr(0) <= '1' when tdest(15 downto 0) = "0000000000000000" else '0';

  -- Addition and subtraction overflow
  cr(1) <= '1' when (op = "000" and (alu_srcA(15) = alu_srcB(15)) and (alu_srcA(15) /= tdest(15))) or 
                  ( op = "001" and alu_srcA(15) = '1' and alu_srcB(15) = '0' and tdest(15) = '0' ) or
                  ( op = "001" and alu_srcA(15) = '0' and alu_srcB(15) = '1' and tdest(15) = '1' ) else '0';

  -- If result is negative
  cr(2) <= '1' when tdest(15) = '1' else '0';

  -- If there is a carry
  cr(3) <= '1' when tdest(16) = '1' else '0';
    

end test;