-- Owen Goldthwaite

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity calculator is
    port( 
    reset:  in std_logic; -- button 1
    clock:  in std_logic;
    b2:     in std_logic; -- switch values to mbr
    b3:     in std_logic; -- push mbr -> stack
    b4:     in std_logic; -- pop stack -> mbr
    op:     in std_logic_vector(2 downto 0);
    data:   in std_logic_vector(7 downto 0);
    digit0: out unsigned(6 downto 0);
    digit1: out unsigned(6 downto 0);
    stackview: out std_logic_vector(3 downto 0)
    );

end calculator;

architecture one of calculator is

    component memram is
    port
	(
		address		: IN STD_LOGIC_VECTOR (3 DOWNTO 0);
		clock		: IN STD_LOGIC  := '1';
		data		: IN STD_LOGIC_VECTOR (7 DOWNTO 0);
		wren		: IN STD_LOGIC ;
		q		: OUT STD_LOGIC_VECTOR (7 DOWNTO 0)
    );
    end component;

    component hexdisplay is
    port 
	(
		a	   : in UNSIGNED  (3 downto 0);
		result : out UNSIGNED (6 downto 0)
    );
    end component;

    signal RAM_input : std_logic_vector(7 downto 0);
    signal RAM_output : std_logic_vector(7 downto 0);
    signal RAM_we : std_logic;
    signal stack_ptr : unsigned(3 downto 0);
    signal mbr: unsigned(7 downto 0);
    signal state : std_logic_vector(2 downto 0);

begin

    stackview <= std_logic_vector(stack_ptr);

    process (clock, reset)
	begin
        if reset = '0' then
            -- Resetting everything
            stack_ptr <= (others => '0'); 
            mbr <= (others => '0');
            RAM_input <= (others => '0');
            state <= (others => '0');
            RAM_we <= '0';
		elsif (rising_edge(clock)) then
			case state is
				when "000"=>
                    if b2 = '0' then -- Button 2 press
                        -- Store value switch value into the mbr
                        mbr <= unsigned(data); 
                        state <= "111"; 
                    elsif b3 = '0' then -- Button 3 press
                        RAM_input <= std_logic_vector(mbr); 
                        RAM_we <= '1';
                        state <= "001";
                    elsif b4 = '0' then -- Button 4 press
                        if stack_ptr /= "0000" then
                            stack_ptr <= stack_ptr - 1;
                            state <= "100";
                        end if;
                    end if;
                when "001"=> 
                    RAM_we <= '0';
                    if stack_ptr < "1111" then -- Making sure stack ptr is within bounds
                        stack_ptr <= stack_ptr + 1;
                    end if;
                    state <= "111";
                when "100"=>    
                    state <= "101"; -- Waiting for address update and output
                when "101"=>       
                    state <= "110"; -- Waiting for address update and output
                when "110"=>      
                    -- Operand gets operand from the stack
                    -- MBR should currently be storing the other operand
                    case op is
                        when "000" => -- Addition
                            mbr <=  unsigned(RAM_output) + mbr;
                        when "001" => -- Subtraction
                            mbr <= unsigned(RAM_output) - mbr;
                            when "010" => -- Division
                            mbr <= unsigned(RAM_output) / mbr;
                        when "011" => -- Multiplication
                            -- Multiplication done only on the low 4 bits of the operands
                            mbr <= unsigned(RAM_output(3 downto 0)) * mbr(3 downto 0);
                        when "100" => -- modulo
                            mbr <= unsigned(RAM_output) mod mbr;
                        when "101" => --Square the mbr
                            mbr <= mbr(3 downto 0) * mbr(3 downto 0);
                        when others => 
                            mbr <= unsigned(RAM_output) + mbr;
                    end case;
                    state <= "111";
                when "111"=>
                    if (b2 = '1') and (b3 = '1') and (b4 = '1') then -- If not button is pressed
                        state <= "000";
                    end if;
                when others =>
                    state <= "000";
			end case;
		end if;
    end process;



S0: memram port map(address=>std_logic_vector(stack_ptr), clock=>clock, data=>RAM_input, wren=>RAM_we, q=>RAM_output);
S1: hexdisplay port map(mbr(3 downto 0),digit0);
S2: hexdisplay port map(mbr(7 downto 4),digit1);

end one;