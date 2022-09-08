// -----------------------------------------------------------------------------
// Auto-Generated by:        __   _ __      _  __
//                          / /  (_) /____ | |/_/
//                         / /__/ / __/ -_)>  <
//                        /____/_/\__/\__/_/|_|
//                     Build your hardware, easily!
//                   https://github.com/enjoy-digital/litex
//
// Filename   : user_module_342176160444056147.v
// Device     : tapeout
// LiteX sha1 : b4bb7aa7
// Date       : 2022-09-09 00:07:27
//------------------------------------------------------------------------------


//------------------------------------------------------------------------------
// Module
//------------------------------------------------------------------------------

module user_module_342176160444056147 (
	input  wire sys_clk,
	input  wire sys_rst,
	output reg  [7:0] io_out0,
	input  wire [7:0] io_in0
);


//------------------------------------------------------------------------------
// Signals
//------------------------------------------------------------------------------

wire sys_clk_1;
wire sys_rst_1;
wire por_clk;
reg  int_rst = 1'd1;
reg  [7:0] storage = 8'd0;
reg  re = 1'd0;
reg  [7:0] chaser = 8'd0;
reg  mode = 1'd0;
wire wait_1;
wire done;
reg  [15:0] count = 16'd62500;
reg  pwm = 1'd0;
wire enable;
wire [31:0] width;
wire [31:0] period;
reg  [31:0] counter = 32'd0;
reg  pwm_enable_storage = 1'd1;
reg  [31:0] pwm_width_storage = 32'd900;
reg  [31:0] pwm_period_storage = 32'd1024;

//------------------------------------------------------------------------------
// Combinatorial Logic
//------------------------------------------------------------------------------

assign sys_clk_1 = sys_clk;
assign por_clk = sys_clk;
assign sys_rst_1 = int_rst;
assign wait_1 = (~done);
always @(*) begin
	io_out0 <= 8'd0;
	if ((mode == 1'd1)) begin
		{io_out0} <= storage;
	end else begin
		{io_out0} <= chaser;
	end
	if ((~pwm)) begin
		{io_out0} <= 1'd0;
	end
end
assign done = (count == 1'd0);
assign enable = pwm_enable_storage;
assign width = pwm_width_storage;
assign period = pwm_period_storage;


//------------------------------------------------------------------------------
// Synchronous Logic
//------------------------------------------------------------------------------

always @(posedge por_clk) begin
	int_rst <= sys_rst;
end

always @(posedge sys_clk_1) begin
	if (done) begin
		chaser <= {chaser, (~chaser[7])};
	end
	if (re) begin
		mode <= 1'd1;
	end
	if (wait_1) begin
		if ((~done)) begin
			count <= (count - 1'd1);
		end
	end else begin
		count <= 16'd62500;
	end
	if (enable) begin
		counter <= (counter + 1'd1);
		if ((counter < width)) begin
			pwm <= 1'd1;
		end else begin
			pwm <= 1'd0;
		end
		if ((counter >= (period - 1'd1))) begin
			counter <= 1'd0;
		end
	end else begin
		counter <= 1'd0;
		pwm <= 1'd0;
	end
	if (sys_rst_1) begin
		chaser <= 8'd0;
		mode <= 1'd0;
		count <= 16'd62500;
		pwm <= 1'd0;
	end
end


//------------------------------------------------------------------------------
// Specialized Logic
//------------------------------------------------------------------------------

endmodule

// -----------------------------------------------------------------------------
//  Auto-Generated by LiteX on 2022-09-09 00:07:27.
//------------------------------------------------------------------------------
