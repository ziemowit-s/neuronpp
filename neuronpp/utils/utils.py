import os
import neuron
from neuron import h

from neuronpp.core.hocwrappers.composed.complex_synapse import ComplexSynapse
from neuronpp.core.hocwrappers.netconn import NetConn

from neuronpp.core.cells.netstim_cell import NetStimCell

from neuronpp.core.hocwrappers.netstim import NetStim

from neuronpp.electrodes.iclamp import IClamp

from neuronpp.utils.compile_mod import CompileMOD

mods_loaded = []


def make_shape_plot(variable=None, min_val=-70, max_val=40):
    ps = h.PlotShape(True)
    if variable:
        ps.variable(variable)
        ps.scale(min_val, max_val)
    ps.show(0)
    h.fast_flush_list.append(ps)
    ps.exec_menu('Shape Plot')
    return ps


def compile_and_load_mods(*mod_folders):
    mod_folders = [m for m in mod_folders if m not in mods_loaded]

    if len(mod_folders) > 0:
        comp = CompileMOD()
        comp.compile(source_paths=mod_folders, target_path=os.getcwd())

        neuron.load_mechanisms("%s%scompiled" % (os.getcwd(), os.sep))
        mods_loaded.extend(mod_folders)
