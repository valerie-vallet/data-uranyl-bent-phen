%mem=8000Mb
%NProc=4
%oldchk=gs-uo2cl2.linear.pbe0-d3.optg.chk
%chk=gs-uo2cl2.linear.pbe0-d3.freq.chk
#p PBE1PBE/GEN GFInput GFPrint 5D 7F IOP(6/7=3, 4/69=2, 6/10=1) Pseudo=Read
   EmpiricalDispersion=GD3BJ
   Symm=(Loose) Int=(UltraFine)
   Guess=(Harris)
   Scf=(NoVarAcc,MaxCycle=100,conver=8)
   Geom=(CheckPoint,ModRedundant)
   Symmetry=Loose
   Freq=Raman

[UO2Cl4]2-

 0  1

L 2 1 3 F

!input file for basis set of U
@/home/vallet/basis.gaussian/U-ECP60MWB_SEG/N
****
Cl 0
Def2TZVP
****
O  0
Def2TZVP
****

!input file for ECP for U
@/home/vallet/basis.gaussian/U-ECP60MWB/N

