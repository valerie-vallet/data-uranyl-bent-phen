%mem=16000Mb
%NProc=8
%oldchk=gs-uo2cl2phen2.mp2.sp.chk
%chk=gs-uo2cl2phen2.bhlyp.sp.chk
#p BHandHLYP/GEN GFInput GFPrint 5D 7F IOP(6/7=3, 4/69=2, 6/10=1) Pseudo=Read
   Symm=(Loose) Int=(UltraFine)
   Guess=(CheckPoint) Geom=CheckPoint
   Scf=(NoVarAcc,MaxCycle=100,conver=8)

[UO2cl2(phen)2] - MP2 - GS

 0  1

!input file for basis set of U
@/home/vallet/basis.gaussian/U-ECP60MWB_SEG/N
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
@/home/vallet/basis.gaussian/U-ECP60MWB/N

