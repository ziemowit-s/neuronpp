import os

import numpy as np
from neuron import h
from neuronpp.cells.cell import Cell

path = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(path, "..",
                          "commons/mods/hay2011")

class Hay2011Cell(Cell):
    def __init__(self, name, compile_paths=model_path):
        """
        Experimental cell of Hay 2011 rewrited to Python
        :param name:
        :param compile_paths:
        """
        Cell.__init__(self, name=name, compile_paths=compile_paths)

    def make_default_mechanisms(self):
        self._adjust_nsec(self.secs)
        self._set_pas(self.secs)
        self.make_axonal_mechanisms()
        self.make_soma_mechanisms()
        self.make_apical_mechanisms()
        self.make_basal_mechanisms()

        for s in self.secs:
            if s.hoc.diam == 0:
                s.hoc.diam = 1

    def make_soma_mechanisms(self, sections='soma'):
        """
        :param sections:
            List of sections or string defining single section name or sections names separated by space
            None will take all sections

        """
        sec = self.filter_secs(name=sections)
        if not isinstance(sec, list):
            sec = [sec]
        for s in sec:
            s.hoc.insert("Im")
            s.hoc.insert("Ca_LVAst")
            s.hoc.insert("Ca_HVA")
            s.hoc.insert("CaDynamics_E2")
            s.hoc.insert("SK_E2")
            s.hoc.insert("SKv3_1")
            s.hoc.insert("NaTs2_t")
            s.hoc.ek = -85
            s.hoc.ena = 50

            s.hoc.insert("Ih")
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
        sec = self.filter_secs(name=section_name)
        if not isinstance(sec, list):
            sec = [sec]
        for s in sec:
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
        sec = self.filter_secs(name=sections)
        if not isinstance(sec, list):
            sec = [sec]
        for s in sec:
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

        if len(sec) > 0:
            # Parameters and the function rewrite to Python from Hay2011 proc distribute_channels()
            self._distribute_channel(mech="Ih", mech_param="gIhbar", dist_type="exp", s3=-0.8696, s4=3.6161, s5=0.0, s6=2.0870, s7=0.0001)
            self._distribute_channel(mech="Ca_LVAst", mech_param="gCa_LVAstbar", dist_type="abs", s3=1, s4=0.01, s5=700, s6=900, s7=0.141954)

    def make_basal_mechanisms(self, sections='dend'):
        """
        :param sections:
            List of sections or string defining single section name or sections names separated by space
            None will take all sections

        """
        sec = self.filter_secs(name=sections)
        if not isinstance(sec, list):
            sec = [sec]
        for s in sec:
            s.hoc.insert("Ih")
            s.hoc.gIhbar_Ih = 0.0001
            s.hoc.cm = 2
            s.hoc.g_pas = 6e-5

    def _distribute_channel(self, mech, mech_param, sections='apic', soma_name='soma', dist_type='abs', s3=None, s4=None, s5=None, s6=None, s7=None):
        """
        This function is rewrited to Python from Hay2011 L5PCTemplate.hoc file, proc distribute_channels()

        :param sections:
        :param soma_name:
        :param dist_type:
            'abs' - absolute [default]
            'lin' - linear
            'sigm' - sigmoidal
            'exp' - exponential
        :return:
        """
        soma = self.filter_secs(soma_name, as_list=True)
        if len(soma) != 1:
            raise LookupError("Central section for channel distribution must be only one for name %s, "
                              "but found %s sections containing this name." % (soma_name, len(soma)))
        soma = soma[0]
        secs = self.filter_secs(name=sections, as_list=True)

        max_dist = max([h.distance(soma(0.5).hoc, s(1).hoc) for s in secs])
        for sec in secs:
            for x in sec.hoc:
                dist = h.distance(soma(0.5).hoc, x)
                dist_norm = dist/max_dist

                if dist_type == 'lin':
                    val = s3 + dist_norm * s4
                elif dist_type == 'sigm':
                    ex = np.exp((dist_norm - s5) / s6)
                    sigmoid = s4 / (1 + ex)
                    val = s3 + sigmoid
                elif dist_type == 'exp':
                    val = s3 + s6 * np.exp(s4 * (dist_norm - s5))
                elif dist_type == 'abs':
                    if s5 < dist < s6:
                        val = s3
                    else:
                        val = s4
                else:
                    raise ValueError("The only allowed dist_type are abs,lin,sigm,exp, but provided %s" % dist_type)
                val *= s7

                mech_obj = getattr(x, mech)
                setattr(mech_obj, mech_param, val)

    @staticmethod
    def _adjust_nsec(secs):
        for s in secs:
            s.hoc.nseg = 1 + 2*int(s.hoc.L/40)

    @staticmethod
    def _set_pas(secs):
        for s in secs:
            s.hoc.insert('pas')
            s.hoc.cm = 1
            s.hoc.Ra = 100
            s.hoc.e_pas = -90
