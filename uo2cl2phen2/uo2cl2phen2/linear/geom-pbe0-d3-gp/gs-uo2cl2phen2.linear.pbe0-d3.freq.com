%mem=24000Mb
%NProc=8
%oldchk=gs-uo2cl2phen2.linear.pbe0-d3.optg.chk
%chk=gs-uo2cl2phen2.linear.pbe0-d3.freq.chk
#p PBE1PBE/GEN GFInput GFPrint 5D 7F IOP(6/7=3, 4/69=2, 6/10=1) Pseudo=Read
   EmpiricalDispersion=GD3BJ
   Symm=(Loose) Int=(UltraFine)
   Guess=(CheckPoint)
   Geom=(ModRedundant,CheckPoint)
   Scf=(NoVarAcc,MaxCycle=100,conver=8)
   Freq=Raman

[UO2cl2(phen)2] - Linear PBE0+D3BJ - GS

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

