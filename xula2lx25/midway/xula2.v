// File: xula2.v
// Generated by MyHDL 1.0dev
// Date: Thu Oct 12 12:56:31 2017


`timescale 1ns/10ps

module xula2 (
    clock,
    photodiodepin,
    polypin,
    laserpin,
    enable,
    reset
);


input clock;
input photodiodepin;
output polypin;
reg polypin;
output laserpin;
reg laserpin;
input enable;
input reset;

reg [13:0] counter_polygon;
reg [0:0] counter;
reg [15:0] counter_photodiode;



always @(posedge clock, posedge reset) begin: XULA2_POLYGEN
    if (reset == 1) begin
        counter_polygon <= 0;
        polypin <= 0;
    end
    else begin
        if (($signed({1'b0, counter_polygon}) >= (15000 - 1))) begin
            counter_polygon <= 0;
            polypin <= (!polypin);
        end
        else begin
            counter_polygon <= (counter_polygon + 1);
        end
    end
end


always @(reset, counter_photodiode, enable) begin: XULA2_SWITCHLASER
    if ((reset == 1)) begin
        laserpin = 0;
    end
    else if (((9000 < counter_photodiode) && ((counter_photodiode < 40500) && enable))) begin
        laserpin = 1;
    end
    else if (($signed({1'b0, counter_photodiode}) >= (45000 - (45000 >>> 7)))) begin
        laserpin = 1;
    end
    else begin
        laserpin = 0;
    end
end


always @(posedge clock, posedge reset) begin: XULA2_COUNT
    if (reset == 1) begin
        counter <= 0;
        counter_photodiode <= 0;
    end
    else begin
        if (($signed({1'b0, counter_photodiode}) >= (45000 - 1))) begin
            counter_photodiode <= 0;
        end
        else if (((photodiodepin == 1) && (counter_photodiode > 42750))) begin
            counter <= (counter + 1);
            counter_photodiode <= (counter_photodiode + 1);
            if ((counter > 0)) begin
                counter_photodiode <= 0;
                counter <= 0;
            end
        end
        else begin
            counter_photodiode <= (counter_photodiode + 1);
            counter <= 0;
        end
    end
end

endmodule
