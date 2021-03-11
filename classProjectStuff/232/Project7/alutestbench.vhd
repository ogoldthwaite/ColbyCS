library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity alutestbench is
end alutestbench;

architecture test of alutestbench is
  constant num_cycles : integer := 20;

  
  signal state: unsigned(3 downto 0);
  signal alu_srcA: unsigned(15 downto 0);
  signal alu_srcB: unsigned(15 downto 0);
  signal dest: unsigned(15 downto 0) := "0000000000000000";
  signal opcode: std_logic_vector(2 downto 0);

  signal output: std_logic_vector(15 downto 0) := "0000000000000000";
  signal CR: std_logic_vector(3 downto 0) := "0000";
  signal clk: std_logic := '1';
  signal reset: std_logic;
  
  -- component statement for the ALU
  component alu
    port (
      alu_srcA : in  unsigned(15 downto 0);         -- input A
      alu_srcB : in  unsigned(15 downto 0);         -- input B
      op   : in  std_logic_vector(2 downto 0);  -- operation
      cr   : out std_logic_vector(3 downto 0);  -- condition outputs
      dest : out unsigned(15 downto 0));        -- output value
  end component;
  
begin

  -- start off with a short reset
  reset <= '0', '1' after 1 ns;

  -- create a clock
  process
  begin
    for i in 1 to num_cycles loop
      clk <= not clk;
      wait for 1 ns;
      clk <= not clk;
      wait for 1 ns;
    end loop;
    wait;
  end process;
  
  output <= std_logic_vector(dest); -- connect dest and the output

  process(clk, reset)
  begin 
    if reset = '0' then
      alu_srcA <= "0000000000000000";
      alu_srcB <= "0000000000000000";
      state <= "0000";
    elsif rising_edge(clk) then
      case state is
        when "0000" =>
          alu_srcA <= x"7FFF";
          alu_srcB <= x"0002";
          opcode <= "000"; -- addition, answer should be x8001, flags "0110"
          state <= state + 1;
        when "0001" =>
          alu_srcA <= x"FF10";
          alu_srcB <= x"FFFF";
          opcode <= "000"; -- addition, answer should be xFF0F, flags "1100"
          state <= state + 1;
        when "0010" =>
          alu_srcA <= x"0014";
          alu_srcB <= x"0012";
          opcode <= "001"; -- subtraction, answer should be x0002, flags "0000"
          state <= state + 1;
        when "0011" =>
          alu_srcA <= x"FFFE";
          alu_srcB <= x"FFFF";
          opcode <= "001"; -- subtraction, answer should be xFFFF, flags "1100"
          state <= state + 1;
        when "0100" =>
          alu_srcA <= x"FFFF";
          alu_srcB <= x"AAAA";
          opcode <= "010"; -- and, answer should be xAAAA, flags "0100"
          state <= state + 1;
        when "0101" =>
          alu_srcA <= x"00FF";
          alu_srcB <= x"AAAA"; -- and, answer should be x00AA, flags "0000"
          opcode <= "010";
          state <= state + 1;
        when "0110" =>
          alu_srcA <= x"FFFF";
          alu_srcB <= x"AAAA";
          opcode <= "011"; -- or, answer should be xFFFF, flags "0100"
          state <= state + 1;
        when "0111" =>
          alu_srcA <= x"FF00";
          alu_srcB <= x"AAAA"; -- or, answer should be xFFAA, flags "0100"
          opcode <= "011";
          state <= state + 1;
        when "1000" =>
          alu_srcA <= x"FFFF";
          alu_srcB <= x"AAAA";
          opcode <= "100"; -- xor, answer should be x5555, flags "0000"
          state <= state + 1;
        when "1001" =>
          alu_srcA <= x"FF00";
          alu_srcB <= x"AAAA";
          opcode <= "100"; -- xor, answer should be x55AA, flags "0000"
          state <= state + 1;
        when "1010" =>
          alu_srcA <= x"AAAA";
          alu_srcB <= x"0000";
          opcode <= "101"; -- shift, left by 1, answer should be x5554, flags "1000"
          state <= state + 1;
        when "1011" =>
          alu_srcA <= x"AAAA";
          alu_srcB <= x"0001";
          opcode <= "101"; -- shift, right by 1, answer should be xD555, flags "0100"
          state <= state + 1;
        when "1100" =>
          alu_srcA <= x"AAAA";
          alu_srcB <= x"0000";
          opcode <= "110"; -- rotate, left by 1, answer should be x5555, flags "1000"
          state <= state + 1;
        when "1101" =>
          alu_srcA <= x"AAAA";
          alu_srcB <= x"0001";
          opcode <= "110"; -- rotate, right by 1, answer should be x5555, flags "0000"
          state <= state + 1;
        when "1110" =>
          alu_srcA <= x"0000";
          alu_srcB <= x"0234";
          opcode <= "111"; -- pass through, answer should be x0000, flags "0001"
          state <= state + 1;
        when others =>
          alu_srcA <= x"F012";
          alu_srcB <= x"0000";
          opcode <= "111"; -- pass through, answer should be xF012, flags "0100"
          state <= state + 1;
      end case;
    end if;
  end process;


  aluinstance: alu
  port map( alu_srcA => alu_srcA, alu_srcB => alu_srcB, dest => dest, op => opcode, cr => CR );

end test;