`ifndef LAB2_FIRRTL_V
`define LAB2_FIRRTL_V

module lab2_FIRRTL
(
    input logic         clk,
    input logic         reset,
    input logic [15:0]  data_in,
    input logic [7:0]   b0,
    input logic [7:0]   b1,
    input logic [7:0]   b2,
    input logic [7:0]   b3,
    output logic [15:0] y
);

logic [15:0] z_1;
logic [15:0] z_2;
logic [15:0] z_3;

always_ff @(posedge clk) begin
    if(reset)  begin   
        z_1 <= 15'b0;
        z_2 <= 15'b0;
        z_3 <= 15'b0;
    end
    else  begin
        z_1 <= data_in;
        z_2 <= z_1;
        z_3 <= z_2;
    end 
end
    
always_comb begin
    y = data_in * b0 + z_1 * b1 + z_2 * b2 + z_3 * b3;
end 

endmodule

`endif /* LAB2_FIRRTL_V */