-- Bruce Maxwell
-- Spring 2015
-- CS 232 Project 2
--

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;


entity hextest is
end entity;

architecture test of hextest is
  signal A: UNSIGNED(3 downto 0);
  signal Aout: UNSIGNED(6 downto 0);

  component hexdisplay
  port(
  A: in UNSIGNED(3 downto 0);
  result: out UNSIGNED(6 downto 0)
  );
  end component;
    
  begin

    A(3) <= '0', '1' after 200 ns, '0' after 400 ns;
    A(2) <= '0', '1' after 100 ns, '0' after 200 ns, '1' after 300 ns;
    A(1) <= '0', '1' after 50 ns, '0' after 100 ns, '1' after 150 ns, '0' after 200 ns, '1' after 250 ns, '0' after 300 ns, '1' after 350 ns;
    A(0) <= '0', '1' after 25 ns, '0' after 50 ns, '1' after 75 ns, '0' after 100 ns, '1' after 125 ns, '0' after 150 ns, '1' after 175 ns, '0' after 200 ns, '1' after 225 ns, '0' after 250 ns, '1' after 275 ns, '0' after 300 ns , '1' after 325 ns, '0' after 350 ns, '1' after 375 ns;

    C0: hexdisplay port map( A, Aout );

  end test;