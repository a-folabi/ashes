module TOP(port1); 
    sky130_hilas_ScannerVertical I__0 (.island_num(0), .row(1), .col(1), .INPUT1_1(a_net1), .INPUT1_2(a_net2), .INPUT1_3(a_net3), .INPUT1_4(a_net4), .RESET_B_1(a_net5), .OUTPUT(a_net6), .CLK1(a_net7), .D(a_net8));
    
    pads_smallframe FRAME (.IO_1(a_net1), .IO_2(a_net2), .IO_92(a_net3), .IO_91(a_net4), .IO_3(a_net5), .IO_90(a_net6), .IO_89(a_net7), .IO_4(a_net8));
endmodule

module other(port1);
    sky130_hilas_ScannerVertical I__0 (.island_num(0), .row(1), .col(1), .INPUT1_1(a_net1), .INPUT1_2(a_net2), .INPUT1_3(a_net3), .INPUT1_4(a_net4), .RESET_B_1(a_net5), .OUTPUT(a_net6), .CLK1(a_net7), .D(a_net8));
    tsmc65_stdcell_nfetGroup I__1 (.island_num(1), .row(1), .col(1), .nfet_small_src(a_net9), .nfet_med_src(a_net10), .nfet_large_src(a_net11), .nfet_gate(a_net12), .nfet_drain(a_net13));
    tsmc65_stdcell_pfetGroup I__2 (.island_num(2), .row(1), .col(1), .pfet_small_src(a_net14), .pfet_med_src(a_net15), .pfet_large_src(a_net16), .pfet_gate(a_net17), .pfet_drain(a_net18), .pfet_body(a_net19));
    sky130_hilas_Alice_AmpDetect I__3 (.island_num(3), .row(1), .col(1), .colsel(a_net20), .gate(a_net21), .ampdet_out(a_net22));
    sky130_hilas_TA2Cell_1FG I__4 (.island_num(4), .row(1), .col(1), .colsel2(a_net23), .gate1(a_net24), .colsel1(a_net25), .out_one(a_net26), .gate2(a_net27), .out_two(a_net28));
    sky130_hilas_TA2Cell_NoFG I__5 (.island_num(5), .row(1), .col(1), .gate(a_net29), .out_one(a_net30), .colsel(a_net31), .out_two(a_net32));
    sky130_hilas_TA2Cell_1FG_Strong I__6 (.island_num(6), .row(1), .col(1), .colsel2(a_net33), .colsel1(a_net34), .out_two(a_net35), .gate2(a_net36), .gate1(a_net37), .out_one(a_net38));
    sky130_hilas_Alice_BPF I__7 (.island_num(7), .row(1), .col(1), .colsel2(a_net39), .gate1(a_net40), .out(a_net41), .gate2(a_net42), .colsel1(a_net43));
    sky130_hilas_VMMWTA I__8 (.island_num(8), .row(1), .col(1), .vgate2(a_net44), .vgate(a_net45), .output1(a_net46), .output2(a_net47), .vgate1(a_net48), .col_sel(a_net49), .output3(a_net50), .output4(a_net51));
    sky130_hilas_FGcharacterization01 I__9 (.island_num(9), .row(1), .col(1), .Gate1(a_net52), .Gate3(a_net53), .Output(a_net54), .Vref(a_net55), .SOURCE(a_net56), .Gate2(a_net57), .Gate4(a_net58), .LargeCapacitor(a_net59), .Vbias(a_net60), .DRAIN(a_net61));
    sky130_hilas_swc4x2celld3 I__10 (.island_num(10), .row(1), .col(1), .Vgate1(a_net62), .Vgate2(a_net63));
    sky130_hilas_swc4x4_indirect I__11 (.island_num(11), .row(1), .col(1), .col_sel1(a_net64), .gate2(a_net65), .col_sel3(a_net66), .gate4(a_net67), .run_drain4(a_net68), .run_drain3(a_net69), .gate1(a_net70), .col_sel2(a_net71), .gate3(a_net72), .col_sel4(a_net73), .run_drain1(a_net74), .run_drain2(a_net75));
    
    pads_smallframe FRAME (.IO_1(a_net1), .IO_2(a_net2), .IO_92(a_net3), .IO_91(a_net4), .IO_3(a_net5), .IO_90(a_net6), .IO_89(a_net7), .IO_4(a_net8), .IO_5(a_net9), .IO_6(a_net10), .IO_7(a_net11), .IO_88(a_net12), .IO_87(a_net13), .IO_8(a_net14), .IO_9(a_net15),.IO_10(a_net16), .IO_86(a_net17), .IO_85(a_net18), .IO_84(a_net19), .IO_11(a_net20), .IO_83(a_net21), .IO_82(a_net22), .IO_12(a_net23), .IO_13(a_net24), .IO_14(a_net25), .IO_15(a_net26), .IO_81(a_net27), .IO_80(a_net28), .IO_16(a_net29), .IO_17(a_net30), .IO_79(a_net31), .IO_78(a_net32), .IO_18(a_net33), .IO_19(a_net34), .IO_20(a_net35), .IO_77(a_net36), .IO_76(a_net37), .IO_75(a_net38), .IO_21(a_net39), .IO_22(a_net40), .IO_23(a_net41), .IO_74(a_net42), .IO_73(a_net43), .IO_24(a_net44), .IO_25(a_net45), .IO_26(a_net46), .IO_27(a_net47), .IO_72(a_net48), .IO_70(a_net49), .IO_69(a_net50), .IO_68(a_net51), .IO_28(a_net52), .IO_29(a_net53), .IO_30(a_net54), .IO_31(a_net55), .IO_32(a_net56), .IO_67(a_net57), .IO_66(a_net58), .IO_65(a_net59), .IO_64(a_net60), .IO_63(a_net61), .IO_62(a_net62), .IO_61(a_net63), .IO_35(a_net64), .IO_36(a_net65), .IO_37(a_net66), .IO_38(a_net67), .IO_39(a_net68), .IO_40(a_net69), .IO_58(a_net70), .IO_57(a_net71), .IO_56(a_net72), .IO_55(a_net73), .IO_54(a_net74), .IO_53(a_net75) );
endmodule