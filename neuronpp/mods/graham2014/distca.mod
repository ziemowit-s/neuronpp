TITLE ...just to store peak calcium conc.
: BPG 3-4-11, adapted from distr.mod by M.Migliore June 2001

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)

}

PARAMETER {
	v (mV)
}


NEURON {
	SUFFIX dca
	USEION ca READ cai	
        RANGE camax
}

PARAMETER {
	cai		(mM)
}

ASSIGNED {
	camax
}

INITIAL {
	camax=cai
}


BREAKPOINT {
	if (cai>camax) {camax=cai}
}
