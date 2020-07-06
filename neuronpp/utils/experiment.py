from typing import Optional

from neuronpp.utils.iclamp import IClamp
from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.hocwrappers.synapses.synapse import Synapse


class Experiment:
    def __init__(self):
        """
        Experimental object which allows to create STDP-like protocols of stimulations.
        """
        self.netstims = []
        self.iclamps = []

    def make_protocol(self, protocol: str, iti=1,
                      epsp_synapse: Optional[Synapse] = None,
                      i_clamp_segment: Optional[Seg] = None, train_number=1):
        """
        Create an experimental protocol of EPSPs and APs:
          * It consist of one or more blocks of Trains
          * Each Train consists of one or more protocols
          * During each Train all protocols defined will be computed
          * Protocol can be EPSP or AP
          * Interval between Trains define: iti value (Inter-Train-Interval)
          * After one block of Train:
             * we choose the end-time of the longest protocol and call it max_time
             * we add iti value to the max_time
             * we update start time of each protocol as: max_time + init value of each protocol

        :param iti:
            Inter Train Interval eg.
                [3xEPSP,2xAP -isi- 3xEPSP,2xAP] -ITI- [3xEPSP,2xAP-isi-3xEPSP,2xAP]
        Each element of the experiment (EPSP or AP) is separated by isi (in ms).

        :param protocol:
            string eg. 3xEPSP[int=10,w=2.5,thr=5,del=2] 3xAP[int=10,dur=3,amp=1.6]

            Params for EPSP only:
            init - start time of the first stimuli in ms, it is absolute time,
            so bear in mind warmup time.
            int - interval between in ms
            w - weight for netconn (default is 1.0) -> used only when copy_netconn_params=False
            del - delay for netconn (default is 1.0) -> used only when copy_netconn_params=False
            thr - threshold for netconn (default is 10) -> used only when copy_netconn_params=False

            Params for AP only:
            init - start time of the first stimuli in ms, it is absolute time,
            so bear in mind warmup time.
            int - interval between in ms
            dur - duration of AP in ms
            amp - amplitude in nA

        :param epsp_synapse:
            synapse to stimulate. Default is None if you don't want to stimulate synapse
        :param i_clamp_segment:
            section to input IClamp. Default is None if you don't want to stimulate any section by
            electrode (eg. making AP)
            It is assumed that IClamp stimulate i_clamp_section(0.5) segment.
        :param iti:
            Inter Train Interval eg.
                [3xEPSP,2xAP] -ITI- [3xEPSP,2xAP]
        :param train_number:
            number of trains. Default is 1
        """
        protocol = protocol.lower()
        protocols = protocol.split(" ")

        for p in protocols:
            if "epsp" in p and epsp_synapse is None or not isinstance(epsp_synapse, Synapse):
                raise ValueError("If you defined EPSP protocol - you need to specify synapse to "
                                 "stimulate as epsp_synapse")
            if "ap" in p and i_clamp_segment is None or not isinstance(i_clamp_segment, Seg):
                raise ValueError("If you defined AP protocol - you need to specify segment to "
                                 "where the AP will be injected.")

        global_time = 0
        for train_no in range(train_number):

            new_global_time = global_time
            for p in protocols:
                new_time = self._prepare_protocol(p, global_time, epsp_synapse, i_clamp_segment)
                if new_time > new_global_time:
                    new_global_time = new_time

            global_time = new_global_time
            global_time += iti

    def _prepare_protocol(self, protocol, global_time, epsp_synapse, i_clamp_segment):
        current_time = global_time
        protocol, params = protocol.split("[")

        num, ptype = protocol.split("x")
        num = int(num)

        dur = 0
        amp = 0
        weight = 1.0
        threshold = 10
        delay = 1.0
        interval = 0
        init = 0

        for par in params.replace("]", "").split(","):
            name, val = par.split('=')
            name = name.strip()
            val = val.strip()
            if name == 'init':
                init = float(val)
            if name == 'int':
                interval = int(val)
            elif name == 'w':
                weight = float(val)
            elif name == 'thr':
                threshold = float(val)
            elif name == 'dur':
                dur = int(val)
            elif name == 'del':
                delay = int(val)
            elif name == 'amp':
                amp = float(val)

        current_time += init
        if ptype == 'epsp':
            netstim = NetStimCell(name="stim")
            self.netstims.append(netstim)

            stim = netstim.make_netstim(start=current_time, number=num, interval=interval)
            epsp_synapse.add_netcon(source=stim, weight=weight, threshold=threshold, delay=delay)
            current_time += interval * num

        elif ptype == 'ap':
            iclamp = IClamp(i_clamp_segment)
            self.iclamps.append(iclamp)
            for _ in range(num):
                iclamp.stim(delay=current_time, dur=dur, amp=amp)
                current_time += interval
        else:
            raise TypeError("Only allowed types are EPSP or AP.")

        return current_time
