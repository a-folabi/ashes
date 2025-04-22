module TOP(port1);


	/* Island 0 */
	TSMC350nm_TA2Cell_Weak I__0 (.island_num(0), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VIN1_PLUSrow_0(net242), .VIN1_MINUSrow_0(net44), .VIN2_PLUSrow_0(net44), .VIN2_MINUSrow_0(net90), .OUTPUT_0_row_0(net44), .OUTPUT_1_row_0(net44));
	TSMC350nm_TA2Cell_Weak I__1 (.island_num(0), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VIN1_PLUSrow_0(net44), .VIN1_MINUSrow_0(net90), .VIN2_PLUSrow_0(net90), .VIN2_MINUSrow_0(net45), .OUTPUT_0_row_0(net90), .OUTPUT_1_row_0(net45));
	TSMC350nm_TA2Cell_Weak I__2 (.island_num(0), .row(2), .col(0), .matrix_row(1), .matrix_col(1), .VIN1_PLUSrow_0(net90), .VIN1_MINUSrow_0(net91), .VIN2_PLUSrow_0(net91), .VIN2_MINUSrow_0(net137), .OUTPUT_0_row_0(net91), .OUTPUT_1_row_0(net91));
	TSMC350nm_TA2Cell_Weak I__3 (.island_num(0), .row(3), .col(0), .matrix_row(1), .matrix_col(1), .VIN1_PLUSrow_0(net91), .VIN1_MINUSrow_0(net137), .VIN2_PLUSrow_0(net137), .VIN2_MINUSrow_0(net92), .OUTPUT_0_row_0(net137), .OUTPUT_1_row_0(net92));
	TSMC350nm_TA2Cell_Weak I__4 (.island_num(0), .row(4), .col(0), .matrix_row(1), .matrix_col(1), .VIN1_PLUSrow_0(net137), .VIN1_MINUSrow_0(net138), .VIN2_PLUSrow_0(net138), .VIN2_MINUSrow_0(net184), .OUTPUT_0_row_0(net138), .OUTPUT_1_row_0(net138));
	TSMC350nm_TA2Cell_Weak I__5 (.island_num(0), .row(5), .col(0), .matrix_row(1), .matrix_col(1), .VIN1_PLUSrow_0(net138), .VIN1_MINUSrow_0(net184), .VIN2_PLUSrow_0(net184), .VIN2_MINUSrow_0(net139), .OUTPUT_0_row_0(net184), .OUTPUT_1_row_0(net139));
	TSMC350nm_TA2Cell_Weak I__6 (.island_num(0), .row(6), .col(0), .matrix_row(1), .matrix_col(1), .VIN1_PLUSrow_0(net184), .VIN1_MINUSrow_0(net185), .VIN2_PLUSrow_0(net185), .VIN2_MINUSrow_0(net231), .OUTPUT_0_row_0(net185), .OUTPUT_1_row_0(net185));
	TSMC350nm_TA2Cell_Weak I__7 (.island_num(0), .row(7), .col(0), .matrix_row(1), .matrix_col(1), .VIN1_PLUSrow_0(net185), .VIN1_MINUSrow_0(net231), .VIN2_PLUSrow_0(net231), .VIN2_MINUSrow_0(net186), .OUTPUT_0_row_0(net231), .OUTPUT_1_row_0(net186));
	TSMC350nm_TA2Cell_Weak I__8 (.island_num(0), .row(8), .col(0), .matrix_row(1), .matrix_col(1), .VIN1_PLUSrow_0(net231), .VIN1_MINUSrow_0(net232), .VIN2_PLUSrow_0(net232), .VIN2_MINUSrow_0(net243), .OUTPUT_0_row_0(net232), .OUTPUT_1_row_0(net232));
	TSMC350nm_TA2Cell_Weak I__9 (.island_num(0), .row(9), .col(0), .matrix_row(1), .matrix_col(1), .VIN1_PLUSrow_0(net232), .VIN1_MINUSrow_0(net243), .VIN2_PLUSrow_0(net243), .VIN2_MINUSrow_0(net233), .OUTPUT_0_row_0(net243), .OUTPUT_1_row_0(net233));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(6));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(10), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(10), .type(prog_switch));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(0));


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .W_w_Vin(net242), .E_e_Vout(net243));
 endmodule