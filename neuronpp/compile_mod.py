import os
from argparse import ArgumentParser
from distutils.dir_util import copy_tree, remove_tree


class CompileMOD:
    def __init__(self, compiled_folder_name="x86_64", mod_compile_command="nrnivmodl"):
        """
        Compile all MOD files from the source folder (recursively if source folder contains folders inside) to a single folder
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

    def compile(self, source_path, target_path):
        """
        Compile recursively from source path to the target path
        :param source_path:
            Path to the source folder.
        :param target_path:
            Path to the target folder.
        """
        if not target_path.endswith(self.compiled_folder_name):
            target_path += "%s%s" % (os.sep, self.compiled_folder_name)
        self._compile_recursively(source_path, target_path)

    def _compile_recursively(self, source_path, target_path):
        os.chdir(source_path)

        for filename in os.listdir(source_path):
            if filename == self.compiled_folder_name:
                continue

            filepath = "%s%s%s" % (source_path, os.sep, filename)

            if os.path.isdir(filepath):
                self._compile_recursively(filepath, target_path)

            elif filename.endswith(".mod"):
                r = os.popen('nrnivmodl')
                print(r.read())
                compiled_path = "%s%s%s" % (source_path, os.sep, self.compiled_folder_name)
                copy_tree(src=compiled_path, dst=target_path, update=1)
                remove_tree(compiled_path)
                break
        os.chdir("..")


if __name__ == '__main__':

    desc = "Compile all MOD files from the source folder (recursively if source folder contains folders inside) to a single" \
           "folder in the target folder. By default works only with Linux NEURON compilation, " \
           "but if you change compiled_folder_name and mod_compile_command - to what is appropriate for your OS," \
           " it will work as well."
    parser = ArgumentParser(description=desc)

    parser.add_argument("-s", "--source", help="Path to the source folder.", required=True)
    parser.add_argument("-t", "--target", help="Path to the target folder.", required=True)
    parser.add_argument("-c", "--compiled_folder_name", help="Name of the folder containing MOD files in your OS."
                                                             "By default it is 'x86_64' for 64 architecture on Linux.",
                        default="x86_64")
    parser.add_argument("-m", "--mod_compile_command", help="MOD compile command of NEURON. By default it is 'nrnivmodl "
                                                            "which is Linux command'. You can give different command specific for your OS",
                        default='nrnivmodl')
    args = parser.parse_args()

    comp = CompileMOD(compiled_folder_name=args.compiled_folder_name, mod_compile_command=args.mod_compile_command)
    comp.compile(source_path=args.source, target_path=args.target)
