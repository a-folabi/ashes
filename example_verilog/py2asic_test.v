module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Direct I__0 (.island_num(0), .row(0), .col(0), .matrix_row(8), .matrix_col(16));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(5));
	TSMC350nm_GateMuxSwcTile switch(.island_num(0), .direction(horizontal), .num(16));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(5));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(8), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(8), .type(prog_switch));
endmodule