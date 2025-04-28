module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(7), .GND_b_1_row_4(net1881[0:7]), .Vs_b_0_row_4(net124[0:7]), .Vs_b_1_row_4(net125[0:7]), .VINJ_b_1_row_4(net1959[0:7]), .Vsel_b_0_row_4(net1894[0:7]), .Vsel_b_1_row_4(net1895[0:7]), .Vg_b_0_row_4(net1920[0:7]), .Vg_b_1_row_4(net1921[0:7]), .VTUN_brow_4(net1946[0:7]));
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
	TSMC350nm_drainSelect_progrundrains switch(.island_num(0), .direction(vertical), .num(5), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(0), .direction(vertical), .num(5), .type(prog_switch));
	none switch_ind(.island_num(0), .direction(horizontal), .col(8));
	none switch_ind(.island_num(0), .direction(horizontal), .col(9));
	none switch_ind(.island_num(0), .direction(horizontal), .col(10));
	none switch_ind(.island_num(0), .direction(horizontal), .col(11));
	none switch_ind(.island_num(0), .direction(horizontal), .col(12));
	none switch_ind(.island_num(0), .direction(horizontal), .col(13));
	none switch_ind(.island_num(0), .direction(horizontal), .col(15));


	/* Island 1 */
	TSMC350nm_4x2_Indirect_top_AorB_matrx I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(8));
	TSMC350nm_4x2_Indirect I__1 (.island_num(1), .row(1), .col(0), .matrix_row(7), .matrix_col(8));
	TSMC350nm_4x2_Indirect_top_AorB_matrx I__2 (.island_num(1), .row(0), .col(8), .matrix_row(1), .matrix_col(10));
	TSMC350nm_4x2_Indirect I__3 (.island_num(1), .row(1), .col(8), .matrix_row(6), .matrix_col(10));
	TSMC350nm_4x2_Indirect_bot_B_matrx I__4 (.island_num(1), .row(7), .col(8), .matrix_row(1), .matrix_col(10));
	TSMC350nm_4TGate_ST_BMatrix I__5 (.island_num(1), .row(0), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net1976), .P_1_row_0(net1977), .A_0_row_0(net1978), .A_1_row_0(net1979), .A_2_row_0(net1980), .A_3_row_0(net1981));
	TSMC350nm_4TGate_ST_BMatrix I__6 (.island_num(1), .row(1), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net1989), .P_1_row_0(net1990), .A_0_row_0(net1991), .A_1_row_0(net1992), .A_2_row_0(net1993), .A_3_row_0(net1994));
	TSMC350nm_4TGate_ST_BMatrix I__7 (.island_num(1), .row(2), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net2007), .P_1_row_0(net2008), .A_0_row_0(net2009), .A_1_row_0(net2010), .A_2_row_0(net2011), .A_3_row_0(net2012));
	TSMC350nm_4TGate_ST_BMatrix_NoSwitch I__8 (.island_num(1), .row(3), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net2025), .P_1_row_0(net2026), .P_2_row_0(net2027), .P_3_row_0(net2028), .A_0_row_0(net2029), .A_1_row_0(net2030), .A_2_row_0(net2031), .A_3_row_0(net2032));
	TSMC350nm_4TGate_ST_BMatrix I__9 (.island_num(1), .row(4), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net2044), .P_1_row_0(net2045), .P_2_row_0(net2046), .P_3_row_0(net2047), .A_0_row_0(net2048), .A_1_row_0(net2049));
	TSMC350nm_4TGate_ST_BMatrix I__10 (.island_num(1), .row(5), .col(18), .matrix_row(1), .matrix_col(1), .A_0_row_0(net2059), .A_1_row_0(net2060), .A_2_row_0(net2061), .A_3_row_0(net2062));
	TSMC350nm_4TGate_ST_BMatrix I__11 (.island_num(1), .row(6), .col(18), .matrix_row(1), .matrix_col(1), .A_0_row_0(net2067), .A_1_row_0(net2068), .A_2_row_0(net2069), .A_3_row_0(net2070));
	TSMC350nm_4TGate_ST_BMatrix I__12 (.island_num(1), .row(7), .col(18), .matrix_row(1), .matrix_col(1));
	TSMC350nm_OutMtrx_IndrctSwcs I__13 (.island_num(1), .row(9), .col(8), .matrix_row(1), .matrix_col(10));
	TSMC350nm_4x2_Indirect I__14 (.island_num(1), .row(10), .col(8), .matrix_row(2), .matrix_col(10));
	TSMC350nm_4TGate_ST_BMatrix I__15 (.island_num(1), .row(10), .col(18), .matrix_row(2), .matrix_col(1));
	TSMC350nm_TA2Cell_Weak cab_device_16 (.island_num(1), .row(2), .col(19), .VD_P_0_(net1976), .VD_P_1_(net1977), .VIN1_PLUS(net1978), .VIN1_MINUS(net1979), .VIN2_PLUS(net1980), .VIN2_MINUS(net1981), .OUTPUT_0_(net1869[8]), .OUTPUT_1_(net1867[9]), .Vsel_0_(net2053), .Vsel_1_(net2054), .RUN(net1984), .Vg_0_(net2055), .Vg_1_(net2056), .PROG(net1985), .VTUN(net1986), .VINJ(net1987), .GND(net1988), .VPWR(net2065), .Vsel_b_0_(net1997), .Vsel_b_1_(net1998), .RUN_b(net1999), .Vg_b_0_(net2000), .Vg_b_1_(net2001), .PROG_b(net2002), .VTUN_b(net2003), .VINJ_b(net2004), .GND_b(net2005), .VPWR_b(net2006));
	TSMC350nm_TA2Cell_Weak cab_device_17 (.island_num(1), .row(3), .col(19), .VD_P_0_(net1989), .VD_P_1_(net1990), .VIN1_PLUS(net1991), .VIN1_MINUS(net1992), .VIN2_PLUS(net1993), .VIN2_MINUS(net1994), .OUTPUT_0_(net1869[9]), .OUTPUT_1_(net1867[10]), .Vsel_0_(net1997), .Vsel_1_(net1998), .RUN(net1999), .Vg_0_(net2000), .Vg_1_(net2001), .PROG(net2002), .VTUN(net2003), .VINJ(net2004), .GND(net2005), .VPWR(net2006), .Vsel_b_0_(net2015), .Vsel_b_1_(net2016), .RUN_b(net2017), .Vg_b_0_(net2018), .Vg_b_1_(net2019), .PROG_b(net2020), .VTUN_b(net2021), .VINJ_b(net2022), .GND_b(net2023), .VPWR_b(net2024));
	TSMC350nm_TA2Cell_Strong cab_device_18 (.island_num(1), .row(4), .col(19), .VD_P_0_(net2007), .VD_P_1_(net2008), .VIN1_PLUS(net2009), .VIN1_MINUS(net2010), .VIN2_PLUS(net2011), .VIN2_MINUS(net2012), .OUTPUT_0_(net1869[10]), .OUTPUT_1_(net1867[11]), .Vsel_0_(net2015), .Vsel_1_(net2016), .RUN(net2017), .Vg_0_(net2018), .Vg_1_(net2019), .PROG(net2020), .VTUN(net2021), .VINJ(net2022), .GND(net2023), .VPWR(net2024), .Vg_b_0_(net2040), .PROG_b(net2043), .VTUN_b(net2041), .VINJ_b(net2039), .GND_b(net2042));
	TSMC350nm_4WTA_IndirectProg cab_device_19 (.island_num(1), .row(5), .col(19), .VD_P_0_(net2025), .VD_P_1_(net2026), .VD_P_2_(net2027), .VD_P_3_(net2028), .Iin_0_(net2029), .Iin_1_(net2030), .Iin_2_(net2031), .Iin_3_(net2032), .Vout_0_(net1869[11]), .Vout_1_(net1867[12]), .Vout_2_(net1869[12]), .Vout_3_(net1867[13]), .Vmid(net1869[13]), .Vbias(net1867[14]), .Vsel(net2053), .Vs(net2065), .VINJ(net2039), .Vg(net2040), .VTUN(net2041), .GND(net2042), .PROG(net2043), .VINJ_b(net2052), .VTUN_b(net2058), .GND_b(net2057));
	TSMC350nm_Cap_Bank cab_device_20 (.island_num(1), .row(6), .col(19), .VD_P_0_(net2044), .VD_P_1_(net2045), .VD_P_2_(net2046), .VD_P_3_(net2047), .VIN_0_(net2048), .VIN_1_(net2049), .OUT_0_(net1869[14]), .OUT_1_(net1867[15]), .VINJ(net2052), .Vsel_0_(net2053), .Vsel_1_(net2054), .Vg_0_(net2055), .Vg_1_(net2056), .GND(net2057), .VTUN(net2058), .GND_b(net2066));
	TSMC350nm_NandPfets cab_device_21 (.island_num(1), .row(7), .col(19), .GATE_N(net2059), .SOURCE_N(net2060), .GATE_P(net2061), .SOURCE_P(net2062), .DRAIN_N(net1869[15]), .DRAIN_P(net1867[16]), .VPWR(net2065), .GND(net2066), .VPWR_b(net2074), .GND_b(net2075));
	TSMC350nm_TGate_2nMirror cab_device_22 (.island_num(1), .row(8), .col(19), .IN_CM_0_(net2067), .IN_CM_1_(net2068), .SelN(net2069), .IN_TG(net2070), .OUT_CM_0_(net1869[16]), .OUT_CM_1_(net1867[17]), .OUT_TG(net1869[17]), .VPWR(net2074), .GND(net2075));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(6));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(1), .direction(vertical), .num(12), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(1), .direction(vertical), .num(12), .type(prog_switch));
	TSMC350nm_GorS_IndrctSwcs switch(.island_num(1), .direction(horizontal), .num(20), .switch_n0_Input_1_(net1881[0]), .switch_n1_Input_0_(net1867[1]), .switch_n1_Input_1_(net1869[1]), .switch_n2_Input_0_(net1867[2]), .switch_n2_Input_1_(net1869[2]), .switch_n3_Input_0_(net1867[3]), .switch_n3_Input_1_(net1869[3]), .switch_n8_Input_1_(net1869[8]), .switch_n9_Input_0_(net1867[9]), .switch_n9_Input_1_(net1869[9]), .switch_n10_Input_0_(net1867[10]), .switch_n10_Input_1_(net1869[10]), .switch_n11_Input_0_(net1867[11]), .switch_n11_Input_1_(net1869[11]), .switch_n12_Input_0_(net1867[12]), .switch_n12_Input_1_(net1869[12]), .switch_n13_Input_0_(net1867[13]), .switch_n13_Input_1_(net1869[13]), .switch_n14_Input_0_(net1867[14]), .switch_n14_Input_1_(net1869[14]), .switch_n15_Input_0_(net1867[15]), .switch_n15_Input_1_(net1869[15]), .switch_n16_Input_0_(net1867[16]), .switch_n16_Input_1_(net1869[16]), .switch_n17_Input_0_(net1867[17]), .switch_n17_Input_1_(net1869[17]), .switch_n0_GND(net1881[0]), .switch_n1_GND(net1881[1]), .switch_n2_GND(net1881[2]), .switch_n3_GND(net1881[3]), .switch_n4_GND(net1881[4]), .switch_n5_GND(net1881[5]), .switch_n6_GND(net1881[6]), .switch_n0_Vsel_0_(net1894[0]), .switch_n0_Vsel_1_(net1895[0]), .switch_n1_Vsel_0_(net1894[1]), .switch_n1_Vsel_1_(net1895[1]), .switch_n2_Vsel_0_(net1894[2]), .switch_n2_Vsel_1_(net1895[2]), .switch_n3_Vsel_0_(net1894[3]), .switch_n3_Vsel_1_(net1895[3]), .switch_n4_Vsel_0_(net1894[4]), .switch_n4_Vsel_1_(net1895[4]), .switch_n5_Vsel_0_(net1894[5]), .switch_n5_Vsel_1_(net1895[5]), .switch_n6_Vsel_0_(net1894[6]), .switch_n6_Vsel_1_(net1895[6]), .switch_n0_Vg_global_0_(net1920[0]), .switch_n0_Vg_global_1_(net1921[0]), .switch_n1_Vg_global_0_(net1920[1]), .switch_n1_Vg_global_1_(net1921[1]), .switch_n2_Vg_global_0_(net1920[2]), .switch_n2_Vg_global_1_(net1921[2]), .switch_n3_Vg_global_0_(net1920[3]), .switch_n3_Vg_global_1_(net1921[3]), .switch_n4_Vg_global_0_(net1920[4]), .switch_n4_Vg_global_1_(net1921[4]), .switch_n5_Vg_global_0_(net1920[5]), .switch_n5_Vg_global_1_(net1921[5]), .switch_n6_Vg_global_0_(net1920[6]), .switch_n6_Vg_global_1_(net1921[6]), .switch_n0_VTUN(net1946[0]), .switch_n1_VTUN(net1946[1]), .switch_n2_VTUN(net1946[2]), .switch_n3_VTUN(net1946[3]), .switch_n4_VTUN(net1946[4]), .switch_n5_VTUN(net1946[5]), .switch_n6_VTUN(net1946[6]), .switch_n0_VINJ(net1959[0]), .switch_n1_VINJ(net1959[1]), .switch_n2_VINJ(net1959[2]), .switch_n3_VINJ(net1959[3]), .switch_n4_VINJ(net1959[4]), .switch_n5_VINJ(net1959[5]), .switch_n6_VINJ(net1959[6]));
	none switch_ind(.island_num(1), .direction(horizontal), .col(18));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(1), .direction(horizontal), .col(19), .GND(net1988), .CTRL_B_0_(net2053), .CTRL_B_1_(net2054), .run_r(net1984), .prog_r(net1985), .Vg_0_(net2055), .Vg_1_(net2056), .VTUN(net1986), .VINJ(net1987), .VDD_1_(net2065));


	/* Island 2 */
	TSMC350nm_volatile_swcs I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(6));

 	/*Programming Mux */ 

 endmodule