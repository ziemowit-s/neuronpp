import os
import shutil
from argparse import ArgumentParser
from distutils.file_util import copy_file
from subprocess import PIPE, Popen, STDOUT

import neuron


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
                copy_file(src=filepath, dst=tmp_path, update=1)
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


def compile_and_load_mods(mod_folders):
    if isinstance(mod_folders, str):
        mod_folders = mod_folders.split(" ")

    mod_folders = [m for m in mod_folders if m not in mods_loaded]

    if len(mod_folders) > 0:
        # Compile
        comp = CompileMOD()
        targ_path = os.path.join(os.getcwd(), "compiled", "mods%s" % len(mods_loaded))
        comp.compile(source_paths=mod_folders, target_path=targ_path)
        # Load
        neuron.load_mechanisms(targ_path)
        mods_loaded.extend(mod_folders)
