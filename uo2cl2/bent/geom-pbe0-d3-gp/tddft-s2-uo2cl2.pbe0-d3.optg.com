%mem=8000Mb
%NProc=4
%oldchk=gs-uo2_cl2.pbe0-d3.optg.chk
%chk=tddft-s2-uo2_cl2.pbe0-d3.optg.chk
#p PBE1PBE/GEN GFInput GFPrint 5D 7F Pseudo=Read
   IOP(2/9=2, 4/69=2, 6/7=3, 8/10=91, 8/37=22, 8/38=0)
   EmpiricalDispersion=GD3BJ
   Symm=(Loose) Int=(UltraFine)
   Guess=(Harris)
   Scf=(NoVarAcc,MaxCycle=100,conver=8)
   td=(triplets,nstates=4,root=2)
   Opt=Tight

[UO2Cl4]2- - PBE0+D3BJ - ES

 0  1
U          0.00000        0.28722       -0.00000
O         -1.77414        0.31429       -0.00000
O          1.77414        0.31429        0.00000
Cl         0.00000       -1.10604       -2.07747
Cl        -0.00000       -1.10604        2.07747

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

