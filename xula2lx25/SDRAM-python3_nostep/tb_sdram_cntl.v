module tb_sdram_cntl;

reg clk_i;
reg host_intf_rd_i;
wire host_intf_rdPending_o;
reg host_intf_wr_i;
reg [23:0] host_intf_addr_i;
wire host_intf_done_o;
wire [15:0] host_intf_data_o;
reg [15:0] host_intf_data_i;
reg host_intf_rst_i;
wire sd_intf_cke;
wire sd_intf_we;
wire sd_intf_ras;
wire [12:0] sd_intf_addr;
wire [1:0] sd_intf_bs;
wire [15:0] sd_intf_dq;
wire sd_intf_cs;
wire sd_intf_dqml;
wire sd_intf_dqmh;
wire sd_intf_cas;

initial begin
    $from_myhdl(
        clk_i,
        host_intf_rd_i,
        host_intf_wr_i,
        host_intf_addr_i,
        host_intf_data_i,
        host_intf_rst_i
    );
    $to_myhdl(
        host_intf_rdPending_o,
        host_intf_done_o,
        host_intf_data_o,
        sd_intf_cke,
        sd_intf_we,
        sd_intf_ras,
        sd_intf_addr,
        sd_intf_bs,
        sd_intf_dq,
        sd_intf_cs,
        sd_intf_dqml,
        sd_intf_dqmh,
        sd_intf_cas
    );
end

sdram_cntl dut(
    clk_i,
    host_intf_rd_i,
    host_intf_rdPending_o,
    host_intf_wr_i,
    host_intf_addr_i,
    host_intf_done_o,
    host_intf_data_o,
    host_intf_data_i,
    host_intf_rst_i,
    sd_intf_cke,
    sd_intf_we,
    sd_intf_ras,
    sd_intf_addr,
    sd_intf_bs,
    sd_intf_dq,
    sd_intf_cs,
    sd_intf_dqml,
    sd_intf_dqmh,
    sd_intf_cas
);

endmodule
