module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(7), .GND_b_0_row_4(net1868[0:7]), .GND_b_1_row_4(net1880[0:7]), .VINJ_b_1_row_4(net1958[0:7]), .Vsel_b_0_row_4(net1893[0:7]), .Vsel_b_1_row_4(net1894[0:7]), .Vg_b_0_row_4(net1919[0:7]), .Vg_b_1_row_4(net1920[0:7]), .VTUN_brow_4(net1945[0:7]));
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
	TSMC350nm_4TGate_ST_BMatrix I__5 (.island_num(1), .row(0), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net1975), .P_1_row_0(net1976), .A_0_row_0(net1977), .A_1_row_0(net1978), .A_2_row_0(net1979), .A_3_row_0(net1980));
	TSMC350nm_4TGate_ST_BMatrix I__6 (.island_num(1), .row(1), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net1988), .P_1_row_0(net1989), .A_0_row_0(net1990), .A_1_row_0(net1991), .A_2_row_0(net1992), .A_3_row_0(net1993));
	TSMC350nm_4TGate_ST_BMatrix I__7 (.island_num(1), .row(2), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net2006), .P_1_row_0(net2007), .A_0_row_0(net2008), .A_1_row_0(net2009), .A_2_row_0(net2010), .A_3_row_0(net2011));
	TSMC350nm_4TGate_ST_BMatrix_NoSwitch I__8 (.island_num(1), .row(3), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net2024), .P_1_row_0(net2025), .P_2_row_0(net2026), .P_3_row_0(net2027), .A_0_row_0(net2028), .A_1_row_0(net2029), .A_2_row_0(net2030), .A_3_row_0(net2031));
	TSMC350nm_4TGate_ST_BMatrix I__9 (.island_num(1), .row(4), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net2043), .P_1_row_0(net2044), .P_2_row_0(net2045), .P_3_row_0(net2046), .A_0_row_0(net2047), .A_1_row_0(net2048));
	TSMC350nm_4TGate_ST_BMatrix I__10 (.island_num(1), .row(5), .col(18), .matrix_row(1), .matrix_col(1), .A_0_row_0(net2058), .A_1_row_0(net2059), .A_2_row_0(net2060), .A_3_row_0(net2061));
	TSMC350nm_4TGate_ST_BMatrix I__11 (.island_num(1), .row(6), .col(18), .matrix_row(1), .matrix_col(1), .A_0_row_0(net2066), .A_1_row_0(net2067), .A_2_row_0(net2068), .A_3_row_0(net2069));
	TSMC350nm_4TGate_ST_BMatrix I__12 (.island_num(1), .row(7), .col(18), .matrix_row(1), .matrix_col(1));
	TSMC350nm_OutMtrx_IndrctSwcs I__13 (.island_num(1), .row(9), .col(8), .matrix_row(1), .matrix_col(10));
	TSMC350nm_4x2_Indirect I__14 (.island_num(1), .row(10), .col(8), .matrix_row(2), .matrix_col(10));
	TSMC350nm_4TGate_ST_BMatrix I__15 (.island_num(1), .row(10), .col(18), .matrix_row(2), .matrix_col(1));
	TSMC350nm_TA2Cell_Weak cab_device_16 (.island_num(1), .row(2), .col(19), .VD_P_0_(net1975), .VD_P_1_(net1976), .VIN1_PLUS(net1977), .VIN1_MINUS(net1978), .VIN2_PLUS(net1979), .VIN2_MINUS(net1980), .OUTPUT_0_(net1868[8]), .OUTPUT_1_(net1866[9]), .Vsel_0_(net2052), .Vsel_1_(net2053), .RUN(net1983), .Vg_0_(net2054), .Vg_1_(net2055), .PROG(net1984), .VTUN(net1985), .VINJ(net1986), .GND(net1987), .VPWR(net2064), .Vsel_b_0_(net1996), .Vsel_b_1_(net1997), .RUN_b(net1998), .Vg_b_0_(net1999), .Vg_b_1_(net2000), .PROG_b(net2001), .VTUN_b(net2002), .VINJ_b(net2003), .GND_b(net2004), .VPWR_b(net2005));
	TSMC350nm_TA2Cell_Weak cab_device_17 (.island_num(1), .row(3), .col(19), .VD_P_0_(net1988), .VD_P_1_(net1989), .VIN1_PLUS(net1990), .VIN1_MINUS(net1991), .VIN2_PLUS(net1992), .VIN2_MINUS(net1993), .OUTPUT_0_(net1868[9]), .OUTPUT_1_(net1866[10]), .Vsel_0_(net1996), .Vsel_1_(net1997), .RUN(net1998), .Vg_0_(net1999), .Vg_1_(net2000), .PROG(net2001), .VTUN(net2002), .VINJ(net2003), .GND(net2004), .VPWR(net2005), .Vsel_b_0_(net2014), .Vsel_b_1_(net2015), .RUN_b(net2016), .Vg_b_0_(net2017), .Vg_b_1_(net2018), .PROG_b(net2019), .VTUN_b(net2020), .VINJ_b(net2021), .GND_b(net2022), .VPWR_b(net2023));
	TSMC350nm_TA2Cell_Strong cab_device_18 (.island_num(1), .row(4), .col(19), .VD_P_0_(net2006), .VD_P_1_(net2007), .VIN1_PLUS(net2008), .VIN1_MINUS(net2009), .VIN2_PLUS(net2010), .VIN2_MINUS(net2011), .OUTPUT_0_(net1868[10]), .OUTPUT_1_(net1866[11]), .Vsel_0_(net2014), .Vsel_1_(net2015), .RUN(net2016), .Vg_0_(net2017), .Vg_1_(net2018), .PROG(net2019), .VTUN(net2020), .VINJ(net2021), .GND(net2022), .VPWR(net2023), .Vg_b_0_(net2039), .PROG_b(net2042), .VTUN_b(net2040), .VINJ_b(net2038), .GND_b(net2041));
	TSMC350nm_4WTA_IndirectProg cab_device_19 (.island_num(1), .row(5), .col(19), .VD_P_0_(net2024), .VD_P_1_(net2025), .VD_P_2_(net2026), .VD_P_3_(net2027), .Iin_0_(net2028), .Iin_1_(net2029), .Iin_2_(net2030), .Iin_3_(net2031), .Vout_0_(net1868[11]), .Vout_1_(net1866[12]), .Vout_2_(net1868[12]), .Vout_3_(net1866[13]), .Vmid(net1868[13]), .Vbias(net1866[14]), .Vsel(net2052), .Vs(net2064), .VINJ(net2038), .Vg(net2039), .VTUN(net2040), .GND(net2041), .PROG(net2042), .VINJ_b(net2051), .VTUN_b(net2057), .GND_b(net2056));
	TSMC350nm_Cap_Bank cab_device_20 (.island_num(1), .row(6), .col(19), .VD_P_0_(net2043), .VD_P_1_(net2044), .VD_P_2_(net2045), .VD_P_3_(net2046), .VIN_0_(net2047), .VIN_1_(net2048), .OUT_0_(net1868[14]), .OUT_1_(net1866[15]), .VINJ(net2051), .Vsel_0_(net2052), .Vsel_1_(net2053), .Vg_0_(net2054), .Vg_1_(net2055), .GND(net2056), .VTUN(net2057), .GND_b(net2065));
	TSMC350nm_NandPfets cab_device_21 (.island_num(1), .row(7), .col(19), .GATE_N(net2058), .SOURCE_N(net2059), .GATE_P(net2060), .SOURCE_P(net2061), .DRAIN_N(net1868[15]), .DRAIN_P(net1866[16]), .VPWR(net2064), .GND(net2065), .VPWR_b(net2073), .GND_b(net2074));
	TSMC350nm_TGate_2nMirror cab_device_22 (.island_num(1), .row(8), .col(19), .IN_CM_0_(net2066), .IN_CM_1_(net2067), .SelN(net2068), .IN_TG(net2069), .OUT_CM_0_(net1868[16]), .OUT_CM_1_(net1866[17]), .OUT_TG(net1868[17]), .VPWR(net2073), .GND(net2074));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(6));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(1), .direction(vertical), .num(12), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(1), .direction(vertical), .num(12), .type(prog_switch));
	TSMC350nm_GorS_IndrctSwcs switch(.island_num(1), .direction(horizontal), .num(20), .switch_n0_Input_1_(net1868[0]), .switch_n1_Input_0_(net1866[1]), .switch_n1_Input_1_(net1868[1]), .switch_n2_Input_0_(net1866[2]), .switch_n2_Input_1_(net1868[2]), .switch_n3_Input_0_(net1866[3]), .switch_n3_Input_1_(net1868[3]), .switch_n8_Input_1_(net1868[8]), .switch_n9_Input_0_(net1866[9]), .switch_n9_Input_1_(net1868[9]), .switch_n10_Input_0_(net1866[10]), .switch_n10_Input_1_(net1868[10]), .switch_n11_Input_0_(net1866[11]), .switch_n11_Input_1_(net1868[11]), .switch_n12_Input_0_(net1866[12]), .switch_n12_Input_1_(net1868[12]), .switch_n13_Input_0_(net1866[13]), .switch_n13_Input_1_(net1868[13]), .switch_n14_Input_0_(net1866[14]), .switch_n14_Input_1_(net1868[14]), .switch_n15_Input_0_(net1866[15]), .switch_n15_Input_1_(net1868[15]), .switch_n16_Input_0_(net1866[16]), .switch_n16_Input_1_(net1868[16]), .switch_n17_Input_0_(net1866[17]), .switch_n17_Input_1_(net1868[17]), .switch_n0_GND_0_(net1880[0]), .switch_n1_GND_0_(net1880[1]), .switch_n2_GND_0_(net1880[2]), .switch_n3_GND_0_(net1880[3]), .switch_n4_GND_0_(net1880[4]), .switch_n5_GND_0_(net1880[5]), .switch_n6_GND_0_(net1880[6]), .switch_n0_Vsel_0_(net1893[0]), .switch_n0_Vsel_1_(net1894[0]), .switch_n1_Vsel_0_(net1893[1]), .switch_n1_Vsel_1_(net1894[1]), .switch_n2_Vsel_0_(net1893[2]), .switch_n2_Vsel_1_(net1894[2]), .switch_n3_Vsel_0_(net1893[3]), .switch_n3_Vsel_1_(net1894[3]), .switch_n4_Vsel_0_(net1893[4]), .switch_n4_Vsel_1_(net1894[4]), .switch_n5_Vsel_0_(net1893[5]), .switch_n5_Vsel_1_(net1894[5]), .switch_n6_Vsel_0_(net1893[6]), .switch_n6_Vsel_1_(net1894[6]), .switch_n0_Vg_global_0_(net1919[0]), .switch_n0_Vg_global_1_(net1920[0]), .switch_n1_Vg_global_0_(net1919[1]), .switch_n1_Vg_global_1_(net1920[1]), .switch_n2_Vg_global_0_(net1919[2]), .switch_n2_Vg_global_1_(net1920[2]), .switch_n3_Vg_global_0_(net1919[3]), .switch_n3_Vg_global_1_(net1920[3]), .switch_n4_Vg_global_0_(net1919[4]), .switch_n4_Vg_global_1_(net1920[4]), .switch_n5_Vg_global_0_(net1919[5]), .switch_n5_Vg_global_1_(net1920[5]), .switch_n6_Vg_global_0_(net1919[6]), .switch_n6_Vg_global_1_(net1920[6]), .switch_n0_VTUN_0_(net1945[0]), .switch_n1_VTUN_0_(net1945[1]), .switch_n2_VTUN_0_(net1945[2]), .switch_n3_VTUN_0_(net1945[3]), .switch_n4_VTUN_0_(net1945[4]), .switch_n5_VTUN_0_(net1945[5]), .switch_n6_VTUN_0_(net1945[6]), .switch_n0_VINJ_0_(net1958[0]), .switch_n1_VINJ_0_(net1958[1]), .switch_n2_VINJ_0_(net1958[2]), .switch_n3_VINJ_0_(net1958[3]), .switch_n4_VINJ_0_(net1958[4]), .switch_n5_VINJ_0_(net1958[5]), .switch_n6_VINJ_0_(net1958[6]));
	none switch_ind(.island_num(1), .direction(horizontal), .col(18));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(1), .direction(horizontal), .col(19), .GND(net1987), .CTRL_B_0_(net2052), .CTRL_B_1_(net2053), .run_r(net1983), .prog_r(net1984), .Vg_0_(net2054), .Vg_1_(net2055), .VTUN(net1985), .VINJ(net1986), .VDD_1_(net2064));


	/* Island 2 */
	TSMC350nm_volatile_swcs I__0 (.island_num(2), .row(0), .col(0), .matrix_row(1), .matrix_col(6));

 	/*Programming Mux */ 

 endmodule