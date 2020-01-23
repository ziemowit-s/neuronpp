import os
import neuron
from neuron import h
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


def stdp_protocol(protocol: str, synapse, section, start, isi, iti, train_number=1):
    """
    :param protocol:
        string eg. 3xEPSP[s=50,int=10] 3xAP[s=50,int=10,dur=3,amp=1.6]
        s - start in ms
        int - interval between in ms
        dur - duration of AP in ms
        amp - amplitude in nA
    :param synapse:
    :param section:
    :param start:
        start time of the first stimuli in ms
    :param isi:
        Inter Stimulus Interval, eg. 3xEPSP,2xAP -isi- 3xEPSP,2xAP
    :param iti:
        Inter Train Interval eg. 3xEPSP,2xAP -isi- 3xEPSP,2xAP -iti- 3xEPSP,2xAP-isi-3xEPSP,2xAP
    :param train_number:
        number of trains. Default is 1
    """
    protocol = protocol.lower()
    protocols = protocol.split(" ")

    netstim = NetStimCell(name="stim")
    iclamp = IClamp(section.hoc(0.5))

    event_time = start
    for train_no in range(train_number):
        for i, p in enumerate(protocols):
            p, params = p.split("[")

            num, ptype = p.split("x")
            num = int(num)

            interval = 0
            dur = 0
            amp = 0

            for par in params.replace("]", "").split(","):
                name, val = par.split('=')
                if name == 'int':
                    interval = int(val)
                elif name == 'dur':
                    dur = int(val)
                elif name == 'amp':
                    amp = float(val)

            if ptype == 'epsp':
                netstim.make_netstim(event_time, number=num, interval=interval)
                #synapse.netconn.hoc.
                event_time += interval * num
            elif ptype == 'ap':
                for _ in range(num):
                    iclamp.stim(delay=event_time, dur=dur, amp=amp)
                    event_time += interval
            else:
                raise TypeError("Only allowed types are EPSP or AP.")

            event_time += isi

        event_time += iti

