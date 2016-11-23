`timescale 1ns/1ns
module tb_gray2bin_1;

reg [3:0] gray;
wire [3:0] bin;

gray2bin_1 dut (bin,gray);

initial begin
    $dumpvars;
  gray = 4'h0;
  #10;
  gray = 4'h1;
  #10;
  gray = 4'h2;
  #10;
  gray = 4'h3;
  #10;  
  gray = 4'he;
  #10;  
  gray = 4'h7;
  #10; 
  gray = 4'hf;
end
endmodule
