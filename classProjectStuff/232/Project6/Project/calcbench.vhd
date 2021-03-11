-- Owen Goldthwaite

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity calcbench is
end entity;

architecture test of calcbench is
  constant num_cycles : integer := 45;

  -- this circuit needs a clock and a reset
  signal clk : std_logic := '1';
  signal reset : std_logic;

  -- stacker component
  component calculator
    port(
        reset:  in std_logic; -- button 1
        clock:  in std_logic;
        b2:     in std_logic; -- switch values to mbr
        b3:     in std_logic; -- push mbr -> stack
        b4:     in hellostd_logic; -- pop stack -> mbr
        op:     in std_logic_vector(2 downto 0);
        data:   in std_logic_vector(7 downto 0);
        digit0: out unsigned(6 downto 0);
        digit1: out unsigned(6 downto 0);
        stackview: out std_logic_vector(3 downto 0)
         );
  end component;

  component hexdisplay is
    port 
	(
		a	   : in UNSIGNED  (3 downto 0);
		result : out UNSIGNED (6 downto 0)
    );
    end component;

  -- output signals
  signal stackview : std_logic_vector(3 downto 0);

  -- buttons
  signal b2, b3, b4 : std_logic;
  signal data: std_logic_vector(7 downto 0);
  signal op: std_logic_vector(2 downto 0);

  signal digit0: unsigned(6 downto 0);
  signal digit1: unsigned(6 downto 0);

begin

  -- start off with a short reset
  reset <= '0', '1' after 5 ns;

  -- create a clock
  process
  begin
    for i in 1 to num_cycles loop
      clk <= not clk;
      wait for 5 ns;
      clk <= not clk;
      wait for 5 ns;
    end loop;
    wait;
  end process;

  -- clock is in 5ns increments, rising edges on 5, 15, 25, 35, 45..., let 5 cycles
  -- go by before doing anything
  --

  op <= "101";

  data <= "00000000", "00000010" after 49 ns, "00000110" after 99 ns;

  -- put data values into the MBR at 50, 100
  b2 <= '1', '0' after 50 ns, '1' after 60 ns, '0' after 100 ns, '1' after 110 ns;

 -- push mbr value onto stack at 70 ns
  b3 <= '1', '0' after 70 ns, '1' after 80 ns;

  -- perform action button / operation at 
  b4 <= '1', '0' after 120 ns, '1' after 130 ns;

-- op <= "011", "001" after 240 ns;

-- data <= "00000000", "00000100" after 49 ns, "00000110" after 99 ns, "00000010" after 150 ns;

-- -- put data values into the MBR at 50, 100
-- b2 <= '1', '0' after 50 ns, '1' after 60 ns, '0' after 100 ns, '1' after 110 ns, '0' after 160 ns, '1' after 170 ns;

-- -- push mbr value onto stack at 70 ns
-- b3 <= '1', '0' after 70 ns, '1' after 80 ns, '0' after 120 ns, '1' after 130 ns;

-- -- perform action button / operation at 
-- b4 <= '1', '0' after 210 ns, '1' after 215 ns, '0' after 240 ns, '1' after 250 ns;

  -- port map the circuit
  S0: calculator port map( reset, clk, b2, b3, b4, op, data, digit0, digit1, stackview);

end test;