-- Quartus II VHDL Template
-- Four-State Moore State Machine

-- A Moore machine's outputs are dependent only on the current state.
-- The output is written only when the state changes.  (State
-- transitions are synchronous.)

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity timer is

	port(
		clk		 : in	std_logic;
		reset	 : in	std_logic;
        start	 : in	std_logic;
        react	 : in	std_logic;        
        redOut   : out std_logic;
        greenOut : out std_logic;
		mstime	 : out	std_logic_vector(7 downto 0)
	);

end entity;

architecture rtl of timer is

	-- Build an enumerated type for the state machine
	type state_type is (sIdle, sWait, sCount);

	-- Register to hold the current state
    signal state   : state_type;
    
    -- Counter for time for wait and count states
    signal count : unsigned(7 downto 0);

begin

	-- Logic to advance to the next state
	process (clk, reset)
	begin
		if reset = '0' then
            state <= sIdle;
            count <= (others => '0');
		elsif (rising_edge(clk)) then
			case state is
				when sIdle=>
					if start = '0' then
                        state <= sWait;
                    else
                        state <= sIdle;
					end if;
				when sWait=>
                    if count > "00000100" then -- State progresses and count resets
                        state <= sCount;
                        count <= (others => '0');
                    elsif react = '0' then -- If react button is hit early
                        state <= sIdle;
                        count <= (others => '1');
                    else -- State stays in wait and count increments
                        state <= sWait;
                        count <= count + 1; 
					end if;
				when sCount=>
					if react = '0' then -- Go to idle
						state <= sIdle;
                    else -- State stays the same and count increments
                        state <= sCount;
                        count <= count + 1; 
					end if;
			end case;
		end if;
	end process;

    greenOut <= '1' when state = sCount else '0';
    redOut   <= '1' when state = sWait else '0';
    mstime   <= "00000000" when state = sWait else std_logic_vector(count(7 downto 0));

        
end rtl;