-- Quartus II VHDL Template
-- Four-State Moore State Machine

-- A Moore machine's outputs are dependent only on the current state.
-- The output is written only when the state changes.  (State
-- transitions are synchronous.)

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity bright is

	port(
		clk		 : in	std_logic;
        reset	 : in	std_logic;
        buttonOne : in std_logic;
        buttonTwo : in std_logic;
        buttonThree : in std_logic;
        redOutput : out std_logic_vector(2 downto 0);
        greenOutput : out std_logic
	);

end entity;

architecture rtl of bright is

	-- Build an enumerated type for the state machine
	type state_type is (s0, s1, s2, s3);

	-- Register to hold the current state
	signal state   : state_type;

begin

	-- Logic to advance to the next state
	process (clk, reset)
	begin
		if reset = '0' then
			state <= s0;
		elsif (rising_edge(clk)) then
			case state is
				when s0=>
					if buttonOne = '0' then
						state <= s1;
					else
						state <= s0;
					end if;
				when s1=>
					if buttonTwo = '0' then
						state <= s2;
					elsif buttonThree = '0' then
                        state <= s0;
                    else
						state <= s1;
					end if;
				when s2=>
					if buttonThree = '0' then
						state <= s3;
					elsif buttonOne = '0' then
                        state <= s0;
                    else
                        state <= s2;
					end if;
				when s3 =>
					if buttonOne = '0' or buttonTwo = '0' then
						state <= s0;
					else
						state <= s3;
					end if;
			end case;
		end if;
	end process;

	-- Output depends solely on the current state
	process (state)
	begin
		case state is
			when s0 =>
                redOutput(0) <= '1';
				redOutput(1) <= '0';
				redOutput(2) <= '0';
				greenOutput <= '0';                
			when s1 =>
                redOutput(0) <= '0';
                redOutput(1) <= '1';
                redOutput(2) <= '0';
                greenOutput <= '0'; 
			when s2 =>
                redOutput(0) <= '0';
                redOutput(1) <= '0';
                redOutput(2) <= '1';
                greenOutput <= '0'; 
			when s3 =>
                redOutput(0) <= '0';
                redOutput(1) <= '0';
                redOutput(2) <= '0';
                greenOutput <= '1'; 
		end case;
	end process;

end rtl;