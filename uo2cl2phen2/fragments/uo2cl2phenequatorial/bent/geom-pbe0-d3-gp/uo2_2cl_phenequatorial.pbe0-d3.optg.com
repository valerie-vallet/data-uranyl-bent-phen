%mem=48000Mb
%NProcShared=16
%chk=uo2_2cl_phenequatorial.pbe0-d3.optg.chk
#p PBE1PBE/GEN GFInput GFPrint 5D 7F IOP(6/7=3, 4/69=2, 6/10=1) Pseudo=Read
   EmpiricalDispersion=GD3BJ
   Symm=(Loose) Int=(UltraFine)
   Guess=(Harris)
   Scf=(NoVarAcc,MaxCycle=100,conver=8)
   Opt=Tight

[UO2Cl2(phen)_axial] - PBE0+D3BJ - GS

 0 1
 U     0.000000    -0.000000     0.134507
 O    -1.735028     0.000000     0.389354
 O     1.735028    -0.000000     0.389354
 N    -0.000000     1.373087     2.398871
 C    -0.000000     2.695378     2.416927
 H    -0.000000     3.182326     1.450857
 C    -0.000000     3.452169     3.590683
 H    -0.000000     4.532056     3.525268
 C    -0.000000     2.803784     4.794668
 H    -0.000000     3.350910     5.730420
 C    -0.000000     1.401215     4.815954
 C    -0.000000     0.675414     6.041629
 H    -0.000000     1.233642     6.970347
 C     0.000000    -0.675414     6.041629
 H     0.000000    -1.233642     6.970347
 C     0.000000    -1.401215     4.815954
 C     0.000000    -2.803784     4.794668
 H     0.000000    -3.350910     5.730420
 C     0.000000    -3.452169     3.590683
 H     0.000000    -4.532056     3.525268
 C     0.000000    -2.695378     2.416927
 H     0.000000    -3.182326     1.450857
 N     0.000000    -1.373087     2.398871
 C     0.000000    -0.717180     3.582062
 C    -0.000000     0.717180     3.582062
Cl    -0.000000     2.519009    -0.827649
Cl     0.000000    -2.519009    -0.827649

!input file for basis set of U
@/home/vallet/basis/U-ECP60MWB_SEG/N
****
Cl 0
Def2TZVP
****
O  0
Def2TZVP
****
N  0
Def2TZVP
****
C  0
Def2TZVP
****
H  0
Def2TZVP
****

!input file for ECP for U
@/home/vallet/basis/U-ECP60MWB/N

