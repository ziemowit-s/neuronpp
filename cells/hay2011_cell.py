from cells.core.basic_cell import BasicCell


class Hay2011Cell(BasicCell):
    def __init__(self, name):
        BasicCell.__init__(self, name)

    def add_soma_mechanisms(self, sections='soma'):
        """
        :param sections:
            List of sections or string defining single section name or sections names separated by space
            None will take all sections
        """
        secs = self.filter_secs(sec_names=sections).values()
        self._set_pas(secs)
        for s in secs:
            s.insert("Im")
            s.insert("Ca_LVAst")
            s.insert("Ca_HVA")
            s.insert("CaDynamics_E2")
            s.insert("SK_E2")
            s.insert("SKv3_1")
            s.insert("NaTs2_t")
            s.insert("Ih")
            s.ek = -85
            s.ena = 50

            s.gIhbar_Ih = 0.0001
            s.g_pas = 3e-5
            s.gImbar_Im = 0.000008
            s.decay_CaDynamics_E2 = 294.679571
            s.gamma_CaDynamics_E2 = 0.000509
            s.gCa_LVAstbar_Ca_LVAst = 0.000557
            s.gCa_HVAbar_Ca_HVA = 0.000644
            s.gSK_E2bar_SK_E2 = 0.09965
            s.gSKv3_1bar_SKv3_1 = 0.338029
            s.gNaTs2_tbar_NaTs2_t = 0.998912

    def add_axonal_mechanisms(self, sec_names='axon'):
        """
        :param sec_names:
            List of sections or string defining single section name or sections names separated by space
            None will take all sections
        """
        secs = self.filter_secs(sec_names=sec_names).values()
        self._set_pas(secs)
        for s in secs:
            s.insert("Im")
            s.insert("Ca_LVAst")
            s.insert("Ca_HVA")
            s.insert("CaDynamics_E2")
            s.insert("SKv3_1")
            s.insert("SK_E2")
            s.insert("K_Tst")
            s.insert("K_Pst")
            s.insert("Nap_Et2")
            s.insert("NaTa_t")

            s.ek = -85
            s.ena = 50

            s.gIhbar_Ih = 0.0001
            s.g_pas = 3e-5
            s.gImbar_Im = 0.013322
            s.decay_CaDynamics_E2 = 277.300774
            s.gamma_CaDynamics_E2 = 0.000525
            s.gCa_LVAstbar_Ca_LVAst = 0.000813
            s.gCa_HVAbar_Ca_HVA = 0.000222
            s.gSKv3_1bar_SKv3_1 = 0.473799
            s.gSK_E2bar_SK_E2 = 0.000047
            s.gK_Tstbar_K_Tst = 0.077274
            s.gK_Pstbar_K_Pst = 0.188851
            s.gNap_Et2bar_Nap_Et2 = 0.005834
            s.gNaTa_tbar_NaTa_t = 3.89618

    def add_apical_mechanisms(self, sections='apic'):
        """
        :param sections:
            List of sections or string defining single section name or sections names separated by space
            None will take all sections
        """
        secs = self.filter_secs(sec_names=sections).values()
        self._set_pas(secs)
        for s in secs:
            s.insert("CaDynamics_E2")
            s.insert("SK_E2")
            s.insert("Ca_LVAst")
            s.insert("Ca_HVA")
            s.insert("SKv3_1")
            s.insert("NaTs2_t")
            s.insert("Im")
            s.insert("Ih")
            s.ek = -85
            s.ena = 50
            s.cm = 2
            s.g_pas = 6e-5
            s.decay_CaDynamics_E2 = 35.725651
            s.gamma_CaDynamics_E2 = 0.000637
            s.gSK_E2bar_SK_E2 = 0.000002
            s.gCa_HVAbar_Ca_HVA = 0.000701
            s.gSKv3_1bar_SKv3_1 = 0.001808
            s.gNaTs2_tbar_NaTs2_t = 0.021489
            s.gImbar_Im = 0.00099

    def add_basal_mechanisms(self, sections='basal'):
        """
        :param sections:
            List of sections or string defining single section name or sections names separated by space
            None will take all sections
        """
        secs = self.filter_secs(sec_names=sections).values()
        self._set_pas(secs)
        for s in secs:
            s.insert("Ih")
            s.gIhbar_Ih = 0.0001
            s.cm = 2
            s.g_pas = 6e-5

    @staticmethod
    def _set_pas(secs):
        for s in secs:
            s.insert('pas')
            s.cm = 1
            s.Ra = 100
            s.e_pas = -90
