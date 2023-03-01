%mem=4000Mb
%NProc=4
%oldchk=gs-uo2cl2.pbe0-d3.freq.chk
%chk=gs-uo2_cl2.mp2.sp.chk
#p MP2(MaxDisk=500Gb, Window=(22,0))/GEN GFInput GFPrint 5D 7F IOP(6/7=3, 4/69=2, 6/10=1) Pseudo=Read
   Symm=(Loose) Int=(UltraFine)
   Guess=(CheckPoint)
   Scf=(NoVarAcc,MaxCycle=100,conver=8)
   Geom=(CheckPoint)
   Symmetry=Loose

[UO2Cl2-bent] - SP MP2 calculation at the PBE0 geometry

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

!input file for ECP for U
@/home/vallet/basis.gaussian/U-ECP60MWB/N

