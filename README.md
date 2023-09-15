# sdat2img

This Python script is used to convert Android system transfer list files to system image files. It’s particularly useful for Android ROM developers.

# Description

The script reads a transfer list file and a new dat file, and writes the output to an image file. The transfer list file contains commands that describe how to transform the old system image into the new one. The new dat file contains the data blocks for the new system image. The script supports two types of commands: ‘new’ and ‘erase’. The ‘new’ command copies blocks from the new dat file to the output image file. The ‘erase’ command is currently ignored.

# Usage

You can run this script from the command line with the following arguments:

    transfer_list: Path to the transfer list file.
    new_dat: Path to the system new dat file.
    output: Path to the output image (default is output.img).
    -v or --verbose: Increase output verbosity (optional).
    Here’s an example of how to run the script:

    python sdat2img.py transfer_list new_dat output.img --verbose

This will create an image file named output.img based on the given transfer list and new dat files, and print detailed information about the process.
