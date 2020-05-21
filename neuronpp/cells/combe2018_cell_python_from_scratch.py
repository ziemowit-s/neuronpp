import os
from neuron import h

from neuronpp.cells.cell import Cell
path = os.path.dirname(os.path.abspath(__file__))
f_path = os.path.join(path, "..", "commons/mods/combe2018")
maximum_segment_length = 75
from neuronpp.cells.morphology_points import axon_points
from neuronpp.cells.morphology_points import trunk_points
from neuronpp.cells.morphology_points import points_apic, points_apic_continued
from neuronpp.cells.morphology_points import points_dend, points_dend_continued
import neuronpp.cells.combe_parameters as params

class Combe2018Cell(Cell):
    def make_axon(self):
        # axon
        self.axon.hoc.pt3dclear()
        for points in axon_points:
            h.pt3dadd(*points, sec=self.axon.hoc)

    def make_soma(self):
        self.soma.hoc.pt3dclear()
        h.pt3dadd(10, 0, 30, 20, sec=self.soma.hoc)
        h.pt3dadd(21.5, 0.4, 30, 2.1, sec=self.soma.hoc)

    def make_trunk(self):
        for i, sec in enumerate(self.trunk):
            sec.hoc.pt3dclear()
            for points in trunk_points[i]:
                h.pt3dadd(*points, sec=sec.hoc)

    def make_apic(self):
        len_1 = len(points_apic)
        for i, sec in enumerate(self.apic):
            sec.hoc.pt3dclear()
            if i < len_1:
                for points in points_apic[i]:
                    h.pt3dadd(*points, sec=sec.hoc)
            else:
                for points in points_apic_continued[i-len_1]:
                    h.pt3dadd(*points, sec=sec.hoc)

    
    def make_dend(self):
        len_1 = len(points_dend)
        for i, sec in enumerate(self.dend):
            sec.hoc.pt3dclear()
            if i < len_1:
                for points in points_dend[i]:
                    h.pt3dadd(*points, sec=sec.hoc)
            else:
                for points in points_dend_continued[i-len_1]:
                    h.pt3dadd(*points, sec=sec.hoc)

    def make_morphology(self):
        self.soma = self.add_sec("soma")
        self.axon = self.add_sec("axon")
        self.trunk = []
        for i in range(19):
            self.trunk.append(self.add_sec("trunk_%d" % i))
        self.apic = []
        for i in range(72):
            self.apic.append(self.add_sec("apic_%i" % i))
        self.dend = []
        for i in range(51):
            self.dend.append(self.add_sec("dend_%i" % i))

        self.connect_secs(self.soma, self.axon)
        for i in range(18):
            if i == 0:
                self.connect_secs(self.trunk[i], self.soma)
            else:
                self.connect_secs(self.trunk[i], self.trunk[i-1])

        for i in range(42, 48):
            self.connect_secs(self.apic[i], self.apic[i-1])
        self.connect_secs(self.apic[48], self.apic[46])
        for i in range(49, 51):
            self.connect_secs(self.apic[i], self.apic[48])
        self.connect_secs(self.apic[51], self.apic[45])
        self.connect_secs(self.apic[52], self.apic[44])
        for i in range(53, 55):
            self.connect_secs(self.apic[i], self.apic[52])
        self.connect_secs(self.apic[55], self.trunk[17])
        self.connect_secs(self.apic[56], self.trunk[18])
        self.connect_secs(self.apic[57], self.apic[56])
        self.connect_secs(self.apic[58], self.apic[56])
        self.connect_secs(self.apic[59], self.apic[55])
        for i in [60, 61]:
            self.connect_secs(self.apic[i], self.apic[i-1])
        self.connect_secs(self.apic[62], self.apic[60])
        self.connect_secs(self.apic[63], self.apic[59])
        for i in [64, 65]:
            self.connect_secs(self.apic[i], self.apic[i-1])
        self.connect_secs(self.apic[66], self.apic[64])
        self.connect_secs(self.apic[67], self.apic[63])
        for i in [68, 69]:
            self.connect_secs(self.apic[i], self.apic[i-1])
        self.connect_secs(self.apic[70], self.apic[68])
        self.connect_secs(self.apic[71], self.apic[67])
        self.connect_secs(self.apic[0], self.trunk[-1])
        for i in [1, 2]:
            self.connect_secs(self.apic[i], self.apic[0])
        for i in [3, 4]:
            self.connect_secs(self.apic[i], self.apic[2])
        for i in [5, 6]:
            self.connect_secs(self.apic[i], self.trunk[i-4])
        for i in [7, 8]:
            self.connect_secs(self.apic[i], self.apic[6])
        for i in [9, 10]:
            self.connect_secs(self.apic[i], self.apic[8])
        for i in [11, 12]:
            self.connect_secs(self.apic[i], self.apic[10])
        self.connect_secs(self.apic[13], self.trunk[3])
        for i in [14, 15]:
            self.connect_secs(self.apic[i], self.apic[13])
        for i in [16, 17]:
            self.connect_secs(self.apic[i], self.trunk[i-12])
        for i in [18, 19]:
            self.connect_secs(self.apic[i], self.apic[17])
        self.connect_secs(self.apic[20], self.trunk[6])
        for i in [21, 22]:
            self.connect_secs(self.apic[i], self.apic[20])
        for i in [23, 24]:
            self.connect_secs(self.apic[i], self.apic[22])
        for i in [25, 27]:
            self.connect_secs(self.apic[i], self.trunk[i-18])
        for i in [28, 29]:
            self.connect_secs(self.apic[i], self.apic[27])
        for i in[30, 32]:
            self.connect_secs(self.apic[i], self.trunk[i-20])
        self.connect_secs(self.apic[33], self.apic[42])
        self.connect_secs(self.apic[34], self.apic[43])
        self.connect_secs(self.apic[35], self.trunk[14])
        self.connect_secs(self.apic[36], self.trunk[15])
        self.connect_secs(self.apic[37], self.trunk[16])
        for i in [38, 39]:
            self.connect_secs(self.apic[i], self.apic[i-1])
        self.connect_secs(self.apic[40], self.apic[38])
        self.connect_secs(self.apic[41], self.apic[37])
        self.connect_secs(self.dend[0], self.soma)
        for i in range(1, 4):
            self.connect_secs(self.dend[i], self.dend[i-1])
        self.connect_secs(self.dend[4], self.dend[2])
        self.connect_secs(self.dend[5], self.dend[1])
        for i in [6, 7]:
            self.connect_secs(self.dend[i], self.dend[5])
        for i in [8, 9]:
            self.connect_secs(self.dend[i], self.dend[7])
        for i in [10, 11]:
            self.connect_secs(self.dend[i], self.dend[9])
        self.connect_secs(self.dend[12], self.dend[0])
        for i in range(13, 16):
            self.connect_secs(self.dend[i], self.dend[i-1])
        self.connect_secs(self.dend[16], self.dend[14])
        self.connect_secs(self.dend[17], self.dend[13])
        for i in [18, 19]:
            self.connect_secs(self.dend[i], self.dend[17])
        self.connect_secs(self.dend[20], self.dend[12])
        for i in [21, 22]:
            self.connect_secs(self.dend[i], self.dend[20])
        self.connect_secs(self.dend[23], self.soma)
        for i in range(24, 27):
            self.connect_secs(self.dend[i], self.dend[i-1])
        self.connect_secs(self.dend[27], self.dend[25])
        self.connect_secs(self.dend[28], self.dend[24])
        self.connect_secs(self.dend[29], self.dend[23])
        for i in [30, 31]:
            self.connect_secs(self.dend[i], self.dend[i-1])
        self.connect_secs(self.dend[32], self.dend[30])
        for i in [33, 34]:
            self.connect_secs(self.dend[i], self.dend[32])
        self.connect_secs(self.dend[35], self.dend[29])
        for i in range(36, 39):
            self.connect_secs(self.dend[i], self.dend[i-1])
        self.connect_secs(self.dend[39], self.dend[37])
        self.connect_secs(self.dend[40], self.dend[36])
        self.connect_secs(self.dend[41], self.dend[35])
        self.connect_secs(self.dend[42], self.soma, source_loc=0, target_loc=0)
        for i in [43, 44]:
            self.connect_secs(self.dend[i], self.dend[i-1])
        self.connect_secs(self.dend[45], self.dend[43])
        for i in [46, 47]:
            self.connect_secs(self.dend[i], self.dend[45])
        self.connect_secs(self.dend[48], self.dend[42])
        for i in [49, 50]:
            self.connect_secs(self.dend[i], self.dend[48])

        self.make_axon()
        self.make_soma()
        self.make_trunk()
        self.make_apic()
        self.make_dend()

    def add_soma_mechanisms(self):
        """
        :param sections:
            List of sections or string defining single section name or sections names separated by space
            None will take all sections

        """
        sec = self.soma.hoc
        sec.insert("na3")
        sec.gbar_na3 = params.gna
        sec.insert("kdr")
        sec.gkdrbar_kdr = params.gkdr
        
        sec.ena = params.potNa
        
        sec.insert("nap")
        sec.gnabar_nap = params.soma_nap_gnabar
        sec.K_nap = params.soma_K_nap
        sec.vhalf_nap = params.soma_vhalf_nap
        
        sec.insert("pas")
        sec.g_pas = 1/params.Rm_soma
        sec.e_pas = params.e_pas
        sec.Ra = params.Ra_soma
        sec.cm = params.Cm_soma
        
        sec.insert("h")
        sec.gbar_h = params.soma_hbar
        sec.K_h = params.soma_K_h
        sec.vhalf_h = params.soma_vhalf_h
        
        sec.insert("kap")
        sec.gkabar_kap = params.soma_kap
        
        sec.insert("km")
        sec.gbar_km = params.soma_km
        sec.ek = params.potK
        
        sec.insert("cal")
        sec.gcalbar_cal = params.soma_caL
        
        sec.insert("cat")
        sec.gcatbar_cat = params.soma_caT
        
        sec.insert("car")
        sec.gcabar_car = params.gsomacar

        sec.insert("kca")
        sec.cac_kca = params.cac_kca
        sec.gbar_kca = params.gbar_kca
        
        sec.insert("mykca") # K(Ca) fAHP potassium type current
        sec.gkbar_mykca = params.gkbar_mykca
        
        # sec.insert("cad") # ca buffering mechanism, we will add this
        # much later

    def add_axon_mechanisms(self):
        sec = self.axon.hoc
        sec.insert("nax")
        sec.gbar_nax = params.gna*params.AXNa
        sec.insert("kdr")
        sec.gkdrbar_kdr = params.gkdr*params.AXKdr
        sec.ena = params.potNa
        sec.insert("pas")
        sec.g_pas = 1/params.Rm_axon
        sec.Ra = params.Ra_axon
        sec.cm = params.Cm_axon
        sec.insert("km")
        sec.gbar_km = 3*params.soma_km
        
        sec.insert("kap")
        sec.gkabar_kap = params.soma_kap
        sec.ek = params.potK

    def __init__(self, name=None, compile_paths=f_path):
        """
        :param name:
            The name of the cell
        :param compile_paths:
            Folder with channels
        """
        Cell.__init__(self, name=name, compile_paths=compile_paths)

        self.make_morphology()
        # adjust segment_number
        for sec in self.secs:
            sec.hoc.nseg = 1+int(sec.hoc.L/maximum_segment_length)
        self.add_soma_mechanisms()
        self.add_axon_mechanisms()
        ObliqueTrunkSection = self.trunk[17]
        BasalTrunkSection   = self.trunk[7]
        
