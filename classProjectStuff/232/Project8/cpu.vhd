-- Owen Goldthwaite

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity cpu is
    port( 
        reset:  in std_logic; -- button 1
        clock:  in std_logic;

        PCview : out std_logic_vector( 7 downto 0);  -- debugging outputs
        IRview : out std_logic_vector(15 downto 0);
        RAview : out std_logic_vector(15 downto 0);
        RBview : out std_logic_vector(15 downto 0);
        RCview : out std_logic_vector(15 downto 0);
        RDview : out std_logic_vector(15 downto 0);
        REview : out std_logic_vector(15 downto 0);

        iport:   in std_logic_vector(7 downto 0); -- input port
        oport:   out std_logic_vector(15 downto 0)  -- output port
    );

end cpu;

architecture one of cpu is

    component alu is
    port (
            alu_srcA : in  unsigned(15 downto 0);         -- input A
            alu_srcB : in  unsigned(15 downto 0);         -- input B
            op   : in  std_logic_vector(2 downto 0);  -- operation
            cr   : out std_logic_vector(3 downto 0);  -- condition outputs
            dest : out unsigned(15 downto 0)          -- output value
        );       
    end component;

    component DataRAM is
	PORT
	(
		address		: IN STD_LOGIC_VECTOR (7 DOWNTO 0);
		clock		: IN STD_LOGIC  := '1';
		data		: IN STD_LOGIC_VECTOR (15 DOWNTO 0);
		wren		: IN STD_LOGIC ;
		q		: OUT STD_LOGIC_VECTOR (15 DOWNTO 0)
	);
    end component;

    component ProgramROM is
	PORT
	(
		address		: IN STD_LOGIC_VECTOR (7 DOWNTO 0);
		clock		: IN STD_LOGIC  := '1';
		q		: OUT STD_LOGIC_VECTOR (15 DOWNTO 0)
	);
    end component;

    signal state : std_logic_vector(3 downto 0);
    signal start_counter : unsigned(2 downto 0); -- small timer to pause start state

    -- ROM and RAM signals, RAM input is basically the mbr
    signal RAM_output : std_logic_vector(15 downto 0);
    signal RAM_we : std_logic;
    signal ROM_output : std_logic_vector(15 downto 0);

    -- Registers A - E
    signal RA : std_logic_vector(15 downto 0); 
    signal RB : std_logic_vector(15 downto 0); 
    signal RC : std_logic_vector(15 downto 0);
    signal RD : std_logic_vector(15 downto 0);
    signal RE : std_logic_vector(15 downto 0);

    signal SP : std_logic_vector(15 downto 0); -- Stack Pointer
    signal IR : std_logic_vector(15 downto 0); -- Instruction Register
    signal mbr: std_logic_vector(15 downto 0); -- Memory buffer register
    signal mar: std_logic_vector(7 downto 0);  -- Memory address register
    signal PC : std_logic_vector(7 downto 0);  -- Program Counter
    
    -- ALU signals
    signal srcA : std_logic_vector(15 downto 0); -- ALU Input A
    signal srcB : std_logic_vector(15 downto 0); -- ALU Input B
    signal ALU_out : unsigned(15 downto 0); -- ALU Output
    signal opcode : std_logic_vector(2 downto 0); --opcode
    signal condreg : std_logic_vector(3 downto 0) := "0000"; -- Condition Register


    signal OUTREG : std_logic_vector(15 downto 0); -- Output vector, to lights or something 

    signal crtest : std_logic_vector(3 downto 0);



begin

    PCview <= PC;  -- debugging outputs
    IRview <= IR;
    RAview <= RA;
    RBview <= RB;
    RCview <= RC;
    RDview <= RD;
    REview <= RE;
    oport <= OUTREG;
    crtest <= condreg;

    -- stackview <= std_logic_vector(stack_ptr);

    process (clock, reset)
	begin
        if reset = '0' then
            -- Resetting everything
            PC <= (others => '0'); 
            IR <= (others => '0'); 
            OUTREG <= (others => '0');
            mar <= (others => '0'); 
            mbr <= (others => '0'); 
            RA <= (others => '0'); 
            RB <= (others => '0'); 
            RC <= (others => '0'); 
            RD <= (others => '0'); 
            RE <= (others => '0'); 
            SP <= (others => '0'); 
            --condreg <= (others => '0'); 
            state <= (others => '0');
            RAM_we <= '0';
            start_counter <= (others => '0'); 
            state <= "0000"; -- Go to start state

		elsif (rising_edge(clock)) then
			case state is
                when "0000"=> -- Start state, incrementing counter until fetch state
                    if start_counter = "111" then -- Go to fetch state
                        state <= "0001";
                    else
                        start_counter <= start_counter + 1;
                    end if;
                when "0001"=> -- fetch state
                    IR <= ROM_output;
                    PC <= std_logic_vector(unsigned(PC) + 1);
                    state <= "0010";
                when "0010"=> -- execute-setup
                    case IR(15 downto 12) is
                    when "0000" =>  -- Load from RAM instruction
                        if IR(11) = '1' then
                            mar <= std_logic_vector(unsigned(RE(7 downto 0)) + unsigned(IR(7 downto 0))); 
                        else
                            mar <= IR(7 downto 0);
                        end if;
                    when "0001" => -- Store to RAM instruction
                        if IR(11) = '1' then
                            mar <= std_logic_vector(unsigned(RE(7 downto 0)) + unsigned(IR(7 downto 0))); 
                        else
                            mar <= IR(7 downto 0);
                        end if;
                        -- Storing value into mbr
                        case IR(10 downto 8) is -- Getting src location
                            when "000" => mbr <= RA;
                            when "001" => mbr <= RB;
                            when "010" => mbr <= RC;
                            when "011" => mbr <= RD;
                            when "100" => mbr <= RE;
                            when "101" => mbr <= SP;
                            when others => null;
                        end case;
                    when "0010" => -- Unconditional Branch
                        PC <= IR(7 downto 0);
                    when "0011" => -- Conditional Branch, Call, Return, Exit
                        case IR(11 downto 10) is
                            when "00" => -- Conditional Branch
                                -- Checking CR bit values against condition values in instruction
                                if IR(9 downto 8) = "00" and condreg(0) = '1' then -- Zero
                                    PC <= IR(7 downto 0);
                                elsif IR(9 downto 8) = "01" and condreg(1) = '1' then -- Overflow
                                    PC <= IR(7 downto 0);
                                elsif IR(9 downto 8) = "10" and condreg(2) = '1' then -- Negative
                                    PC <= IR(7 downto 0);
                                elsif IR(9 downto 8) = "11" and condreg(3) = '1' then -- Carry
                                    PC <= IR(7 downto 0);
                                end if;
                            when "01" => -- Call
                                PC <= IR(7 downto 0);
                                mar <= SP(7 downto 0);
                                mbr <= "0000" & condreg & PC; -- Assuming this is right order
                                SP <= std_logic_vector(unsigned(SP) + 1);
                            when "10" => -- Return
                                mar <= std_logic_vector(unsigned(SP(7 downto 0)) - 1); -- Maybe just make this SP
                                SP <= std_logic_vector(unsigned(SP) - 1);
                            when "11" => -- Exit
                                null;
                            when others =>
                                null;
                        end case;
                    when "0100" => -- Push instruction
                        mar <= SP(7 downto 0);
                        SP <= std_logic_vector(unsigned(SP) + 1);
                        case IR(11 downto 9) is -- Getting src location
                            when "000" => mbr <= RA;
                            when "001" => mbr <= RB;
                            when "010" => mbr <= RC;
                            when "011" => mbr <= RD;
                            when "100" => mbr <= RE;
                            when "101" => mbr <= SP;
                            when "110" => mbr <= "00000000" & PC; 
                            when "111" => mbr <= "000000000000" & condreg;
                            when others => null;
                        end case;
                    when "0101" => -- Pop instruction
                        mar <= std_logic_vector(unsigned(SP(7 downto 0)) - 1); -- Maybe just make this SP
                        SP <= std_logic_vector(unsigned(SP) - 1);
                    when "0110" => null; -- Store to ouput
                    when "0111" => null; -- Load from input
                    when "1000" | "1001" | "1010" | "1011" | "1100" => -- Binary ALU Operations
                        case IR(11 downto 9) is -- Getting src location
                            when "000" => srcA <= RA;
                            when "001" => srcA <= RB;
                            when "010" => srcA <= RC;
                            when "011" => srcA <= RD;
                            when "100" => srcA <= RE;
                            when "101" => srcA <= SP;
                            when "110" => srcA <= "0000000000000000"; 
                            when "111" => srcA <= "1111111111111111";
                            when others => null;
                        end case;

                        case IR(8 downto 6) is
                            when "000" => srcB <= RA;
                            when "001" => srcB <= RB;
                            when "010" => srcB <= RC;
                            when "011" => srcB <= RD;
                            when "100" => srcB <= RE;
                            when "101" => srcB <= SP;
                            when "110" => srcB <= "0000000000000000"; 
                            when "111" => srcB <= "1111111111111111";
                            when others => null;
                        end case;   

                        opcode <= IR(14 downto 12); -- OPcode for ALU operation
                    when "1101" | "1110" => -- Unary ALU operations, shift/rotate
                        srcB(0) <= IR(11); -- Getting direction bit

                        case IR(10 downto 8) is -- Getting src location
                            when "000" => srcA <= RA;
                            when "001" => srcA <= RB;
                            when "010" => srcA <= RC;
                            when "011" => srcA <= RD;
                            when "100" => srcA <= RE;
                            when "101" => srcA <= SP;
                            when "110" => srcA <= "0000000000000000"; 
                            when "111" => srcA <= "1111111111111111";
                            when others => null;
                        end case;

                        opcode <= IR(14 downto 12); -- OPcode for ALU operation
                    when "1111" => -- Move instruction
                        if IR(11) = '1' then
                            srcA <= std_logic_vector(resize(signed(IR(10 downto 3)), srcA'length));
                        else 
                            case IR(10 downto 8) is -- Getting src location
                                when "000" => srcA <= RA;
                                when "001" => srcA <= RB;
                                when "010" => srcA <= RC;
                                when "011" => srcA <= RD;
                                when "100" => srcA <= RE;
                                when "101" => srcA <= SP;
                                when "110" => srcA <= PC; 
                                when "111" => srcA <= IR;
                                when others => null;
                            end case;
                        end if;

                        opcode <= "111";
                    when others => null;
                    end case;
                    state <= "0011";
                when "0011"=> -- execute-ALU
                    if IR(15 downto 12) = "0001" or IR(15 downto 12) = "0100" or IR(15 downto 10) = "001101" then
                        RAM_we <= '1';
                    end if;
                    state <= "0100"; 
                when "0100"=> -- execute-MemWait
                        state <= "0101";
                when "0101"=> -- execute-Write
                    case IR(15 downto 12) is
                        when "0000" => -- Load instruction
                            case IR(10 downto 8) is -- Getting src location
                                when "000" => RA <= RAM_output;
                                when "001" => RB <= RAM_output;
                                when "010" => RC <= RAM_output;
                                when "011" => RD <= RAM_output;
                                when "100" => RE <= RAM_output;
                                when "101" => SP <= RAM_output;
                                when others => null;
                            end case;
                        when "0001" => RAM_we <= '0'; -- store, maybe put null here
                        when "0010" => null; -- unconditional branch
                        when "0011" => -- conditional branch, call, return, exit
                            case IR(11 downto 10) is 
                                when "00" => null; -- Conditional branch
                                when "01" => RAM_we <= '0'; -- call, maybe put null here
                                when "10" => -- Return 
                                    --condreg <= RAM_output(11 downto 8);
                                    PC <= RAM_output(7 downto 0);
                                when "11" => null; -- Exit
                                when others => null;
                            end case;
                        when "0100" => RAM_we <= '0'; -- Push, maybe put null here
                        when "0101" => -- Pop
                            case IR(11 downto 9) is
                                when "000" => RA <= RAM_output;
                                when "001" => RB <= RAM_output;
                                when "010" => RC <= RAM_output;
                                when "011" => RD <= RAM_output;
                                when "100" => RE <= RAM_output;
                                when "101" => SP <= RAM_output;
                                when "110" => PC <= RAM_output(7 downto 0); -- Maybe change these two
                                --when "111" => condreg <= RAM_output(3 downto 0);
                                when others => null;
                            end case;
                        when "0110" => -- Store to output
                            case IR(11 downto 9) is
                                when "000" => OUTREG <= RA;
                                when "001" => OUTREG <= RB;
                                when "010" => OUTREG <= RC;
                                when "011" => OUTREG <= RD;
                                when "100" => OUTREG <= RE;
                                when "101" => OUTREG <= SP;
                                when "110" => OUTREG <= "00000000" & PC; -- Maybe change these two
                                when "111" => OUTREG <= IR;
                                when others => null;
                            end case;
                        when "0111" => -- Load from input
                            case IR(11 downto 9) is
                                when "000" => RA <= iport;
                                when "001" => RB <= iport;
                                when "010" => RC <= iport;
                                when "011" => RD <= iport;
                                when "100" => RE <= iport;
                                when "101" => SP <= iport;
                                when others => null;
                            end case;
                        when "1000" | "1001" | "1010" | "1011" | "1100" | "1101" | "1110" => -- ALU operations
                            case IR(2 downto 0) is -- Getting src location
                                when "000" => RA <= std_logic_vector(ALU_out);
                                when "001" => RB <= std_logic_vector(ALU_out);
                                when "010" => RC <= std_logic_vector(ALU_out);
                                when "011" => RD <= std_logic_vector(ALU_out);
                                when "100" => RE <= std_logic_vector(ALU_out);
                                when "101" => SP <= std_logic_vector(ALU_out);
                                when others => null;
                            end case;
                        when "1111" =>
                            case IR(2 downto 0) is -- Getting src location
                                when "000" => RA <= std_logic_vector(ALU_out);
                                when "001" => RB <= std_logic_vector(ALU_out);
                                when "010" => RC <= std_logic_vector(ALU_out);
                                when "011" => RD <= std_logic_vector(ALU_out);
                                when "100" => RE <= std_logic_vector(ALU_out);
                                when "101" => SP <= std_logic_vector(ALU_out);
                                when others => null;
                            end case;
                        when others => null;
                    end case;
                    if IR(15 downto 9) = "001110" then -- If rreturn instruction then go to return states
                        state <= "0110";
                    else
                        state <= "0001";
                    end if;
                when "0110"=> -- Execute-Return1
                    state <= "0111";
                when "0111"=> -- Execute-Return2
                    state <= "0001";
                when "1000"=> -- Halt state
                when others =>
                    state <= "0000";
			end case;
		end if;
    end process;


ROMinst: programROM port map(address=>PC, clock=>clock, q=>ROM_output);
RAMinst: dataRAM port map(address=>mar, clock=>clock, data=>mbr, wren=>RAM_we, q=>RAM_output);
aluinst: alu port map(alu_srcA=>unsigned(srcA), alu_srcB=>unsigned(srcB), op=>opcode, cr=>condreg, dest=>alu_OUT);
-- S1: hexdisplay port map(mbr(3 downto 0),digit0);
-- S2: hexdisplay port map(mbr(7 downto 4),digit1);

end one;