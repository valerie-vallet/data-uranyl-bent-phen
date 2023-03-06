%mem=36000Mb
%NProc=12
%oldchk=tddft-uo2_2cl_2phen.pbe0-d3.optg.chk
%chk=tddft-uo2_2cl_2phen.pbe0-d3.freq.chk
#p PBE1PBE/GEN GFInput GFPrint 5D 7F Pseudo=Read
   IOP(2/9=2, 4/69=2, 6/7=3, 8/10=91, 8/37=50, 8/38=0)
   EmpiricalDispersion=GD3BJ
   Int=(UltraFine)
   Geom=(CheckPoint)
   Guess=(CheckPoint)
   Scf=(NoVarAcc,MaxCycle=100,conver=8)
   td=(triplets,nstates=4,root=1)
   Symmetry=(Follow, Loose, SaveOrientation, PrintOrientation)
   Freq=NoRaman

[UO2cl2(phen)2] - PBE0+D3BJ - ES in GP

 0  1

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

