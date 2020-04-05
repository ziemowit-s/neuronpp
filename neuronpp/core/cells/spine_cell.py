import random
import numpy as np

from neuron import h

from neuronpp.core.cells.section_cell import SectionCell
from neuronpp.core.hocwrappers.sec import Sec
from neuronpp.core.cells.utils import establish_electric_properties
from neuronpp.core.cells.utils import get_spine_number
from neuronpp.core.cells.utils import get_area

### Nomenclature and values adapted from Harris KM, Jensen FE, Tsao BE.
### J Neurosci 1992

SPINE_DIMENSIONS = {
    "mushroom":  {
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
    "generic":  {
        "head_diam": 1.,
        "head_len": 1,
        "neck_diam": 0.5,
        "neck_len": 0.5,
    }
}





class SpineCell(SectionCell):
    def __init__(self, name=None, compile_paths=None):
        SectionCell.__init__(self, name, compile_paths=compile_paths)
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

        heads = []
        necks = []
        for _ in range(spine_number):
            i = self._next_index
            head = self.add_sec(name="head[%s]" % i, diam=1, l=1, nseg=head_nseg)
            neck = self.add_sec(name="neck[%s]" % i, diam=0.5, l=0.5, nseg=neck_nseg)
            heads.append(head)
            necks.append(neck)
            self.connect_secs(source=head, target=neck)
            self._connect_necks_rand_uniform(neck, secs)
            self._next_index += 1
        
        self.heads.extend(heads)
        self.necks.extend(necks)
        return heads, necks

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


    def add_spines_at(self, dist_range, spine_density,
                      spine_type="generic", **kwargs):
        """
        Add spines with specified linear density (per 1 um) to a part
        of dendritic range specified as distance from the soma. Spines can have
        a predifined type (stubby, thin, mushroom) or, alternatively, their
        dimentions (head_diam, head_len, neck_diam, neck_len) can be specified
        in kwargs.


        :param dist_range: tuple or list 
            tuple containing begining and end of the distance range
            where spines will be added
        :param spine_density:
            Linear spine density in [um]
        :param spine_type:
            Spine type. There are four predifined types: thin, stubby,
            mushroom and other.
        :param **kwargs:
            See below

        Keyword arguments:
        :spine name:
            String attached to name of every head and neck
        :head_diam:
            Spine head diameter
        :head_len:
            Length of the spine head
        :neck_diam:
            Spine neck diameter
        :neck_len:
            Length of the spine neck
        :g_pas:
            pas conductance
        :E_pas:
            pas reversal potential:
        :r_m:
            membrane resistivity
        :r_a:
            axial resistivity
        :add_pas:
            add passive mechanism
        :seed: None
            seed for the random number generator used for picking out
            spine positions
        :return:
            list of added spine heads
        """
        soma = self.filter_secs("soma")
        secs = []
        if isinstance(soma, list):
            soma = soma[0]

        if isinstance(dist_range, int) or isinstance(dist_range, float):
            dist_range = [dist_range, -1]
        if isinstance(dist_range, list) and len(dist_range) == 1:
            dist_range.append(-1)

        if isinstance(dist_range, list):
            if dist_range[1] > 0:
                assert dist_range[1] > dist_range[0]
                secs = self.filter_secs(obj_filter=lambda o: h.distance(soma.hoc(0.5), o.hoc(0.0)) >= dist_range[0] and  h.distance(soma.hoc(0.5), o.hoc(1.0)) <= dist_range[1] and "soma" not in o.name, as_list=True)
            elif dist_range[1] == -1:
                secs = self.filter_secs(obj_filter=lambda o: h.distance(soma.hoc(0.5), o.hoc(0.0)) >= dist_range[0] and "soma" not in o.name, as_list=True)
        if len(secs):
            self.add_spines_section_list(secs, spine_density, spine_type, **kwargs)
        else:
            print("""Wrong distance chosen, couldn't find appropriate sections,
            didn't add any spines""")
        return secs

    def add_spines_to_regions(self, region, spine_density,
                              spine_type="generic", **kwargs):
        """
        Add spines with specified linear density (per 1 um) to regions with section
        names starting with string region.
        Spines can have a predifined type (stubby, thin, mushroom) or, alternatively, their
        dimentions (head_diam, head_len, neck_diam, neck_len) can be specified
        in kwargs.

        :param region:
            Region that will have spines
        :param spine_density:
            spine density
        :param spine_type:
            Spine type. There are four predifined types: thin, stubby,
            mushroom and other.
        :param **kwargs:
            See below

        Keyword arguments:
        :spine name:
            String attached to name of every head and neck
        :head_diam:
            Spine head diameter
        :head_len:
            Length of the spine head
        :neck_diam:
            Spine neck diameter
        :neck_len:
            Length of the spine neck
        :g_pas:
            pas conductance
        :E_pas:
            pas reversal potential:
        :r_m:
            membrane resistivity
        :r_a:
            axial resistivity
        :add_pas:
            add passive mechanism
        :area_densisty:
            if False spine_density is treated as linear spine density [um]
            if True  spine_density is treated as area density [um2]
        :return:
            list of added spine heads
        """

        secs = self.filter_secs(obj_filter=lambda o: o.name.startswith(region),
                                as_list=True)
        self.add_spines_section_list(secs, spine_density, spine_type, **kwargs)

        return secs


    def add_spines_section_list(self, sections, spine_density,
                                spine_type="generic", **kwargs):
        """
        Add spines with specified linear density (per 1 um) to specified
        secions (compartments). Spines can have
        a predifined type (stubby, thin, mushroom) or, alternatively, their
        dimentions (head_diam, head_len, neck_diam, neck_len) can be specified
        in kwargs.

        :param regions:
            Section that will have spines
        :param spine_density:
            spine density 
        :param spine_type:
            Spine type. There are four predifined types: thin, stubby,
            mushroom and other.
        :param **kwargs:
            See below

        Keyword arguments:
        :spine name:
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
        :seed: None
            seed for the random number generator used for picking out
            spine positions
        :g_pas:
            pas conductance. By default g_pas of the parent section
            will be used.
        :E_pas:
            pas reversal potential. By default pas reversal potential
            of the parent section will be used.
        :r_m:
            membrane resistivity. By default 1/pas conductance of the
            parent section will be used.
        :r_a:
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
        spine_name = kwargs.pop("spine_name", spine_type)
        head_diam = kwargs.pop("head_diam", spine_dimensions["head_diam"])
        head_len = kwargs.pop("head_len", spine_dimensions["head_len"])
        neck_diam = kwargs.pop("neck_diam", spine_dimensions["neck_diam"])
        neck_len = kwargs.pop("neck_len", spine_dimensions["neck_len"])
        #If Falde
        spine_E_pas = kwargs.pop("spine_E_pas", None)
        spine_g_pas = kwargs.pop("spine_g_pas", None)
        spine_rm = kwargs.pop("spine_rm", None)
        spine_ra = kwargs.pop("spine_ra", None)
        spine_cm = kwargs.pop("spine_cm", None)
        add_pas = kwargs.pop("add_pas", False)
        if isinstance(spine_rm, int) or isinstance(spine_rm, float):
            spine_g_pas = 1/spine_rm
        area_density = kwargs.pop("area_density", False)
        seed = kwargs.pop("seed", None)
        if seed is not None:
            np.random.seed(seed)

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
            self._add_spines_to_section_with_location(sec, spine_name,
                                                      spine_number,
                                                      head_diam, head_len,
                                                      neck_diam, neck_len,
                                                      E_pas, g_pas,
                                                      ra, cm, u_random=seed,
                                                      add_pas=add_pas)


    def _add_spines_to_section_with_location(self, section, spine_name,
                                             n_spines, head_diam,
                                             head_len, neck_diam,
                                             neck_len, E_pas,
                                             g_pas, ra, cm, u_random=None,
                                             add_pas=True):
        """
        Add spines to a section of a dedrite. There are two possibilities:
        1) spines are added uniformly every n_spines/section_length,
        2) spines positions on the dendrite's section are drawn
        from the uniform distribution.
        
        :param section:
           section
        :param spine_name:
           string attached to name of every head and neck
        :param n_spines:
           number of spines
        :param head_diam:
           diameter of the spine head
        :param head_len:
           length of the spine_head
        :param neck_diam:
           diameter of the neck
        :param neck_len:
           length of the neck
        :param add_pas:
           add passive mechanism
        :param u_random:
           if int draw spine position from the uniform distribution
        """
        if not isinstance(section, Sec):
            section = Sec(section)
        if isinstance(u_random, int):
            target_locations = np.random.uniform(0., 1., n_spines).tolist()
        else:
            target_locations = np.linspace(0., .99, n_spines).tolist()

        self._add_spines_to_section(section, spine_name,
                                    target_locations, head_diam,
                                    head_len, neck_diam, neck_len,
                                    E_pas, g_pas, ra, cm,
                                    add_pas=add_pas)
        return target_locations

    def _add_spines_to_section(self, section, spine_name,
                               target_location, head_diam,
                               head_len, neck_diam, neck_len,
                               E_pas, g_pas, ra, cm, add_pas=True):
        name = section.name
        if not isinstance(target_location, list):
            target_location = [target_location]
        for i, location in enumerate(target_location):
            head = self.add_sec(name="%s_%s_head[%d]" % (name, spine_name, i),
                                diam=head_diam, l=head_len, nseg=2,
                                E_rest=E_pas, ra=ra, cm=cm,
                                g_pas=g_pas, add_pas=add_pas)
            neck = self.add_sec(name="%s_%s_neck[%d]" % (name, spine_name, i),
                                diam=neck_diam, l=neck_len, nseg=1,
                                E_rest=E_pas, ra=ra, cm=cm,
                                g_pas=g_pas, add_pas=add_pas)
            self.heads.append(head)
            self.necks.append(neck)
            self.connect_secs(source=head, target=neck, source_loc=1.0,
                              target_loc=0.0)
            self.connect_secs(source=neck, target=section, source_loc=location,
                              target_loc=0.0)



    def find_sections_with_mech(self, mech_name, spine_names=["head", "neck"]):
        mech_dend_loc = {}
        all_spines = []
        for name in spine_names:
            all_spines.extend(self.filter_secs(name, as_list=True))

        for spine in all_spines:
            mechanisms = spine.hoc.psection()["density_mechs"]
            if mech in mechanisms.keys():
                parent = Sec(h.SectionRef(sec=neck.hoc).parent)
                if mech in parent.hoc.psection()["density_mechs"]:
                    if parent not in mech_dend_loc:
                        mech_dend_loc[parent] = [spine]
                    else:
                        mech_dend_loc[parent].append(spine)
        return mech_dend_loc

    def compensate(self, mechs_with_gbar_name, cm_adjustment=True):
        """mechs_with_gbar_name needs to be a double list
        """
        assert len(mechs_with_gbar_name) == 2
        assert isinstance(mechs_with_gbar_name[0], list)
        assert isinstance(mechs_with_gbar_name[1], list)
        assert len(mechs_with_gbar_name[1]) == len(mechs_with_gbar_name[0])

        for mech, gbar in mechs_with_gbar_name:
            mech_loc = self.find_sections_with_mech(mech)
            for dend in mech_loc.keys():
                gbar_val = dend.hoc.psection()["density_mechs"][mech][gbar]
                area_dend = dend.hoc.L*dend.hoc.diam*np.pi
                spine_list = mech_loc[dend]
                cum_spine_area = get_area(spine_list)
                new_val = gbar_val*(area_dend-cum_spine_area)/area_dend
                mech_obj = getattr(dend, mech)
                setattr(mech_obj, gbar, new_val)
                print("Setting %s %s in %s to %f" % (dend.hoc.name(),
                                                     mech, gbar, new_val))

        if cm_adjustment:
            #get all spines
            #get all dendrites
            #for each dendrite adjust by cumulative spine area
            pass
