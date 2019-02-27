-- File: polydriver.vhd
-- Generated by MyHDL 0.9.0
-- Date: Thu Feb  2 09:38:38 2017


library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;
use std.textio.all;

use work.pck_myhdl_090.all;

entity polydriver is
    port (
        clock: in std_logic;
        reset: in std_logic;
        photodiodepin: in std_logic;
        polypin: inout std_logic;
        laserpin: out std_logic;
        start: in std_logic;
        sdram_clk_o: out std_logic;
        sdram_clk_i: in std_logic;
        sdramCntl_inst_sd_intf_cke: out std_logic;
        sdramCntl_inst_sd_intf_we: out std_logic;
        sdramCntl_inst_sd_intf_addr: out unsigned(12 downto 0);
        sdramCntl_inst_sd_intf_dqml: out std_logic;
        sdramCntl_inst_sd_intf_cas: out std_logic;
        sdramCntl_inst_sd_intf_dqmh: out std_logic;
        sdramCntl_inst_sd_intf_ras: out std_logic;
        sdramCntl_inst_sd_intf_bs: out unsigned(1 downto 0);
        sdramCntl_inst_sd_intf_cs: out std_logic;
        sdramCntl_inst_sd_intf_dq: inout unsigned(15 downto 0)
    );
end entity polydriver;


architecture MyHDL of polydriver is


constant mode_c: integer := 48;
constant ba_len_c: integer := 2;
constant rp_cycles_c: integer := 2;
constant read_c: integer := 1;
constant ref_cycles_c: integer := 782;
constant ras_cycles_c: integer := 5;
constant mode_cmd_c: integer := 0;
constant rfsh_ops_c: integer := 8;
constant write_cmd_c: integer := 4;
constant row_len_c: integer := 13;
constant rfsh_cmd_c: integer := 1;
constant wr_cycles_c: integer := 2;
constant LOW_DIODE: integer := 16265;
constant rcd_cycles_c: integer := 2;
constant init_cycles_c: integer := 2000;
constant nop_cmd_c: integer := 7;
constant all_banks_c: integer := 2**9;
constant col_len_c: integer := 9;
constant output_c: integer := 1;
constant cas_cycles_c: integer := 3;
constant one_bank_c: integer := 0;
constant LOW_LASER: integer := 9036;
constant nop_c: integer := 0;
constant input_c: integer := 0;
constant read_cmd_c: integer := 5;
constant pchg_cmd_c: integer := 2;
constant mode_cycles_c: integer := 2;
constant active_cmd_c: integer := 3;
constant rfc_cycles_c: integer := 7;


type t_enum_cntlstatetype_1 is (
    INITWAIT,
    INITPCHG,
    INITSETMODE,
    INITRFSH,
    RW,
    ACTIVATE,
    REFRESHROW,
    SELFREFRESH
);

signal counter_photodiode: unsigned(16 downto 0);
signal host_intf_done_o: std_logic;
signal val: std_logic;
signal host_intf_data_o: unsigned(15 downto 0);
signal host_intf_wr_i: std_logic;
signal rd_enable: std_logic;
signal counter_line: unsigned(9 downto 0);
signal host_intf_data_i: unsigned(15 downto 0);
signal counter_polygon: unsigned(12 downto 0);
signal memreset: std_logic;
signal address: unsigned(26 downto 0);
signal counter_speed: unsigned(23 downto 0);
signal host_intf_rst_i: std_logic;
signal laserpin_mem: std_logic;
signal counter_value: unsigned(16 downto 0);
signal host_intf_rd_i: std_logic;
signal wr_enable: std_logic;
signal host_intf_addr_i: unsigned(23 downto 0);
signal sdramCntl_inst_cmd_r: unsigned(2 downto 0);
signal sdramCntl_inst_rdpipeline_r: unsigned(4 downto 0);
signal sdramCntl_inst_rfshcntr_x: unsigned(13 downto 0);
signal sdramCntl_inst_cmd_x: unsigned(2 downto 0);
signal sdramCntl_inst_rdpipeline_x: unsigned(4 downto 0);
signal sdramCntl_inst_row_s: unsigned(12 downto 0);
signal sdramCntl_inst_rfshcntr_r: unsigned(13 downto 0);
signal sdramCntl_inst_reftimer_x: unsigned(9 downto 0);
signal sdramCntl_inst_sdatadir_x: std_logic;
signal sdramCntl_inst_timer_r: unsigned(10 downto 0);
signal sdramCntl_inst_sdatadir_r: std_logic;
signal sdramCntl_inst_doactivate_s: std_logic;
signal sdramCntl_inst_ba_x: unsigned(1 downto 0);
signal sdramCntl_inst_wrtimer_x: unsigned(1 downto 0);
signal sdramCntl_inst_ba_r: unsigned(1 downto 0);
signal sdramCntl_inst_sdramdata_r: unsigned(15 downto 0);
signal sdramCntl_inst_sdata_r: unsigned(15 downto 0);
signal sdramCntl_inst_rd_in_progress_s: std_logic;
signal sdramCntl_inst_sdata_x: unsigned(15 downto 0);
signal sdramCntl_inst_wrpipeline_x: unsigned(4 downto 0);
signal sdramCntl_inst_bank_s: unsigned(1 downto 0);
signal sdramCntl_inst_wrtimer_r: unsigned(1 downto 0);
signal sdramCntl_inst_wrpipeline_r: unsigned(4 downto 0);
signal sdramCntl_inst_sdriver: unsigned(15 downto 0);
signal sdramCntl_inst_sdramdata_x: unsigned(15 downto 0);
signal sdramCntl_inst_state_x: t_enum_cntlstatetype_1;
signal sdramCntl_inst_rastimer_x: unsigned(2 downto 0);
signal sdramCntl_inst_col_s: unsigned(8 downto 0);
signal sdramCntl_inst_state_r: t_enum_cntlstatetype_1;
signal sdramCntl_inst_rastimer_r: unsigned(2 downto 0);
signal sdramCntl_inst_timer_x: unsigned(10 downto 0);
signal sdramCntl_inst_wr_in_progress_s: std_logic;
signal sdramCntl_inst_saddr_x: unsigned(12 downto 0);
signal sdramCntl_inst_host_intf_rdPending_o: std_logic;
signal sdramCntl_inst_reftimer_r: unsigned(9 downto 0);
signal sdramCntl_inst_saddr_r: unsigned(12 downto 0);
signal sdramCntl_inst_activate_in_progress_s: std_logic;
signal sdramCntl_inst_activebank_r: unsigned(1 downto 0);
signal sdramCntl_inst_activebank_x: unsigned(1 downto 0);
type t_array_sdramCntl_inst_activerow_x is array(0 to 4-1) of unsigned(12 downto 0);
signal sdramCntl_inst_activerow_x: t_array_sdramCntl_inst_activerow_x;
type t_array_sdramCntl_inst_activerow_r is array(0 to 4-1) of unsigned(12 downto 0);
signal sdramCntl_inst_activerow_r: t_array_sdramCntl_inst_activerow_r;
type t_array_sdramCntl_inst_activeflag_x is array(0 to 4-1) of std_logic;
signal sdramCntl_inst_activeflag_x: t_array_sdramCntl_inst_activeflag_x;
type t_array_sdramCntl_inst_activeflag_r is array(0 to 4-1) of std_logic;
signal sdramCntl_inst_activeflag_r: t_array_sdramCntl_inst_activeflag_r;

begin


val <= '0';
memreset <= '0';
wr_enable <= '0';

sdramCntl_inst_sd_intf_dq <= sdramCntl_inst_sdriver;


POLYDRIVER_POLYGEN: process (clock, reset) is
begin
    if (reset = '1') then
        counter_polygon <= to_unsigned(0, 13);
        polypin <= '0';
    elsif rising_edge(clock) then
        if (signed(resize(counter_polygon, 14)) >= (6000 - 1)) then
            counter_polygon <= to_unsigned(0, 13);
            polypin <= stdl((not bool(polypin)));
        else
            counter_polygon <= (counter_polygon + 1);
        end if;
    end if;
end process POLYDRIVER_POLYGEN;


POLYDRIVER_SDRAMCNTL_INST_COMB_FUNC: process (sdramCntl_inst_cmd_r, sdramCntl_inst_rdpipeline_r, sdramCntl_inst_rfshcntr_r, sdramCntl_inst_row_s, sdramCntl_inst_timer_r, sdramCntl_inst_sdatadir_r, sdramCntl_inst_doactivate_s, sdramCntl_inst_ba_x, sdramCntl_inst_ba_r, host_intf_wr_i, sdramCntl_inst_rd_in_progress_s, sdramCntl_inst_bank_s, sdramCntl_inst_wrtimer_r, sdramCntl_inst_col_s, sdramCntl_inst_state_r, sdramCntl_inst_rastimer_r, sdramCntl_inst_activeflag_r, sdramCntl_inst_activerow_r, sdramCntl_inst_reftimer_r, sdramCntl_inst_wr_in_progress_s, sdramCntl_inst_saddr_r, sdramCntl_inst_activate_in_progress_s, host_intf_rd_i, sdramCntl_inst_activebank_r) is
begin
    sdramCntl_inst_rdpipeline_x <= unsigned'('0' & sdramCntl_inst_rdpipeline_r((cas_cycles_c + 2)-1 downto 1));
    sdramCntl_inst_wrpipeline_x <= to_unsigned(0, 5);
    if (sdramCntl_inst_rastimer_r /= 0) then
        sdramCntl_inst_rastimer_x <= (sdramCntl_inst_rastimer_r - 1);
    else
        sdramCntl_inst_rastimer_x <= sdramCntl_inst_rastimer_r;
    end if;
    if (sdramCntl_inst_wrtimer_r /= 0) then
        sdramCntl_inst_wrtimer_x <= (sdramCntl_inst_wrtimer_r - 1);
    else
        sdramCntl_inst_wrtimer_x <= sdramCntl_inst_wrtimer_r;
    end if;
    if (sdramCntl_inst_reftimer_r /= 0) then
        sdramCntl_inst_reftimer_x <= (sdramCntl_inst_reftimer_r - 1);
        sdramCntl_inst_rfshcntr_x <= sdramCntl_inst_rfshcntr_r;
    else
        sdramCntl_inst_reftimer_x <= to_unsigned(ref_cycles_c, 10);
        sdramCntl_inst_rfshcntr_x <= (sdramCntl_inst_rfshcntr_r + 1);
    end if;
    sdramCntl_inst_cmd_x <= sdramCntl_inst_cmd_r;
    sdramCntl_inst_state_x <= sdramCntl_inst_state_r;
    sdramCntl_inst_saddr_x <= sdramCntl_inst_saddr_r;
    sdramCntl_inst_activebank_x <= sdramCntl_inst_activebank_r;
    sdramCntl_inst_sdatadir_x <= sdramCntl_inst_sdatadir_r;
    for index in 0 to (2 ** ba_len_c)-1 loop
        sdramCntl_inst_activeflag_x(index) <= sdramCntl_inst_activeflag_r(index);
        sdramCntl_inst_activerow_x(index) <= sdramCntl_inst_activerow_r(index);
    end loop;
    if (sdramCntl_inst_timer_r /= 0) then
        sdramCntl_inst_timer_x <= (sdramCntl_inst_timer_r - 1);
        sdramCntl_inst_cmd_x <= to_unsigned(nop_cmd_c, 3);
    else
        sdramCntl_inst_timer_x <= sdramCntl_inst_timer_r;
        case sdramCntl_inst_state_r is
            when INITWAIT =>
                sdramCntl_inst_timer_x <= to_unsigned(init_cycles_c, 11);
                sdramCntl_inst_state_x <= INITPCHG;
            when INITPCHG =>
                sdramCntl_inst_cmd_x <= to_unsigned(pchg_cmd_c, 3);
                sdramCntl_inst_timer_x <= to_unsigned(rp_cycles_c, 11);
                sdramCntl_inst_state_x <= INITRFSH;
                sdramCntl_inst_saddr_x <= to_unsigned(all_banks_c, 13);
                sdramCntl_inst_rfshcntr_x <= to_unsigned(rfsh_ops_c, 14);
            when INITRFSH =>
                sdramCntl_inst_cmd_x <= to_unsigned(rfsh_cmd_c, 3);
                sdramCntl_inst_timer_x <= to_unsigned(rfc_cycles_c, 11);
                sdramCntl_inst_rfshcntr_x <= (sdramCntl_inst_rfshcntr_r - 1);
                if (sdramCntl_inst_rfshcntr_r = 1) then
                    sdramCntl_inst_state_x <= INITSETMODE;
                end if;
            when INITSETMODE =>
                sdramCntl_inst_cmd_x <= to_unsigned(mode_cmd_c, 3);
                sdramCntl_inst_timer_x <= to_unsigned(mode_cycles_c, 11);
                sdramCntl_inst_state_x <= RW;
                sdramCntl_inst_saddr_x <= to_unsigned(mode_c, 13);
            when RW =>
                if (sdramCntl_inst_rfshcntr_r /= 0) then
                    if ((not bool(sdramCntl_inst_activate_in_progress_s)) and (not bool(sdramCntl_inst_wr_in_progress_s)) and (not bool(sdramCntl_inst_rd_in_progress_s))) then
                        sdramCntl_inst_cmd_x <= to_unsigned(pchg_cmd_c, 3);
                        sdramCntl_inst_timer_x <= to_unsigned(rp_cycles_c, 11);
                        sdramCntl_inst_state_x <= REFRESHROW;
                        sdramCntl_inst_saddr_x <= to_unsigned(all_banks_c, 13);
                        for index in 0 to (2 ** ba_len_c)-1 loop
                            sdramCntl_inst_activeflag_x(index) <= '0';
                        end loop;
                    end if;
                elsif bool(host_intf_rd_i) then
                    if (sdramCntl_inst_ba_x = sdramCntl_inst_ba_r) then
                        if bool(sdramCntl_inst_doactivate_s) then
                            if ((not bool(sdramCntl_inst_activate_in_progress_s)) and (not bool(sdramCntl_inst_wr_in_progress_s)) and (not bool(sdramCntl_inst_rd_in_progress_s))) then
                                sdramCntl_inst_cmd_x <= to_unsigned(pchg_cmd_c, 3);
                                sdramCntl_inst_timer_x <= to_unsigned(rp_cycles_c, 11);
                                sdramCntl_inst_state_x <= ACTIVATE;
                                sdramCntl_inst_saddr_x <= to_unsigned(one_bank_c, 13);
                                sdramCntl_inst_activeflag_x(to_integer(sdramCntl_inst_bank_s)) <= '0';
                            end if;
                        elsif (not bool(sdramCntl_inst_rd_in_progress_s)) then
                            sdramCntl_inst_cmd_x <= to_unsigned(read_cmd_c, 3);
                            sdramCntl_inst_sdatadir_x <= '0';
                            sdramCntl_inst_saddr_x <= resize(sdramCntl_inst_col_s, 13);
                            sdramCntl_inst_rdpipeline_x <= unsigned'('1' & sdramCntl_inst_rdpipeline_r((cas_cycles_c + 2)-1 downto 1));
                        end if;
                    end if;
                elsif bool(host_intf_wr_i) then
                    if (sdramCntl_inst_ba_x = sdramCntl_inst_ba_r) then
                        if bool(sdramCntl_inst_doactivate_s) then
                            if ((not bool(sdramCntl_inst_activate_in_progress_s)) and (not bool(sdramCntl_inst_wr_in_progress_s)) and (not bool(sdramCntl_inst_rd_in_progress_s))) then
                                sdramCntl_inst_cmd_x <= to_unsigned(pchg_cmd_c, 3);
                                sdramCntl_inst_timer_x <= to_unsigned(rp_cycles_c, 11);
                                sdramCntl_inst_state_x <= ACTIVATE;
                                sdramCntl_inst_saddr_x <= to_unsigned(one_bank_c, 13);
                                sdramCntl_inst_activeflag_x(to_integer(sdramCntl_inst_bank_s)) <= '0';
                            end if;
                        elsif (not bool(sdramCntl_inst_rd_in_progress_s)) then
                            sdramCntl_inst_cmd_x <= to_unsigned(write_cmd_c, 3);
                            sdramCntl_inst_sdatadir_x <= '1';
                            sdramCntl_inst_saddr_x <= resize(sdramCntl_inst_col_s, 13);
                            sdramCntl_inst_wrpipeline_x <= to_unsigned(1, 5);
                            sdramCntl_inst_wrtimer_x <= to_unsigned(wr_cycles_c, 2);
                        end if;
                    end if;
                else
                    sdramCntl_inst_cmd_x <= to_unsigned(nop_cmd_c, 3);
                    sdramCntl_inst_state_x <= RW;
                end if;
            when ACTIVATE =>
                sdramCntl_inst_cmd_x <= to_unsigned(active_cmd_c, 3);
                sdramCntl_inst_timer_x <= to_unsigned(rcd_cycles_c, 11);
                sdramCntl_inst_state_x <= RW;
                sdramCntl_inst_rastimer_x <= to_unsigned(ras_cycles_c, 3);
                sdramCntl_inst_saddr_x <= sdramCntl_inst_row_s;
                sdramCntl_inst_activebank_x <= sdramCntl_inst_bank_s;
                sdramCntl_inst_activerow_x(to_integer(sdramCntl_inst_bank_s)) <= sdramCntl_inst_row_s;
                sdramCntl_inst_activeflag_x(to_integer(sdramCntl_inst_bank_s)) <= '1';
            when REFRESHROW =>
                sdramCntl_inst_cmd_x <= to_unsigned(rfsh_cmd_c, 3);
                sdramCntl_inst_timer_x <= to_unsigned(rfc_cycles_c, 11);
                sdramCntl_inst_state_x <= RW;
                sdramCntl_inst_rfshcntr_x <= (sdramCntl_inst_rfshcntr_r - 1);
            when others =>
                sdramCntl_inst_state_x <= INITWAIT;
        end case;
    end if;
end process POLYDRIVER_SDRAMCNTL_INST_COMB_FUNC;


POLYDRIVER_SDRAMCNTL_INST_SEQ_FUNC: process (sdram_clk_i, host_intf_rst_i) is
begin
    if (host_intf_rst_i = '1') then
        sdramCntl_inst_activerow_r(0) <= to_unsigned(0, 13);
        sdramCntl_inst_activerow_r(1) <= to_unsigned(0, 13);
        sdramCntl_inst_activerow_r(2) <= to_unsigned(0, 13);
        sdramCntl_inst_activerow_r(3) <= to_unsigned(0, 13);
        sdramCntl_inst_cmd_r <= to_unsigned(7, 3);
        sdramCntl_inst_rdpipeline_r <= to_unsigned(0, 5);
        sdramCntl_inst_sdramdata_r <= to_unsigned(0, 16);
        sdramCntl_inst_ba_r <= to_unsigned(0, 2);
        sdramCntl_inst_wrpipeline_r <= to_unsigned(0, 5);
        sdramCntl_inst_sdata_r <= to_unsigned(0, 16);
        sdramCntl_inst_wrtimer_r <= to_unsigned(0, 2);
        sdramCntl_inst_rfshcntr_r <= to_unsigned(0, 14);
        sdramCntl_inst_saddr_r <= to_unsigned(0, 13);
        sdramCntl_inst_timer_r <= to_unsigned(0, 11);
        sdramCntl_inst_activebank_r <= to_unsigned(0, 2);
        sdramCntl_inst_reftimer_r <= to_unsigned(782, 10);
        sdramCntl_inst_state_r <= INITWAIT;
        sdramCntl_inst_rastimer_r <= to_unsigned(0, 3);
        sdramCntl_inst_sdatadir_r <= '0';
        sdramCntl_inst_activeflag_r(0) <= '0';
        sdramCntl_inst_activeflag_r(1) <= '0';
        sdramCntl_inst_activeflag_r(2) <= '0';
        sdramCntl_inst_activeflag_r(3) <= '0';
    elsif rising_edge(sdram_clk_i) then
        sdramCntl_inst_state_r <= sdramCntl_inst_state_x;
        sdramCntl_inst_cmd_r <= sdramCntl_inst_cmd_x;
        sdramCntl_inst_saddr_r <= sdramCntl_inst_saddr_x;
        sdramCntl_inst_sdata_r <= sdramCntl_inst_sdata_x;
        sdramCntl_inst_sdatadir_r <= sdramCntl_inst_sdatadir_x;
        sdramCntl_inst_activebank_r <= sdramCntl_inst_activebank_x;
        sdramCntl_inst_sdramdata_r <= sdramCntl_inst_sdramdata_x;
        sdramCntl_inst_wrpipeline_r <= sdramCntl_inst_wrpipeline_x;
        sdramCntl_inst_rdpipeline_r <= sdramCntl_inst_rdpipeline_x;
        sdramCntl_inst_ba_r <= sdramCntl_inst_ba_x;
        sdramCntl_inst_timer_r <= sdramCntl_inst_timer_x;
        sdramCntl_inst_rastimer_r <= sdramCntl_inst_rastimer_x;
        sdramCntl_inst_reftimer_r <= sdramCntl_inst_reftimer_x;
        sdramCntl_inst_wrtimer_r <= sdramCntl_inst_wrtimer_x;
        sdramCntl_inst_rfshcntr_r <= sdramCntl_inst_rfshcntr_x;
        for index in 0 to (2 ** ba_len_c)-1 loop
            sdramCntl_inst_activerow_r(index) <= sdramCntl_inst_activerow_x(index);
            sdramCntl_inst_activeflag_r(index) <= sdramCntl_inst_activeflag_x(index);
        end loop;
    end if;
end process POLYDRIVER_SDRAMCNTL_INST_SEQ_FUNC;


POLYDRIVER_SDRAMCNTL_INST_SDRAM_PIN_MAP: process (sdramCntl_inst_cmd_r, sdramCntl_inst_sdata_r, sdramCntl_inst_saddr_r, sdramCntl_inst_bank_s, sdramCntl_inst_sdatadir_r) is
begin
    sdramCntl_inst_sd_intf_cke <= '1';
    sdramCntl_inst_sd_intf_cs <= '0';
    sdramCntl_inst_sd_intf_ras <= sdramCntl_inst_cmd_r(2);
    sdramCntl_inst_sd_intf_cas <= sdramCntl_inst_cmd_r(1);
    sdramCntl_inst_sd_intf_we <= sdramCntl_inst_cmd_r(0);
    sdramCntl_inst_sd_intf_bs <= sdramCntl_inst_bank_s;
    sdramCntl_inst_sd_intf_addr <= sdramCntl_inst_saddr_r;
    if (sdramCntl_inst_sdatadir_r = '1') then
        sdramCntl_inst_sdriver <= sdramCntl_inst_sdata_r;
    else
        sdramCntl_inst_sdriver <= (others => 'Z');
    end if;
    sdramCntl_inst_sd_intf_dqml <= '0';
    sdramCntl_inst_sd_intf_dqmh <= '0';
end process POLYDRIVER_SDRAMCNTL_INST_SDRAM_PIN_MAP;



host_intf_done_o <= stdl(bool(sdramCntl_inst_rdpipeline_r(0)) or bool(sdramCntl_inst_wrpipeline_r(0)));
host_intf_data_o <= sdramCntl_inst_sdramdata_r;
sdramCntl_inst_host_intf_rdPending_o <= sdramCntl_inst_rd_in_progress_s;
sdramCntl_inst_sdata_x <= host_intf_data_i;



sdramCntl_inst_bank_s <= host_intf_addr_i(((ba_len_c + row_len_c) + col_len_c)-1 downto (row_len_c + col_len_c));
sdramCntl_inst_ba_x <= host_intf_addr_i(((ba_len_c + row_len_c) + col_len_c)-1 downto (row_len_c + col_len_c));
sdramCntl_inst_row_s <= host_intf_addr_i((row_len_c + col_len_c)-1 downto col_len_c);
sdramCntl_inst_col_s <= host_intf_addr_i(col_len_c-1 downto 0);


POLYDRIVER_SDRAMCNTL_INST_DO_ACTIVE: process (sdramCntl_inst_activerow_r, sdramCntl_inst_rdpipeline_r, sdramCntl_inst_bank_s, sdramCntl_inst_sdramdata_r, sdramCntl_inst_activebank_r, sdramCntl_inst_wrtimer_r, sdramCntl_inst_sd_intf_dq, sdramCntl_inst_row_s, sdramCntl_inst_rastimer_r, sdramCntl_inst_activeflag_r) is
begin
    if ((sdramCntl_inst_bank_s /= sdramCntl_inst_activebank_r) or (sdramCntl_inst_row_s /= sdramCntl_inst_activerow_r(to_integer(sdramCntl_inst_bank_s))) or (not bool(sdramCntl_inst_activeflag_r(to_integer(sdramCntl_inst_bank_s))))) then
        sdramCntl_inst_doactivate_s <= '1';
    else
        sdramCntl_inst_doactivate_s <= '0';
    end if;
    if (sdramCntl_inst_rdpipeline_r(1) = '1') then
        sdramCntl_inst_sdramdata_x <= sdramCntl_inst_sd_intf_dq;
    else
        sdramCntl_inst_sdramdata_x <= sdramCntl_inst_sdramdata_r;
    end if;
    if (sdramCntl_inst_rastimer_r /= 0) then
        sdramCntl_inst_activate_in_progress_s <= '1';
    else
        sdramCntl_inst_activate_in_progress_s <= '0';
    end if;
    if (sdramCntl_inst_wrtimer_r /= 0) then
        sdramCntl_inst_wr_in_progress_s <= '1';
    else
        sdramCntl_inst_wr_in_progress_s <= '0';
    end if;
    if (sdramCntl_inst_rdpipeline_r((cas_cycles_c + 2)-1 downto 1) /= 0) then
        sdramCntl_inst_rd_in_progress_s <= '1';
    else
        sdramCntl_inst_rd_in_progress_s <= '0';
    end if;
end process POLYDRIVER_SDRAMCNTL_INST_DO_ACTIVE;


POLYDRIVER_SDRAM_READER: process (sdram_clk_i) is
begin
    if rising_edge(sdram_clk_i) then
        if (start = '0') then
            laserpin_mem <= '0';
        else
            if (host_intf_done_o = '0') then
                rd_enable <= '1';
            else
                rd_enable <= '0';
                address(5-1 downto 0) <= counter_photodiode(15-1 downto 10);
                address(15-1 downto 5) <= counter_line;
                address(27-1 downto 15) <= to_unsigned(0, 12);
                laserpin_mem <= host_intf_data_o(0);
            end if;
        end if;
    end if;
end process POLYDRIVER_SDRAM_READER;



sdram_clk_o <= clock;



host_intf_rst_i <= memreset;
host_intf_wr_i <= stdl(bool(wr_enable) and (not bool(host_intf_done_o)));
host_intf_rd_i <= stdl(bool(rd_enable) and (not bool(host_intf_done_o)));
host_intf_data_i <= to_unsigned(val, 16);
host_intf_addr_i <= resize(address, 24);


POLYDRIVER_LINECOUNT: process (clock) is
begin
    if rising_edge(clock) then
        if (reset = '1') then
            counter_line <= to_unsigned(0, 10);
        else
            if (signed(resize(counter_speed, 25)) >= (12000000 - 1)) then
                counter_speed <= to_unsigned(0, 24);
                if (signed(resize(counter_line, 11)) >= (1000 - 1)) then
                    counter_line <= counter_line;
                else
                    counter_line <= (counter_line + 1);
                end if;
            else
                counter_speed <= (counter_speed + 1);
            end if;
        end if;
    end if;
end process POLYDRIVER_LINECOUNT;


POLYDRIVER_COUNT: process (clock, reset) is
begin
    if (reset = '1') then
        counter_photodiode <= to_unsigned(0, 17);
        counter_value <= to_unsigned(0, 17);
    elsif rising_edge(clock) then
        if ((photodiodepin = '1') and (counter_photodiode > LOW_DIODE)) then
            counter_value <= counter_photodiode;
            counter_photodiode <= to_unsigned(0, 17);
        elsif (signed(resize(counter_photodiode, 18)) >= (120000 - 1)) then
            counter_photodiode <= to_unsigned(0, 17);
        else
            counter_photodiode <= (counter_photodiode + 1);
        end if;
    end if;
end process POLYDRIVER_COUNT;


POLYDRIVER_SWITCHLASER: process (reset, laserpin_mem, counter_photodiode, counter_value) is
begin
    if (reset = '1') then
        laserpin <= '0';
    else
        if (counter_photodiode < LOW_LASER) then
            laserpin <= '0';
        else
            if (signed(resize(counter_photodiode, 18)) >= (signed(resize(counter_value, 18)) - signed(shift_right(resize(counter_value, 18), 10)))) then
                laserpin <= '1';
            else
                laserpin <= laserpin_mem;
            end if;
        end if;
    end if;
end process POLYDRIVER_SWITCHLASER;

end architecture MyHDL;