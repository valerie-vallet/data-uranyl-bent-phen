%mem=8000Mb
%NProc=4
%chk=gs-uo2_cl2_2ar.pbe0-d3.optg.chk
#p PBE1PBE/GEN GFInput GFPrint 5D 7F IOP(6/7=3, 4/69=2, 6/10=1) Pseudo=Read
   EmpiricalDispersion=GD3BJ
   Symm=(Loose) Int=(UltraFine)
   Guess=(Read)
   Scf=(NoVarAcc,MaxCycle=100,conver=8)
   Opt=Tight

[UO2Cl2Ar2]2- - PBE0+D3BJ - GS

 0  1
U         -0.00000       -0.00432        0.00000
O         -1.77434       -0.05158       -0.00000
O          1.77434       -0.05158        0.00000
Cl        -0.00000       -1.47154        2.07688
Cl         0.00000       -1.47154       -2.07688
Ar         0.00000        1.42127       -2.59790
Ar        -0.00000        1.42127        2.59790

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

