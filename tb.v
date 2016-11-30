//File : tb.v
//This file is auto generated, do not edit!

module tb #
(
  parameter DSIZE = 32,
  parameter ASIZE = 4
)
(

);

  wire [DSIZE-1+1-1:0] rdata;
  wire wfull;
  wire rempty;
  reg [DSIZE-1+1-1:0] wdata;
  reg winc;
  reg wclk;
  reg wrst_n;
  reg rinc;
  reg rclk;
  reg rrst_n;

  async_fifo
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
    wrst_n = 0;
    #100;
    wrst_n = 1;
    #100;
    wrst_n = 0;
  end


  initial begin
    rrst_n = 0;
    #100;
    rrst_n = 1;
    #100;
    rrst_n = 0;
  end


  always @(posedge wclk) begin
    if(winc & ~wfull) begin
      wdata <= $random;
    end 
  end


  always @(posedge rclk) begin
    if(rinc & ~rempty) begin
      rdata <= $random;
    end 
  end


endmodule

