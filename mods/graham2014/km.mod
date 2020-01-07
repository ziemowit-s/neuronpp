COMMENT
km.mod
Potassium channel, Hodgkin-Huxley style kinetics
Based on I-M (muscarinic K channel)
Slow, noninactivating
Author: Zach Mainen, Salk Institute, 1995, zach@salk.edu
Code updated to run with CVODE (BPG 20-8-09)
	
ENDCOMMENT

INDEPENDENT {t FROM 0 TO 1 WITH 1 (ms)}

NEURON {
	SUFFIX km
	USEION k READ ek WRITE ik
	RANGE n, gk, gbar
	RANGE ninf, ntau
	GLOBAL Ra, Rb
	GLOBAL q10, temp, tadj, vmin, vmax
}

UNITS {
	(mA) = (milliamp)
	(mV) = (millivolt)
	(pS) = (picosiemens)
	(um) = (micron)
} 

PARAMETER {
	v 		(mV)
	dt		(ms)
	gbar = 10   	(pS/um2)	: 0.03 mho/cm2
	tha  = -30	(mV)		: v 1/2 for inf
	qa   = 9	(mV)		: inf slope		
	Ra   = 0.001	(/ms)		: max act rate  (slow)
	Rb   = 0.001	(/ms)		: max deact rate  (slow)
	celsius		(degC)
	temp = 23	(degC)		: original temp 	
	q10  = 2.3			: temperature sensitivity
	vmin = -120	(mV)
	vmax = 100	(mV)
} 


ASSIGNED {
	a		(/ms)
	b		(/ms)
	ik 		(mA/cm2)
	gk		(pS/um2)
	ek		(mV)
	ninf
	ntau (ms)	
	tadj
}
 

STATE { n }

INITIAL { 
	trates(v)
	n = ninf
}

BREAKPOINT {
        SOLVE states METHOD derivimplicit
	gk = tadj*gbar*n
	ik = (1e-4) * gk * (v - ek)
} 

LOCAL nexp

DERIVATIVE states {
        rates(v)
        trates(v)
        :n = n + nexp*(ninf-n)
	n' = (ninf - n) / ntau
}

PROCEDURE trates(v) {  :Computes rate and other constants at current v.
                       :Call once from HOC to initialize inf at resting v.
        LOCAL tinc
        TABLE ninf, nexp
	DEPEND dt, celsius, temp, Ra, Rb, tha, qa
	
	FROM vmin TO vmax WITH 199

	rates(v): not consistently executed from here if usetable_hh == 1
        tadj = q10^((celsius - temp)/10)  :temperature adjastment
        tinc = -dt * tadj
        nexp = 1 - exp(tinc/ntau)
}


PROCEDURE rates(v) {  :Computes rate and other constants at current v.
                      :Call once from HOC to initialize inf at resting v.

        a = Ra * (v - tha) / (1 - exp(-(v - tha)/qa))
        b = -Rb * (v - tha) / (1 - exp((v - tha)/qa))
        ntau = 1/(a+b)
	ninf = a*ntau
}

