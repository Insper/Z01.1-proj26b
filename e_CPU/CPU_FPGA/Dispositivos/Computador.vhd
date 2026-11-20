-------------------------------------------------------------------
-- Elementos de Sistemas
-------------------------------------------------------------------
-- Adaptado de Luciano Pereira
-------------------------------------------------------------------
-- Descricao :
-- Entidade central do desenvolvimento do computador
-------------------------------------------------------------------
-- Historico:
--  29/11/2016 : Criacao do projeto
-------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity ClockDivider is
    port (
        CLK_IN  : in  std_logic;
        RESET   : in  std_logic;
        CLK_OUT : out std_logic
    );
end entity;

architecture clk_div of ClockDivider is
    signal counter : unsigned(1 downto 0) := "00";
    signal clk_reg : std_logic := '0';
begin

    process(CLK_IN, RESET)
    begin
        if RESET = '1' then
            counter <= "00";
            clk_reg <= '0';

        elsif rising_edge(CLK_IN) then
            if counter = 1 then
                counter <= "00";
                clk_reg <= not clk_reg;
            else
                counter <= counter + 1;
            end if;
        end if;
    end process;

    CLK_OUT <= clk_reg;

end clk_div;


library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity Computador is
   generic(
        IS_SIMULATION : std_logic := '1'
   );
   port(
        -- Sistema
        MAX10_CLK1_50: in    std_logic;
        RESET_N      : in    std_logic;
        LEDR         : out   std_logic_vector(9 downto 0);
        SW           : in    std_logic_vector(9 downto 0);
	KEY          : in    std_logic_vector(1 downto 0);
	GPIO  	     : inout std_logic_vector(35 downto 0)
	--GPIO(26 to 35)    : out    std_logic_vector(9 downto 0)
       );

end entity;


architecture logic of Computador is

	component ClockDivider is
		 port (
			  CLK_IN  : in  std_logic;
			  RESET   : in  std_logic;
			  CLK_OUT : out std_logic
		 );
	end component;

	component CPU is
		 port(
			  clock       :	in  std_logic;
			  inM         : in  std_logic_vector(15 downto 0);
			  instruction : in  std_logic_vector(17 downto 0);
			  reset       : in  std_logic;
			  outM        : out std_logic_vector(15 downto 0);
			  writeM      : out std_logic;
			  addressM    : out std_logic_vector(14 downto 0);
			  pcout       : out std_logic_vector(14 downto 0)
	  );
	end component;

	component ROM is
		port(
			address	  : in std_logic_vector (14 downto 0);
			clock	  : in std_logic  := '1';
			q	  : out std_logic_vector (17 downto 0)
		);
	end component;

	component MemoryIO is
		port(
		  	CLK			: IN  STD_LOGIC;
		 	 ADDRESS		: IN  STD_LOGIC_VECTOR (14 DOWNTO 0);
		  	--RAM
        		INPUT			: IN  STD_LOGIC_VECTOR (15 DOWNTO 0);
        		LOAD			: IN  STD_LOGIC ;
       	 		OUTPUT			: OUT STD_LOGIC_VECTOR (15 DOWNTO 0);	
			--INPUTS/OUTPUTS
			SW  	: in std_logic_vector(9 downto 0);
			GPIN	: inout std_logic_vector(9 downto 0);
			LED 	: OUT std_logic_vector(9 downto 0);		  
			GPOUT 	: INOUT std_logic_vector(9 downto 0)
		);
	end component;

  signal INPUT        : std_logic_vector(15 downto 0) := "1111111111111111";
  signal ADDRESS      : std_logic_vector(14 downto 0) := (others => '0') ; -- meio 00100101101010
  signal LOAD, clock, clock_slow  : std_logic := '0';
  signal GPOUT10		 : std_logic_vector(9 downto 0);
  signal GPIN10		 : std_logic_vector(9 downto 0);

  signal RST_CPU              : std_logic := '1';

  signal OUTPUT_RAM   : std_logic_vector(15 downto 0);
  signal INSTRUCTION  : std_logic_vector(17 downto 0);
  signal PC           : std_logic_vector(14 downto 0);

begin

clock <= MAX10_CLK1_50;
--clock <= not KEY(0);	 	 
CLK_slow : ClockDivider port map (
    CLK_IN       => clock,
    reset       => '0',
    CLK_OUT       => clock_slow
);

GPIN10 <= GPIO(9 downto 0);
GPOUT10 <= GPIO(35 downto 26);

MAIN_CPU : CPU port map (
    clock       => clock_slow,
    inM         => OUTPUT_RAM,
    instruction => instruction,
    reset       => '0',
    outM        => INPUT,
    writeM      => LOAD,
    addressM    => ADDRESS,
    pcout       => PC
	);

ROM32k : ROM port map (
    address	=> PC(14 downto 0),
    clock	  => clock_slow,
    q		    => INSTRUCTION
    );

MEMORY_MAPED : MemoryIO port map (
    CLK         => clock,
    ADDRESS		 => ADDRESS,
    INPUT       => INPUT,
    LOAD        => LOAD,
    OUTPUT		 => OUTPUT_RAM,
    SW          => SW,
    GPIN        => GPIN10,
    LED         => LEDR,
    GPOUT       => GPOUT10
   );

end logic;

