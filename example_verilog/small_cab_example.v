module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(6));
	TSMC350nm_4x2_Indirect I__1 (.island_num(0), .row(0), .col(6), .matrix_row(5), .matrix_col(10));
	TSMC350nm_4x2_Indirect I__2 (.island_num(0), .row(0), .col(16), .matrix_row(5), .matrix_col(6));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(6));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(22));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(5));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(5), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(5), .type(prog_switch));


	/* Island 1 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(1), .row(0), .col(0), .matrix_row(8), .matrix_col(8));
	TSMC350nm_4x2_Indirect I__1 (.island_num(1), .row(0), .col(8), .matrix_row(8), .matrix_col(9), .Vd_P_0_col_8(net837[0:8]), .Vd_P_1_col_8(net838[0:8]), .Vd_R_0_col_8(net865[0:8]), .Vd_R_1_col_8(net866[0:8]), .Vd_R_2_col_8(net867[0:8]), .Vd_R_3_col_8(net868[0:8]));
	TSMC350nm_4x2_Indirect I__2 (.island_num(1), .row(8), .col(8), .matrix_row(2), .matrix_col(9));
	TSMC350nm_TA2Cell_Strong cab_device_3 (.island_num(1), .row(2), .col(17), .VD_P_0_(net837[0]), .VD_P_1_(net838[0]), .VIN1_PLUS(net865[0]), .VIN1_MINUS(net866[0]), .VIN2_PLUS(net867[0]), .VIN2_MINUS(net868[0]), .OUTPUT_0_(net1327[0]), .OUTPUT_1_(net1328[0]));
	TSMC350nm_TA2Cell_LongL_Cab cab_device_4 (.island_num(1), .row(3), .col(17));
	TSMC350nm_TA2Cell_Weak cab_device_5 (.island_num(1), .row(4), .col(17));
	TSMC350nm_TA2Cell_NoFG cab_device_6 (.island_num(1), .row(5), .col(17));
	TSMC350nm_4WTA cab_device_7 (.island_num(1), .row(6), .col(17));
	TSMC350nm_4WTA cab_device_8 (.island_num(1), .row(7), .col(17));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(6));
	TSMC350nm_drainSelect01d3 switch(.island_num(1), .direction(vertical), .num(10), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(1), .direction(vertical), .num(10), .type(prog_switch));
	TSMC350nm_GorS_IndrctSwcs switch(.island_num(1), .direction(horizontal), .num(18), .switch_n0_Input_0_(net1327[0]),.switch_n0_Input_1_(net1328[0]));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(1), .direction(horizontal), .col(17));
endmodule