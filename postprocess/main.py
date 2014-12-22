
#'''
# Main method for the package to post-process the 3D-Images created from 2D-Electron crystallography
#'''
#
#__author__='Nikhil Biyani, C-CINA, University of Basel'
#__version__='04/12/2014'
#__email__="nikhilbiyani@gmail.com"


import sys

from emvol import EMVol
from applyconstraints import Constraints

import utils.InputUtils as inp
import utils.SystemUtils as system
import utils.OutputUtils as out

if __name__ =='__main__':
    
    print '\nProgram Initiated...\n'
    
    # Get the inputs
    input_parser = inp.InputParser(args = sys.argv[1:])
    input_parser.print_inputs()
    inputs = input_parser.arguments

    # Check Input File
    dir_in = system.get_dir_path(inputs.hkz_file)
    filename_in = system.get_file_name(inputs.hkz_file)
    
    # Create unique output directory
    dir_out = dir_in + "/" + system.get_current_time()
    print ' Creating output directory:'
    print ' {}\n' .format(dir_out)
    system.create_dir(dir_out)
    
    # Set the output for OutputUtils
    outUtil = out.OutputUtils(output_path=dir_out)
    
    # Convert input hkz file to mrc
    print "Converting image from:\n {}/{}" .format(dir_in,filename_in)
    vol_input_raw = EMVol.from_hkz_file(inputs.hkz_file, inputs.nx, inputs.ny, inputs.nz, inputs.apix, inputs.max_resolution)
    outUtil.file_name = "input_volume_raw.mrc"
    print "Done.. writing at {}\n" .format(outUtil.get_write_name())
    vol_input_raw.write_image(outUtil.get_write_name())
    
    # Symmetrize input volume
    vol_input = vol_input_raw.symmetrize(inputs.symmetry, inputs.amp_epsilon)
    outUtil.file_name = "input_volume_symmetrized.mrc"
    print "Done.. writing at {}\n" .format(outUtil.get_write_name())
    vol_input.write_image(outUtil.get_write_name())
    
    print "Input volume information:"
    vol_input.print_info(inputs.amp_epsilon)
        
    # Prepare for iterations
    constrts = Constraints(inputs, outUtil)
    vol_processed = constrts.apply_constraints(vol_input)
    
    # Write final output
    outUtil.output_path = dir_out
    outUtil.file_name = "final_processed.mrc"
    print "Done.. writing at {}\n" .format(outUtil.get_write_name())
    vol_processed.write_image(outUtil.get_write_name())
  
    
    