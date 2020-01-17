import os
from argparse import ArgumentParser
from distutils.dir_util import copy_tree, remove_tree
from distutils.file_util import copy_file


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

        if not target_path.endswith(self.compiled_folder_name):
            target_path += "%s%s" % (os.sep, self.compiled_folder_name)

        if isinstance(source_paths, str):
            source_paths = source_paths.split(" ")

        tmp_path = "%s%s%s%s" % (target_path, os.sep, "tmp", os.sep)
        os.makedirs(tmp_path, exist_ok=True)

        for s in source_paths:
            self.copy_mods(s, tmp_path)

        if len(os.listdir(tmp_path)) == 0:
            remove_tree(tmp_path)
            raise FileNotFoundError("No *.mod files copied from source paths: %s. Check if source paths contains mod files" % source_paths)

        os.chdir(tmp_path)
        r = os.popen('nrnivmodl')
        output = r.read()
        print(output)

        compiled_path = "%s%s%s" % (tmp_path, os.sep, self.compiled_folder_name)
        copy_tree(src=compiled_path, dst=target_path, update=1)
        os.chdir(working_dir)

        remove_tree(tmp_path)

    def copy_mods(self, source_path, tmp_path):
        for filename in os.listdir(source_path):
            filepath = "%s%s%s" % (source_path, os.sep, filename)

            if filename == self.compiled_folder_name or os.path.isdir(filepath):
                continue
            elif filename.endswith(".mod"):
                copy_file(src=filepath, dst=tmp_path, update=1)


if __name__ == '__main__':

    desc = "Compile all MOD files from the source folder to a single" \
           "folder in the target folder. By default works only with Linux NEURON compilation, " \
           "but if you change compiled_folder_name and mod_compile_command - to what is appropriate for your OS," \
           " it will work as well."
    parser = ArgumentParser(description=desc)

    parser.make_argument("-s", "--sources", help="Paths to the source folder.", required=True, nargs='+')
    parser.make_argument("-t", "--target", help="Path to the target folder.", required=True)
    parser.make_argument("-c", "--compiled_folder_name", help="Name of the folder containing MOD files in your OS."
                                                             "By default it is 'x86_64' for 64 architecture on Linux.",
                        default="x86_64")
    parser.make_argument("-m", "--mod_compile_command", help="MOD compile command of NEURON. By default it is 'nrnivmodl "
                                                            "which is Linux command'. You can give different command specific for your OS",
                        default='nrnivmodl')
    args = parser.parse_args()

    comp = CompileMOD(compiled_folder_name=args.compiled_folder_name, mod_compile_command=args.mod_compile_command)
    comp.compile(source_paths=args.sources, target_path=args.target)
