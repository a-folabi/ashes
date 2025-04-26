module TOP(port1);


	/* Island 0 */
	TSMC350nm_4x2_Indirect I__0 (.island_num(0), .row(0), .col(0), .matrix_row(5), .matrix_col(7), .GND_b_0_row_4(net1405[0:7]));
	TSMC350nm_4x2_Indirect I__1 (.island_num(0), .row(0), .col(17), .matrix_row(5), .matrix_col(9));
	TSMC350nm_4TGate_ST_BMatrix I__2 (.island_num(0), .row(0), .col(26), .matrix_row(5), .matrix_col(1));
	S_BLOCK_SEC1_PINS I__3 (.island_num(0), .row(0), .col(7), .matrix_row(5), .matrix_col(1));
	S_BLOCK_BUFFER I__4 (.island_num(0), .row(0), .col(8), .matrix_row(5), .matrix_col(1));
	S_BLOCK_SPACE_UP_PINS I__5 (.island_num(0), .row(0), .col(9), .matrix_row(4), .matrix_col(1));
	S_BLOCK_CONN_PINS I__6 (.island_num(0), .row(4), .col(9), .matrix_row(1), .matrix_col(1));
	S_BLOCK_SPACE_UP_PINS I__7 (.island_num(0), .row(0), .col(10), .matrix_row(3), .matrix_col(1));
	S_BLOCK_CONN_PINS I__8 (.island_num(0), .row(3), .col(10), .matrix_row(1), .matrix_col(1));
	S_BLOCK_SPACE_DOWN_PINS I__9 (.island_num(0), .row(4), .col(10));
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
	none switch_ind(.island_num(0), .direction(horizontal), .col(15));


	/* Island 1 */
	TSMC350nm_4x2_Indirect_top_AorB_matrx I__0 (.island_num(1), .row(0), .col(0), .matrix_row(1), .matrix_col(8));
	TSMC350nm_4x2_Indirect I__1 (.island_num(1), .row(1), .col(0), .matrix_row(7), .matrix_col(8));
	TSMC350nm_4x2_Indirect_top_AorB_matrx I__2 (.island_num(1), .row(0), .col(8), .matrix_row(1), .matrix_col(10));
	TSMC350nm_4x2_Indirect I__3 (.island_num(1), .row(1), .col(8), .matrix_row(6), .matrix_col(10));
	TSMC350nm_4x2_Indirect_bot_B_matrx I__4 (.island_num(1), .row(7), .col(8), .matrix_row(1), .matrix_col(10));
	TSMC350nm_4TGate_ST_BMatrix I__5 (.island_num(1), .row(0), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net1428), .P_1_row_0(net1429), .A_0_row_0(net1430), .A_1_row_0(net1431), .A_2_row_0(net1432), .A_3_row_0(net1433));
	TSMC350nm_4TGate_ST_BMatrix I__6 (.island_num(1), .row(1), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net1443), .P_1_row_0(net1444), .A_0_row_0(net1445), .A_1_row_0(net1446), .A_2_row_0(net1447), .A_3_row_0(net1448));
	TSMC350nm_4TGate_ST_BMatrix I__7 (.island_num(1), .row(2), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net1461), .P_1_row_0(net1462), .A_0_row_0(net1463), .A_1_row_0(net1464), .A_2_row_0(net1465), .A_3_row_0(net1466));
	TSMC350nm_4TGate_ST_BMatrix I__8 (.island_num(1), .row(3), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net1479), .P_1_row_0(net1480), .P_2_row_0(net1481), .P_3_row_0(net1482), .A_0_row_0(net1483), .A_1_row_0(net1484));
	TSMC350nm_4TGate_ST_BMatrix_NoSwitch I__9 (.island_num(1), .row(4), .col(18), .matrix_row(1), .matrix_col(1), .P_0_row_0(net1494), .P_1_row_0(net1495), .P_2_row_0(net1496), .P_3_row_0(net1497), .A_0_row_0(net1498), .A_1_row_0(net1499), .A_2_row_0(net1500), .A_3_row_0(net1501));
	TSMC350nm_4TGate_ST_BMatrix I__10 (.island_num(1), .row(5), .col(18), .matrix_row(1), .matrix_col(1), .A_0_row_0(net1513), .A_1_row_0(net1514), .A_2_row_0(net1515), .A_3_row_0(net1516));
	TSMC350nm_4TGate_ST_BMatrix I__11 (.island_num(1), .row(6), .col(18), .matrix_row(1), .matrix_col(1), .A_0_row_0(net1520), .A_1_row_0(net1521), .A_2_row_0(net1522), .A_3_row_0(net1523));
	TSMC350nm_4TGate_ST_BMatrix I__12 (.island_num(1), .row(7), .col(18), .matrix_row(1), .matrix_col(1));
	TSMC350nm_OutMtrx_IndrctSwcs I__13 (.island_num(1), .row(9), .col(8), .matrix_row(1), .matrix_col(10));
	TSMC350nm_4TGate_ST_BMatrix I__14 (.island_num(1), .row(10), .col(18), .matrix_row(2), .matrix_col(1));
	TSMC350nm_TA2Cell_Weak cab_device_15 (.island_num(1), .row(2), .col(19), .VD_P_0_(net1428), .VD_P_1_(net1429), .VIN1_PLUS(net1430), .VIN1_MINUS(net1431), .VIN2_PLUS(net1432), .VIN2_MINUS(net1433), .OUTPUT_0_(net1405[8]), .OUTPUT_1_(net1404[9]), .Vsel_0_(net1508), .Vsel_1_(net1436), .RUN(net1437), .Vg_0_(net1438), .Vg_1_(net1439), .PROG(net1512), .VTUN(net1440), .VINJ(net1441), .GND(net1442), .VPWR(net1404[0]), .Vsel_b_0_(net1451), .Vsel_b_1_(net1452), .RUN_b(net1453), .Vg_b_0_(net1454), .Vg_b_1_(net1455), .PROG_b(net1456), .VTUN_b(net1457), .VINJ_b(net1458), .GND_b(net1459), .VPWR_b(net1460));
	TSMC350nm_TA2Cell_Weak cab_device_16 (.island_num(1), .row(3), .col(19), .VD_P_0_(net1443), .VD_P_1_(net1444), .VIN1_PLUS(net1445), .VIN1_MINUS(net1446), .VIN2_PLUS(net1447), .VIN2_MINUS(net1448), .OUTPUT_0_(net1405[9]), .OUTPUT_1_(net1404[10]), .Vsel_0_(net1451), .Vsel_1_(net1452), .RUN(net1453), .Vg_0_(net1454), .Vg_1_(net1455), .PROG(net1456), .VTUN(net1457), .VINJ(net1458), .GND(net1459), .VPWR(net1460), .Vsel_b_0_(net1469), .Vsel_b_1_(net1470), .RUN_b(net1471), .Vg_b_0_(net1472), .Vg_b_1_(net1473), .PROG_b(net1474), .VTUN_b(net1475), .VINJ_b(net1476), .GND_b(net1477), .VPWR_b(net1478));
	TSMC350nm_TA2Cell_Strong cab_device_17 (.island_num(1), .row(4), .col(19), .VD_P_0_(net1461), .VD_P_1_(net1462), .VIN1_PLUS(net1463), .VIN1_MINUS(net1464), .VIN2_PLUS(net1465), .VIN2_MINUS(net1466), .OUTPUT_0_(net1405[10]), .OUTPUT_1_(net1404[11]), .Vsel_0_(net1469), .Vsel_1_(net1470), .RUN(net1471), .Vg_0_(net1472), .Vg_1_(net1473), .PROG(net1474), .VTUN(net1475), .VINJ(net1476), .GND(net1477), .VPWR(net1478), .Vsel_b_0_(net1488), .Vsel_b_1_(net1489), .Vg_b_0_(net1490), .Vg_b_1_(net1491), .VTUN_b(net1493), .VINJ_b(net1487), .GND_b(net1492));
	TSMC350nm_Cap_Bank cab_device_18 (.island_num(1), .row(5), .col(19), .VD_P_0_(net1479), .VD_P_1_(net1480), .VD_P_2_(net1481), .VD_P_3_(net1482), .VIN_0_(net1483), .VIN_1_(net1484), .OUT_0_(net1405[11]), .OUT_1_(net1404[12]), .VINJ(net1487), .Vsel_0_(net1488), .Vsel_1_(net1489), .Vg_0_(net1490), .Vg_1_(net1491), .GND(net1492), .VTUN(net1493), .VINJ_b(net1509), .GND_b(net1511), .VTUN_b(net1510));
	TSMC350nm_4WTA_IndirectProg cab_device_19 (.island_num(1), .row(6), .col(19), .VD_P_0_(net1494), .VD_P_1_(net1495), .VD_P_2_(net1496), .VD_P_3_(net1497), .Iin_0_(net1498), .Iin_1_(net1499), .Iin_2_(net1500), .Iin_3_(net1501), .Vout_0_(net1405[12]), .Vout_1_(net1404[13]), .Vout_2_(net1405[13]), .Vout_3_(net1404[14]), .Vmid(net1405[14]), .Vbias(net1404[15]), .Vsel(net1508), .Vs(net1404[0]), .VINJ(net1509), .VTUN(net1510), .GND(net1511), .PROG(net1512), .GND_b(net1519));
	TSMC350nm_NandPfets cab_device_20 (.island_num(1), .row(7), .col(19), .GATE_N(net1513), .SOURCE_N(net1514), .GATE_P(net1515), .SOURCE_P(net1516), .DRAIN_N(net1405[15]), .DRAIN_P(net1404[16]), .VPWR(net1404[0]), .GND(net1519), .VPWR_b(net1527), .GND_b(net1528));
	TSMC350nm_TGate_2nMirror cab_device_21 (.island_num(1), .row(8), .col(19), .IN_CM_0_(net1520), .IN_CM_1_(net1521), .SelN(net1522), .IN_TG(net1523), .OUT_CM_0_(net1405[16]), .OUT_CM_1_(net1404[17]), .OUT_TG(net1405[17]), .VPWR(net1527), .GND(net1528));

 	/*Programming Mux */ 
	TSMC350nm_VinjDecode2to4_vtile decoder(.island_num(1), .direction(vertical), .bits(6));
	TSMC350nm_drainSelect_progrundrains switch(.island_num(1), .direction(vertical), .num(12), .type(drain_select));
	TSMC350nm_4TGate_ST_draincutoff switch(.island_num(1), .direction(vertical), .num(12), .type(prog_switch));
	TSMC350nm_GorS_IndrctSwcs switch(.island_num(1), .direction(horizontal), .num(20), .switch_n0_Input_0_(net1404[0]), .switch_n0_Input_1_(net1405[0]), .switch_n8_Input_1_(net1405[8]), .switch_n9_Input_0_(net1404[9]), .switch_n9_Input_1_(net1405[9]), .switch_n10_Input_0_(net1404[10]), .switch_n10_Input_1_(net1405[10]), .switch_n11_Input_0_(net1404[11]), .switch_n11_Input_1_(net1405[11]), .switch_n12_Input_0_(net1404[12]), .switch_n12_Input_1_(net1405[12]), .switch_n13_Input_0_(net1404[13]), .switch_n13_Input_1_(net1405[13]), .switch_n14_Input_0_(net1404[14]), .switch_n14_Input_1_(net1405[14]), .switch_n15_Input_0_(net1404[15]), .switch_n15_Input_1_(net1405[15]), .switch_n16_Input_0_(net1404[16]), .switch_n16_Input_1_(net1405[16]), .switch_n17_Input_0_(net1404[17]), .switch_n17_Input_1_(net1405[17]));
	none switch_ind(.island_num(1), .direction(horizontal), .col(18));
	TSMC350nm_IndirectSwitches switch_ind(.island_num(1), .direction(horizontal), .col(19), .GND_0_(net1442), .CTRL_B_0_(net1508), .CTRL_B_1_(net1436), .run_r(net1437), .prog_r(net1512), .Vg_0_(net1438), .Vg_1_(net1439), .VTUN(net1440), .VINJ(net1441), .VDD_1_(net1404[0]));

 endmodule