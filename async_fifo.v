//File : async_fifo.v
//This file is auto generated, do not edit!

module async_fifo #
(
  parameter DSIZE = 8,
  parameter ASIZE = 4
)
(
  output [DSIZE-1:0] rdata,
  output wfull,
  output rempty,
  input [DSIZE-1:0] wdata,
  input winc,
  input wclk,
  input wrst_n,
  input rinc,
  input rclk,
  input rrst_n
);

  wire [ASIZE-1:0] waddr;
  wire [ASIZE-1:0] raddr;
  wire [ASIZE:0] wptr;
  wire [ASIZE:0] rptr;
  wire [ASIZE:0] wrptr2;
  wire [ASIZE:0] rwptr2;

  sync_r2w
  sync_r2w
  (
    .wrptr2(wrptr2),
    .rptr(rptr),
    .wclk(wclk),
    .wrst_n(wrst_n)
  );


  sync_w2r
  sync_w2r
  (
    .rwptr2(rwptr2),
    .wptr(wptr),
    .rclk(rclk),
    .rrst_n(rrst_n)
  );


  fifomem
  #(
    DSIZE,
    ASIZE
  )
  fifomem
  (
    .rdata(rdata),
    .wdata(wdata),
    .waddr(waddr),
    .raddr(raddr),
    .wclken(winc),
    .wclk(wclk)
  );


  rptr_empty
  #(
    ASIZE
  )
  rptr_empty
  (
    .rempty(rempty),
    .raddr(raddr),
    .rptr(rptr),
    .rwptr2(rwptr2),
    .rinc(rinc),
    .rclk(rclk),
    .rrst_n(rrst_n)
  );


  wptr_full
  #(
    ASIZE
  )
  wptr_full
  (
    .wfull(wfull),
    .waddr(waddr),
    .wptr(wptr),
    .wrptr2(wrptr2),
    .winc(winc),
    .wclk(wclk),
    .wrst_n(wrst_n)
  );


endmodule

