-- Owen Goldthwaite
-- CS232

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity lights is

	port(
		clk		 : in	std_logic;
		reset	 : in	std_logic;
        lightsOut	 : out	std_logic_vector(7 downto 0);
        IRView	 : out	std_logic_vector(3 downto 0)      
	);

end entity;

architecture rtl of lights is

    component lightrom is
        port 
        (
          addr  : in std_logic_vector (4 downto 0);
          data  : out std_logic_vector (3 downto 0)
        );
    end component;

	-- Build an enumerated type for the state machine
	type state_type is (sFetch, sExecute);
	-- Register to hold the current state
    signal state   : state_type;
    -- Other signals
    signal IR : std_logic_vector(3 downto 0);
    signal PC : unsigned(4 downto 0);
    signal LR : unsigned(7 downto 0);
    signal ROMvalue : std_logic_vector(3 downto 0);

begin

	-- Logic to advance to the next state
	process (clk, reset)
	begin
        if reset = '0' then
            -- Resetting everything
            LR <= (others => '0'); 
            PC <= (others => '0');
            IR <= (others => '0');
            state <= sFetch;
		elsif (rising_edge(clk)) then
			case state is
				when sFetch=>
                    IR <= ROMvalue;
                    PC <= PC + 1;
                    state <= sExecute;
				when sExecute=>
                    case IR is -- Set of rules/instructions based on IR, extended to 4 bits
                        when "0000" => LR <= "00000000";
                        when "0001" => LR <= shift_right(LR, 1);
                        when "0010" => LR <= shift_left(LR, 1);
                        when "0011" => LR <= LR + 1;
                        when "0100" => LR <= LR - 1;
                        when "0101" => LR <= not LR;
                        when "0110" => LR <= rotate_right(LR,1);
                        when "0111" => LR <= rotate_left(LR,1);
                        when "1000" => LR <= "11111111";
                        when "1001" => LR <= shift_right(LR, 2);
                        when "1010" => LR <= shift_left(LR, 2); 
                        when "1011" => LR <= LR + 2;
                        when "1100" => LR <= LR - 2;
                        when "1101" => LR <= "10101010";
                        when "1110" => LR <= rotate_right(LR,2);
                        when "1111" => LR <= rotate_left(LR,2);
                        when others => LR <= "11111111";
                    end case;   
                    state <= sFetch;             
			end case;
		end if;
    end process;
    
    IRview <= IR;
    lightsOut <= std_logic_vector(LR);

    lightsrom1: lightrom port map(addr=>std_logic_vector(PC), data=>ROMvalue);

end rtl;


ghdl -c --ieee=synopsys -fexplicit --work=altera_mf C:\Users\Owen\Desktop\232 Stuff\altera_stuff\altera/*.vhd stackertest.vhd stacker.vhd memram_lab.vhd -r stackertest --vcd=stackertest.vcd