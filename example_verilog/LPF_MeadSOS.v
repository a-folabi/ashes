module TOP(port1);


	/* Island 0 */
	TSMC350nm_TA2Cell_Weak I__0 (.island_num(0), .row(0), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net286[0]), .VD_P_1_row_0(net287[0]), .VIN1_PLUSrow_0(net354), .VIN1_MINUSrow_0(net36), .VIN2_PLUSrow_0(net36), .VIN2_MINUSrow_0(net78), .OUTPUT_0_row_0(net36), .OUTPUT_1_row_0(net36), .Vsel_0_row_0(net352), .Vsel_1_row_0(net353), .Vg_0_row_0(net350), .Vg_1_row_0(net351));
	TSMC350nm_TA2Cell_Weak I__1 (.island_num(0), .row(1), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net288[0]), .VD_P_1_row_0(net289[0]), .VIN1_PLUSrow_0(net36), .VIN1_MINUSrow_0(net78), .VIN2_PLUSrow_0(net78), .VIN2_MINUSrow_0(net37), .OUTPUT_0_row_0(net78), .OUTPUT_1_row_0(net37));
	TSMC350nm_TA2Cell_Weak I__2 (.island_num(0), .row(2), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net290[0]), .VD_P_1_row_0(net291[0]), .VIN1_PLUSrow_0(net78), .VIN1_MINUSrow_0(net79), .VIN2_PLUSrow_0(net79), .VIN2_MINUSrow_0(net121), .OUTPUT_0_row_0(net79), .OUTPUT_1_row_0(net79));
	TSMC350nm_TA2Cell_Weak I__3 (.island_num(0), .row(3), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net292[0]), .VD_P_1_row_0(net293[0]), .VIN1_PLUSrow_0(net79), .VIN1_MINUSrow_0(net121), .VIN2_PLUSrow_0(net121), .VIN2_MINUSrow_0(net80), .OUTPUT_0_row_0(net121), .OUTPUT_1_row_0(net80));
	TSMC350nm_TA2Cell_Weak I__4 (.island_num(0), .row(4), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net294[0]), .VD_P_1_row_0(net295[0]), .VIN1_PLUSrow_0(net121), .VIN1_MINUSrow_0(net122), .VIN2_PLUSrow_0(net122), .VIN2_MINUSrow_0(net164), .OUTPUT_0_row_0(net122), .OUTPUT_1_row_0(net122));
	TSMC350nm_TA2Cell_Weak I__5 (.island_num(0), .row(5), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net296[0]), .VD_P_1_row_0(net297[0]), .VIN1_PLUSrow_0(net122), .VIN1_MINUSrow_0(net164), .VIN2_PLUSrow_0(net164), .VIN2_MINUSrow_0(net123), .OUTPUT_0_row_0(net164), .OUTPUT_1_row_0(net123));
	TSMC350nm_TA2Cell_Weak I__6 (.island_num(0), .row(6), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net298[0]), .VD_P_1_row_0(net299[0]), .VIN1_PLUSrow_0(net164), .VIN1_MINUSrow_0(net165), .VIN2_PLUSrow_0(net165), .VIN2_MINUSrow_0(net207), .OUTPUT_0_row_0(net165), .OUTPUT_1_row_0(net165));
	TSMC350nm_TA2Cell_Weak I__7 (.island_num(0), .row(7), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net300[0]), .VD_P_1_row_0(net301[0]), .VIN1_PLUSrow_0(net165), .VIN1_MINUSrow_0(net207), .VIN2_PLUSrow_0(net207), .VIN2_MINUSrow_0(net166), .OUTPUT_0_row_0(net207), .OUTPUT_1_row_0(net166));
	TSMC350nm_TA2Cell_Weak I__8 (.island_num(0), .row(8), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net302[0]), .VD_P_1_row_0(net303[0]), .VIN1_PLUSrow_0(net207), .VIN1_MINUSrow_0(net208), .VIN2_PLUSrow_0(net208), .VIN2_MINUSrow_0(net355), .OUTPUT_0_row_0(net208), .OUTPUT_1_row_0(net208));
	TSMC350nm_TA2Cell_Weak I__9 (.island_num(0), .row(9), .col(0), .matrix_row(1), .matrix_col(1), .VD_P_0_row_0(net304[0]), .VD_P_1_row_0(net305[0]), .VIN1_PLUSrow_0(net208), .VIN1_MINUSrow_0(net355), .VIN2_PLUSrow_0(net355), .VIN2_MINUSrow_0(net209), .OUTPUT_0_row_0(net355), .OUTPUT_1_row_0(net209));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(6));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(10), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(10), .type(prog_switch), .switch_n0_PR_0_(net286[0]), .switch_n0_PR_1_(net287[0]), .switch_n0_PR_2_(net288[0]), .switch_n0_PR_3_(net289[0]), .switch_n1_PR_0_(net290[0]), .switch_n1_PR_1_(net291[0]), .switch_n1_PR_2_(net292[0]), .switch_n1_PR_3_(net293[0]), .switch_n2_PR_0_(net294[0]), .switch_n2_PR_1_(net295[0]), .switch_n2_PR_2_(net296[0]), .switch_n2_PR_3_(net297[0]), .switch_n3_PR_0_(net298[0]), .switch_n3_PR_1_(net299[0]), .switch_n3_PR_2_(net300[0]), .switch_n3_PR_3_(net301[0]), .switch_n4_PR_0_(net302[0]), .switch_n4_PR_1_(net303[0]), .switch_n4_PR_2_(net304[0]), .switch_n4_PR_3_(net305[0]));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1), .switch_n0_CTRL_B_0_(net352), .switch_n0_CTRL_B_1_(net353), .switch_n0_Vg_0_(net350), .switch_n0_Vg_1_(net351));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(0));


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .W_w_Vin(net354), .E_e_Vout(net355));
 endmodule