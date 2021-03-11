-- Owen Goldthwaite
-- CS232

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity pld2 is

	port(
		clk		 : in	std_logic;
		reset	 : in	std_logic;
        lights	 : out	std_logic_vector(7 downto 0);
        IRView	 : out	std_logic_vector(9 downto 0)      
	);

end entity;

architecture rtl of pld2 is

    component pldrom is
        port 
        (
          addr  : in std_logic_vector (3 downto 0);
          data  : out std_logic_vector (9 downto 0)
        );
    end component;

	-- Build an enumerated type for the state machine
	type state_type is (sFetch, sExecute1, sExecute2);
	-- Register to hold the current state
    signal state   : state_type;
    -- Other signals
    signal IR : std_logic_vector(9 downto 0);
    signal ROMvalue : std_logic_vector(9 downto 0);
    signal PC : unsigned(3 downto 0);
    signal LR : unsigned(7 downto 0);
    signal ACC : unsigned(7 downto 0);
    signal SRC : unsigned(7 downto 0);


begin

	-- Logic to advance to the next state
	process (clk, reset)
	begin
        if reset = '0' then
            -- Resetting everything
            LR <= (others => '0'); 
            PC <= (others => '0');
            IR <= (others => '0');
            ACC <= (others => '0');
            SRC <= (others => '0');
            state <= sFetch;
		elsif (rising_edge(clk)) then
			case state is
				when sFetch=>
                    IR <= ROMvalue;
                    PC <= PC + 1;
                    state <= sExecute1;
                when sExecute1=> 
                    case IR(9 downto 8) is --C1C0 bits for definding operation type
                        when "00" => -- Move conditions
                            case IR(5 downto 4) is -- Move SRC assigning
                                when "00" => SRC <= ACC; -- SRC gets ACC
                                when "01" => SRC <= LR; -- SRC gets LR
                                when "10" => 
                                    if IR(3) = '0' then
                                        SRC <= "0000" & unsigned(IR(3 downto 0)); -- SRC gets low 4 IR bits, sign extending 0
                                    else
                                        SRC <= "1111" & unsigned(IR(3 downto 0)); -- SRC gets low 4 IR bits, sign extending 1
                                    end if;
                                when "11" => SRC <= "11111111"; -- SRC gets all 1s
                                when others => null;
                            end case;
                        when "01" => -- Binary Operator SRC assigning
                            case IR(4 downto 3) is
                                when "00" => SRC <= ACC; -- SRC gets ACC
                                when "01" => SRC <= LR;  -- SRC gets LR
                                when "10" => 
                                    if IR(3) = '0' then
                                        SRC <= "000000" & unsigned(IR(1 downto 0)); -- SRC gets low 4 IR bits, sign extending 0
                                    else
                                        SRC <= "111111" & unsigned(IR(1 downto 0)); -- SRC gets low 4 IR bits, sign extending 1
                                    end if;
                                when "11" => SRC <= "11111111"; -- SRC gets all 1s
                                when others => null;
                            end case;
                        when "10" => -- Unconditional Branch
                            PC <= unsigned(IR(3 downto 0)); -- PC gets 4 address bits
                        when "11" => -- Conditional Branch
                            case IR(7) is 
                                when '0' => -- When checking against ACC 
                                    if IR(6) = '1' then
                                        if ACC = "00001000" then -- Extension Branch, if = 8
                                            PC <= unsigned(IR(3 downto 0)); -- Branch
                                        end if;
                                    elsif ACC = "00000000" then -- If 0
                                        PC <= unsigned(IR(3 downto 0)); -- Branch
                                    end if;
                                when '1' => -- When checking aginst LR
                                    if IR(6) = '1' then
                                        if LR = "00001000" then -- Extension Branch, if = 8
                                            PC <= unsigned(IR(3 downto 0)); -- Branch
                                        end if;
                                    elsif LR = "00000000" then -- If 0
                                        PC <= unsigned(IR(3 downto 0)); -- Branch
                                    end if;
                                when others => null;
                            end case;
                        when others => null;
                    end case;
                    state <= sExecute2; -- Setting to sExecute2 
                when sExecute2=>
                    case IR(9 downto 8) is --C1C0 bits for defining operation type
                    when "00" => -- Move conditions
                        case IR(7 downto 6) is -- Move SRC assigning
                            when "00" => ACC <= SRC; -- ACC gets SRC
                            when "01" => LR <= SRC; -- LR gets SRC
                            when "10" => ACC(3 downto 0) <= SRC(3 downto 0); -- Low ACC bits getting low SRC bits
                            when "11" => ACC(7 downto 4) <= SRC(3 downto 0); -- High ACC bits getting low SRC bits
                            when others => null;
                        end case;
                    when "01" => -- Binary Operator 
                        case IR(2) is
                            when '0' => -- Assigning to ACC
                                case IR(7 downto 5) is
                                    when "000" => ACC <= ACC + SRC; -- Dest gets Dest + SRC
                                    when "001" => ACC <= ACC - SRC; -- Dest gets Dest - SRC
                                    when "010" => ACC <= shift_left(SRC,1); -- Dest gets SRC shifted 1 left
                                    when "011" => ACC <= shift_right(SRC,1); -- Dest gets SRC shifted 1 right, add sign bit maintaining
                                    when "100" => ACC <= ACC xor SRC; -- Dest gets Dest xor SRC
                                    when "101" => ACC <= ACC and SRC; -- Dest gets Dest and SRC
                                    when "110" => ACC <= rotate_left(SRC,1); -- Dest gets SRC rotated left 1
                                    when "111" => ACC <= rotate_right(SRC,1); -- Dest gets SRC rotated right 1
                                    when others => null;
                                end case;
                            when '1' => -- Assigning to LR
                                case IR(7 downto 5) is
                                    when "000" => LR <= LR + SRC; -- Dest gets Dest + SRC
                                    when "001" => LR <= LR - SRC; -- Dest gets Dest - SRC
                                    when "010" => LR <= shift_left(SRC,1); -- Dest gets SRC shifted 1 left
                                    when "011" => LR <= shift_right(SRC,1); -- Dest gets SRC shifted 1 right, add sign bit maintaining
                                    when "100" => LR <= LR xor SRC; -- Dest gets Dest xor SRC
                                    when "101" => LR <= LR and SRC; -- Dest gets Dest and SRC
                                    when "110" => LR <= rotate_left(SRC,1); -- Dest gets SRC rotated left 1
                                    when "111" => LR <= rotate_right(SRC,1); -- Dest gets SRC rotated right 1
                                    when others => null;
                                end case;
                            when others => null;                            
                        end case;
                    when others => null;
                end case;
                    state <= sFetch; -- Setting state back to fetch, get next IR 
			end case;
		end if;
    end process;
    
    IRview <= IR;
    lights <= std_logic_vector(LR);

    pldrom1: pldrom port map(addr=>std_logic_vector(PC), data=>ROMvalue);

end rtl;