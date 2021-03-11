-- Bruce Maxwell
-- Spring 2015
-- CS 232 Project 2
--

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;


entity adderbench is
end entity;

architecture test of adderbench is
  signal A: UNSIGNED(3 downto 0);
  signal B: UNSIGNED(3 downto 0);
  signal answer: UNSIGNED(4 downto 0);
  signal disp0 : unsigned(6 downto 0);
  signal disp1 : unsigned(6 downto 0);
  signal otheranswer : unsigned(3 downto 0); -- Bits that get sent to 3rd disp
  signal subt : std_logic;


    component hexdisplay
        port(
            A: in UNSIGNED(3 downto 0);
            result: out UNSIGNED(6 downto 0)
        );
    end component;

    component fourbitadder
        port(
            A, B: in UNSIGNED(3 downto 0);
            subt: in std_logic;
            answer: out UNSIGNED(4 downto 0)
        );
    end component;
    
  begin

    A(3) <= '0', '1' after 200 ns, '0' after 400 ns;
    A(2) <= '0', '1' after 100 ns, '0' after 200 ns, '1' after 300 ns;
    A(1) <= '0', '1' after 50 ns, '0' after 100 ns, '1' after 150 ns, '0' after 200 ns, '1' after 250 ns, '0' after 300 ns, '1' after 350 ns;
    A(0) <= '0', '1' after 25 ns, '0' after 50 ns, '1' after 75 ns, '0' after 100 ns, '1' after 125 ns, '0' after 150 ns, '1' after 175 ns, '0' after 200 ns, '1' after 225 ns, '0' after 250 ns, '1' after 275 ns, '0' after 300 ns , '1' after 325 ns, '0' after 350 ns, '1' after 375 ns;

    B(3) <= '0', '1' after 200 ns, '0' after 400 ns;
    B(2) <= '0', '1' after 100 ns, '0' after 200 ns, '1' after 300 ns;
    B(1) <= '0', '1' after 50 ns, '0' after 100 ns, '1' after 150 ns, '0' after 200 ns, '1' after 250 ns, '0' after 300 ns, '1' after 350 ns;
    B(0) <= '0', '1' after 25 ns, '0' after 50 ns, '1' after 75 ns, '0' after 100 ns, '1' after 125 ns, '0' after 150 ns, '1' after 175 ns, '0' after 200 ns, '1' after 225 ns, '0' after 250 ns, '1' after 275 ns, '0' after 300 ns , '1' after 325 ns, '0' after 350 ns, '1' after 375 ns;

    subt <= '0', '1' after 300 ns;

    otheranswer <= "000" & answer(4);

    C0: hexdisplay port map( answer(3 downto 0), disp0);
    C1: hexdisplay port map(otheranswer, disp1);
    C2: fourbitadder port map(A, B, subt, answer);

end test;