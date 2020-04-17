import random
from typing import List
import numpy as np

from neuronpp.core.cells.section_cell import SectionCell
from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.hocwrappers.spine import Spine
from neuronpp.core.cells.utils import establish_electric_properties
from neuronpp.core.cells.utils import get_spine_number

# Nomenclature and values adapted from Harris KM, Jensen FE, Tsao BE.
# J Neurosci 1992

SPINE_DIMENSIONS = {
    "mushroom": {
        "head_diam": 1.1,
        "head_len": 0.8,
        "neck_diam": 0.20,
        "neck_len": 0.43,
    },
    "thin": {
        "head_diam": 0.2,
        "head_len": 0.5,
        "neck_diam": 0.1,
        "neck_len": 0.5,
    },
    "stubby": {
        "head_diam": 0.32,
        "head_len": 0.2,
        "neck_diam": 0.32,
        "neck_len": 0.2,
    },
    "generic": {
        "head_diam": 1.,
        "head_len": 1,
        "neck_diam": 0.5,
        "neck_len": 0.5,
    }
}


class SpineCell(SectionCell):
    def __init__(self, name=None, compile_paths=None):
        SectionCell.__init__(self, name, compile_paths=compile_paths)
        self.spines = []
        self.heads = []
        self.necks = []
        self._next_index = 0

    def make_spines(self, spine_number, secs=None, head_nseg=2, neck_nseg=2, seed: int = None):
        """
        Currently the only supported spine distribution is random_uniform

        Single spine is 2 x cylinder:
          * head: L=1um diam=1um
          * neck: L=0.5um diam=0.5um

        :param spine_number:
            The number of spines to make
        :param secs:
        :param head_nseg
        :param neck_nseg
        :param seed:
            seed int for random uniform distribution of the spines.
        :return:
            list of added spine heads
        """
        if not isinstance(secs, list):
            secs = [secs]
        # Hack to prevent a loop between sections while adding necks
        # neck is added to self.secs, so if param secs is the same list it will append to the list each head and neck
        # after each iteration of the loop. To prevent this we need to copy secs list
        secs = [s for s in secs]

        if seed:
            random.seed(seed)

        spines = []
        heads = []
        necks = []
        for _ in range(spine_number):
            i = self._next_index
            head = self.add_sec(name="head[%s]" % i, diam=1, l=1, nseg=head_nseg)
            neck = self.add_sec(name="neck[%s]" % i, diam=0.5, l=0.5, nseg=neck_nseg)
            spine = Spine(head, neck, self, "spine")
            spines.append(spine)
            heads.append(head)
            necks.append(neck)
            self._connect_necks_rand_uniform(neck, secs)
            self._next_index += 1

        self.spines.extend(spines)
        self.heads.extend(heads)
        self.necks.extend(necks)
        return spines

    @staticmethod
    def _connect_necks_rand_uniform(neck: Sec, sections):
        """
        Connect necks list to sections list with uniform random distribution
        :param neck:
        :param sections:
        """
        max_l = int(sum([s.hoc.L for s in sections]))
        added = dict([(s.hoc.name(), []) for s in sections])

        i = 0
        r = random.randint(0, max_l)
        for s in sections:
            s = s.hoc
            i += s.L
            if i > r:
                loc = (r - i + s.L) / s.L
                if loc in added[s.name()]:
                    break
                neck.hoc.connect(s(loc), 0.0)
                added[s.name()].append(loc)
                break

    def add_spines_to_section_list(self, sections: List[Sec], spine_density,
                                   spine_type="generic", **spine_params):
        """
        Add spines with specified linear density (per 1 um) to specified
        secions (compartments). Spines can have
        a predifined type (stubby, thin, mushroom) or, alternatively, their
        dimentions (head_diam, head_len, neck_diam, neck_len) can be specified
        in spine_params.

        :param regions:
            Section that will have spines
        :param spine_density:
            spine density 
        :param spine_type:
            Spine type. There are four predifined types: thin, stubby,
            mushroom and other.
        :param **spine_params:
            See below

        Keyword arguments:
        :spine_tag:
            String attached to name of every head and neck
        :head_diam:
            Spine head diameter
        :head_len:
            Length of the spine head
        :neck_diam:
            Spine neck diameter
        :neck_len:
            Length of the spine neck
        :area_densisty:
            if False spine_density is treated as linear spine density [um]
            if True  spine_density is treated as area density [um2]
        :u_random: None
            seed for the random number generator used for picking out
            spine positions
        :spine_g_pas:
            pas conductance. By default g_pas of the parent section
            will be used.
        :spine_E_pas:
            pas reversal potential. By default pas reversal potential
            of the parent section will be used.
        :spine_rm:
            membrane resistivity. By default 1/pas conductance of the
            parent section will be used.
        :spine_ra:
            axial resistivity. By default axial resistivity of the parent
            section will be used.
        :area_densisty:
            if False spine_density is treated as linear spine density [um]
            if True  spine_density is treated as area density [um2]
        :add_pas:
            add passive mechanism
        :return:
            list of added spine heads

        TODO: add spines with a distribution of head dimensions and
              neck dimensions
        """
        try:
            spine_dimensions = SPINE_DIMENSIONS[spine_type]
        except KeyError:
            spine_dimensions = SPINE_DIMENSIONS["generic"]
        spine_tag = spine_params.pop("spine_tag", spine_type)
        head_diam = spine_params.pop("head_diam", spine_dimensions["head_diam"])
        head_len = spine_params.pop("head_len", spine_dimensions["head_len"])
        neck_diam = spine_params.pop("neck_diam", spine_dimensions["neck_diam"])
        neck_len = spine_params.pop("neck_len", spine_dimensions["neck_len"])
        # If Falde
        spine_E_pas = spine_params.pop("spine_E_pas", None)
        spine_g_pas = spine_params.pop("spine_g_pas", None)
        spine_rm = spine_params.pop("spine_rm", None)
        spine_ra = spine_params.pop("spine_ra", None)
        spine_cm = spine_params.pop("spine_cm", None)
        add_pas = spine_params.pop("add_pas", False)
        if isinstance(spine_rm, int) or isinstance(spine_rm, float):
            spine_g_pas = 1 / spine_rm
        area_density = spine_params.pop("area_density", False)
        seed = spine_params.pop("u_random", None)
        if seed is not None:
            np.random.seed(seed)
        all_target_locations = []
        for sec in sections:
            spine_number = get_spine_number(sec, spine_density, area_density)
            E_pas, g_pas, ra, cm = establish_electric_properties(sec,
                                                                 spine_E_pas,
                                                                 spine_g_pas,
                                                                 spine_ra,
                                                                 spine_cm)
            if not add_pas:
                E_pas = None
                g_pas = None
            if isinstance(seed, int):
                target_locations = np.random.uniform(0., 1.,
                                                     spine_number).tolist()
            else:
                target_locations = np.linspace(0., .99,
                                               spine_number).tolist()

            self._add_spines_to_section(sec, spine_tag, target_locations,
                                        head_diam, head_len, neck_diam,
                                        neck_len, E_pas, g_pas, ra, cm,
                                        add_pas=add_pas)
            all_target_locations.append(target_locations)
        return all_target_locations

    def _add_spines_to_section(self, section: Sec, spine_tag,
                               target_location, head_diam,
                               head_len, neck_diam, neck_len,
                               E_pas, g_pas, ra, cm, add_pas=True):
        name = section.name
        if not isinstance(target_location, list):
            target_location = [target_location]
        for i, location in enumerate(target_location):
            head = self.add_sec(name="%s_%s_head[%d]" % (name, spine_tag, i),
                                diam=head_diam, l=head_len, nseg=2,
                                E_rest=E_pas, ra=ra, cm=cm,
                                g_pas=g_pas, add_pas=add_pas)
            neck = self.add_sec(name="%s_%s_neck[%d]" % (name, spine_tag, i),
                                diam=neck_diam, l=neck_len, nseg=1,
                                E_rest=E_pas, ra=ra, cm=cm,
                                g_pas=g_pas, add_pas=add_pas)
            self.heads.append(head)
            self.necks.append(neck)
            spine = Spine(head, neck, self, "%s_spine_%s[%d]" % (name,
                                                                 spine_tag,
                                                                 i))
            self.spines.append(spine)
            self.connect_secs(source=neck, target=section, source_loc=location,
                              target_loc=0.0)

    def get_spines_by_section_with_mech(self, mech_name):
        mech_dend_loc = {}
        all_spines = self.spines

        for spine in all_spines:
            spine_mechs = set(list(spine.neck.hoc.psection()["density_mechs"]) +
                              list(spine.head.hoc.psection()["density_mechs"]))

            if mech_name is None or mech_name in spine_mechs:
                parent_mechs = spine.parent.hoc.psection()["density_mechs"]
                if mech_name is None or mech_name in parent_mechs:
                    if spine.parent not in mech_dend_loc:
                        mech_dend_loc[spine.parent] = []
                    mech_dend_loc[spine.parent].append(spine)
        return mech_dend_loc

    def _get_spine_factor(self, spines: List[Spine], mech_name: str, gbar: str):
        """
        Find sum(gbar*Area_spine) for mech_name in spines. If gbar is None
        sum(spine_cm*Area_spine) will be returned
        This factor will further be used in lowering gbar in
        the dendrite the spine are attached to.
        """
        factor = 0
        for spine in spines:
            for sec in spine.sections:
                sec_mech = sec.hoc.psection()["density_mechs"]
                nseg = sec.hoc.nseg
                for seg in sec.hoc:
                    if gbar is not None:
                        try:
                            mech = getattr(seg, mech_name)
                            gbar_val = getattr(mech, gbar)
                        except AttributeError:
                            continue
                    else:
                        gbar_val = getattr(seg, mech_name)
                    factor += gbar_val * sec.area / nseg
        return factor

    def compensate(self, cm_adjustment=False, **mechs_with_gbar_name):
        """
        Compensate for a chosen channel/density mechanism after adding spines.
        Adding spines means adding additional membrane area, increasing
        conductance and capacitance of the section and thus changing its
        electric properties. Adding ion channels to spines will also change
        overall channel conductance of the neuron. If you want to add spines
        and try to preserve neuron behavior (so you don't have to retune
        your model) you might try to compensate for that additional membrane
        area and added mechanisms.

        This function finds dendrites with spines, which both have mechanisms
        specified in mechs_with_gbar_names, and lowers conductances (gbars)
        by a
        (Area_dendrite*dendritic_conductance-sum(spine_conductance*Area_spine)/
        Area_dendrite*dendritic_conductance

        :param cm_adjustment:
             if True cm of the section with spines will be lowered
             to account for membrane area of added spines
        :param mechs_with_gbar_name:
             specify mechanisms and their respective conductance names
             (gbars), e.g. pas="g_pas"
        """
        for mech_name, gbar in mechs_with_gbar_name.items():
            mech_loc = self.get_spines_by_section_with_mech(mech_name)
            for dend in mech_loc.keys():
                A_d = dend.area
                spine_factor = self._get_spine_factor(mech_loc[dend],
                                                      mech_name, gbar=gbar)
                for seg in dend.hoc:
                    mech = getattr(seg, mech_name)
                    gbar_val = getattr(mech, gbar)
                    new_val = (gbar_val * A_d - spine_factor) / (gbar_val * A_d)
                    setattr(mech, gbar, new_val)

        if cm_adjustment:
            all_spines = self.get_spines_by_section_with_mech(None)
            for dend in all_spines:
                A_d = dend.area
                spine_factor = self._get_spine_factor(all_spines[dend],
                                                      "cm", None)
                cm_val = dend.hoc.cm
                new_val = (cm_val * A_d - spine_factor) / (cm_val * A_d)
                dend.hoc.cm = new_val
