module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .Vd_P_0_(net150[0]), .Vd_P_1_(net151[0]), .Vd_P_2_(net70[0]), .Vd_P_3_(net71[0]));
	TSMC350nm_4x2_Direct I__1 (.island_num(0), .row(0), .col(1), .Vd_0_(net150[0]), .Vd_1_(net151[0]), .Vd_2_(net70[0]), .Vd_3_(net71[0]));
	TSMC350nm_TA2Cell_NoFG I__2 (.island_num(0), .row(0), .col(2), .VD_P_0_(net150[0]), .VD_P_1_(net151[0]));
	TSMC350nm_VMMWTA I__3 (.island_num(0), .row(0), .col(3), .Vd_0_(net150[0]), .Vd_1_(net151[0]), .Vd_2_(net70[0]), .Vd_3_(net71[0]));
	TSMC350nm_TA2Cell_Weak I__4 (.island_num(0), .row(0), .col(4), .VD_P_0_(net150[0]), .VD_P_1_(net151[0]));
	TSMC350nm_TA2Cell_Strong I__5 (.island_num(0), .row(0), .col(5), .VD_P_0_(net150[0]), .VD_P_1_(net151[0]));
	TSMC350nm_TA2Cell_LongL_Cab I__6 (.island_num(0), .row(0), .col(6), .VD_P_0_(net150[0]), .VD_P_1_(net151[0]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(2));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(1), .type(drain_select));
	TSMC350nm_FourTgate_ThickOx_FG_MEM switch(.island_num(0), .direction(vertical), .num(1), .type(prog_switch));
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(4));
	TSMC350nm_GateMuxSwcTile switch(.island_num(0), .direction(horizontal), .num(7));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(0));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(2));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(3));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(4));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(5));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(6));
endmodule