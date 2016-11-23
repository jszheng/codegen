module sync_w2r (rwptr2, wptr, rclk, rrst_n);
	parameter ADDRSIZE = 4;
	output [ADDRSIZE:0] rwptr2;
	input [ADDRSIZE:0] wptr;
	input rclk, rrst_n;
	reg [ADDRSIZE:0] rwptr2, rwptr1;
	always @(posedge rclk or negedge rrst_n)
    	if (!rrst_n)
        	{rwptr2,rwptr1} <= 0;
    	else
        	{rwptr2,rwptr1} <= {rwptr1,wptr};
endmodule
