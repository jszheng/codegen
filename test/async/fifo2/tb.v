//File : tb.v
//This file is auto generated, do not edit!

module tb;

parameter DSIZE = 32;
wire [DSIZE-1:0] rdata;
wire wfull;
wire rempty;
reg [DSIZE-1:0] wdata;
reg [DSIZE-1:0] refdata;
reg winc;
reg wclk;
reg wrst_n;
reg rinc;
reg rclk;
reg rrst_n;

reg fail;

async_fifo2
    #(
        .DSIZE(32),
        .ASIZE(4)
    )
    uut
    (
        .rdata(rdata),
        .wfull(wfull),
        .rempty(rempty),
        .wdata(wdata),
        .winc(winc),
        .wclk(wclk),
        .wrst_n(wrst_n),
        .rinc(rinc),
        .rclk(rclk),
        .rrst_n(rrst_n)
    );


initial begin
    $dumpfile("uut.vcd");
    $dumpvars(0, uut);
end


initial begin
    wclk = 0;
    forever begin
        #2 wclk = !wclk;
    end
end


initial begin
    rclk = 0;
    forever begin
        #20 rclk = !rclk;
    end
end


initial begin
    fail = 0;
    wrst_n = 0;
    rrst_n = 0;
    #100;
    wrst_n = 1;
    rrst_n = 1;
    #100000000;
    $display("[TIMEOUT ERROR]");
end


always @(posedge wclk or negedge wrst_n) begin
    if (! wrst_n) begin
        winc <= 0;
        wdata <= 0;
    end else begin
        winc <= 1;
        if (!wfull & winc) begin
            wdata <= wdata + 1;
        end
        if(wdata > 100) begin
            if (fail)
                $display("Test Failed!");
            else
                $display("Test Passed!");
            $finish;
        end
    end
end

always @(posedge rclk or negedge rrst_n) begin
    if (! rrst_n ) begin
        rinc <= 0;
        refdata <= 0;
    end else begin
        rinc <= 1;
        if (!rempty & rinc) begin
            refdata <= refdata + 1;
            if (rdata !== refdata) begin
                $display("[CMP ERROR] expect=%X, real=%X. (%t)", refdata, rdata, $time);
                fail = 1;
            end
        end
    end
end

endmodule

