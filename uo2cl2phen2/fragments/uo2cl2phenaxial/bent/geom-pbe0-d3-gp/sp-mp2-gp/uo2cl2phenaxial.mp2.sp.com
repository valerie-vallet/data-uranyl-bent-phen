%mem=8000Mb
%NProcShared=8
%chk=uo2_2cl_phenaxial.mp2.sp.chk
#p MP2(MaxDisk=500Gb, Window(36,0))/GEN GFInput GFPrint 5D 7F IOP(6/7=3, 4/69=2, 6/10=1) Pseudo=Read
   Symm=(Loose) Int=(UltraFine)
   Guess=(CheckPoint) Geom=CheckPoint
   Scf=(NoVarAcc,MaxCycle=100,conver=8)

[UO2Cl2(phen)_axial] - MP2 - GS

 0 1

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

