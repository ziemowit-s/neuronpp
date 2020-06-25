from typing import Optional

from neuronpp.utils.iclamp import IClamp
from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.hocwrappers.synapse import Synapse
from neuronpp.core.cells.netstim_cell import NetStimCell


class Experiment:
    def __init__(self):
        """
        Experimental object which allows to create STDP-like protocols of stimulations.
        """
        self.netstims = []
        self.iclamps = []

    def make_protocol(self, protocol: str, start, isi=1, iti=1,
                      epsp_synapse: Optional[Synapse] = None,
                      i_clamp_section: Sec = None, train_number=1):
        """
        Create an experimental protocol of EPSPs and APs.

        Each element of the experiment (EPSP or AP) is separated by isi (in ms).

        :param protocol:
            string eg. 3xEPSP[int=10,w=2.5,thr=5,del=2] 3xAP[int=10,dur=3,amp=1.6]

            Params ofr EPSP and AP:
            int - interval between in ms

            Params for EPSP only:
            w - weight for netconn (default is 1.0) -> used only when copy_netconn_params=False
            del - delay for netconn (default is 1.0) -> used only when copy_netconn_params=False
            thr - threshold for netconn (default is 10) -> used only when copy_netconn_params=False

            Params for AP only:
            dur - duration of AP in ms
            amp - amplitude in nA

        :param epsp_synapse:
            synapse to stimulate. Default is None if you don't want to stimulate synapse
        :param i_clamp_section:
            section to input IClamp. Default is None if you don't want to stimulate any section by
            electrode (eg. making AP)
            It is assumed that IClamp stimulate i_clamp_section(0.5) segment.
        :param start:
            start time of the first stimuli in ms, it is absolute time, so bear in mind warmup time.
        :param isi:
            Inter Stimulus Interval, eg. 3xEPSP,2xAP -isi- 3xEPSP,2xAP
        :param iti:
            Inter Train Interval eg. 3xEPSP,2xAP -isi- 3xEPSP,2xAP -iti- 3xEPSP,2xAP-isi-3xEPSP,2xAP
        :param train_number:
            number of trains. Default is 1
        :return:
            tuple(NetStim, IClamp).
            If epsp_synapse is None NetStim will be None
            If i_clamp_section is None IClamp will be None
        """
        protocol = protocol.lower()
        protocols = protocol.split(" ")

        netstim = None
        if epsp_synapse:
            netstim = NetStimCell(name="stim")
            self.netstims.append(netstim)

        iclamp = None
        if i_clamp_section:
            iclamp = IClamp(i_clamp_section(0.5))
            self.iclamps.append(iclamp)

        event_time = start
        for train_no in range(train_number):

            for p in protocols:
                event_time = self._prepare_protocol(p, netstim, iclamp, event_time, epsp_synapse)
                event_time += isi

            event_time += iti
            return netstim, iclamp

    def _prepare_protocol(self, protocol, netstim, iclamp, event_time, epsp_synapse):
        protocol, params = protocol.split("[")

        num, ptype = protocol.split("x")
        num = int(num)

        dur = 0
        amp = 0
        weight = 1.0
        threshold = 10
        delay = 1.0
        interval = 0

        for par in params.replace("]", "").split(","):
            name, val = par.split('=')
            name = name.strip()
            val = val.strip()
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

        if ptype == 'epsp':
            stim = netstim.make_netstim(event_time, number=num, interval=interval)
            epsp_synapse.add_netcon(source=stim, weight=weight, threshold=threshold, delay=delay)
            event_time += interval * num

        elif ptype == 'ap':
            for _ in range(num):
                iclamp.stim(delay=event_time, dur=dur, amp=amp)
                event_time += interval
        else:
            raise TypeError("Only allowed types are EPSP or AP.")

        return event_time
