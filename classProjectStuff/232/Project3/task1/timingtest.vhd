-- Bruce A. Maxwell
-- Spring 2013
-- CS 232 Lab 3
-- Test bench for the bright state machine circuit
--

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- a test bench has no inputs or outputs
entity timingtest is
end timingtest;

-- architecture
architecture test of timingtest is

  -- internal signals for everything we want to send to or receive from the
  -- test circuit
  signal reset, start, react: std_logic;
  signal rled: std_logic;
  signal gled: std_logic;
  signal timeval: std_logic_vector(7 downto 0);
  signal disp0 : unsigned(6 downto 0);
  signal disp1 : unsigned(6 downto 0);
  signal disptime0 : unsigned(3 downto 0);
  signal disptime1 : unsigned(3 downto 0);

  component timer
    port(
		clk		 : in	std_logic;
		reset	 : in	std_logic;
        start	 : in	std_logic;
        react	 : in	std_logic;        
        redOut   : out std_logic;
        greenOut : out std_logic;
		mstime	 : out	std_logic_vector(7 downto 0)
      );
  end component;

  component hexdisplay
    port(
        A: in UNSIGNED(3 downto 0);
        result: out UNSIGNED(6 downto 0)
        );
  end component;

  -- signals for making the clock
  constant num_cycles : integer := 20;
  signal clk : std_logic := '1';

begin
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

  -- these are timed signal assignments to create specific patterns
  reset <= '0', '1' after 8 ns, '0' after 100 ns, '1' after 200 ns;
  start <= '1', '0' after 12 ns, '1' after 22 ns; 
  react <= '1', '0' after 150 ns, '1' after 165 ns;

  disptime0 <= unsigned(timeval(3 downto 0));
  disptime1 <= unsigned(timeval(7 downto 4));


  -- this instantiates a bright circuit and sets up the inputs and outputs
  B0: timer port map (clk, reset, start, react, rled, gled, timeval);
  B1: hexdisplay port map(disptime0, disp0);
  B2: hexdisplay port map(disptime1, disp1);

end test;