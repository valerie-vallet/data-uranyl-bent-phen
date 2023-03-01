%mem=8000Mb
%NProc=8
%chk=gs-uo2_cl2.linear.mp2.sp.chk
#p MP2(MaxDisk=500Gb, Window=(22,0))/GEN GFInput GFPrint 5D 7F IOP(6/7=3, 4/69=2, 6/10=1) Pseudo=Read
   Symm=(Loose) Int=(UltraFine)
   Guess=(CheckPoint)
   Scf=(NoVarAcc,MaxCycle=100,conver=8)
   Geom=(CheckPoint,ModRedundant)
   Symmetry=Loose

UO2Cl2 - linear - MP2 - GP

 0  1

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

!input file for ECP for U
@/home/vallet/basis/U-ECP60MWB/N

