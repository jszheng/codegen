module gray2bin_1 (binarycode, graycode); 
  parameter n = 4;      // this module is parameterizable 
  output reg [n-1:0] binarycode; 
  input  [n-1:0] graycode; 
  integer i;
  always @ (graycode)
     begin
          binarycode[n-1]=graycode[n-1];
          for(i=n-1;i>0;i=i-1)
          binarycode[i-1]=graycode[i-1] ^ binarycode[i];//比较节省空间
     end
endmodule
