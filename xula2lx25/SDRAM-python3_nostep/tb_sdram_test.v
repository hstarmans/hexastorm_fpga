module tb_sdram_test;

reg master_clk_i;
wire sdram_clk_o;
reg sdram_clk_i;
wire led;
wire sdram_cntl_1_sd_intf_cs;
wire sdram_cntl_1_sd_intf_cas;
wire [1:0] sdram_cntl_1_sd_intf_bs;
wire sdram_cntl_1_sd_intf_we;
wire sdram_cntl_1_sd_intf_dqmh;
wire [12:0] sdram_cntl_1_sd_intf_addr;
wire sdram_cntl_1_sd_intf_ras;
wire sdram_cntl_1_sd_intf_dqml;
wire [15:0] sdram_cntl_1_sd_intf_dq;
wire sdram_cntl_1_sd_intf_cke;

initial begin
    $from_myhdl(
        master_clk_i,
        sdram_clk_i
    );
    $to_myhdl(
        sdram_clk_o,
        led,
        sdram_cntl_1_sd_intf_cs,
        sdram_cntl_1_sd_intf_cas,
        sdram_cntl_1_sd_intf_bs,
        sdram_cntl_1_sd_intf_we,
        sdram_cntl_1_sd_intf_dqmh,
        sdram_cntl_1_sd_intf_addr,
        sdram_cntl_1_sd_intf_ras,
        sdram_cntl_1_sd_intf_dqml,
        sdram_cntl_1_sd_intf_dq,
        sdram_cntl_1_sd_intf_cke
    );
end

sdram_test dut(
    master_clk_i,
    sdram_clk_o,
    sdram_clk_i,
    led,
    sdram_cntl_1_sd_intf_cs,
    sdram_cntl_1_sd_intf_cas,
    sdram_cntl_1_sd_intf_bs,
    sdram_cntl_1_sd_intf_we,
    sdram_cntl_1_sd_intf_dqmh,
    sdram_cntl_1_sd_intf_addr,
    sdram_cntl_1_sd_intf_ras,
    sdram_cntl_1_sd_intf_dqml,
    sdram_cntl_1_sd_intf_dq,
    sdram_cntl_1_sd_intf_cke
);

endmodule
