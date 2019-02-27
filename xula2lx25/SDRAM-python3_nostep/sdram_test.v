// File: sdram_test.v
// Generated by MyHDL 1.0dev
// Date: Mon Jan  9 16:32:17 2017


`timescale 1ns/10ps

module sdram_test (
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


input master_clk_i;
output sdram_clk_o;
wire sdram_clk_o;
input sdram_clk_i;
output led;
reg led;
output sdram_cntl_1_sd_intf_cs;
reg sdram_cntl_1_sd_intf_cs;
output sdram_cntl_1_sd_intf_cas;
reg sdram_cntl_1_sd_intf_cas;
output [1:0] sdram_cntl_1_sd_intf_bs;
reg [1:0] sdram_cntl_1_sd_intf_bs;
output sdram_cntl_1_sd_intf_we;
reg sdram_cntl_1_sd_intf_we;
output sdram_cntl_1_sd_intf_dqmh;
reg sdram_cntl_1_sd_intf_dqmh;
output [12:0] sdram_cntl_1_sd_intf_addr;
reg [12:0] sdram_cntl_1_sd_intf_addr;
output sdram_cntl_1_sd_intf_ras;
reg sdram_cntl_1_sd_intf_ras;
output sdram_cntl_1_sd_intf_dqml;
reg sdram_cntl_1_sd_intf_dqml;
inout [15:0] sdram_cntl_1_sd_intf_dq;
wire [15:0] sdram_cntl_1_sd_intf_dq;
output sdram_cntl_1_sd_intf_cke;
reg sdram_cntl_1_sd_intf_cke;

wire clk;
wire [15:0] memory_test_1_host_intf_data_o;
wire memory_test_1_wr_enable;
wire memory_test_1_host_intf_done_o;
reg memory_test_1_rd_enable;
wire memory_test_1_reset;
reg [26:0] memory_test_1_address;
wire memory_test_1_host_intf_rst_i;
wire memory_test_1_host_intf_rd_i;
wire memory_test_1_val;
wire memory_test_1_host_intf_wr_i;
wire [23:0] memory_test_1_host_intf_addr_i;
wire [15:0] memory_test_1_host_intf_data_i;
wire [15:0] sdram_cntl_1_sdata_x;
reg [1:0] sdram_cntl_1_activebank_x;
reg sdram_cntl_1_sdatadir_x;
reg [0:0] sdram_cntl_1_reftimer_x;
reg [4:0] sdram_cntl_1_rdpipeline_x;
reg [4:0] sdram_cntl_1_wrpipeline_r;
reg [2:0] sdram_cntl_1_state_r;
reg sdram_cntl_1_sdatadir_r;
reg sdram_cntl_1_activate_in_progress_s;
reg sdram_cntl_1_wr_in_progress_s;
reg [1:0] sdram_cntl_1_activebank_r;
reg [13:0] sdram_cntl_1_rfshcntr_x;
reg [0:0] sdram_cntl_1_reftimer_r;
reg [15:0] sdram_cntl_1_sdata_r;
wire [8:0] sdram_cntl_1_col_s;
reg [4:0] sdram_cntl_1_wrpipeline_x;
reg [1:0] sdram_cntl_1_wrtimer_r;
reg [0:0] sdram_cntl_1_timer_r;
reg [1:0] sdram_cntl_1_wrtimer_x;
reg [4:0] sdram_cntl_1_rdpipeline_r;
reg [13:0] sdram_cntl_1_rfshcntr_r;
wire [12:0] sdram_cntl_1_row_s;
reg [1:0] sdram_cntl_1_ba_r;
reg [2:0] sdram_cntl_1_state_x;
reg [15:0] sdram_cntl_1_sdramdata_r;
wire [1:0] sdram_cntl_1_ba_x;
wire [1:0] sdram_cntl_1_bank_s;
reg [0:0] sdram_cntl_1_rastimer_r;
reg [15:0] sdram_cntl_1_sdriver;
reg [12:0] sdram_cntl_1_saddr_x;
reg [0:0] sdram_cntl_1_timer_x;
reg [2:0] sdram_cntl_1_cmd_r;
reg [15:0] sdram_cntl_1_sdramdata_x;
reg [12:0] sdram_cntl_1_saddr_r;
reg [0:0] sdram_cntl_1_rastimer_x;
reg [2:0] sdram_cntl_1_cmd_x;
reg sdram_cntl_1_rd_in_progress_s;
reg sdram_cntl_1_doactivate_s;
wire sdram_cntl_1_host_intf_rdPending_o;
reg sdram_cntl_1_activeflag_r [0:4-1];
reg sdram_cntl_1_activeflag_x [0:4-1];
reg [12:0] sdram_cntl_1_activerow_x [0:4-1];
reg [12:0] sdram_cntl_1_activerow_r [0:4-1];

assign memory_test_1_wr_enable = 1'd0;
assign memory_test_1_reset = 1'd0;
assign memory_test_1_val = 1'd0;
assign sdram_cntl_1_sd_intf_dq = sdram_cntl_1_sdriver;


always @(posedge clk) begin: SDRAM_TEST_MEMORY_TEST_1_SDRAM_TESTER
    if ((memory_test_1_host_intf_done_o == 0)) begin
        memory_test_1_rd_enable <= 1'b1;
    end
    else begin
        memory_test_1_address <= 1;
        if ((0 == memory_test_1_host_intf_data_o)) begin
            led <= 1;
        end
        else begin
            led <= 0;
        end
    end
end



assign memory_test_1_host_intf_rst_i = memory_test_1_reset;
assign memory_test_1_host_intf_wr_i = (memory_test_1_wr_enable && (!memory_test_1_host_intf_done_o));
assign memory_test_1_host_intf_rd_i = (memory_test_1_rd_enable && (!memory_test_1_host_intf_done_o));
assign memory_test_1_host_intf_data_i = memory_test_1_val;
assign memory_test_1_host_intf_addr_i = memory_test_1_address;



assign sdram_clk_o = master_clk_i;
assign clk = sdram_clk_i;


always @(sdram_cntl_1_rdpipeline_r, sdram_cntl_1_activeflag_r[0], sdram_cntl_1_activeflag_r[1], sdram_cntl_1_activeflag_r[2], sdram_cntl_1_activeflag_r[3], sdram_cntl_1_state_r, sdram_cntl_1_wrtimer_r, sdram_cntl_1_activate_in_progress_s, sdram_cntl_1_wr_in_progress_s, sdram_cntl_1_doactivate_s, sdram_cntl_1_reftimer_r, sdram_cntl_1_activebank_r, memory_test_1_host_intf_rd_i, sdram_cntl_1_col_s, sdram_cntl_1_timer_r, sdram_cntl_1_sdatadir_r, sdram_cntl_1_cmd_r, sdram_cntl_1_rfshcntr_r, sdram_cntl_1_row_s, sdram_cntl_1_ba_r, sdram_cntl_1_ba_x, sdram_cntl_1_bank_s, sdram_cntl_1_rastimer_r, sdram_cntl_1_saddr_r, memory_test_1_host_intf_wr_i, sdram_cntl_1_rd_in_progress_s, sdram_cntl_1_activerow_r[0], sdram_cntl_1_activerow_r[1], sdram_cntl_1_activerow_r[2], sdram_cntl_1_activerow_r[3]) begin: SDRAM_TEST_SDRAM_CNTL_1_COMB_FUNC
    integer index;
    sdram_cntl_1_rdpipeline_x = {1'b0, sdram_cntl_1_rdpipeline_r[(3 + 2)-1:1]};
    sdram_cntl_1_wrpipeline_x = 5'h0;
    if ((sdram_cntl_1_rastimer_r != 0)) begin
        sdram_cntl_1_rastimer_x = (sdram_cntl_1_rastimer_r - 1);
    end
    else begin
        sdram_cntl_1_rastimer_x = sdram_cntl_1_rastimer_r;
    end
    if ((sdram_cntl_1_wrtimer_r != 0)) begin
        sdram_cntl_1_wrtimer_x = (sdram_cntl_1_wrtimer_r - 1);
    end
    else begin
        sdram_cntl_1_wrtimer_x = sdram_cntl_1_wrtimer_r;
    end
    if ((sdram_cntl_1_reftimer_r != 0)) begin
        sdram_cntl_1_reftimer_x = (sdram_cntl_1_reftimer_r - 1);
        sdram_cntl_1_rfshcntr_x = sdram_cntl_1_rfshcntr_r;
    end
    else begin
        sdram_cntl_1_reftimer_x = 0;
        sdram_cntl_1_rfshcntr_x = (sdram_cntl_1_rfshcntr_r + 1);
    end
    sdram_cntl_1_cmd_x = sdram_cntl_1_cmd_r;
    sdram_cntl_1_state_x = sdram_cntl_1_state_r;
    sdram_cntl_1_saddr_x = sdram_cntl_1_saddr_r;
    sdram_cntl_1_activebank_x = sdram_cntl_1_activebank_r;
    sdram_cntl_1_sdatadir_x = sdram_cntl_1_sdatadir_r;
    for (index=0; index<(2 ** 2); index=index+1) begin
        sdram_cntl_1_activeflag_x[index] = sdram_cntl_1_activeflag_r[index];
        sdram_cntl_1_activerow_x[index] = sdram_cntl_1_activerow_r[index];
    end
    if ((sdram_cntl_1_timer_r != 0)) begin
        sdram_cntl_1_timer_x = (sdram_cntl_1_timer_r - 1);
        sdram_cntl_1_cmd_x = 7;
    end
    else begin
        sdram_cntl_1_timer_x = sdram_cntl_1_timer_r;
        case (sdram_cntl_1_state_r)
            3'b000: begin
                sdram_cntl_1_timer_x = 0;
                sdram_cntl_1_state_x = 3'b001;
            end
            3'b001: begin
                sdram_cntl_1_cmd_x = 2;
                sdram_cntl_1_timer_x = 0;
                sdram_cntl_1_state_x = 3'b011;
                sdram_cntl_1_saddr_x = 512;
                sdram_cntl_1_rfshcntr_x = 8;
            end
            3'b011: begin
                sdram_cntl_1_cmd_x = 1;
                sdram_cntl_1_timer_x = 0;
                sdram_cntl_1_rfshcntr_x = (sdram_cntl_1_rfshcntr_r - 1);
                if ((sdram_cntl_1_rfshcntr_r == 1)) begin
                    sdram_cntl_1_state_x = 3'b010;
                end
            end
            3'b010: begin
                sdram_cntl_1_cmd_x = 0;
                sdram_cntl_1_timer_x = 2;
                sdram_cntl_1_state_x = 3'b100;
                sdram_cntl_1_saddr_x = 48;
            end
            3'b100: begin
                if ((sdram_cntl_1_rfshcntr_r != 0)) begin
                    if (((!sdram_cntl_1_activate_in_progress_s) && (!sdram_cntl_1_wr_in_progress_s) && (!sdram_cntl_1_rd_in_progress_s))) begin
                        sdram_cntl_1_cmd_x = 2;
                        sdram_cntl_1_timer_x = 0;
                        sdram_cntl_1_state_x = 3'b110;
                        sdram_cntl_1_saddr_x = 512;
                        for (index=0; index<(2 ** 2); index=index+1) begin
                            sdram_cntl_1_activeflag_x[index] = 1'b0;
                        end
                    end
                end
                else if (memory_test_1_host_intf_rd_i) begin
                    if ((sdram_cntl_1_ba_x == sdram_cntl_1_ba_r)) begin
                        if (sdram_cntl_1_doactivate_s) begin
                            if (((!sdram_cntl_1_activate_in_progress_s) && (!sdram_cntl_1_wr_in_progress_s) && (!sdram_cntl_1_rd_in_progress_s))) begin
                                sdram_cntl_1_cmd_x = 2;
                                sdram_cntl_1_timer_x = 0;
                                sdram_cntl_1_state_x = 3'b101;
                                sdram_cntl_1_saddr_x = 0;
                                sdram_cntl_1_activeflag_x[sdram_cntl_1_bank_s] = 1'b0;
                            end
                        end
                        else if ((!sdram_cntl_1_rd_in_progress_s)) begin
                            sdram_cntl_1_cmd_x = 5;
                            sdram_cntl_1_sdatadir_x = 1'b0;
                            sdram_cntl_1_saddr_x = sdram_cntl_1_col_s;
                            sdram_cntl_1_rdpipeline_x = {1'b1, sdram_cntl_1_rdpipeline_r[(3 + 2)-1:1]};
                        end
                    end
                end
                else if (memory_test_1_host_intf_wr_i) begin
                    if ((sdram_cntl_1_ba_x == sdram_cntl_1_ba_r)) begin
                        if (sdram_cntl_1_doactivate_s) begin
                            if (((!sdram_cntl_1_activate_in_progress_s) && (!sdram_cntl_1_wr_in_progress_s) && (!sdram_cntl_1_rd_in_progress_s))) begin
                                sdram_cntl_1_cmd_x = 2;
                                sdram_cntl_1_timer_x = 0;
                                sdram_cntl_1_state_x = 3'b101;
                                sdram_cntl_1_saddr_x = 0;
                                sdram_cntl_1_activeflag_x[sdram_cntl_1_bank_s] = 1'b0;
                            end
                        end
                        else if ((!sdram_cntl_1_rd_in_progress_s)) begin
                            sdram_cntl_1_cmd_x = 4;
                            sdram_cntl_1_sdatadir_x = 1'b1;
                            sdram_cntl_1_saddr_x = sdram_cntl_1_col_s;
                            sdram_cntl_1_wrpipeline_x = 5'h1;
                            sdram_cntl_1_wrtimer_x = 2;
                        end
                    end
                end
                else begin
                    sdram_cntl_1_cmd_x = 7;
                    sdram_cntl_1_state_x = 3'b100;
                end
            end
            3'b101: begin
                sdram_cntl_1_cmd_x = 3;
                sdram_cntl_1_timer_x = 0;
                sdram_cntl_1_state_x = 3'b100;
                sdram_cntl_1_rastimer_x = 0;
                sdram_cntl_1_saddr_x = sdram_cntl_1_row_s;
                sdram_cntl_1_activebank_x = sdram_cntl_1_bank_s;
                sdram_cntl_1_activerow_x[sdram_cntl_1_bank_s] = sdram_cntl_1_row_s;
                sdram_cntl_1_activeflag_x[sdram_cntl_1_bank_s] = 1'b1;
            end
            3'b110: begin
                sdram_cntl_1_cmd_x = 1;
                sdram_cntl_1_timer_x = 0;
                sdram_cntl_1_state_x = 3'b100;
                sdram_cntl_1_rfshcntr_x = (sdram_cntl_1_rfshcntr_r - 1);
            end
            default: begin
                sdram_cntl_1_state_x = 3'b000;
            end
        endcase
    end
end


always @(posedge clk, posedge memory_test_1_host_intf_rst_i) begin: SDRAM_TEST_SDRAM_CNTL_1_SEQ_FUNC
    integer index;
    if (memory_test_1_host_intf_rst_i == 1) begin
        sdram_cntl_1_wrpipeline_r <= 0;
        sdram_cntl_1_rfshcntr_r <= 0;
        sdram_cntl_1_saddr_r <= 0;
        sdram_cntl_1_rdpipeline_r <= 0;
        sdram_cntl_1_reftimer_r <= 0;
        sdram_cntl_1_ba_r <= 0;
        sdram_cntl_1_activebank_r <= 0;
        sdram_cntl_1_sdata_r <= 0;
        sdram_cntl_1_activeflag_r[0] <= 0;
        sdram_cntl_1_activeflag_r[1] <= 0;
        sdram_cntl_1_activeflag_r[2] <= 0;
        sdram_cntl_1_activeflag_r[3] <= 0;
        sdram_cntl_1_sdramdata_r <= 0;
        sdram_cntl_1_activerow_r[0] <= 0;
        sdram_cntl_1_activerow_r[1] <= 0;
        sdram_cntl_1_activerow_r[2] <= 0;
        sdram_cntl_1_activerow_r[3] <= 0;
        sdram_cntl_1_sdatadir_r <= 0;
        sdram_cntl_1_rastimer_r <= 0;
        sdram_cntl_1_cmd_r <= 7;
        sdram_cntl_1_state_r <= 3'b000;
        sdram_cntl_1_wrtimer_r <= 0;
        sdram_cntl_1_timer_r <= 0;
    end
    else begin
        sdram_cntl_1_state_r <= sdram_cntl_1_state_x;
        sdram_cntl_1_cmd_r <= sdram_cntl_1_cmd_x;
        sdram_cntl_1_saddr_r <= sdram_cntl_1_saddr_x;
        sdram_cntl_1_sdata_r <= sdram_cntl_1_sdata_x;
        sdram_cntl_1_sdatadir_r <= sdram_cntl_1_sdatadir_x;
        sdram_cntl_1_activebank_r <= sdram_cntl_1_activebank_x;
        sdram_cntl_1_sdramdata_r <= sdram_cntl_1_sdramdata_x;
        sdram_cntl_1_wrpipeline_r <= sdram_cntl_1_wrpipeline_x;
        sdram_cntl_1_rdpipeline_r <= sdram_cntl_1_rdpipeline_x;
        sdram_cntl_1_ba_r <= sdram_cntl_1_ba_x;
        sdram_cntl_1_timer_r <= sdram_cntl_1_timer_x;
        sdram_cntl_1_rastimer_r <= sdram_cntl_1_rastimer_x;
        sdram_cntl_1_reftimer_r <= sdram_cntl_1_reftimer_x;
        sdram_cntl_1_wrtimer_r <= sdram_cntl_1_wrtimer_x;
        sdram_cntl_1_rfshcntr_r <= sdram_cntl_1_rfshcntr_x;
        for (index=0; index<(2 ** 2); index=index+1) begin
            sdram_cntl_1_activerow_r[index] <= sdram_cntl_1_activerow_x[index];
            sdram_cntl_1_activeflag_r[index] <= sdram_cntl_1_activeflag_x[index];
        end
    end
end


always @(sdram_cntl_1_sdatadir_r, sdram_cntl_1_sdata_r, sdram_cntl_1_saddr_r, sdram_cntl_1_cmd_r, sdram_cntl_1_bank_s) begin: SDRAM_TEST_SDRAM_CNTL_1_SDRAM_PIN_MAP
    sdram_cntl_1_sd_intf_cke = 1;
    sdram_cntl_1_sd_intf_cs = 0;
    sdram_cntl_1_sd_intf_ras = sdram_cntl_1_cmd_r[2];
    sdram_cntl_1_sd_intf_cas = sdram_cntl_1_cmd_r[1];
    sdram_cntl_1_sd_intf_we = sdram_cntl_1_cmd_r[0];
    sdram_cntl_1_sd_intf_bs = sdram_cntl_1_bank_s;
    sdram_cntl_1_sd_intf_addr = sdram_cntl_1_saddr_r;
    if ((sdram_cntl_1_sdatadir_r == 1'b1)) begin
        sdram_cntl_1_sdriver = sdram_cntl_1_sdata_r;
    end
    else begin
        sdram_cntl_1_sdriver = 'bz;
    end
    sdram_cntl_1_sd_intf_dqml = 0;
    sdram_cntl_1_sd_intf_dqmh = 0;
end



assign memory_test_1_host_intf_done_o = (sdram_cntl_1_rdpipeline_r[0] || sdram_cntl_1_wrpipeline_r[0]);
assign memory_test_1_host_intf_data_o = sdram_cntl_1_sdramdata_r;
assign sdram_cntl_1_host_intf_rdPending_o = sdram_cntl_1_rd_in_progress_s;
assign sdram_cntl_1_sdata_x = memory_test_1_host_intf_data_i;



assign sdram_cntl_1_bank_s = memory_test_1_host_intf_addr_i[((2 + 13) + 9)-1:(13 + 9)];
assign sdram_cntl_1_ba_x = memory_test_1_host_intf_addr_i[((2 + 13) + 9)-1:(13 + 9)];
assign sdram_cntl_1_row_s = memory_test_1_host_intf_addr_i[(13 + 9)-1:9];
assign sdram_cntl_1_col_s = memory_test_1_host_intf_addr_i[9-1:0];


always @(sdram_cntl_1_rdpipeline_r, sdram_cntl_1_row_s, sdram_cntl_1_activebank_r, sdram_cntl_1_activeflag_r[0], sdram_cntl_1_activeflag_r[1], sdram_cntl_1_activeflag_r[2], sdram_cntl_1_activeflag_r[3], sdram_cntl_1_sd_intf_dq, sdram_cntl_1_sdramdata_r, sdram_cntl_1_bank_s, sdram_cntl_1_rastimer_r, sdram_cntl_1_wrtimer_r, sdram_cntl_1_activerow_r[0], sdram_cntl_1_activerow_r[1], sdram_cntl_1_activerow_r[2], sdram_cntl_1_activerow_r[3]) begin: SDRAM_TEST_SDRAM_CNTL_1_DO_ACTIVE
    if (((sdram_cntl_1_bank_s != sdram_cntl_1_activebank_r) || (sdram_cntl_1_row_s != sdram_cntl_1_activerow_r[sdram_cntl_1_bank_s]) || (!sdram_cntl_1_activeflag_r[sdram_cntl_1_bank_s]))) begin
        sdram_cntl_1_doactivate_s = 1'b1;
    end
    else begin
        sdram_cntl_1_doactivate_s = 1'b0;
    end
    if ((sdram_cntl_1_rdpipeline_r[1] == 1'b1)) begin
        sdram_cntl_1_sdramdata_x = sdram_cntl_1_sd_intf_dq;
    end
    else begin
        sdram_cntl_1_sdramdata_x = sdram_cntl_1_sdramdata_r;
    end
    if ((sdram_cntl_1_rastimer_r != 0)) begin
        sdram_cntl_1_activate_in_progress_s = 1'b1;
    end
    else begin
        sdram_cntl_1_activate_in_progress_s = 1'b0;
    end
    if ((sdram_cntl_1_wrtimer_r != 0)) begin
        sdram_cntl_1_wr_in_progress_s = 1'b1;
    end
    else begin
        sdram_cntl_1_wr_in_progress_s = 1'b0;
    end
    if ((sdram_cntl_1_rdpipeline_r[(3 + 2)-1:1] != 0)) begin
        sdram_cntl_1_rd_in_progress_s = 1'b1;
    end
    else begin
        sdram_cntl_1_rd_in_progress_s = 1'b0;
    end
end

endmodule
