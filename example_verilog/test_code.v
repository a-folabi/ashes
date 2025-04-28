module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(1), .matrix_col(2), .GND_b_0_row_0(net31[0:2]), .Vs_b_0_row_0(net33[0:2]));

 	/*Programming Mux */ 


	/* Island 1 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(2));

 	/*Programming Mux */ 
	TSMC350nm_GorS_IndrctSwcs switch(.island_num(1), .direction(horizontal), .num(2), .switch_n0_Input_1_(net31[0]), .switch_n1_Input_1_(net33[1]));

 endmodule