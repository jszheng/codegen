module fifomem (rdata, wdata, waddr, raddr, wclken, wclk);
	parameter DATASIZE = 8; // Memory data word width
	parameter ADDRSIZE = 4; // Number of memory address bits
	output [DATASIZE-1:0] rdata;
	input [DATASIZE-1:0] wdata;
	input [ADDRSIZE-1:0] waddr, raddr;
	input wclken, wclk;
	`ifdef VENDORRAM
		// instantiation of a vendor's dual-port RAM
		VENDOR_RAM MEM (.dout(rdata), .din(wdata),
                		.waddr(waddr), .raddr(raddr),
                		.wclken(wclken), .clk(wclk));
	`else
		reg [DATASIZE-1:0] MEM [0:(1<<ADDRSIZE)-1];
		assign rdata = MEM[raddr];
		always @(posedge wclk)
    		if (wclken)
        		MEM[waddr] <= wdata;
	`endif
endmodule
