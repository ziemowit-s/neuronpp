import random
import numpy as np
from random import randint

from neuron import h

from neuronpp.core.cells.section_cell import SectionCell
from neuronpp.core.hocwrappers.sec import Sec
### Nomenclature and values adapted from Harris KM, Jensen FE, Tsao BE.
### J Neurosci 1992

SPINE_DIMENSIONS = {
    "mushroom_spine":  {
        "head_diam": 1.1,
        "head_len": 0.8,
        "neck_diam": 0.20,
        "neck_len": 0.43,
    },
    "thin_spine": {
        "head_diam": 0.2,
        "head_len": 0.5,
        "neck_diam": 0.1,
        "neck_len": 0.5,
    },
    "stubby_spine": {
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
        for _ in range(spine_number):
            i = self._next_index
            head = self.add_sec(name="head[%s]" % i, diam=1, l=1, nseg=head_nseg)
            neck = self.add_sec(name="neck[%s]" % i, diam=0.5, l=0.5, nseg=neck_nseg)
            self.heads.append(head)
            self.necks.append(neck)
            self.connect_secs(source=head, target=neck)
            self._connect_necks_rand_uniform(neck, secs)
            self._next_index += 1

        return self.heads, self.necks

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
        r = randint(0, max_l)
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


    def add_spines_at(self, distance_range, spine_density,
                                         spine_type, **kwargs):
        """
        Add spines with specified linear density (per 1 um) to a part
        of dendritic range specified as distance from the soma. Spines can have
        a predifined type (stubby, thin, mushroom) or, alternatively, their
        dimentions (head_diam, head_len, neck_diam, neck_len) can be specified
        in kwargs.


        :param distance_range: tuple or list 
            tuple containing begining and end of the distance range
            where spines will be added
        :param spine_density:
            Linear spine density in [um]
        :param spine_type:
            Spine type. There are four predifined types: thin, stubby,
            mushroom and other.
        :param \**kwargs:
            See below

        Keyword arguments:
        :head_diam:
            Spine head diameter
        :head_len:
            Length of the spine head
        :neck_diam:
            Spine neck diameter
        :neck_len:
            Length of the spine neck
        :seed: None
            seed for the random number generator used for picking out
            spine positions
        :return:
            list of added spine heads

        """

        soma = self.filter_secs("soma")
        secs = self.filter_secs(obj_filter=lambda o: h.distance(soma(0.0), o(1.0)) > distance_range[0]\
                         and  h.distance(soma(0.0), o(1.0)) < distance_range[1] )
        self._add_spines_to_sections(secs, spine_density, spine_type, kwargs)

    def add_spines_to_regions(self, region, spine_density, spine_type,
                               **kwargs):
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
        :param \**kwargs:
            See below

        Keyword arguments:
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
        :return:
            list of added spine heads

        """

        secs = self.filter_secs(obj_filter=lambda o: o.name.startswith(region))
        self.add_spines_to_sections(secs, spine_density, spine_type, kwargs)



    def add_spines_to_sections(self, sections, spine_density, spine_type,
                               **kwargs):
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
        :param \**kwargs:
            See below

        Keyword arguments:
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
        :return:
            list of added spine heads

        TODO: add spines with a distribution of head dimensions and
              neck dimensions
        TODO: add distribution of locations along the dendrite
        """
        try:
            spine_dimensions = SPINE_DIMENSIONS[spine_type]
        except KeyError
            spine_dimensions = SPINE_DIMENSIONS["generic"]

        head_diam = kwargs.pop("head_diam", spine_dimesions["head_diam"])
        head_len = kwargs.pop("head_len", spine_dimesions["head_len"])
        neck_diam = kwargs.pop("neck_diam", spine_dimesions["neck_diam"])
        neck_len = kwargs.pop("neck_len", spine_dimesions["neck_len"])
        area_density = kwargs.pop("area_density", False)
        for sec in sections:
            if area_density:
                area = sec.L*np.pi*sec.diam
                spine_number = int(np.round(area * spine_density))
            else:
                spine_number = int(np.round(sec.L * spine_density))
            self._add_spines_to_section(sec, spine_number, head_diam,
                              head_len, neck_diam, neck_len)
        return self.heads, self.necks

    def _add_spines_to_section(self, section, n_spines, head_diam,
                              head_len, neck_diam, neck_len):
        name = section.name()
        for i in range(n_spines):
            head = self.add_sec(name="%s_head[%d]" % (name, i),
                                diam=head_diam,
                                l=head_len, nseg=2)
            neck = self.add_sec(name="%s_neck[%d]" % (name, i),
                                diam=neck_diam,
                                l=neck_len, nseg=1)
            self.heads.append(head)
            self.necks.append(neck)
            self.connect_secs(source=head, target=neck)
            self.connect_secs(source=neck, target=sec, source_loc=1.0,
                              target_loc=i/spine_number)
