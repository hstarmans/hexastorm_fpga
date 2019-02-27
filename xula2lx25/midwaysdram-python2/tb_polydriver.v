module tb_polydriver;

reg clock;
reg reset;
reg photodiodepin;
wire polypin;
wire laserpin;
reg start;
wire sdram_clk_o;
reg sdram_clk_i;

initial begin
    $from_myhdl(
        clock,
        reset,
        photodiodepin,
        start,
        sdram_clk_i
    );
    $to_myhdl(
        polypin,
        laserpin,
        sdram_clk_o
    );
end

polydriver dut(
    clock,
    reset,
    photodiodepin,
    polypin,
    laserpin,
    start,
    sdram_clk_o,
    sdram_clk_i
);

endmodule
