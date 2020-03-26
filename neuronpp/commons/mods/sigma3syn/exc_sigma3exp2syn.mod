COMMENT
Excitatory synapse
Default parameters assume that eq membrane potential~=-68mV

Modified version of original Exp2Syn which implements additional LTP/LTD hebbian learning.

The learnable weight of the synapse is the RANGE variable 'w', which by default is set to 1.0
ENDCOMMENT

NEURON {
	POINT_PROCESS ExcSigma3Exp2Syn
	RANGE tau1, tau2, e, i
	NONSPECIFIC_CURRENT i
	RANGE g

    RANGE ltd, ltp, learning_slope, learning_tau
	RANGE ltd_sigmoid_half, ltp_threshold
	RANGE w, learning_w
}

UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(uS) = (microsiemens)
}

PARAMETER {
	tau1 = 1 (ms) <1e-9,1e9>
	tau2 = 5 (ms) <1e-9,1e9>
	e=0	(mV)

    ltd_theshold = -60 (mV) <1e-9,1e9>
	ltp_theshold = -45 (mV) <1e-9,1e9>

    ltd_sigmoid_half = -55 (mV) <1e-9,1e9>
	ltp_sigmoid_half = -40 (mV) <1e-9,1e9>

	learning_slope = 1.3
	learning_tau = 20
	w = 1.0
}

ASSIGNED {
	v (mV)
	i (nA)
	g (uS)
	factor

	ltd
	ltp
}

STATE {
	A (uS)
	B (uS)
	learning_w
}

INITIAL {
	LOCAL tp
	if (tau1/tau2 > 0.9999) {
		tau1 = 0.9999*tau2
	}
	if (tau1/tau2 < 1e-9) {
		tau1 = tau2*1e-9
	}
	A = 0
	B = 0
	tp = (tau1*tau2)/(tau2 - tau1) * log(tau2/tau1)
	factor = -exp(-tp/tau1) + exp(-tp/tau2)
	factor = 1/factor

	ltd = 0
	ltp = 0
	learning_w = 0
}

BREAKPOINT {
    if(v-ltd_theshold > 0) {
        ltd = sigmoid_thr(learning_slope, v, ltd_sigmoid_half)
    } else {
        ltd = 0
    }
    if(v-ltp_theshold > 0) {
	    ltp = sigmoid_thr(learning_slope, v, ltp_sigmoid_half)
	} else {
	    ltp = 0
	}
	learning_w = learning_w + sigmoid_sat(learning_slope, (-ltd + 2 * ltp) / learning_tau)/5000

	SOLVE state METHOD cnexp

	g = B - A
	i = g*(v - e)

	w = w + learning_w * w

	if (w > 5) {
	    w = 5
	}
	if (w < 0) {
	    w = 0.0001
	}
}

DERIVATIVE state {
	A' = -A/tau1
	B' = -B/tau2
	learning_w' = -learning_w/4
}

NET_RECEIVE(weight (uS)) {
	A = A + w*weight*factor
	B = B + w*weight*factor
}

: sigmoid with threshold
FUNCTION sigmoid_thr(slope, value, thr) {
    sigmoid_thr = 1 / (1.0 + pow(slope, -(value-thr)))
}

: sigmoidal saturation
FUNCTION sigmoid_sat(slope, value) {
    sigmoid_sat = 2.0 / (1.0 + pow(slope, -value)) - 1.0 : [-1 move down to -1; 2: move up to 1]
}

: rectification function
FUNCTION relu(value) {
	if(value < 0) {
		relu = 0
	}
	else {
		relu = value
	}
}