module Top(port1);
	/*Tile Verilog*/
	/* C, S, C blocks of the tile */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(6), .Vs_b_0_row_4(c_net60[0:4]), .Vs_b_1_row_4(c_net61[0:4]));
	TSMC350nm_4x2_Indirect I__1 (.island_num(0), .row(0), .col(6), .matrix_row(5), .matrix_col(10));
	TSMC350nm_4x2_Indirect I__2 (.island_num(0), .row(0), .col(16), .matrix_row(5), .matrix_col(6), .Vs_b_0_row_4(c_net62[0:4]), .Vs_b_1_row_4(c_net63[0:4]));

	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(5));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(5), .type(drain_select));
    TSMC350nm_FourTgate_ThickOx switch(.island_num(0), .direction(vertical), .num(5), .type(prog_switch));

	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(6), .decode_n0_ENABLE(a_net1), .decode_n0_VGRUN_0_(a_net2), .decode_n0_VGRUN_1_(a_net5), .decode_n10_VGRUN_3_(a_net3));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(22));

	/* CAB elements of tile*/
	TSMC350nm_4x2_Indirect I__2 (.island_num(1), .row(0), .col(0), .matrix_row(8), .matrix_col(8));
	TSMC350nm_4x2_Indirect I__3 (.island_num(1), .row(0), .col(8), .matrix_row(8), .matrix_col(9), .Vd_P_0_col_8(c_net18[0:8]), .Vd_P_1_col_8(c_net19[0:8]), .Vd_P_2_col_8(c_net20[0:8]), .Vd_P_3_col_8(c_net21[0:8]), .Vd_R_0_col_8(c_net22[0:8]), .Vd_R_1_col_8(c_net23[0:8]), .Vd_R_2_col_8(c_net24[0:8]), .Vd_R_3_col_8(c_net25[0:8]));
	TSMC350nm_4x2_Indirect I__4 (.island_num(1), .row(8), .col(8), .matrix_row(2), .matrix_col(9), .Vs_b_0_row_1(a_net4[0:8]));
	TSMC350nm_TA2Cell_Strong cab_device_0 (.island_num(1), .row(2), .col(17), .OUTPUT1(c_net0), .OUTPUT2(c_net1), .DRAIN1(c_net18[0]), .DRAIN2(c_net21[0]), .VIN1_PLUS(c_net22[0]), .VIN1_MINUS(c_net23[0]), .VIN2_PLUS(c_net24[0]), .VIN2_MINUS(c_net25[0]), .COLSEL2(c_net26), .GATE2(c_net27), .VTUN(c_net28), .GATE1(c_net29), .COLSEL1(c_net30), .VINJ(c_net31), .GND(c_net32), .VPWR(c_net33), .COLSEL2_b(c_net34), .RUN_b(c_net35), .GATE2_b(c_net36), .PROG_b(c_net37), .VTUN_b(c_net38), .GATE1_b(c_net39), .COLSEL1_b(c_net40), .VINJ_b(c_net41), .GND_b(c_net42), .VPWR_b(c_net43));
	TSMC350nm_TA2Cell_LongL_Cab cab_device_1 (.island_num(1), .row(3), .col(17), .OUTPUT1(c_net2), .OUTPUT2(c_net3), .DRAIN1(c_net18[1]), .DRAIN2(c_net21[1]), .VIN1_PLUS(c_net22[1]), .VIN1_MINUS(c_net23[1]), .VIN2_PLUS(c_net24[1]), .VIN2_MINUS(c_net25[1]), .COLSEL2(c_net34), .RUN(c_net35), .GATE2(c_net36), .PROG(c_net37), .VTUN(c_net38), .GATE1(c_net39), .COLSEL1(c_net40), .VINJ(c_net41), .GND(c_net42), .VPWR(c_net43), .COLSEL2_b(c_net44), .RUN_b(c_net45), .GATE2_b(c_net46), .PROG_b(c_net47), .VTUN_b(c_net48), .GATE1_b(c_net49), .COLSEL1_b(c_net50), .VINJ_b(c_net51), .GND_b(c_net52), .VPWR_b(c_net53));
	TSMC350nm_TA2Cell_Weak cab_device_2 (.island_num(1), .row(4), .col(17), .OUTPUT1(c_net4), .OUTPUT2(c_net5), .DRAIN1(c_net18[2]), .DRAIN2(c_net21[2]), .VIN1_PLUS(c_net22[2]), .VIN1_MINUS(c_net23[2]), .VIN2_PLUS(c_net24[2]), .VIN2_MINUS(c_net25[2]), .COLSEL2(c_net44), .RUN(c_net45), .GATE2(c_net46), .PROG(c_net47), .VTUN(c_net48), .GATE1(c_net49), .COLSEL1(c_net50), .VINJ(c_net51), .GND(c_net52), .VPWR(c_net53), .VTUN_b(c_net54), .GATE1_b(c_net55), .COLSEL1_b(c_net56), .VINJ_b(c_net57), .GND_b(c_net58), .VPWR_b(c_net59));
	TSMC350nm_TA2Cell_NoFG cab_device_3 (.island_num(1), .row(5), .col(17), .OUTPUT1(c_net6), .OUTPUT2(c_net7), .DRAIN1(c_net18[3]), .DRAIN2(c_net21[3]), .VIN1_PLUS(c_net22[3]), .VIN1_MINUS(c_net23[3]), .VIN2_PLUS(c_net24[3]), .VIN2_MINUS(c_net25[3]), .VTUN(c_net54), .GATE1(c_net55), .COLSEL1(c_net56), .VINJ(c_net57), .GND(c_net58), .VPWR(c_net59));
	TSMC350nm_4WTA cab_device_4 (.island_num(1), .row(6), .col(17), .Vout_0_(c_net8), .Vout_1_(c_net9), .Vout_2_(c_net10), .Vout_3_(c_net11), .Iin_0_(c_net18[4]), .Iin_1_(c_net19[4]), .Iin_2_(c_net20[4]), .Iin_3_(c_net21[4]));
	TSMC350nm_4WTA cab_device_5 (.island_num(1), .row(7), .col(17), .Vout_0_(c_net12), .Vout_1_(c_net13), .Vout_2_(c_net14), .Vout_3_(c_net15), .Iin_0_(c_net18[5]), .Iin_1_(c_net19[5]), .Iin_2_(c_net20[5]), .Iin_3_(c_net21[5]));

	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(6));
	TSMC350nm_drainSelect01d3 switch(.island_num(1), .direction(vertical), .num(10), .type(drain_select));
    TSMC350nm_FourTgate_ThickOx switch(.island_num(1), .direction(vertical), .num(10), .type(prog_switch));

	TSMC350nm_GorS_IndrctSwcs switch(.island_num(1), .direction(horizontal), .num(18), .switch_n8_Input_0_(c_net0), .switch_n8_Input_1_(c_net1), .switch_n9_Input_0_(c_net2), .switch_n9_Input_1_(c_net3), .switch_n10_Input_0_(c_net4), .switch_n10_Input_1_(c_net5), .switch_n11_Input_0_(c_net6), .switch_n11_Input_1_(c_net7), .switch_n12_Input_0_(c_net8), .switch_n12_Input_1_(c_net9), .switch_n13_Input_0_(c_net10), .switch_n13_Input_1_(c_net11), .switch_n14_Input_0_(c_net12), .switch_n14_Input_1_(c_net13), .switch_n15_Input_0_(c_net14), .switch_n15_Input_1_(c_net15), .switch_n0_Input_0_(c_net60[0]), .switch_n0_Input_1_(c_net61[0]), .switch_n1_Input_0_(c_net60[1]), .switch_n1_Input_1_(c_net61[1]), .switch_n2_Input_0_(c_net60[2]), .switch_n2_Input_1_(c_net61[2]), .switch_n3_Input_0_(c_net60[3]), .switch_n3_Input_1_(c_net61[3]), .switch_n4_Input_0_(c_net62[0]), .switch_n4_Input_1_(c_net63[0]), .switch_n5_Input_0_(c_net62[1]), .switch_n5_Input_1_(c_net63[1]), .switch_n6_Input_0_(c_net62[2]), .switch_n6_Input_1_(c_net63[2]), .switch_n7_Input_0_(c_net62[3]), .switch_n7_Input_1_(c_net63[3]));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(1), .direction(horizontal), .col(17), .CTRL_B_0_(c_net26), .Vg_0_(c_net27), .VTUN(c_net28), .Vg_1_(c_net29), .CTRL_B_1_(c_net30), .VINJ(c_net31), .GND_0_(c_net32), .VDD_1_(c_net33));

	/*
	- Generate a frame with cab_frame instance name 
	- Specify frame edge with first letter in name
	- Specify a default pin layer and optionally modify individual pins with _metal#_ eg _metal2_
	- Specify the pin name last and pass in the net
	*/
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_p1(a_net1), .N_p5(a_net5), .E_metal2_p2(a_net2), .W_p3(a_net3), .S_p4(a_net4[0]));

endmodule
