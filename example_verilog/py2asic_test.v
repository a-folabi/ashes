module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Direct I__0 (.island_num(0), .row(0), .col(0), .matrix_row(4), .matrix_col(8), .Vd_0_col_8(net232[0:12:4]),.Vd_1_col_8(net232[1:13:4]),.Vd_2_col_8(net232[2:14:4]),.Vd_3_col_8(net232[3:15:4]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(4));
	TSMC350nm_GateMuxSwcTile switch(.island_num(0), .direction(horizontal), .num(8));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch));


	/* Island 1 */
	TSMC350nm_4x2_Direct I__0 (.island_num(1), .row(0), .col(0), .matrix_row(4), .matrix_col(8), .Vg_0_row_0(net232[0:14:2]),.Vg_1_row_0(net232[1:15:2]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(1), .direction(horizontal), .bits(4));
	TSMC350nm_GateMuxSwcTile switch(.island_num(1), .direction(horizontal), .num(8));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(4));
	TSMC350nm_drainSelect01d3 switch(.island_num(1), .direction(vertical), .num(4), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(1), .direction(vertical), .num(4), .type(prog_switch));
endmodule