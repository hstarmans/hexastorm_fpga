module tb_sdramtest;

reg clock;

initial begin
    $from_myhdl(
        clock
    );
end

sdramtest dut(
    clock
);

endmodule
