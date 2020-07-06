from collections import namedtuple

from neuronpp.utils.iclamp import IClamp
from neuronpp.core.hocwrappers.seg import Seg
from neuronpp.core.cells.netstim_cell import NetStimCell
from neuronpp.core.hocwrappers.synapses.synapse import Synapse

EpspProtocol = namedtuple("EpspProtocol", "num init int w delay thr syn")
IClampProtocol = namedtuple("IClampProtocol", "num init int dur amp seg")


class Experiment:
    def __init__(self, iti: float):
        """
        Experimental object which allows to create protocols of stimulations.

        Creates an experimental protocol of EPSPs and IClamp:
          * It consist of one or more blocks of Trains
          * Each Train consists of one or more protocols
          * During each Train all protocols defined will be computed
          * Protocol can be EPSP or IClamp
          * Interval between Trains define: iti value (Inter-Train-Interval)
          * After one block of Train:
             * we choose the end-time of the longest protocol and call it max_time
             * we add iti value to the max_time
             * we update start time of each protocol as: max_time + init value of each protocol

        :param iti:
            in ms.
            Inter Train Interval - after executing each protocol, we wait iti-time and then execute
            once againt the same set of experimental trainings, eg:
                [3xEPSP,2xAP] -ITI- [3xEPSP,2xAP]

            It is used only if during build() train_number > 1

        """
        self.iti = iti
        self.iclamp = []
        self.netstims = []

        self.epsp_protocols = []
        self.iclamp_protocols = []
        self._builded = False

    def add_iclamp(self, num: int, segment: Seg, init: float = 0, interval: float = 0,
                   dur: float = 0, amp: float = 0):
        """
        Add IClamp Protocol to the experiment.
        It function as the equivalent of Action Potential for the cell,
        especially if it is injected around soma(0.5).

        :param num:
            number of execution of this protocol
        :param init:
            start time of the first stimuli in ms, it is absolute time, so bear in mind warmup time.
            Default is 0
        :param interval:
            interval between each each IClamps in ms. Default is 0
        :param dur:
            duration of IClamp in ms
        :param amp:
            amplitude in nA
        :param segment:
            segment to input IClamp eg. soma(0.5)
        """
        protocol = IClampProtocol(num=num, init=init, int=interval, dur=dur, amp=amp, seg=segment)
        self.iclamp_protocols.append(protocol)

    def add_epsp(self, num: int, synapse: Synapse, init: float = 0, interval: float = 0, 
                 weight: float = 1.0, delay: float = 1.0, thr: float = 10):
        """
        Add EPSP (Excitatory Post Synaptic Potential) Protocol to the experiment.

        :param num:
            number of execution of this protocol
        :param init:
            start time of the first stimuli in ms, it is absolute time, so bear in mind warmup time.
            Default is 0
        :param interval:
            interval between each EPSP in ms. Default is 0
        :param weight:
            weight for netconn. Default is 1.0 -> used only when copy_netconn_params=False
        :param delay:
            delay for netconn. Default is 1.0 -> used only when copy_netconn_params=False
        :param thr:
            threshold for netconn. Default is 10 -> used only when copy_netconn_params=False
        :param synapse:
            synapse to stimulate
        """
        protocol = EpspProtocol(num=num, init=init, int=interval, w=weight, delay=delay, thr=thr, syn=synapse)
        self.epsp_protocols.append(protocol)

    def build(self, train_number=1):
        """
        :param train_number:
            number of trains. Default is 1
        """
        if self._builded:
            raise ValueError("You cannot build Experiment which have been already built.")
        self._builded = True

        global_time = 0
        for train_no in range(train_number):
            new_global_time = global_time

            for e in self.epsp_protocols:
                new_time = self._prepare_epsp_protocol(e, global_time)
                if new_time > new_global_time:
                    new_global_time = new_time

            for i in self.iclamp_protocols:
                new_time = self._prepare_iclamp_protocol(i, global_time)
                if new_time > new_global_time:
                    new_global_time = new_time

            global_time = new_global_time
            global_time += self.iti

    def _prepare_epsp_protocol(self, epsp: EpspProtocol, global_time):
        synapse = epsp.syn
        current_time = global_time + epsp.init

        netstim = NetStimCell(name="stim")
        self.netstims.append(netstim)

        stim = netstim.make_netstim(start=current_time, number=epsp.num, interval=epsp.int)
        synapse.add_netcon(source=stim, weight=epsp.w, threshold=epsp.thr, delay=epsp.delay)
        current_time += epsp.int * epsp.num

        return current_time

    def _prepare_iclamp_protocol(self, iclamp: IClampProtocol, global_time):
        iclamp_obj = IClamp(iclamp.seg)
        current_time = global_time + iclamp.init

        for _ in range(iclamp.num):
            iclamp_obj.stim(delay=current_time, dur=iclamp.dur, amp=iclamp.amp)
            current_time += iclamp.int
        current_time = global_time
        current_time += iclamp.init

        self.iclamp.append(iclamp_obj)
        return current_time
