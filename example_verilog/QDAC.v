module TOP(port1);


	/* Island 0 */
	EPOT I__0 (.island_num(0), .row(0), .col(0), .matrix_row(6), .matrix_col(1), .VDDrow_0(net125[0:1]), .VDD_brow_5(net147[0:1]), .VINJrow_0(net164[0:1]), .VINJ_brow_5(net157[0:1]), .GNDrow_0(net165[0:1]), .GND_brow_5(net158[0:1]), .Progrow_0(net153[0:1]), .Prog_brow_5(net148[0:1]), .Vg_0_row_0(net154[0:1]), .Vg_1_row_0(net155[0:1]), .Vg_b_0_row_5(net149[0:1]), .Vsel_b_0_row_5(net150[0:1]), .VD_P_0_col_0(net108[0:6]), .VD_P_1_col_0(net109[0:6]), .Voutcol_0(net12[0:6]));
	TSMC350nm_Amplifier9T_FGBias I__1 (.island_num(0), .row(7), .col(0), .VDD(net147[0]), .VINJ(net157[0]), .Vg(net149[0]), .VD_P(net120[0]), .VD_R(net121[0]), .Vsel(net150[0]), .PROG(net148[0]), .VIN_PLUS(net145[4]), .VIN_MINUS(net12[4]), .Vout(net152));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_htile decoder(.island_num(0), .direction(horizontal), .bits(2), .decode_n0_ENABLE(net166), .decode_n0_VINJV(net164[0]), .decode_n0_GNDV(net165[0]), .decode_n0_n0_IN_1_(net168), .decode_n0_n0_IN_0_(net167));
	TSMC350nm_IndirectSwitches switch(.island_num(0), .direction(horizontal), .num(1));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(0), .direction(horizontal), .col(0), .GND_T(net165[0]), .VINJ_T(net164[0]), .GND(net158[0]), .CTRL_B_0_(net154[0]), .CTRL_B_1_(net155[0]), .VINJ(net164[0]), .PROG(net153[0]));
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(0), .direction(vertical), .bits(4), .decode_n0_VINJ(net157[0]), .decode_n0_GND(net158[0]), .decode_n0_IN_1_(net162), .decode_n0_IN_0_(net161), .decode_n2_IN_1_(net160), .decode_n2_IN_0_(net159), .decode_n0_ENABLE(net163));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(4), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(4), .type(prog_switch), .switch_n0_PR_0_(net108[0]), .switch_n0_PR_1_(net109[0]), .switch_n0_PR_2_(net108[1]), .switch_n0_PR_3_(net109[1]), .switch_n1_PR_0_(net108[2]), .switch_n1_PR_1_(net109[2]), .switch_n1_PR_2_(net108[3]), .switch_n1_PR_3_(net109[3]), .switch_n2_PR_0_(net108[4]), .switch_n2_PR_1_(net109[4]), .switch_n2_PR_2_(net108[5]), .switch_n2_PR_3_(net109[5]), .switch_n3_PR_0_(net120[0]), .switch_n3_In_0_(net121[0]), .switch_n0_RUN(net156));


	/* Island 1 */
	TGate_DT I__0 (.island_num(1), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDDrow_0(net164[0:1]), .VDD_brow_4(net157[0:1]), .GNDrow_0(net165[0:1]), .GND_brow_4(net158[0:1]), .SELAcol_0(net131[0:5]), .Ccol_0(net126[0:5]), .Acol_0(net12[0:5]), .Bcol_0(net12[0:5]));

 	/*Programming Mux */ 


	/* Island 2 */
	TGate_DT I__0 (.island_num(2), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .VDD_brow_4(net157[0:1]), .GNDrow_0(net165[0:1]), .SELAcol_0(net146[0:5]), .Ccol_0(net140[0:5]), .Acol_0(net12[0:5]), .Bcol_0(net126[0:5]));

 	/*Programming Mux */ 


	/* Island 3 */
	Capacitor_80ff I__0 (.island_num(3), .row(0), .col(0), .matrix_row(5), .matrix_col(1), .Topcol_0(net140[0:5]), .Botcol_0(net145[0:5]));

 	/*Programming Mux */ 


	/* Island 4 */
	TGate_DT I__0 (.island_num(4), .row(0), .col(0), .VDD_b(net157[0]), .GND_b(net158[0]), .SELA(net146[4]), .C(net152), .A(net12[4]));

 	/*Programming Mux */ 


	/* Island 5 */
	Capacitor_80ff I__0 (.island_num(5), .row(0), .col(0), .Top(net12[4]), .Bot(net152));

 	/*Programming Mux */ 


	/* Frame */ 
	tile_analog_frame cab_frame(.pin_layer(METAL3), .N_n_Prog(net153[0]), .N_n_Run(net156), .N_n_AVDD(net125[0]), .N_n_gnd(net165[0]), .S_s_gnd(net158[0]), .N_n_vinj(net164[0]), .S_s_vinj(net157[0]), .W_w_DrainB_0_(net159), .W_w_DrainB_1_(net160), .W_w_DrainB_2_(net161), .W_w_DrainB_3_(net162), .W_w_DrainEnable(net163), .W_w_GateB_0_(net167), .W_w_GateB_1_(net168), .W_w_GateEnable(net166), .S_s_Vout(net152), .N_n_RST(net146[4]), .N_n_Code_0_(net131[0]), .N_n_Code_1_(net131[1]), .N_n_Code_2_(net131[2]), .N_n_Code_3_(net131[3]), .N_n_Code_4_(net131[4]));
 endmodule