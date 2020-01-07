: "Standard" NMDA model
: Dual exponential, with voltage-dependent max conductance
: A fraction of the current is carried by calcium
: BPG 22-8-11

TITLE nmda synapse 

NEURON {
	POINT_PROCESS NMDAca
	NONSPECIFIC_CURRENT i
	USEION ca READ eca WRITE  ica
        RANGE g,a,b,gNMDAmax,tcon,tcoff,enmda, mgconc, eta, gamma
        RANGE fCa,i,ica
}

UNITS {
        (uS) = (microsiemens)
        (nA) = (nanoamp)
        (mV) = (millivolt)
}

PARAMETER {
	fCa = 1.0	: fraction of current is calcium (BPG)
	tcon = 3 (ms)
	tcoff = 150 (ms)
	enmda = 0 	(mV)
	gNMDAmax = 1	(uS)
	mgconc = 1	(mM)	: magnesium concentration
	eta = 0.33	(/mM)
	gamma = 0.06	(/mV)
}

ASSIGNED {
	eca	(mV)
	v 	(mV)
	i	(nA)
	ica	(nA)
	g       (uS)
	factor
}

INITIAL { 
   LOCAL tp
   a=0  
   b=0 
:   factor=tcon*tcoff/(tcoff-tcon)
   tp = (tcon*tcoff)/(tcoff - tcon) * log(tcoff/tcon)
   factor = -exp(-tp/tcon) + exp(-tp/tcoff)
   factor = 1/factor
}

STATE {
      a
      b
}

BREAKPOINT {
	LOCAL s
	SOLVE states METHOD derivimplicit
	s = 1.0/(1+eta*mgconc*exp(-gamma*v))
        g = b-a
	i = (1-fCa)*gNMDAmax*g*s*(v-enmda)
	ica = fCa*gNMDAmax*g*s*(v-enmda)
}

DERIVATIVE states {
	a' = -a/tcon
	b' = -b/tcoff
}

NET_RECEIVE(wgt) {
        LOCAL x
	x=wgt*factor
	state_discontinuity(a,a+x)
	state_discontinuity(b,b+x)
}
