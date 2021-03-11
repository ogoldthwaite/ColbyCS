-- Bruce A. Maxwell
-- Spring 2013
-- CS 232 Lab 3
-- Test bench for the bright state machine circuit
--

library ieee;
use ieee.std_logic_1164.all;

-- a test bench has no inputs or outputs
entity brighttest is
end brighttest;

-- architecture
architecture test of brighttest is

  -- internal signals for everything we want to send to or receive from the
  -- test circuit
  signal Reset, P1, P2, P3: std_logic;
  signal rled: std_logic_vector (2 downto 0);
  signal gled: std_logic;

  -- the component statement lets us instantiate a bright circuit
  component bright
    port(
      clk		 : in	std_logic;
      buttonOne	 : in	std_logic;
      buttonTwo	: in std_logic;
      buttonThree	: in std_logic;
      reset	 : in	std_logic;
      redOutput	 : out	std_logic_vector(2 downto 0);
      greenOutput : out std_logic
      );
  end component;

  -- signals for making the clock
  constant num_cycles : integer := 20;
  signal clk : std_logic := '1';

begin

  -- these are timed signal assignments to create specific patterns
  Reset <= '0', '1' after 7 ns;
  P1 <= '1', '0' after 20 ns, '1' after 35 ns, '0' after 105 ns, '1' after 125 ns,
      '0' after 155 ns, '1' after 165 ns;
  P2 <= '1', '0' after 45 ns, '1' after 65 ns, '0' after 135 ns, '1' after 145 ns;
  P3 <= '1', '0' after 75 ns, '1' after 90 ns;
  

  -- we can use a process and a for loop to generate a clock signal
  process begin
    for i in 1 to num_cycles loop
      clk <= not clk;
      wait for 5 ns;
      clk <= not clk;
      wait for 5 ns;
    end loop;
    wait;
  end process;

  -- this instantiates a bright circuit and sets up the inputs and outputs
  B0: bright port map (clk, P1, P2, P3, reset, rled, gled);
end test;