TITLE Calcium dependent potassium channel (small conductance SK)
 
UNITS {
        (molar) = (1/liter)
        (mV) =	(millivolt)
        (S)  =  (siemens)
	      (mA) =	(milliamp)
	      (mM) =	(millimolar)
}

NEURON {
	SUFFIX kcas
	USEION ca READ cai
	USEION k WRITE ik
	RANGE  gk,gbar,km,oinf,ik,n,otau
}


PARAMETER {
        cai (mM) 
        gbar  (S/cm2)
        gk  (S/cm2)
        ek = -90      (mV)
        km = 0.00019   (mM)
        n  = 4.0       (1)
        otau=28	(ms)

}

ASSIGNED {
	v	(mV)
	ik	(mA/cm2)
	oinf  (1)         
}


BREAKPOINT {
	SOLVE states METHOD cnexp
	if (cai>0) {
	  oinf = 1/(1 + pow(km/cai,n))
	} else {
	 oinf=0
	 }
     :ik = oinf*gbar*(v - ek)
    ik = o*gbar*(v - ek)
    gk = o*gbar
 }

STATE { o <1e-4>}

INITIAL {
	o = 1/(1 + pow(km/cai,n))
}

UNITSOFF
DERIVATIVE states {
     if (cai>0) {
	   oinf = 1/(1 + pow(km/cai,n))
	 }  else {
	 oinf=0
	 }
     o'  = (oinf-o)/otau
}
UNITSON
