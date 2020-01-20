TITLE Ca R-type channel with high threshold for activation

: HVA calcium channels are inserted in the spine head
: Activation and inactivation parameters taken from
: Foehring RC, Mermelstein PG, Song W, Ulrich S and Surmeier DJ
: Unique properities of R-type calcium currents in neucortical and neostriatal neurons
: J Neurophysiol (2000) 84: 2225 - 2236
:
: written by Lei Tian on 04/11/06
: As used by Holbro et al PNAS 107:15975-15980, 2010 (BPG)
: Parameters made available through hoc (BPG)

NEURON {
	SUFFIX carF
	USEION ca  WRITE ica
        RANGE gcabar, m, h, g, p, eca
	RANGE inf, fac, vha, ka, ta, vhi, ki, ti
	RANGE irtype
}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
}

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

PARAMETER {	: parameters that can be entered when function is called in cell-setup
    	v               (mV)
    	celsius = 30	(degC)
	dt              (ms)
    	gcabar = 0.351  (mho/cm2) : initialized conductance 
	eca = 10	(mV)      : Ca++ reversal potential was choosen to best fit the GHK between -40 and -10 mV	
	vha = -14	(mV)	: half activation voltage (BPG)
	ka = -6.7	(1)	: activation slope (BPG)
	ta = 3.6	(ms)	: activation time constant (BPG)
	vhi = -65	(mV)	: half inactivation voltage (BPG)
	ki = 11.8	(1)	: inactivation slope (BPG)
	ti = 200	(ms)	: inactivation time constant (BPG)
}  

STATE {	m h }               

ASSIGNED {                  
	ica             (mA/cm2)
    	inf[2]
	fac[2]
	tau[2]
	irtype
	g                       :R_type channel total conductance
	p
	
}

BREAKPOINT {
	SOLVE states METHOD derivimplicit
	ica = gcabar*m*m*m*h*(v - eca)
	irtype= -ica
	}

INITIAL {
    	m = 0                               : initial activation parameter value
	h = 0.5                             : initial inactivation parameter value
	states()
	ica = gcabar*m*m*m*h*(v - eca)      : initial Ca++ current value
    	irtype=-ica 				: the ca current through R_type channel
	}

DERIVATIVE states {
	mhn(v*1(/mV))
	m' = (inf[0] - m) / tau[0]
	h' = (inf[1] - h) / tau[1]
}

FUNCTION varss(v, i) {
	if (i==0) {
           varss = 1 / (1 + exp((v-vha)/(ka)))	: Ca activation
	}
	else if (i==1) {    
        varss = 1/ (1 + exp((v-vhi)/(ki)))     : Ca inactivation
	}
}

FUNCTION vartau(v, i) {
	if (i==0) {
           vartau = ta		: activation variable time constant 
        }
	else if (i==1) {
           vartau = ti		: inactivation variable time constant 
       }
	
}	

PROCEDURE mhn(v) {LOCAL a, b :rest = -70
:	TABLE inf, fac DEPEND dt, celsius FROM -100 TO 100 WITH 200
	FROM i=0 TO 1 {
		tau[i] = vartau(v,i)
		inf[i] = varss(v,i)
:		fac[i] = (1 - exp(-dt/tau[i]))
	}
}


