%mem=8000Mb
%NProc=4
%oldchk=tddft-s1-uo2_cl2_2ar.pbe0-d3.optg.chk
%chk=tddft-s1-uo2_cl2_2ar.pbe0-d3.freq.chk
#p PBE1PBE/GEN GFInput GFPrint 5D 7F Pseudo=Read
   IOP(2/9=2, 4/69=2, 6/7=3, 8/10=91, 8/37=32, 8/38=0)
   EmpiricalDispersion=GD3BJ
   Symm=(Loose) Int=(UltraFine)
   Guess=(Read) Geom=CheckPoint
   Scf=(NoVarAcc,MaxCycle=100,conver=8)
   td=(triplets,nstates=4,root=1)
   Freq

[UO2Cl2Ar2]2- - PBE0+D3BJ - GS

 0  1

!input file for basis set of U
@/home/vallet/basis/U-ECP60MWB_SEG/N
****
!input file for basis set of Ar
@/home/vallet/basis/Ar-ECP10MWB_SEG/N
****
Cl 0
Def2TZVP
****
O  0
Def2TZVP
****

!input file for ECP for U
@/home/vallet/basis/U-ECP60MWB/N
!input file for ECP for Ar
@/home/vallet/basis/Ar-ECP10MWB/N

