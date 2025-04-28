module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(7), .GND_b_0_row_4(net117[0:7]), .GND_b_1_row_4(net2105[0:7]), .Vs_b_0_row_4(net123[0:7]), .Vs_b_1_row_4(net124[0:7]), .VINJ_b_1_row_4(net2112[0:7]), .Vsel_b_0_row_4(net2070[0:7]), .Vsel_b_1_row_4(net2071[0:7]), .Vg_b_0_row_4(net2084[0:7]), .Vg_b_1_row_4(net2085[0:7]), .VTUN_brow_4(net2098[0:7]));
	TSMC350nm_4x2_Indirect I__1 (.island_num(0), .row(0), .col(17), .matrix_row(5), .matrix_col(9));
	TSMC350nm_4TGate_ST_BMatrix I__2 (.island_num(0), .row(0), .col(26), .matrix_row(5), .matrix_col(1));
	S_BLOCK_SEC1_PINS I__3 (.island_num(0), .row(0), .col(7), .matrix_row(5), .matrix_col(1), .VINJ_brow_4(net2125[0]), .Vsel_b_0_row_4(net2126[0]), .Vsel_b_1_row_4(net2127[0]), .Vg_b_0_row_4(net2128[0]), .Vg_b_1_row_4(net2129[0]), .VTUN_brow_4(net2130[0]), .GND_b_1_row_4(net2131[0]));
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
	TSMC350nm_4TGate_ST_BMatrix I__5 (.island_num(1), .row(0), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net1969), .P_1_row_0(net1970), .A_0_row_0(net1971), .A_1_row_0(net1972), .A_2_row_0(net1973), .A_3_row_0(net1974));
	TSMC350nm_4TGate_ST_BMatrix I__6 (.island_num(1), .row(1), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net1982), .P_1_row_0(net1983), .A_0_row_0(net1984), .A_1_row_0(net1985), .A_2_row_0(net1986), .A_3_row_0(net1987));
	TSMC350nm_4TGate_ST_BMatrix I__7 (.island_num(1), .row(2), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net2000), .P_1_row_0(net2001), .A_0_row_0(net2002), .A_1_row_0(net2003), .A_2_row_0(net2004), .A_3_row_0(net2005));
	TSMC350nm_4TGate_ST_BMatrix_NoSwitch I__8 (.island_num(1), .row(3), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net2018), .P_1_row_0(net2019), .P_2_row_0(net2020), .P_3_row_0(net2021), .A_0_row_0(net2022), .A_1_row_0(net2023), .A_2_row_0(net2024), .A_3_row_0(net2025));
	TSMC350nm_4TGate_ST_BMatrix I__9 (.island_num(1), .row(4), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net2037), .P_1_row_0(net2038), .P_2_row_0(net2039), .P_3_row_0(net2040), .A_0_row_0(net2041), .A_1_row_0(net2042));
	TSMC350nm_4TGate_ST_BMatrix I__10 (.island_num(1), .row(5), .col(18), .matrix_row(1), .matrix_col(1), .A_0_row_0(net2052), .A_1_row_0(net2053), .A_2_row_0(net2054), .A_3_row_0(net2055));
	TSMC350nm_4TGate_ST_BMatrix I__11 (.island_num(1), .row(6), .col(18), .matrix_row(1), .matrix_col(1), .A_0_row_0(net2060), .A_1_row_0(net2061), .A_2_row_0(net2062), .A_3_row_0(net2063));
	TSMC350nm_4TGate_ST_BMatrix I__12 (.island_num(1), .row(7), .col(18), .matrix_row(1), .matrix_col(1));
	TSMC350nm_OutMtrx_IndrctSwcs I__13 (.island_num(1), .row(9), .col(8), .matrix_row(1), .matrix_col(10));
	TSMC350nm_4x2_Indirect I__14 (.island_num(1), .row(10), .col(8), .matrix_row(2), .matrix_col(10));
	TSMC350nm_4TGate_ST_BMatrix I__15 (.island_num(1), .row(10), .col(18), .matrix_row(2), .matrix_col(1));
	TSMC350nm_TA2Cell_Weak cab_device_16 (.island_num(1), .row(2), .col(19), .VD_P_0_(net1969), .VD_P_1_(net1970), .VIN1_PLUS(net1971), .VIN1_MINUS(net1972), .VIN2_PLUS(net1973), .VIN2_MINUS(net1974), .OUTPUT_0_(net1975[0]), .OUTPUT_1_(net1976[0]), .Vsel_0_(net2046), .Vsel_1_(net2047), .RUN(net1977), .Vg_0_(net2048), .Vg_1_(net2049), .PROG(net1978), .VTUN(net1979), .VINJ(net1980), .GND(net1981), .VPWR(net2058), .Vsel_b_0_(net1990), .Vsel_b_1_(net1991), .RUN_b(net1992), .Vg_b_0_(net1993), .Vg_b_1_(net1994), .PROG_b(net1995), .VTUN_b(net1996), .VINJ_b(net1997), .GND_b(net1998), .VPWR_b(net1999));
	TSMC350nm_TA2Cell_Weak cab_device_17 (.island_num(1), .row(3), .col(19), .VD_P_0_(net1982), .VD_P_1_(net1983), .VIN1_PLUS(net1984), .VIN1_MINUS(net1985), .VIN2_PLUS(net1986), .VIN2_MINUS(net1987), .OUTPUT_0_(net1988[0]), .OUTPUT_1_(net1989[0]), .Vsel_0_(net1990), .Vsel_1_(net1991), .RUN(net1992), .Vg_0_(net1993), .Vg_1_(net1994), .PROG(net1995), .VTUN(net1996), .VINJ(net1997), .GND(net1998), .VPWR(net1999), .Vsel_b_0_(net2008), .Vsel_b_1_(net2009), .RUN_b(net2010), .Vg_b_0_(net2011), .Vg_b_1_(net2012), .PROG_b(net2013), .VTUN_b(net2014), .VINJ_b(net2015), .GND_b(net2016), .VPWR_b(net2017));
	TSMC350nm_TA2Cell_Strong cab_device_18 (.island_num(1), .row(4), .col(19), .VD_P_0_(net2000), .VD_P_1_(net2001), .VIN1_PLUS(net2002), .VIN1_MINUS(net2003), .VIN2_PLUS(net2004), .VIN2_MINUS(net2005), .OUTPUT_0_(net2006[0]), .OUTPUT_1_(net2007[0]), .Vsel_0_(net2008), .Vsel_1_(net2009), .RUN(net2010), .Vg_0_(net2011), .Vg_1_(net2012), .PROG(net2013), .VTUN(net2014), .VINJ(net2015), .GND(net2016), .VPWR(net2017), .Vg_b_0_(net2033), .PROG_b(net2036), .VTUN_b(net2034), .VINJ_b(net2032), .GND_b(net2035));
	TSMC350nm_4WTA_IndirectProg cab_device_19 (.island_num(1), .row(5), .col(19), .VD_P_0_(net2018), .VD_P_1_(net2019), .VD_P_2_(net2020), .VD_P_3_(net2021), .Iin_0_(net2022), .Iin_1_(net2023), .Iin_2_(net2024), .Iin_3_(net2025), .Vout_0_(net2026[0]), .Vout_1_(net2027[0]), .Vout_2_(net2028[0]), .Vout_3_(net2029[0]), .Vmid(net2030[0]), .Vbias(net2031[0]), .Vsel(net2046), .Vs(net2058), .VINJ(net2032), .Vg(net2033), .VTUN(net2034), .GND(net2035), .PROG(net2036), .VINJ_b(net2045), .VTUN_b(net2051), .GND_b(net2050));
	TSMC350nm_Cap_Bank cab_device_20 (.island_num(1), .row(6), .col(19), .VD_P_0_(net2037), .VD_P_1_(net2038), .VD_P_2_(net2039), .VD_P_3_(net2040), .VIN_0_(net2041), .VIN_1_(net2042), .OUT_0_(net2043[0]), .OUT_1_(net2044[0]), .VINJ(net2045), .Vsel_0_(net2046), .Vsel_1_(net2047), .Vg_0_(net2048), .Vg_1_(net2049), .GND(net2050), .VTUN(net2051), .GND_b(net2059));
	TSMC350nm_NandPfets cab_device_21 (.island_num(1), .row(7), .col(19), .GATE_N(net2052), .SOURCE_N(net2053), .GATE_P(net2054), .SOURCE_P(net2055), .DRAIN_N(net2056[0]), .DRAIN_P(net2057[0]), .VPWR(net2058), .GND(net2059), .VPWR_b(net2067), .GND_b(net2068));
	TSMC350nm_TGate_2nMirror cab_device_22 (.island_num(1), .row(8), .col(19), .IN_CM_0_(net2060), .IN_CM_1_(net2061), .SelN(net2062), .IN_TG(net2063), .OUT_CM_0_(net2064[0]), .OUT_CM_1_(net2065[0]), .OUT_TG(net2066[0]), .VPWR(net2067), .GND(net2068));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(6));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(1), .direction(vertical), .num(12), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(1), .direction(vertical), .num(12), .type(prog_switch));
	TSMC350nm_GorS_IndrctSwcs switch(.island_num(1), .direction(horizontal), .num(20), .switch_n0_Input_1_(net117[0]), .switch_n1_Input_0_(net123[1]), .switch_n1_Input_1_(net124[1]), .switch_n2_Input_0_(net123[2]), .switch_n2_Input_1_(net124[2]), .switch_n3_Input_0_(net123[3]), .switch_n3_Input_1_(net124[3]), .switch_n8_Input_1_(net1975[0]), .switch_n9_Input_0_(net1976[0]), .switch_n9_Input_1_(net1988[0]), .switch_n10_Input_0_(net1989[0]), .switch_n10_Input_1_(net2006[0]), .switch_n11_Input_0_(net2007[0]), .switch_n11_Input_1_(net2026[0]), .switch_n12_Input_0_(net2027[0]), .switch_n12_Input_1_(net2028[0]), .switch_n13_Input_0_(net2029[0]), .switch_n13_Input_1_(net2030[0]), .switch_n14_Input_0_(net2031[0]), .switch_n14_Input_1_(net2043[0]), .switch_n15_Input_0_(net2044[0]), .switch_n15_Input_1_(net2056[0]), .switch_n16_Input_0_(net2057[0]), .switch_n16_Input_1_(net2064[0]), .switch_n17_Input_0_(net2065[0]), .switch_n17_Input_1_(net2066[0]), .switch_n0_GND(net2105[0]), .switch_n1_GND(net2105[1]), .switch_n2_GND(net2105[2]), .switch_n3_GND(net2105[3]), .switch_n4_GND(net2105[4]), .switch_n5_GND(net2105[5]), .switch_n6_GND(net2105[6]), .switch_n7_GND(net2131[0]), .switch_n0_Vsel_0_(net2070[0]), .switch_n0_Vsel_1_(net2071[0]), .switch_n1_Vsel_0_(net2070[1]), .switch_n1_Vsel_1_(net2071[1]), .switch_n2_Vsel_0_(net2070[2]), .switch_n2_Vsel_1_(net2071[2]), .switch_n3_Vsel_0_(net2070[3]), .switch_n3_Vsel_1_(net2071[3]), .switch_n4_Vsel_0_(net2070[4]), .switch_n4_Vsel_1_(net2071[4]), .switch_n5_Vsel_0_(net2070[5]), .switch_n5_Vsel_1_(net2071[5]), .switch_n6_Vsel_0_(net2070[6]), .switch_n6_Vsel_1_(net2071[6]), .switch_n7_Vsel_0_(net2126[0]), .switch_n7_Vsel_1_(net2127[0]), .switch_n0_Vg_global_0_(net2084[0]), .switch_n0_Vg_global_1_(net2085[0]), .switch_n1_Vg_global_0_(net2084[1]), .switch_n1_Vg_global_1_(net2085[1]), .switch_n2_Vg_global_0_(net2084[2]), .switch_n2_Vg_global_1_(net2085[2]), .switch_n3_Vg_global_0_(net2084[3]), .switch_n3_Vg_global_1_(net2085[3]), .switch_n4_Vg_global_0_(net2084[4]), .switch_n4_Vg_global_1_(net2085[4]), .switch_n5_Vg_global_0_(net2084[5]), .switch_n5_Vg_global_1_(net2085[5]), .switch_n6_Vg_global_0_(net2084[6]), .switch_n6_Vg_global_1_(net2085[6]), .switch_n7_Vg_global_0_(net2128[0]), .switch_n7_Vg_global_1_(net2129[0]), .switch_n0_VTUN(net2098[0]), .switch_n1_VTUN(net2098[1]), .switch_n2_VTUN(net2098[2]), .switch_n3_VTUN(net2098[3]), .switch_n4_VTUN(net2098[4]), .switch_n5_VTUN(net2098[5]), .switch_n6_VTUN(net2098[6]), .switch_n7_VTUN(net2130[0]), .switch_n0_VINJ(net2112[0]), .switch_n1_VINJ(net2112[1]), .switch_n2_VINJ(net2112[2]), .switch_n3_VINJ(net2112[3]), .switch_n4_VINJ(net2112[4]), .switch_n5_VINJ(net2112[5]), .switch_n6_VINJ(net2112[6]), .switch_n7_VINJ(net2125[0]));
	none switch_ind(.island_num(1), .direction(horizontal), .col(18));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(1), .direction(horizontal), .col(19), .GND(net1981), .CTRL_B_0_(net2046), .CTRL_B_1_(net2047), .run_r(net1977), .prog_r(net1978), .Vg_0_(net2048), .Vg_1_(net2049), .VTUN(net1979), .VINJ(net1980), .VDD_1_(net2058));

 endmodule