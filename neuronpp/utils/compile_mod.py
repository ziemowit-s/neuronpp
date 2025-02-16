import hashlib
import os
import shutil
import time
from argparse import ArgumentParser
from distutils.file_util import copy_file
from subprocess import PIPE, Popen, STDOUT

import neuron
import numpy as np


class CompileMOD:
    def __init__(self, compiled_folder_name="x86_64", mod_compile_command="nrnivmodl"):
        """
        Compile all MOD files from the source folder to a single folder
        in the target folder.

        By default works only with Linux NEURON compilation

        However if you change compiled_folder_name and mod_compile_command to what is appropriate for your OS it will work as well.

        :param compiled_folder_name:
            Name of the folder containing MOD files in your OS. By default it is 'x86_64' for 64 architecture on Linux.
        :param mod_compile_command:
            MOD compile command of NEURON. By default it is 'nrnivmodl' which is Linux command'.
            You can give different command specific for your OS.
        """
        self.compiled_folder_name = compiled_folder_name
        self.mod_compile_command = mod_compile_command

    def compile(self, source_paths, target_path):
        """
        Compile from source path to the target path
        :param source_paths:
            Path to the source folder.
        :param target_path:
            Path to the target folder.
        """
        working_dir = os.getcwd()
        target_path = target_path.replace(self.compiled_folder_name, "")
        shutil.rmtree(target_path, ignore_errors=True, onerror=None)
        os.makedirs(target_path)

        if isinstance(source_paths, str):
            source_paths = source_paths.split(" ")

        for s in source_paths:
            self.copy_mods(s, target_path)

        os.chdir(target_path)
        p = Popen('nrnivmodl', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
        output = p.stdout.read().decode('utf-8')

        print('nrniv output:', output)
        print('mod path:', target_path)
        print('mod path list dir:', os.listdir(target_path))

        if "failed" in output.lower() or "error" in output.lower():
            raise RuntimeError("MOD compilation error: %s" % output)
        else:
            print(output)

        os.chdir(working_dir)

    def copy_mods(self, source_path, tmp_path):
        mods_found = 0
        for filename in os.listdir(source_path):
            filepath = "%s%s%s" % (source_path, os.sep, filename)

            if filename == self.compiled_folder_name or os.path.isdir(filepath):
                continue
            elif filename.endswith(".mod"):
                copy_file(src=filepath, dst=tmp_path, update=1, preserve_times=False)
                mods_found += 1
        if mods_found == 0:
            raise RuntimeError("No MOD files found on path: %s" % source_path)


if __name__ == '__main__':
    desc = "Compile all MOD files from the source folder to a single" \
           "folder in the target folder. By default works only with Linux NEURON compilation, " \
           "but if you change compiled_folder_name and mod_compile_command - to what is appropriate for your OS," \
           " it will work as well."
    parser = ArgumentParser(description=desc)

    parser.add_argument("-s", "--sources", help="Paths to the source folder.", required=True,
                        nargs='+')
    parser.add_argument("-t", "--target", help="Path to the target folder.", required=True)
    parser.add_argument("-c", "--compiled_folder_name",
                        help="Name of the folder containing MOD files in your OS."
                             "By default it is 'x86_64' for 64 architecture on Linux.",
                        default="x86_64")
    parser.add_argument("-m", "--mod_compile_command",
                        help="MOD compile command of NEURON. By default it is 'nrnivmodl "
                             "which is Linux command'. You can give different command specific for your OS",
                        default='nrnivmodl')
    args = parser.parse_args()

    comp = CompileMOD(compiled_folder_name=args.compiled_folder_name,
                      mod_compile_command=args.mod_compile_command)
    comp.compile(source_paths=args.sources, target_path=args.target)

mods_loaded = []


def get_mod_compiled_target_path(compile_mods_with_random_subfolder=True):
    if compile_mods_with_random_subfolder is True:
        # Generate a short random string using the MD5 hash of the current timestamp
        random_str = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]  # First 8 characters of MD5 hash
        return os.path.join(os.getcwd(), "compiled", random_str, "mods%s" % len(mods_loaded))
    else:
        return os.path.join(os.getcwd(), "compiled", "mods%s" % len(mods_loaded))


def compile_mods(mod_folders, override=True, compile_mods_with_random_subfolder=True):
    """
    Compile all MOD files from the source folder(s) and load them into NEURON.

    By default, the function compiles and loads mechanisms for Linux. However, if you modify the
    compilation and loading commands, it can be adapted for other operating systems.

    :param mod_folders:
       Path(s) to the folders containing MOD files. Can be a single string (space-separated) or
       a list of strings. The function compiles and loads these files into NEURON.
    :param override:
       If True, the function will override existing compiled MOD files in the target folder.
       If False and the target path exists, the function will skip the compilation step.
       Default is True.
    :param compile_mods_with_random_subfolder:
        if True it will create a random subfolder in the target folder as compiled/random_string/modsNUM.
        if False it will create folder compiled/modsNUM
    """

    if isinstance(mod_folders, str):
        mod_folders = mod_folders.split(" ")

    mod_folders = [m for m in mod_folders if m not in mods_loaded]

    if len(mod_folders) == 0:
        return

    targ_path = get_mod_compiled_target_path(compile_mods_with_random_subfolder=compile_mods_with_random_subfolder)

    do_compile = True
    if os.path.exists(targ_path):
        if override:
            print(f"Overriding existing target path: {targ_path}")
        else:
            print(f"Target path exists and override is False. Skipping compilation: {targ_path}")
            do_compile = False

    if do_compile:
        comp = CompileMOD()
        comp.compile(source_paths=mod_folders, target_path=targ_path)

    return targ_path


def load_mods(path: str, try_num=10, wait_in_sec=2):
    """
    :param path:
       Single string containing compiled folder (in most cases named x86_64/ on 64-bit architecture).
    :param wait_in_sec:
       The number of seconds to wait between retries if loading the mechanisms fails.
       Default is 2 seconds.
    :param try_num:
       The number of retry attempts if loading the mechanisms fails. After `try_num` failed
       attempts, the function will raise an error. Default is 10 attempts.
    """
    # Load compiled MODS with retries
    for attempt in range(try_num):
        try:
            neuron.load_mechanisms(path)
            mods_loaded.append(path)
            print(f"Successfully loaded mechanisms from {path}")
            break

        except Exception as e:
            print(f"Attempt to load MODs ({attempt + 1}/{try_num}) failed: {e}")

            if attempt < try_num - 1:
                # wait_tmp hack - to prevent race condition where all processes will wait the same anout of
                # time and possibly block each other
                wait_tmp = wait_in_sec + np.random.rand()

                print(f"Retrying in {wait_tmp} seconds...")
                time.sleep(wait_tmp)
            else:
                print(f"Failed to load mechanisms after {try_num} attempts.")
                raise e

