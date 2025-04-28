module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(1), .matrix_col(2));

 	/*Programming Mux */ 
	TSMC350nm_GorS_IndrctSwcs switch(.island_num(0), .direction(horizontal), .num(2), .switch_n0_Input_0_(net66[0]), .switch_n0_Input_1_(net67[0]), .switch_n1_Input_0_(net66[1]), .switch_n1_Input_1_(net67[1]), .switch_n0_VTUN(net64[0]), .switch_n1_VTUN(net64[1]));


	/* Island 1 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(2), .Vd_R_0_col_1(net66[0]), .Vd_R_1_col_1(net67[0]), .Vd_R_2_col_1(net66[1]), .Vd_R_3_col_1(net67[1]), .VTUNrow_0(net64[0:2]));

 	/*Programming Mux */ 

 endmodule