module rptr_empty (rempty, raddr, rptr, rwptr2, rinc, rclk, rrst_n);
	parameter ADDRSIZE = 4;
	
	output rempty;
	output [ADDRSIZE-1:0] raddr;
	output [ADDRSIZE:0] rptr;
	input [ADDRSIZE:0] rwptr2;
	input rinc, rclk, rrst_n;
	
	reg [ADDRSIZE:0] rptr, rbin, rgnext, rbnext;
	reg rempty, raddrmsb;
	
	//-------------------
	// GRAYSTYLE1 pointer
	//-------------------
	always @(posedge rclk or negedge rrst_n)
    	if (!rrst_n) begin
        	rptr <= 0;
        	raddrmsb <= 0;
    	end else begin
        	rptr <= rgnext;
        	raddrmsb <= rgnext[ADDRSIZE]^rgnext[ADDRSIZE-1];
    	end
    	
	always @(*) begin: Gray_inc
    	    integer i;
    	    for (i=0; i<=ADDRSIZE; i=i+1)
        	rbin[i] = ^(rptr>>i);
    	    if (!rempty)
        	rbnext = rbin + rinc;
    	    else
        	rbnext = rbin;
    	    rgnext = (rbnext>>1) ^ rbnext;
	end
	
	// Memory read-address pointer
	assign raddr = {raddrmsb,rptr[ADDRSIZE-2:0]};
	
	//---------------------------------------------------------------
	// FIFO empty on reset or when the next rptr == synchronized wptr
	//---------------------------------------------------------------
	always @(posedge rclk or negedge rrst_n)
    	if (!rrst_n)
        	rempty <= 1'b1;
    	else
        	rempty <= (rgnext == rwptr2);
        	
endmodule
