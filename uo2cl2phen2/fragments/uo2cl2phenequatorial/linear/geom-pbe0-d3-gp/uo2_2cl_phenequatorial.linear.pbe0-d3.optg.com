%mem=48000Mb
%NProcShared=16
%chk=uo2_2cl_phenequatorial.linear.pbe0-d3.optg.chk
#p PBE1PBE/GEN GFInput GFPrint 5D 7F IOP(6/7=3, 4/69=2, 6/10=1) Pseudo=Read
   EmpiricalDispersion=GD3BJ
   Symm=(Loose) Int=(UltraFine)
   Guess=(Harris) Geom=ModRedundant
   Scf=(NoVarAcc,MaxCycle=100,conver=8)
   Symm=Loose
   Opt=Tight

[UO2Cl2(phen)_axial] - PBE0+D3BJ - GS

 0 1
 U     0.000000     0.000000     0.134507
 O    -1.735028     0.000000     0.389354
 O     1.735072     0.000000    -0.120037
 N     0.650768     1.373087     2.303342
 C     0.820432     2.684333     2.278278
 H     0.677338     3.162245     1.318312
 C     1.163413     3.440744     3.401060
 H     1.285032     4.511202     3.302242
 C     1.336540     2.803970     4.598778
 H     1.602924     3.351267     5.495709
 C     1.165122     1.413323     4.664889
 C     1.333123     0.699896     5.886307
 H     1.599413     1.258165     6.776004
 C     1.163696    -0.639555     5.929941
 H     1.289956    -1.188337     6.855701
 C     0.813629    -1.365503     4.755412
 C     0.633215    -2.756367     4.779913
 H     0.762353    -3.294105     5.712189
 C     0.297442    -3.405440     3.624082
 H     0.148173    -4.476566     3.595028
 C     0.144300    -2.661019     2.452408
 H    -0.120944    -3.148800     1.523901
 N     0.306332    -1.349957     2.392048
 C     0.638653    -0.693532     3.527311
 C     0.818557     0.728748     3.480979
Cl     0.112603     2.492878    -0.887272
Cl    -0.519287    -2.502706    -0.724535

L 2 1 3 F

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

