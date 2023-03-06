#!/usr/bin/env python3

"""
This script creates an input XML file for the ezFCF 1.0 (formerly ezSpectrum) program

Script supports the following ab initio outputs:

Q-Chem
ACES II (versions 0.3 [old] and 2.5.0 [new])
Cfour (should be handled by new ACES II)
Molpro
GAMESS (linear molecules are not supported)
ORCA
Gaussian (we can not guarantee it works, since we are not allowed to touch it)

Script requires a set of ab initio outputs with frequency jobs in
the optimized geometries. First file in the argument's list is
the initial state, others are the target states.
From each file this script copies a geometry, frequencies and
normal modes into the XML file.
Default job parameters and energy difference between the electronic
states (IP, EA, etc) should be adjusted as necessary in the created XML file.
"""

import sys

DEFAULT_JOB_PARAMETERS = """<input
  job = "harmonic_pes">

<job_parameters
        temperature                              = "300"
        spectrum_intensity_threshold             = "0.001" >
</job_parameters>

<!--
  ______________________________________________________________________

    Tags which start with "OPT_" will be ignored.
    To include these optional keywords please "uncomment" by removing
    "OPT_" from the start and the corresponding end tag (if present)
  ______________________________________________________________________

 -->

<parallel_approximation
        max_vibr_excitations_in_initial_el_state = "1"
        max_vibr_excitations_in_target_el_state  = "4"
        combination_bands                        = "true"
        use_normal_coordinates_of_target_states  = "true"
 >

  <OPT_do_not_excite_subspace size = "0" normal_modes = " " >
  </OPT_do_not_excite_subspace>

  <OPT_energy_thresholds  units="eV, K, cm-1">
    <initial_state   units="K">      1000    </initial_state>
    <target_state   units="eV">      0.25    </target_state>
  </OPT_energy_thresholds>

  <OPT_print_franck_condon_matrices flag="true">
  </OPT_print_franck_condon_matrices>

</parallel_approximation>

<!--
  ______________________________________________________________________

 -->

<OPT_dushinsky_rotations target_state="1"
      max_vibr_excitations_in_initial_el_state = "1"
      max_vibr_excitations_in_target_el_state  = "4"
      >
  <OPT_max_vibr_to_store  target_el_state="4">
  </OPT_max_vibr_to_store>

  <OPT_do_not_excite_subspace size = "2" normal_modes = "0 1">
  </OPT_do_not_excite_subspace>

  <OPT_energy_thresholds  units="eV, K, cm-1">
    <initial_state   units="K">      1000    </initial_state>
    <target_state   units="eV">      0.25    </target_state>
  </OPT_energy_thresholds>

  <OPT_single_excitation
       ini="0"
       targ="1v1">
  </OPT_single_excitation>

</OPT_dushinsky_rotations>

<!--
  ______________________________________________________________________

 -->\n\n"""

WRONG_INPUT = """To create an XML file from ab initio outputs type:
make_xml.py  <filename.xml> <initial_state.out> <target_state_1.out> <target_state_2.out> etc...
"""


def parse_qchem(StateF, data: dict):
    """ Parser of a Q-Chem output. """
    no_lines_with_frequencies = 0
    if_geometry_is_loaded = False
    Line = StateF.readline()
    while Line:
        if (Line.find('Standard Nuclear Orientation') >= 0) and (if_geometry_is_loaded is False):
            StateF.readline()
            StateF.readline()
            Line = StateF.readline()
            while Line.find('----') == -1:
                data['NAtoms'] += 1
                data['Geometry'] += Line[5:]
                data['atoms_list'] += Line[8:14]
                Line = StateF.readline()
            if_geometry_is_loaded = True

        if Line.find('Raman Active: ') >= 0:
            StateF.readline()
            for _ in range(data['NAtoms']):
                Line = StateF.readline()
                data['NormalModes'] += Line[2:]
            data['NormalModes'] += '\n'

        # TODO: I do not understand the comment below. 
        # It comes from the previous version of the script. Pawel

        # remove end of the line symbols!!!
        if Line.find('Frequency: ') >= 0:
            data['Frequencies'] += Line.replace('Frequency:', '')
            no_lines_with_frequencies += 1

        Line = StateF.readline()

    if no_lines_with_frequencies == data['NAtoms']-1:
        data['ifLinear'] = True

    data['if_normal_modes_weighted'] = True
    data['geometry_units'] = "angstr"

    # END Q-Chem
    # =========================================================================


def parse_aces_old(StateF, data: dict):
    """ Parser of an ACESII 0.3 version output. """
    no_lines_with_frequencies = 0
    if_geometry_is_loaded = False
    Line = StateF.readline()
    while Line:
        # TODO: I do not understand the comment below. 
        # It comes from the previous version of the script. Pawel

        # in FREQ job only one such line. Check it if it will be from OPT job....
        if (Line.find('Coordinates (in bohr)') >= 0) and (if_geometry_is_loaded is False):
            StateF.readline()
            StateF.readline()
            Line = StateF.readline()
            while Line.find('----') == -1:
                data['NAtoms'] += 1
                data['Geometry'] += "      " + Line[5:9] + Line[20:]
                data['atoms_list'] += Line[5:9]
                Line = StateF.readline()
                if_geometry_is_loaded = True

        if Line.find('Normal Coordinates') >= 0:
            Line = StateF.readline()
            while Line == "\n":
                StateF.readline()
                Line = StateF.readline()
                no_lines_with_frequencies += 1
                data['Frequencies'] += Line
                StateF.readline()
                StateF.readline()
                for _ in range(data['NAtoms']):
                    Line = StateF.readline()
                    data['NormalModes'] += Line[4:]
                data['NormalModes'] += '\n'
                Line = StateF.readline()
        Line = StateF.readline()
    if no_lines_with_frequencies == data['NAtoms']-1:
        data['ifLinear'] = True

    data['if_normal_modes_weighted'] = False
    data['geometry_units'] = "au"

    # END ACES_OLD
    # =========================================================================


def parse_aces_new(StateF, data: dict):
    """ Parser of an ACESII 2.5.0 version output. """
    no_lines_with_frequencies = 0
    if_geometry_is_loaded = False
    Line = StateF.readline()
    while Line:
        # TODO: I do not understand the comment below. 
        # It comes from the previous version of the script. Pawel

        # in FREQ job only one such line. Check it if it will be from OPT job....
        if (Line.find('C o o r d i n a t e s') >= 0) and (if_geometry_is_loaded is False):
            StateF.readline()
            StateF.readline()
            Line = StateF.readline()
            while Line.find('----') == -1:
                data['NAtoms'] += 1
                data['Geometry'] += "      " + Line[5:9] + Line[20:]
                data['atoms_list'] += Line[5:9]
                Line = StateF.readline()
            if_geometry_is_loaded = True

        if Line.find('Normal Coordinates') >= 0:
            Line = StateF.readline()
            Line = StateF.readline()
            while Line == "\n":
                StateF.readline()
                Line = StateF.readline()
                no_lines_with_frequencies += 1
                data['Frequencies'] += Line
                StateF.readline()
                StateF.readline()
                for _ in range(data['NAtoms']):
                    Line = StateF.readline()
                    data['NormalModes'] += Line[4:]
                data['NormalModes'] += '\n'
                Line = StateF.readline()
        Line = StateF.readline()
    if no_lines_with_frequencies == data['NAtoms']-1:
        data['ifLinear'] = True

    data['if_normal_modes_weighted'] = False
    data['geometry_units'] = "au"

# END ACES_NEW
# ================================================================================


def parse_molpro_old(StateF, data: dict):
    """ Parser of a Molpro output. """
    normal_coordinates = []
    n_normal_modes = 0
    no_lines_with_frequencies = 0
    if_geometry_is_loaded = False
    if_frequencies_are_loaded = False
    if_normal_modes_are_loaded = False

    Line = StateF.readline()
    while Line:
        # geometry
        if (Line.find('ATOMIC COORDINATES') >= 0) and (if_geometry_is_loaded is False):
            StateF.readline()
            StateF.readline()
            StateF.readline()
            Line = StateF.readline()
            while Line.find('Bond lengths in Bohr (Angstrom)') == -1:
                data['NAtoms'] += 1
                data['Geometry'] += "      " + Line[5:8] + Line[19:]
                data['atoms_list'] += Line[5:8]
                Line = StateF.readline()
            if_geometry_is_loaded = True
            data['NAtoms'] -= 1
            # create an empty list of coordinates for every atom in form "X_nm1 Y_nm1 Z_nm1 X_nm2 Y_nm2 Z_nm2 X_nm3..."
            for i in range(data['NAtoms']):
                normal_coordinates.append([])

        if (Line.find('Intensities [relative]') >= 0) and (if_normal_modes_are_loaded is False):
            for i in range(data['NAtoms']):
                LineX = StateF.readline()
                LineY = StateF.readline()
                LineZ = StateF.readline()

                # analyse the length of the line 20+12*j:
                nm_per_line = (len(LineX)-23)//12

                n_normal_modes += nm_per_line

                for j in range(nm_per_line):
                    new_entry = LineX[23+12*j:23+12*(j+1)] + LineY[23+12*j:23+12*(j+1)] + LineZ[23+12*j:23+12*(j+1)]
                    normal_coordinates[i].append(new_entry)

            n_normal_modes //= data['NAtoms']  # repeated "NAtoms"-times

        if (Line.find('Wavenumbers [cm-1]') >= 0) and (if_frequencies_are_loaded is False):
            data['Frequencies'] += Line.replace('Wavenumbers [cm-1]', '')
            no_lines_with_frequencies += 1

        if Line.find('Normal Modes of low/zero frequencies') >= 0:
            if_frequencies_are_loaded = True
            if_normal_modes_are_loaded = True

        Line = StateF.readline()

    # now create normal modes in q-chem format:
    printed_normal_modes = 0
    for_range = len(normal_coordinates[0])//3
    for j in range(for_range):
        for i in range(data['NAtoms']):
            new_entry = normal_coordinates[i][j*3] + "   "
            new_entry += normal_coordinates[i][j*3 + 1] + "   "
            new_entry += normal_coordinates[i][j*3 + 2] + '\n'
            data['NormalModes'] += new_entry
        printed_normal_modes += 3
        data['NormalModes'] += '\n'

    # add the reminder of 3
    reminder = len(normal_coordinates[0]) % 3
    if reminder > 0:
        for i in range(data['NAtoms']):
            for j in range(reminder):
                data['NormalModes'] += normal_coordinates[i][printed_normal_modes + j] + "   "
            data['NormalModes'] += '\n'
        data['NormalModes'] += '\n'

    if n_normal_modes == (3 * data['NAtoms'] - 5):
        data['ifLinear'] = True

    data['if_normal_modes_weighted'] = True
    data['geometry_units'] = "au"

    # END OLD MOLPRO
    # =========================================================================


def parse_molpro_new(StateF, data: dict):
    """ Parser of a new version of the Molpro output. """
    normal_coordinates = []
    n_normal_modes = 0
    no_lines_with_frequencies = 0
    if_geometry_is_loaded = False
    if_frequencies_are_loaded = False
    if_normal_modes_are_loaded = False

    Line = StateF.readline()
    while Line:
        # geometry
        if (Line.find('Atomic Coordinates') >= 0) and (if_geometry_is_loaded is False):
            StateF.readline()
            StateF.readline()
            StateF.readline()
            Line = StateF.readline()
            """
             parse_molpro_old seraches for 'Bond lengths in Bohr (Angstrom)' 
             to detect the end of the atoms list.
             This section is missing in the 2015 version.
             I have replaced it with a search for an empty line as a marker 
             of the end of the atoms list. Pawel
             Aug 2021:
             After a bug reported by Wensha, I added the section assuring 
             that the first letter of a symbol is uppercase and the 
             second one is lowercase. Pawel
            """
            while not Line.rstrip() == '':
                # atom name is the first (not zeroth) position in the line
                atom_symbol = Line.split()[1].lower()
                # assure that cases are correct
                atom_symbol = Line.split()[1].lower()
                atom_symbol = atom_symbol[0].upper() + atom_symbol[1:]
                # display symbol as 3 characters long string (fill with spaces)
                atom_symbol = f"{atom_symbol:3s}" 
                data['NAtoms'] += 1
                data['Geometry'] += "      " + atom_symbol + Line[19:]
                data['atoms_list'] += atom_symbol
                Line = StateF.readline()
            if_geometry_is_loaded = True
            # create an empty list of coordinates for every atom in form 
            # "X_nm1 Y_nm1 Z_nm1 X_nm2 Y_nm2 Z_nm2 X_nm3..."
            for i in range(data['NAtoms']):
                normal_coordinates.append([])

        """
         Everything below works just the same as in the pasrse_molpro_old. Pawel
        """
        if (Line.find('Intensities [relative]') >= 0) and (if_normal_modes_are_loaded is False):
            for i in range(data['NAtoms']):
                LineX = StateF.readline()
                LineY = StateF.readline()
                LineZ = StateF.readline()

                # analyse the length of the line 23+12*j:
                nm_per_line = (len(LineX)-23)//12

                n_normal_modes += nm_per_line

                for j in range(nm_per_line):
                    new_entry = LineX[23+12*j:23+12*(j+1)] + LineY[23+12*j:23+12*(j+1)] + LineZ[23+12*j:23+12*(j+1)]
                    normal_coordinates[i].append(new_entry)

            n_normal_modes //= data['NAtoms']  # repeated "NAtoms"-times

        if (Line.find('Wavenumbers [cm-1]') >= 0) and (if_frequencies_are_loaded is False):
            data['Frequencies'] += Line.replace('Wavenumbers [cm-1]', '')
            no_lines_with_frequencies += 1

        if Line.find('Normal Modes of low/zero frequencies') >= 0:
            if_frequencies_are_loaded = True
            if_normal_modes_are_loaded = True

        Line = StateF.readline()

    # now create normal modes in q-chem format:
    printed_normal_modes = 0
    for_range = len(normal_coordinates[0])//3
    for j in range(for_range):
        for i in range(data['NAtoms']):
            new_entry = normal_coordinates[i][j*3] + "   "
            new_entry += normal_coordinates[i][j*3 + 1] + "   "
            new_entry += normal_coordinates[i][j*3 + 2] + '\n'
            data['NormalModes'] += new_entry
        printed_normal_modes += 3
        data['NormalModes'] += '\n'

    # add the reminder of 3
    reminder = len(normal_coordinates[0]) % 3
    if reminder > 0:
        for i in range(data['NAtoms']):
            for j in range(reminder):
                data['NormalModes'] += normal_coordinates[i][printed_normal_modes + j] + "   "
            data['NormalModes'] += '\n'
        data['NormalModes'] += '\n'

    if n_normal_modes == (3 * data['NAtoms'] - 5):
        data['ifLinear'] = True

    data['if_normal_modes_weighted'] = True
    data['geometry_units'] = "au"

    # END MOLPRO
    # =========================================================================


def parse_gamess(StateF, data: dict, run_type):
    """ Parser of a GAMESS output. (Note: linear molecules are not supported) """
    if run_type != "web":
        print("\nWarning! All geometries from GAMESS' outputs treated as non-linear.")

    data['ifLinear'] = False
    if_geometry_is_loaded = False
    if_frequencies_are_loaded = False
    if_normal_modes_are_loaded = False

    normal_coordinates = []
    n_normal_modes = 0
    no_lines_with_frequencies = 0

    Line = StateF.readline()
    while Line:
        # geometry
        if (Line.find('COORDINATES (BOHR)') >= 0) and (if_geometry_is_loaded is False):
            StateF.readline()
            Line = StateF.readline()
            while Line.find('INTERNUCLEAR DISTANCES (ANGS.)') == -1:
                data['NAtoms'] += 1
                data['Geometry'] += "     " + Line[0:5] + Line[19:]
                data['atoms_list'] += Line[0:5]
                Line = StateF.readline()
            if_geometry_is_loaded = True
            data['NAtoms'] -= 1
            # create an empty list of coordinates for every atom in form 
            # "X_nm1 Y_nm1 Z_nm1 X_nm2 Y_nm2 Z_nm2 X_nm3..."
            for i in range(data['NAtoms']):
                normal_coordinates.append([])

        if (Line.find(' IR INTENSITY:') >= 0) and (if_normal_modes_are_loaded is False):
            Line = StateF.readline()

            for i in range(data['NAtoms']):
                LineX = StateF.readline()
                LineY = StateF.readline()
                LineZ = StateF.readline()

                # analyse the length of the line 20+12*j:
                nm_per_line = (len(LineX) - 20)//12

                for j in range(nm_per_line):
                    new_entry = LineX[20+12*j:20+12*(j+1)]
                    new_entry += LineY[20+12*j:20+12*(j+1)]
                    new_entry += LineZ[20+12*j:20+12*(j+1)]
                    normal_coordinates[i].append(new_entry)

            n_normal_modes //= data['NAtoms']  # repeated "NAtoms"-times

        if (Line.find('   FREQUENCY:') >= 0) and (if_frequencies_are_loaded is False):
            data['Frequencies'] += Line.replace('   FREQUENCY:', '')
            no_lines_with_frequencies += 1

        if Line.find('REFERENCE ON SAYVETZ CONDITIONS') >= 0:
            if_frequencies_are_loaded = True
            if_normal_modes_are_loaded = True

        Line = StateF.readline()

    # now create normal modes in q-chem format:
    printed_normal_modes = 0
    for_range = len(normal_coordinates[0])//3
    for j in range(for_range):
        for i in range(data['NAtoms']):
            new_entry = normal_coordinates[i][j*3] + "   "
            new_entry += normal_coordinates[i][j*3+1] + "   "
            new_entry += normal_coordinates[i][j*3+2] + '\n'
            data['NormalModes'] += new_entry
        printed_normal_modes += 3
        data['NormalModes'] += '\n'

    # add the reminder of 3
    reminder = len(normal_coordinates[0]) % 3
    if reminder > 0:
        for i in range(data['NAtoms']):
            for j in range(reminder):
                data['NormalModes'] += normal_coordinates[i][printed_normal_modes+j] + "   "
            data['NormalModes'] += '\n'
        data['NormalModes'] += '\n'

    # remove first 6 normal modes (two lines of three normal modes)
    # i.e. rotation+translation (works only for non-linear molecules!):
    for i in range((data['NAtoms']+1)*2):
        data['NormalModes'] = data['NormalModes'][data['NormalModes'].find('\n')+1:]
    # remove first 6 frequencies:
    Frequencies_set = data['Frequencies'].split()
    Frequencies_set = Frequencies_set[6:]
    data['Frequencies'] = " ".join([f"{f:s}" for f in Frequencies_set])
    data['Frequencies'] = "       " + data['Frequencies'] + "\n"

    data['if_normal_modes_weighted'] = True
    data['geometry_units'] = "au"

    # END GAMESS
    # =========================================================================


def parse_orca(StateF, data: dict):
    """ Parser of an ORCA output. """
    import numpy as np

    data['if_normal_modes_weighted'] = True                 # this is what the ORCA output is saying
    data['geometry_units'] = "angstr"                       # the same with previous

    Lines = [line.rstrip() for line in StateF.readlines()]  # load file with newline symbols ('\n') stripped
    IndNormModes = Lines.index('$normal_modes')             # index of the line where normal modes start
    IndVibFreq = Lines.index('$vibrational_frequencies')    # index of the line where vibrational frequencies start
    IndXYZ = Lines.index('$atoms')                          # index of the XYZ coordinates

    NAt = int(Lines[IndXYZ + 1].split()[0])                 # number of atoms in the molecule (next line after $atoms)
    for a in Lines[(IndXYZ + 2):(IndXYZ + 2 + NAt)]:        # parse the XYZ block
        words = a.split()
        # Geometry is the XYZ geometry in the format <Atom Label>  <X> <Y> <Z>, atomic masses (2nd column) are ignored
        data['Geometry'] += f"{words[0]:6s}  "
        for word in words[2:5]:
            coordinate = 0.529177210903 * float(word)
            data['Geometry'] += f" {coordinate:12.6f}"
        data['Geometry'] += "\n"
        # atom list is the list of atomic labels
        data['atoms_list'] += "   " + words[0] + " "

    NInRow = len(Lines[IndNormModes + 2].split())
    NVib = 3 * NAt
    NormModes = np.zeros((NVib, NAt, 3), dtype=float)
    data['NAtoms'] = NAt

    BlockNum = 0
    while BlockNum * NInRow < 3 * NAt:
        NModes = np.array(Lines[IndNormModes + 2 + BlockNum * (NVib + 1)].split(), dtype=int)
        for i in range(0, NVib):
            words = Lines[IndNormModes + 2 + BlockNum * (NVib + 1) + 1 + i].split()
            tmp = np.array(words[1:], dtype=float)
            for imode, nmode in enumerate(NModes):
                NormModes[nmode][i // 3][i % 3] = tmp[imode]
        BlockNum += 1

    for nmodeblock in range(6, NVib, 3):
        for nat in range(0, NAt):
            for nmib in range(0, 3):
                data['NormalModes'] += "  "
                for mode in NormModes[nmodeblock + nmib][nat]:
                    data['NormalModes'] += f" {mode:7.3f}"
            data['NormalModes'] += "\n"
        data['NormalModes'] += "\n"

    count = 0
    for i in range(6, NVib):
        freq = float(Lines[IndVibFreq + 2 + i].split()[1])
        data['Frequencies'] += "    " + f"{freq:7.2f}"
        count += 1
        if count % 3 == 0 and count >= 3:
            data['Frequencies'] += "\n"

    # END ORCA
    # =========================================================================


def parse_orca_new(StateF, data: dict, run_type):
    """ Parser of an ORCA output. 
    On Sep 8th 2021 users reported that optput of Orca 4.2.0
    is not recognized by the script. This is a version of 
    'parse_orca' function edited to match the new output format.
    """

    if run_type != "web":
        print("\nWarning! All geometries from ORCA's outputs treated as non-linear (excpet for diatomics).")


    line = StateF.readline()
    while line.find('Program Version') <= 0:
        line = StateF.readline()

    # version detection, without a use so far
    version = line.split()[2]
    #print(f"Orca version {version} detected")

    # load file with newline symbols ('\n') stripped
    Lines = [line.rstrip() for line in StateF.readlines()]  

    all_number_of_atoms = [x for x in Lines if x.startswith('Number of atoms')]
    # take the number of atoms from the last calculation
    NAt = int(all_number_of_atoms[-1].split()[-1])
    # raise an error in case that the number of atoms changed
    for number in all_number_of_atoms:
        local_n_at = int(number.split()[-1])
        if local_n_at != NAt:
            err = "Number of atoms changed during the calculation"
            raise RuntimeError(err)
    data['NAtoms'] = NAt
    # TODO: Detect general linear molecule 
    if NAt == 2:
        data['ifLinear'] = True 

    # Parse geometry
    """
    ---------------------------------
    CARTESIAN COORDINATES (ANGSTROEM)
    ---------------------------------
      <atom>     <x>    <y>  <z> 
      ...
    """
    data['geometry_units'] = "angstr"
    # find the last index of the geometry 
    # (in case that the optimization precedes the frequencies)
    Lines.reverse()
    IndXYZ = Lines.index('CARTESIAN COORDINATES (ANGSTROEM)')
    IndXYZ = - IndXYZ - 1
    Lines.reverse()

    for line in Lines[(IndXYZ + 2):(IndXYZ + 2 + NAt)]:
        words = line.split()
        data['Geometry'] += f"{words[0]:6s}  "
        for word in words[1:4]:
            coordinate = float(word)
            data['Geometry'] += f" {coordinate:12.6f}"
        data['Geometry'] += "\n"
        # atom list is the list of atomic labels
        data['atoms_list'] += "   " + words[0] + " "

    # Parse frequencies in the ORCA format
    """ 
    -----------------------
    VIBRATIONAL FREQUENCIES
    -----------------------

    Scaling factor for frequencies =  1.000000000 (already applied!)

       0:         0.00 cm**-1
       1:         0.00 cm**-1
       2:         0.00 cm**-1
       3:         0.00 cm**-1
       4:         0.00 cm**-1
       5:       516.22 cm**-1
    """
    # TODO: What is the role of the scaling factor?

    # index of vibrational frequencies start
    IndVibFreq = Lines.index('VIBRATIONAL FREQUENCIES')
    NVib = 3 * NAt

    # TODO: Check if there is more to be done for linear molecules 
    # other than changing number of normal modes from 3N - 6 to 3N - 5. 
    range_start = 6
    if data['ifLinear']:
        range_start = 5

    count = 0
    for i in range(range_start, NVib):
        freq = float(Lines[IndVibFreq + 5 + i].split()[1])
        data['Frequencies'] += "    " + f"{freq:7.2f}"
        count += 1
        if count % 3 == 0 and count >= 3:
            data['Frequencies'] += "\n"

    # Parse normal modes. The example of h2o:
    """
    ------------
    NORMAL MODES
    ------------

    These modes are the Cartesian displacements weighted by the diagonal matrix
    M(i,i)=1/sqrt(m[i]) where m[i] is the mass of the displaced atom
    Thus, these vectors are normalized but *not* orthogonal

                     0          1          2          3          4          5
         0       0.000000   0.000000   0.000000   0.000000   0.000000   0.000000
         1       0.000000   0.000000   0.000000   0.000000   0.000000   0.000000
         ...
         8       0.000000   0.000000   0.000000   0.000000   0.000000   0.000000
                      6          7          8
         0       0.000000   0.000000   0.000000
         1      -0.000000  -0.000001  -0.070719
         ...
         8      -0.559003  -0.398458   0.427232
    """
    data['if_normal_modes_weighted'] = True

    # index of the line where normal modes start
    IndNormModes = Lines.index('NORMAL MODES')

    # NormalModes is a list of normal modes: [mode_1, mode_2, ...]
    # len(NormalModes) equals NVib which equals 3 * NAt (ORCA's convention)
    # each mode_n is a list of lenth NAt: [At_1, At_2, ..., At_{NAt}]
    # each At_n is a list of length 3: [x, y, z]
    # initialize the container
    NormalModes = [[[0.0 for i in range(3)] for j in range(NAt)] for k in range(NVib)]

    # max number of normal modes displayed in a row
    NInRow = len(Lines[IndNormModes + 7].split())
    BlockNum = 0
    # parse normal modes blocks
    # BlockNum * NInRow in number of modes already parsed
    while BlockNum * NInRow < 3 * NAt:
        labels_line = Lines[IndNormModes + 7 + BlockNum * (NVib + 1)]
        # len of mode_labels is less or equal to NInRow
        mode_labels = [int(x) for x in labels_line.split()]
        for i in range(0, NVib):
            tmp_coordinates = Lines[IndNormModes + 7 + BlockNum * (NVib + 1) + 1 + i]
            coordinates = [float(word) for word in tmp_coordinates.split()[1:]]
            for imode, mode_label in enumerate(mode_labels):
                atom_idx = i // 3
                xyz_idx = i % 3
                NormalModes[mode_label][atom_idx][xyz_idx] = coordinates[imode]
        BlockNum += 1

    # Copy normal modes to the data['NormalModes'] in a Q-Chem format
    """
     0.000  -0.000   0.070     0.000  -0.000   0.050     0.000  -0.071  -0.000
     0.000  -0.430  -0.559     0.000   0.583  -0.398     0.000   0.561  -0.427
     0.000   0.430  -0.559     0.000  -0.583  -0.398     0.000   0.561   0.427
     0.000   0.430  -0.559     0.000  -0.583  -0.398     0.000   0.561   0.427

     0.000  -0.000   0.070
     0.000  -0.430  -0.559
     0.000   0.430  -0.559
     0.000   0.430  -0.559
    """
    # each block contains at most 3 normal modes
    block = 0
    # There is 'NVib - range_start' normal modes to print
    while block * 3 < NVib - range_start:
        modes_left = NVib - range_start - block * 3
        no_of_modes_to_print = min(3, modes_left)
        for nat in range(0, NAt):
            for nmib in range(0, no_of_modes_to_print):
                data['NormalModes'] += "  "
                for mode in NormalModes[range_start + block * 3 + nmib][nat]:
                    data['NormalModes'] += f" {mode:7.3f}"
            data['NormalModes'] += "\n"
        data['NormalModes'] += "\n"
        block += 1

    # END ORCA NEW
    # =========================================================================

def parse_other(StateF, data: dict):
    """
    Parser of a Gaussian output.
    We can not guarantee it is fully supported, since we are not allowed to touch it.
    Use at your own risk!
    This script will not copy the geometry if the "nosymm" keyword is used in Gaussian.
    """
    ifAtomsLoaded = False
    if_geometry_is_loaded = False
    no_lines_with_frequencies = 0

    Line = StateF.readline()
    while Line:
        if (Line.find('Distance matrix') >= 0) and (ifAtomsLoaded is False):
            StateF.readline()
            while Line.find('Stoichiometry') == -1:
                data['atoms_list'] += Line[8:12]
                Line = StateF.readline()
            atoms_set = data['atoms_list'].split()
            ifAtomsLoaded = True

        if (Line.find('Standard orientation') >= 0) and (if_geometry_is_loaded is False):
            for _ in range(4):
                StateF.readline()
            Line = StateF.readline()
            while Line.find('----') == -1:
                data['Geometry'] += "      " + atoms_set[data['NAtoms']] + Line[32:]
                Line = StateF.readline()
                data['NAtoms'] += 1
            if_geometry_is_loaded = True

        if Line.find('Atom AN') >= 0 or Line.find('Atom  AN') >= 0 :
            for _ in range(data['NAtoms']):
                Line = StateF.readline()
                data['NormalModes'] += Line[10:]
            data['NormalModes'] += '\n'

        # TODO: I do not understand the comment below. It comes from the previous version of the script. Pawel
        # remove end of the line symbols!!!
        if Line.find('Frequencies --') >= 0:
            data['Frequencies'] += Line.replace('Frequencies --', '')
            no_lines_with_frequencies += 1

        Line = StateF.readline()

    if no_lines_with_frequencies == data['NAtoms']-1:
        data['ifLinear'] = True

    data['if_normal_modes_weighted'] = True
    data['geometry_units'] = "angstr"

    # END OTHER
    # =========================================================================


def read_state(FileName, data: dict, run_type: str):
    """Reads one state from an ab-initio packackage output file."""

    # check which ab initio package created the input file
    file_type_detected = False
    StateF = open(FileName, 'r')
    Line = StateF.readline()
    while Line:
        if Line.find('Welcome to Q-Chem') >= 0:
            file_type_detected = True
            parse_qchem(StateF, data)
            break

        if Line.find('* ACES2:') >= 0:
            file_type_detected = True
            parse_aces_old(StateF, data)
            break

        if Line.find('* ACES :') >= 0:
            file_type_detected = True
            parse_aces_new(StateF, data)
            break

        if Line.find('PROGRAM SYSTEM MOLPRO') >= 0:
            file_type_detected = True
            # Skip to the line that starts with 'Version'
            while not Line.lstrip().startswith("Version"):
                Line = StateF.readline()

            version = Line.split()[1]
            version_year = int(version.split(".")[0])
            # TODO: Molpro version 2015.1 produces new outptu,
            # but it might be not the oldest version which does so.
            if version_year < 2015:
                parse_molpro_old(StateF, data)
            else:
                parse_molpro_new(StateF, data)
            break

        if Line.find('GAMESS VERSION = ') >= 0:
            file_type_detected = True
            parse_gamess(StateF, data, run_type)
            break

        if Line.find('$orca_hessian_file') >= 0:
            file_type_detected = True
            parse_orca(StateF, data)
            break

        if Line.find('* O   R   C   A *') >= 0:
            file_type_detected = True
            parse_orca_new(StateF, data, run_type)
            break

        if Line.find('RESTRICTED RIGHTS') >= 0:
            file_type_detected = True
            parse_other(StateF, data)
            break

        Line = StateF.readline()

    if file_type_detected is False:
        unknown_format = f'Error: File "{FileName}" has an unknown format.'
        unknown_format += ' Q-Chem, Molpro, ACES II, GAMESS, ORCA, or Gaussian frequency jobs are supported.'
        raise ValueError(unknown_format)

    return data


def write_state_xml_file(xmlF, data: dict, which_state: str, run_type: str):
    """ Write the state to the xml file. """
    # To improve readability, each item of the data dictionary is unpacked to a variable.

    xmlF.write('  <geometry\n')
    no_atoms = data["NAtoms"]
    xmlF.write(f'    number_of_atoms = "{str(no_atoms)}"\n')
    # linear?
    is_linear = data['ifLinear']
    if is_linear:
        xmlF.write('    linear = "true"\n')
    else:
        xmlF.write('    linear = "false"\n')

    geometry_units = data["geometry_units"]
    xmlF.write(f'    units   = "{geometry_units}"\n')

    xmlF.write('    text   = "\n')
    geometry = data['Geometry']
    xmlF.write(geometry)
    xmlF.write('             ">\n')
    xmlF.write('  </geometry>\n\n')

    atoms_order = " ".join([f"{str(nm)}" for nm in range(no_atoms)])

    xmlF.write('  <OPT_manual_atoms_reordering\n')
    xmlF.write(f'     new_order="{atoms_order}">\n')
    xmlF.write('  </OPT_manual_atoms_reordering>\n\n')

    xmlF.write('  <normal_modes\n')
    if_normal_modes_weighted = data["if_normal_modes_weighted"]
    xmlF.write(f'    if_mass_weighted="{if_normal_modes_weighted}"\n')
    xmlF.write('    text = "\n')
    normal_modes = data['NormalModes']
    xmlF.write(normal_modes)
    xmlF.write('           "\n')
    xmlF.write('   atoms = "')
    atoms_list = data['atoms_list']
    xmlF.write(atoms_list)
    xmlF.write('           ">\n')
    xmlF.write('  </normal_modes>\n\n')

    if is_linear:
        normal_modes = " ".join([f"{str(nm)}" for nm in range(3*no_atoms - 5)])
    else:
        normal_modes = " ".join([f"{str(nm)}" for nm in range(3*no_atoms - 6)])

    if which_state == "target":
        if run_type != "web":
            xmlF.write('  <OPT_manual_normal_modes_reordering\n')
            xmlF.write(f'     new_order="{normal_modes}">\n')
            xmlF.write('  </OPT_manual_normal_modes_reordering>\n\n')
        else:  # web version:
            xmlF.write('  <manual_normal_modes_reordering\n')
            xmlF.write(f'     new_order="{normal_modes}">\n')
            xmlF.write('  </manual_normal_modes_reordering>\n\n')

    xmlF.write('  <frequencies\n')
    xmlF.write('    text = "\n')
    frequencies = data['Frequencies']
    xmlF.write(frequencies)
    xmlF.write('             ">\n')
    xmlF.write('  </frequencies>\n\n')


def read_write_state(file_name, run_type: str, which_state: str, xmlF):
    """ Controls reading input and writing output. """

    # data necessary for xml output
    data = {'NAtoms': 0,
            'ifLinear': False,
            'Geometry': '',
            'atoms_list': '',
            'NormalModes': '',
            'Frequencies': '',
            'if_normal_modes_weighted': None,
            'geometry_units': None}
    read_state(file_name, data, run_type)
    write_state_xml_file(xmlF, data, which_state, run_type)


def main(xml_filename, ai_filenames, run_type):
    if len(ai_filenames) == 0:
        if run_type != "web":
            print(WRONG_INPUT)
            sys.exit(2)
        else:
            return "Error. make_xml.py: no ab-initio file names found"

    xmlF = open(xml_filename, 'w')

    # Write default job parameters
    xmlF.write(DEFAULT_JOB_PARAMETERS)

    # web version
    if run_type == "web":
        xmlF.write('<if_web_version flag="true">\n</if_web_version>\n\n')

    xmlF.write('<initial_state>\n')
    xmlF.write(f'  <!-- THIS INITIAL STATE IS FROM "{ai_filenames[0]}" FILE -->\n\n')

    try:
        read_write_state(ai_filenames[0], run_type, "initial", xmlF)
    except (ValueError, IOError) as e:
        xmlF.close()
        if run_type == "web":
            return str(e)
        else:
            print(e)
            sys.exit(2)

    xmlF.write('</initial_state>\n\n')
    xmlF.write("""<!--
  ______________________________________________________________________

 -->\n\n""")

    state_n = 0
    for targetStateFileName in ai_filenames[1:]:
        state_n += 1
        xmlF.write('<target_state>\n\n')
        xmlF.write(f'  <excitation_energy units="eV"> {str(state_n)} </excitation_energy>\n\n')
        xmlF.write(f'  <!-- THIS TARGET STATE IS FROM "{targetStateFileName}" FILE -->\n')

        try:
            read_write_state(targetStateFileName, run_type, "target", xmlF)
        except (ValueError, IOError) as e:
            xmlF.close()
            if run_type == "web":
                return str(e)
            else:
                print(e)
                sys.exit(2)

        xmlF.write('</target_state>\n\n')
        xmlF.write("""<!--
  ______________________________________________________________________

 -->\n\n""")
    xmlF.write('</input>\n')
    xmlF.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(WRONG_INPUT)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2:], "command_line")

