#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@ File Name    :   sdat2img.py
"""

import argparse
import os
import time

# Define the block size
BLOCK_SIZE = 4096


def range_set(src):
    """
    Convert a comma-separated string into a list of tuples representing ranges.

    Args:
        src (str): A comma-separated string where the first number is the count of ranges,
                   followed by pairs of numbers representing each range.

    Returns:
        list: A list of tuples where each tuple represents a range.
    """
    num_set = [int(item) for item in src.split(",")]
    if len(num_set) != num_set[0] + 1:
        raise ValueError(f"Error on parsing following data to range_set:\n{src}")
    return [(num_set[i], num_set[i + 1]) for i in range(1, len(num_set), 2)]


def transfer_list_file_to_commands(trans_list):
    """
    Parse the transfer list file into commands.

    Args:
        trans_list (file): The transfer list file.

    Returns:
        list: A list of commands where each command is a list containing the command name and its arguments.
    """

    version = int(trans_list.readline())
    trans_list.readline()  # new blocks
    if version >= 2:
        trans_list.readline()  # simultaneously stashed entries
        trans_list.readline()  # max num blocks simultaneously stashed

    commands = []
    for line in trans_list:
        cmd, *args = line.split()
        if cmd in ["erase", "new", "zero"]:
            commands.append([cmd, range_set(args[0])])
        elif not cmd[0].isdigit():
            raise ValueError(f'Command "{cmd}" is not valid.')
    return commands


def sdat2img(transfer_list_filename, new_dat_filename, output_filename, verbose):
    """
    Convert sparse Android data image (.dat) to ext4 image (.img).

    Args:
        transfer_list_filename (str): The path to the transfer list file.
        new_dat_filename (str): The path to the .dat file.
        output_filename (str): The path to the output .img file.
        verbose (bool): Whether to print detailed information during conversion.

    Returns:
        bool: True if the conversion is successful, False otherwise.
    """
    try:
        start_time = time.time()

        with open(transfer_list_filename, "r", encoding="utf-8") as transfer_list_file:
            commands = transfer_list_file_to_commands(transfer_list_file)

        if os.path.exists(output_filename):
            if verbose:
                print(f"The output file {output_filename} already exists")
            if verbose:
                print(f"Delete {output_filename}")
            os.remove(output_filename)

        with open(output_filename, "wb") as output_img, open(
            new_dat_filename, "rb"
        ) as new_dat_file:
            max_file_size = (
                max(pair[1] for command in commands for pair in command[1]) * BLOCK_SIZE
            )  # type: ignore

            for command in commands:
                if command[0] == "new":
                    for begin, end in command[1]:
                        block_count = end - begin
                        if verbose:
                            print(f"Copying {block_count} blocks to position {begin}...")
                        output_img.seek(begin * BLOCK_SIZE)
                        output_img.write(new_dat_file.read(BLOCK_SIZE * block_count))

                else:
                    if verbose:
                        print(f"Skipping command {command[0]}")

            if output_img.tell() < max_file_size:
                output_img.truncate(max_file_size)

        end_time = time.time()
        execution_time = end_time - start_time

        print(f"Execution time: {execution_time} seconds")

        return True

    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        return False


if __name__ == "__main__":
    # Create an argument parser
    parser = argparse.ArgumentParser()

    # Define command-line arguments
    parser.add_argument("transfer_list", help="Path to the transfer list file")
    parser.add_argument("new_dat", help="Path to the system new dat file")
    parser.add_argument("output", default="output.img", help="Path to the output image")

    # Add verbose argument to suppress print statements
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")

    args = parser.parse_args()

    sdat2img(args.transfer_list, args.new_dat, args.output, args.verbose)
