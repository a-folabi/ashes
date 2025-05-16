module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(1));
	TSMC350nm_Amplifier9T_FGBias I__1 (.island_num(0), .row(6), .col(0));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(0));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(3), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(3), .type(prog_switch));


	/* Island 1 */
	TGate_DT I__0 (.island_num(1), .row(0), .col(0), .matrix_row(5), .matrix_col(1));

 	/*Programming Mux */ 


	/* Island 2 */
	TGate_DT I__0 (.island_num(2), .row(0), .col(0), .matrix_row(5), .matrix_col(1));

 	/*Programming Mux */ 


	/* Island 3 */
	Capacitor_80ff I__0 (.island_num(3), .row(0), .col(0), .matrix_row(5), .matrix_col(1));

 	/*Programming Mux */ 


	/* Island 4 */
	TGate_DT I__0 (.island_num(4), .row(0), .col(0));

 	/*Programming Mux */ 


	/* Island 5 */
	Capacitor_80ff I__0 (.island_num(5), .row(0), .col(0));

 	/*Programming Mux */ 

 endmodule