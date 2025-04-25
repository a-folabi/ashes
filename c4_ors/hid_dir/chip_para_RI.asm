/* RI (Recover Injection Above & Sub threshold) parameters */
.set RI_GATE_S_SWC, 0x0040 /* Gate(SWC) = gnd */
.set RI_VC1_SWC, 9087 /* Ivfg @Vgm=0V -> 1nA@Vgm=0.6V */
.set RI_VC2_SWC, 8815 /* Ivfg*2/5 @Vgm=0V */
.set RI_VC3_SWC, 7998 /* Ivfg*1/10 @Vgm=0V */
.set RI_VC4_SWC, 6364 /* Ivfg=1nA @Vgm=0V */
.set RI_VD1_SWC, 0xea0e /* Vd @ final stage */
.set RI_VD2_SWC, 0xfe0e /* Vd @ pre-final stage */
.set RI_INJ_T_SWC, 1 /* Injection time unit (*10us) */
.set RI_NUM_SWC, 300 /* # of Recover Injection */

.set RI_GATE_S_OTA, 0x3730 /* Gate(OTA) = 2.5V */
.set RI_VC1_OTA, 10613 /* Ivfg @Vgm=0V -> 1nA@Vgm=0.6V */
.set RI_VC2_OTA, 10188 /* Ivfg*2/5 @Vgm=0V */
.set RI_VC3_OTA, 8913 /* Ivfg*1/10 @Vgm=0V */
.set RI_VC4_OTA, 6364 /* Ivfg=1nA @Vgm=0V */
.set RI_VD1_OTA, 0xea0e /* Vd @ final stage */
.set RI_VD2_OTA, 0xfe0e /* Vd @ pre-final stage */
.set RI_INJ_T_OTA, 1 /* Injection time unit (*10us) */
.set RI_NUM_OTA, 300 /* # of Recover Injection */

.set RI_GATE_S_OTAREF, 0x0040 /* Gate(OTAREF) = gnd */
.set RI_VC1_OTAREF, 9291 /* Ivfg @Vgm=0V -> 1nA@Vgm=0.6V */
.set RI_VC2_OTAREF, 8998 /* Ivfg*2/5 @Vgm=0V */
.set RI_VC3_OTAREF, 8120 /* Ivfg*1/10 @Vgm=0V */
.set RI_VC4_OTAREF, 6364 /* Ivfg=1nA @Vgm=0V */
.set RI_VD1_OTAREF, 0xea0e /* Vd @ final stage */
.set RI_VD2_OTAREF, 0xfe0e /* Vd @ pre-final stage */
.set RI_INJ_T_OTAREF, 1 /* Injection time unit (*10us) */
.set RI_NUM_OTAREF, 300 /* # of Recover Injection */

.set RI_GATE_S_MITE, 0x3730 /* Gate(MITE) = 2.0V */
.set RI_VC1_MITE, 11266 /* Ivfg @Vgm=0V -> 1nA@Vgm=0.6V */
.set RI_VC2_MITE, 10776 /* Ivfg*2/5 @Vgm=0V */
.set RI_VC3_MITE, 9305 /* Ivfg*1/10 @Vgm=0V */
.set RI_VC4_MITE, 6364 /* Ivfg=1nA @Vgm=0V */
.set RI_VD1_MITE, 0xea0e /* Vd @ final stage */
.set RI_VD2_MITE, 0xfe0e /* Vd @ pre-final stage */
.set RI_INJ_T_MITE, 1 /* Injection time unit (*10us) */
.set RI_NUM_MITE, 300 /* # of Recover Injection */

.set RI_GATE_S_DIRSWC, 0x0530 /* Gate(DIRSWC) = 1.4V */
.set RI_VC1_DIRSWC, 9090 /* Ivfg @Vgm=0V -> 1nA@Vgm=0.6V */
.set RI_VC2_DIRSWC, 8817 /* Ivfg*2/5 @Vgm=0V */
.set RI_VC3_DIRSWC, 7999 /* Ivfg*1/10 @Vgm=0V */
.set RI_VC4_DIRSWC, 6364 /* Ivfg=1nA @Vgm=0V */
.set RI_VD1_DIRSWC, 0xea0e /* Vd @ final stage */
.set RI_VD2_DIRSWC, 0xfe0e /* Vd @ pre-final stage */
.set RI_INJ_T_DIRSWC, 1 /* Injection time unit (*10us) */
.set RI_NUM_DIRSWC, 300 /* # of Recover Injection */

/* RIL (Recover Injection low sub threshold) parameters */
.set RIL_GATE_S_SWC, 0x0040 /* Gate(SWC) = gnd */
.set RIL_VC1_SWC, 6364 /* Ivfg=1n A@Vgm=0V */
.set RIL_VC2_SWC, 5832 /* Ivfg=lowest current @Vgm=0V */
.set RIL_VD1_SWC, 0xea0e /* Vd @ final stage */
.set RIL_INJ_T_SWC, 1 /* Injection time unit (*10us) */
.set RIL_NUM_SWC, 300 /* # of Recover Injection */

.set RIL_GATE_S_OTA, 0x3730 /* Gate(OTA) = 2.5V */
.set RIL_VC1_OTA, 6364 /* Ivfg=1n A@Vgm=0V */
.set RIL_VC2_OTA, 5856 /* Ivfg=lowest current @Vgm=0V */
.set RIL_VD1_OTA, 0xea0e /* Vd @ final stage */
.set RIL_INJ_T_OTA, 1 /* Injection time unit (*10us) */
.set RIL_NUM_OTA, 300 /* # of Recover Injection */

.set RIL_GATE_S_OTAREF, 0x0040 /* Gate(OTAREF) = gnd */
.set RIL_VC1_OTAREF, 6364 /* Ivfg=1n A@Vgm=0V */
.set RIL_VC2_OTAREF, 5859 /* Ivfg=lowest current @Vgm=0V */
.set RIL_VD1_OTAREF, 0xea0e /* Vd @ final stage */
.set RIL_INJ_T_OTAREF, 1 /* Injection time unit (*10us) */
.set RIL_NUM_OTAREF, 300 /* # of Recover Injection */

.set RIL_GATE_S_MITE, 0x3730 /* Gate(MITE) = 2.0V */
.set RIL_VC1_MITE, 6364 /* Ivfg=1n A@Vgm=0V */
.set RIL_VC2_MITE, 5887 /* Ivfg=lowest current @Vgm=0V */
.set RIL_VD1_MITE, 0xea0e /* Vd @ final stage */
.set RIL_INJ_T_MITE, 1 /* Injection time unit (*10us) */
.set RIL_NUM_MITE, 300 /* # of Recover Injection */

.set RIL_GATE_S_DIRSWC, 0x0530 /* Gate(DIRSWC) = 1.4V */
.set RIL_VC1_DIRSWC, 6364 /* Ivfg=1n A@Vgm=0V */
.set RIL_VC2_DIRSWC, 5914 /* Ivfg=lowest current @Vgm=0V */
.set RIL_VD1_DIRSWC, 0xea0e /* Vd @ final stage */
.set RIL_INJ_T_DIRSWC, 1 /* Injection time unit (*10us) */
.set RIL_NUM_DIRSWC, 300 /* # of Recover Injection */

