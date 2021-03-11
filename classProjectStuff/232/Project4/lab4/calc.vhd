-- simple template

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity calc is
  port 
  (
    a      : in unsigned  (3 downto 0);
    b      : in unsigned  (3 downto 0);
    c      : in std_logic_vector (1 downto 0);
    result : out unsigned (4 downto 0)
  );

end entity;

architecture rtl of calc is

  component alu
    port
    (
        d      : in unsigned  (3 downto 0);
        e      : in unsigned  (3 downto 0);
        f      : in std_logic_vector (1 downto 0);
        q      : out unsigned (4 downto 0)
    );
  end component;

begin
  -- assignments and processes go here

  alu1: alu port map(d=>a, e=>b, f=>c, q=>result);

end rtl;