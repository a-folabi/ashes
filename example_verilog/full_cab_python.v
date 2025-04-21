module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(7));
	TSMC350nm_4x2_Indirect I__1 (.island_num(0), .row(0), .col(17), .matrix_row(5), .matrix_col(9));
	TSMC350nm_4TGate_ST_BMatrix I__2 (.island_num(0), .row(0), .col(26), .matrix_row(5), .matrix_col(1));
	S_BLOCK_SEC1_PINS I__3 (.island_num(0), .row(0), .col(7), .matrix_row(5), .matrix_col(1));
	S_BLOCK_BUFFER I__4 (.island_num(0), .row(0), .col(8), .matrix_row(5), .matrix_col(1));
	S_BLOCK_SPACE_UP_PINS I__5 (.island_num(0), .row(0), .col(9), .matrix_row(4), .matrix_col(1));
	S_BLOCK_CONN_PINS I__6 (.island_num(0), .row(4), .col(9), .matrix_row(1), .matrix_col(1));
	S_BLOCK_SPACE_UP_PINS I__7 (.island_num(0), .row(0), .col(10), .matrix_row(3), .matrix_col(1));
	S_BLOCK_CONN_PINS I__8 (.island_num(0), .row(3), .col(10), .matrix_row(1), .matrix_col(1));
	S_BLOCK_SPACE_DOWN_PINS I__9 (.island_num(0), .row(4), .col(10), .matrix_row(1), .matrix_col(1));
	S_BLOCK_SPACE_UP_PINS I__10 (.island_num(0), .row(0), .col(11), .matrix_row(2), .matrix_col(1));
	S_BLOCK_CONN_PINS I__11 (.island_num(0), .row(2), .col(11), .matrix_row(1), .matrix_col(1));
	S_BLOCK_SPACE_DOWN_PINS I__12 (.island_num(0), .row(3), .col(11), .matrix_row(2), .matrix_col(1));
	S_BLOCK_SPACE_UP_PINS I__13 (.island_num(0), .row(0), .col(12), .matrix_row(1), .matrix_col(1));
	S_BLOCK_CONN_PINS I__14 (.island_num(0), .row(1), .col(12), .matrix_row(1), .matrix_col(1));
	S_BLOCK_SPACE_DOWN_PINS I__15 (.island_num(0), .row(2), .col(12), .matrix_row(3), .matrix_col(1));
	S_BLOCK_CONN_PINS I__16 (.island_num(0), .row(0), .col(13), .matrix_row(1), .matrix_col(1));
	S_BLOCK_SPACE_DOWN_PINS I__17 (.island_num(0), .row(1), .col(13), .matrix_row(4), .matrix_col(1));
	S_BLOCK_SEC2_PINS I__18 (.island_num(0), .row(0), .col(14), .matrix_row(5), .matrix_col(1));
	S_BLOCK_23CONN I__19 (.island_num(0), .row(0), .col(15), .matrix_row(5), .matrix_col(1));
	S_BLOCK_SEC3_PINS I__20 (.island_num(0), .row(0), .col(16), .matrix_row(5), .matrix_col(1));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(6));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(26));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(5));
	TSMC350nm_drainSelect01d3 switch(.island_num(0), .direction(vertical), .num(5), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(5), .type(prog_switch));
	none switch_ind(.island_num(0), .direction(horizontal), .col(8));
	none switch_ind(.island_num(0), .direction(horizontal), .col(9));
	none switch_ind(.island_num(0), .direction(horizontal), .col(10));
	none switch_ind(.island_num(0), .direction(horizontal), .col(11));
	none switch_ind(.island_num(0), .direction(horizontal), .col(12));
	none switch_ind(.island_num(0), .direction(horizontal), .col(13));
	none switch_ind(.island_num(0), .direction(horizontal), .col(14));
	none switch_ind(.island_num(0), .direction(horizontal), .col(15));


	/* Island 1 */
	TSMC350nm_4x2_Indirect_top_AorB_matrx I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(8));
	TSMC350nm_4x2_Indirect I__1 (.island_num(1), .row(1), .col(0), .matrix_row(7), .matrix_col(8));
	TSMC350nm_4x2_Indirect_top_AorB_matrx I__2 (.island_num(1), .row(0), .col(8), .matrix_row(1), .matrix_col(9));
	TSMC350nm_4x2_Indirect I__3 (.island_num(1), .row(1), .col(8), .matrix_row(6), .matrix_col(9));
	TSMC350nm_4x2_Indirect_bot_B_matrx I__4 (.island_num(1), .row(7), .col(8), .matrix_row(1), .matrix_col(9));
	TSMC350nm_4TGate_ST_BMatrix I__5 (.island_num(1), .row(0), .col(17), .matrix_row(8), .matrix_col(1), .P_0_col_0(net976[0:8]), .P_1_col_0(net977[0:8]), .A_0_col_0(net998[0:8]), .A_1_col_0(net999[0:8]), .A_2_col_0(net996[0:8]), .A_3_col_0(net997[0:8]));
	TSMC350nm_OutMtrx_IndrctSwcs I__6 (.island_num(1), .row(9), .col(8), .matrix_row(1), .matrix_col(9));
	TSMC350nm_4x2_Indirect I__7 (.island_num(1), .row(10), .col(8), .matrix_row(2), .matrix_col(9));
	TSMC350nm_4TGate_ST_BMatrix I__8 (.island_num(1), .row(10), .col(17), .matrix_row(2), .matrix_col(1));
	TSMC350nm_TA2Cell_Weak cab_device_9 (.island_num(1), .row(2), .col(18), .VD_P_0_(net976[0]), .VD_P_1_(net977[0]), .VIN1_PLUS(net999[0]), .VIN1_MINUS(net998[0]), .VIN2_PLUS(net996[0]), .VIN2_MINUS(net997[0]), .OUTPUT_0_(net1252[8]), .OUTPUT_1_(net1251[9]));
	TSMC350nm_TA2Cell_Weak cab_device_10 (.island_num(1), .row(3), .col(18), .VD_P_0_(net976[1]), .VD_P_1_(net977[1]), .VIN1_PLUS(net999[1]), .VIN1_MINUS(net998[1]), .VIN2_PLUS(net996[1]), .VIN2_MINUS(net997[1]), .OUTPUT_0_(net1252[9]), .OUTPUT_1_(net1251[10]));
	TSMC350nm_TA2Cell_Strong cab_device_11 (.island_num(1), .row(4), .col(18), .OUTPUT_0_(net1252[10]), .OUTPUT_1_(net1251[11]));
	TSMC350nm_4WTA cab_device_12 (.island_num(1), .row(5), .col(18), .Iin_0_(net998[2]), .Iin_1_(net999[2]), .Iin_2_(net996[2]), .Iin_3_(net997[2]), .Vout_0_(net1252[11]), .Vout_1_(net1251[12]), .Vout_2_(net1252[12]), .Vout_3_(net1251[13]));
	TSMC350nm_Cap_Bank cab_device_13 (.island_num(1), .row(6), .col(18), .VD_P_0_(net976[3]), .VD_P_1_(net977[3]), .VD_P_2_(net972[3]), .VD_P_3_(net973[3]), .VIN_0_(net998[3]), .VIN_1_(net999[3]), .OUT_0_(net1252[13]), .OUT_1_(net1251[14]));
	TSMC350nm_NandPfets cab_device_14 (.island_num(1), .row(7), .col(18), .GATE_N(net996[3]), .SOURCE_N(net997[3]), .GATE_P(net998[4]), .SOURCE_P(net999[4]), .DRAIN_N(net1251[15]), .DRAIN_P(net1252[14]));
	TSMC350nm_TGate_2nMirror cab_device_15 (.island_num(1), .row(8), .col(18), .IN_CM_0_(net996[4]), .IN_CM_1_(net997[4]), .SelN(net998[5]), .IN_TG(net999[5]), .OUT_CM_0_(net1252[15]), .OUT_CM_1_(net1251[16]), .OUT_TG(net1252[16]));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(6));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(1), .direction(vertical), .num(12), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(1), .direction(vertical), .num(12), .type(prog_switch));
	TSMC350nm_GorS_IndrctSwcs switch(.island_num(1), .direction(horizontal), .num(19), .switch_n8_Input_0_(net1251[8]), .switch_n8_Input_1_(net1252[8]), .switch_n9_Input_0_(net1251[9]), .switch_n9_Input_1_(net1252[9]), .switch_n10_Input_0_(net1251[10]), .switch_n10_Input_1_(net1252[10]), .switch_n11_Input_0_(net1251[11]), .switch_n11_Input_1_(net1252[11]), .switch_n12_Input_0_(net1251[12]), .switch_n12_Input_1_(net1252[12]), .switch_n13_Input_0_(net1251[13]), .switch_n13_Input_1_(net1252[13]), .switch_n14_Input_0_(net1251[14]), .switch_n14_Input_1_(net1252[14]), .switch_n15_Input_0_(net1251[15]), .switch_n15_Input_1_(net1252[15]), .switch_n16_Input_0_(net1251[16]), .switch_n16_Input_1_(net1252[16]));
	none switch_ind(.island_num(1), .direction(horizontal), .col(17));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(1), .direction(horizontal), .col(18));


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_testPin(net1251[8]));
 endmodule