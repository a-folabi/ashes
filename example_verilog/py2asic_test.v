module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(4), .matrix_col(8), .Vd_R_0_col_7(net378[0:4]),.Vd_R_1_col_7(net379[0:4]),.Vd_R_2_col_7(net380[0:4]),.Vd_R_3_col_7(net381[0:4]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(4));
	TSMC350nm_GateMuxSwcTile switch(.island_num(0), .direction(horizontal), .num(8));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch));


	/* Island 1 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(1), .row(0), .col(0), .matrix_row(4), .matrix_col(8));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(1), .direction(horizontal), .bits(4), .decode_n0_VGRUN_0_(net378[0]),.decode_n0_VGRUN_1_(net379[0]),.decode_n0_VGRUN_2_(net380[0]),.decode_n0_VGRUN_3_(net381[0]),.decode_n1_VGRUN_0_(net378[1]),.decode_n1_VGRUN_1_(net379[1]),.decode_n1_VGRUN_2_(net380[1]),.decode_n1_VGRUN_3_(net381[1]),.decode_n2_VGRUN_0_(net378[2]),.decode_n2_VGRUN_1_(net379[2]),.decode_n2_VGRUN_2_(net380[2]),.decode_n2_VGRUN_3_(net381[2]),.decode_n3_VGRUN_0_(net378[3]),.decode_n3_VGRUN_1_(net379[3]),.decode_n3_VGRUN_2_(net380[3]),.decode_n3_VGRUN_3_(net381[3]));
	TSMC350nm_GateMuxSwcTile switch(.island_num(1), .direction(horizontal), .num(8));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(4));
	TSMC350nm_drainSelect01d3 switch(.island_num(1), .direction(vertical), .num(4), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(1), .direction(vertical), .num(4), .type(prog_switch));
endmodule