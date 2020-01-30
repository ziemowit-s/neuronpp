from neuronpp.cells.cell import Cell


class Hay2011Cell(Cell):
    def __init__(self, name, compile_paths='../commons/mods/hay2011'):
        Cell.__init__(self, name=name, compile_paths=compile_paths)

    def make_default_mechanisms(self):
        self.make_soma_mechanisms()
        self.make_apical_mechanisms()
        self.make_basal_mechanisms()
        self.make_axonal_mechanisms()

    def make_soma_mechanisms(self, sections='soma'):
        """
        :param sections:
            List of sections or string defining single section name or sections names separated by space
            None will take all sections

        """
        secs = self.filter_secs(name=sections)
        self._set_pas(secs)
        for s in secs:
            s.hoc.insert("Im")
            s.hoc.insert("Ca_LVAst")
            s.hoc.insert("Ca_HVA")
            s.hoc.insert("CaDynamics_E2")
            s.hoc.insert("SK_E2")
            s.hoc.insert("SKv3_1")
            s.hoc.insert("NaTs2_t")
            s.hoc.insert("Ih")
            s.hoc.ek = -85
            s.hoc.ena = 50

            s.hoc.gIhbar_Ih = 0.0001
            s.hoc.g_pas = 3e-5
            s.hoc.gImbar_Im = 0.000008
            s.hoc.decay_CaDynamics_E2 = 294.679571
            s.hoc.gamma_CaDynamics_E2 = 0.000509
            s.hoc.gCa_LVAstbar_Ca_LVAst = 0.000557
            s.hoc.gCa_HVAbar_Ca_HVA = 0.000644
            s.hoc.gSK_E2bar_SK_E2 = 0.09965
            s.hoc.gSKv3_1bar_SKv3_1 = 0.338029
            s.hoc.gNaTs2_tbar_NaTs2_t = 0.998912

    def make_axonal_mechanisms(self, section_name: str = 'axon'):
        """
        :param section_name:
            start with 'regex:any pattern' to use regular expression. If without 'regex:' - will look which Hoc objects contain the str
        """
        secs = self.filter_secs(name=section_name)
        self._set_pas(secs)
        for s in secs:
            s.hoc.insert("Im")
            s.hoc.insert("Ca_LVAst")
            s.hoc.insert("Ca_HVA")
            s.hoc.insert("CaDynamics_E2")
            s.hoc.insert("SKv3_1")
            s.hoc.insert("SK_E2")
            s.hoc.insert("K_Tst")
            s.hoc.insert("K_Pst")
            s.hoc.insert("Nap_Et2")
            s.hoc.insert("NaTa_t")

            s.hoc.ek = -85
            s.hoc.ena = 50

            s.hoc.insert("Ih")
            s.hoc.gIhbar_Ih = 0.0001
            s.hoc.g_pas = 3e-5
            s.hoc.gImbar_Im = 0.013322
            s.hoc.decay_CaDynamics_E2 = 277.300774
            s.hoc.gamma_CaDynamics_E2 = 0.000525
            s.hoc.gCa_LVAstbar_Ca_LVAst = 0.000813
            s.hoc.gCa_HVAbar_Ca_HVA = 0.000222
            s.hoc.gSKv3_1bar_SKv3_1 = 0.473799
            s.hoc.gSK_E2bar_SK_E2 = 0.000047
            s.hoc.gK_Tstbar_K_Tst = 0.077274
            s.hoc.gK_Pstbar_K_Pst = 0.188851
            s.hoc.gNap_Et2bar_Nap_Et2 = 0.005834
            s.hoc.gNaTa_tbar_NaTa_t = 3.89618

    def make_apical_mechanisms(self, sections='apic'):
        """
        :param sections:
            List of sections or string defining single section name or sections names separated by space
            None will take all sections

        """
        secs = self.filter_secs(name=sections)
        self._set_pas(secs)
        for s in secs:
            s.hoc.insert("CaDynamics_E2")
            s.hoc.insert("SK_E2")
            s.hoc.insert("Ca_LVAst")
            s.hoc.insert("Ca_HVA")
            s.hoc.insert("SKv3_1")
            s.hoc.insert("NaTs2_t")
            s.hoc.insert("Im")
            s.hoc.insert("Ih")
            s.hoc.ek = -85
            s.hoc.ena = 50
            s.hoc.cm = 2
            s.hoc.g_pas = 6e-5
            s.hoc.decay_CaDynamics_E2 = 35.725651
            s.hoc.gamma_CaDynamics_E2 = 0.000637
            s.hoc.gSK_E2bar_SK_E2 = 0.000002
            s.hoc.gCa_HVAbar_Ca_HVA = 0.000701
            s.hoc.gSKv3_1bar_SKv3_1 = 0.001808
            s.hoc.gNaTs2_tbar_NaTs2_t = 0.021489
            s.hoc.gImbar_Im = 0.00099

    def make_basal_mechanisms(self, sections='basal'):
        """
        :param sections:
            List of sections or string defining single section name or sections names separated by space
            None will take all sections

        """
        secs = self.filter_secs(name=sections)
        self._set_pas(secs)
        for s in secs:
            s.hoc.insert("Ih")
            s.hoc.gIhbar_Ih = 0.0001
            s.hoc.cm = 2
            s.hoc.g_pas = 6e-5

    def distribute_channel(self):
        """
        $o1.distribute_channels("apic","gIhbar_Ih",2,-0.8696,3.6161,0.0,2.0870,0.00010000000)
        $o1.distribute_channels("apic","gCa_LVAstbar_Ca_LVAst",3,1.000000,0.010000,700.000000,900.000000,0.1419540000)
        :return:
        """
        pass

    @staticmethod
    def _set_pas(secs):
        for s in secs:
            s.hoc.insert('pas')
            s.hoc.cm = 1
            s.hoc.Ra = 100
            s.hoc.e_pas = -90
