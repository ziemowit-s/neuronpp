COMMENT
Two state kinetic scheme synapse described by rise time tau1,
and decay time constant tau2. The normalized peak conductance is 1.
Decay time MUST be greater than rise time.

The solution of A->G->bath with rate constants 1/tau1 and 1/tau2 is
 A = a*exp(-t/tau1) and
 G = a*tau2/(tau2-tau1)*(-exp(-t/tau1) + exp(-t/tau2))
	where tau1 < tau2

If tau2-tau1 is very small compared to tau1, this is an alphasynapse with time constant tau2.
If tau1/tau2 is very small, this is single exponential decay with time constant tau2.

The factor is evaluated in the initial block
such that an event of weight 1 generates a
peak conductance of 1.

Because the solution is a sum of exponentials, the
coupled equations can be solved as a pair of independent equations
by the more efficient cnexp method.

Neuromodulatory mechanism:
---------------------------
All weights must be (0-1). To distinguish general weight, ACh and Da weights from single real value in NET_RECEIVE block
it assumes that:
* general weight is (0-1)
* ACh weight is (1-2)
* Da weight is (2-3)

Then substraction are performed to distinguish which signal is passed:
* general weight - no substraction
* ACh weight which fo distinguish purpose is substracted by ach_substractor
* Da weight which fo distinguish purpose is substracted by da_substractor

The key assumption here is Thread safety, the other approach is to use POINTER (which is not thread safe)
and artificial ionic concetration. For more info see discussion:
https://www.neuron.yale.edu/phpBB/viewtopic.php?f=31&t=4239

ENDCOMMENT

NEURON {
	POINT_PROCESS ExcSigma3Exp2SynAchDa
	RANGE tau1, tau2, e, i

	RANGE ach, ach_w, ach_tau, ach_substractor
	RANGE da, da_w, da_tau, da_substractor, last_max_da_w
	RANGE heb_ach_w, heb_da_w
	RANGE modulatory_w

	RANGE ltd, ltp, learning_slope, learning_tau
	RANGE ltd_sigmoid_half, ltp_threshold
	RANGE w, learning_w

	NONSPECIFIC_CURRENT i

	RANGE g
}

UNITS {
	(nA) = (nanoamp)
	(mV) = (millivolt)
	(uS) = (microsiemens)
}

PARAMETER {
	tau1 = 0.1 (ms) <1e-9,1e9>
	tau2 = 10 (ms) <1e-9,1e9>
	e=0	(mV)

    ltd_theshold = -60 (mV) <1e-9,1e9>
	ltp_theshold = -45 (mV) <1e-9,1e9>

    ltd_sigmoid_half = -55 (mV) <1e-9,1e9>
	ltp_sigmoid_half = -40 (mV) <1e-9,1e9>

	learning_slope = 1.3
	learning_tau = 20
	w = 1.0

	ach_tau = 10 (ms) <1e-9,1e9>
	da_tau = 10 (ms) <1e-9,1e9>
	ach_substractor = 1 <1e-9,1e9> : value to distinguish ACh stimulation
	da_substractor = 2 <1e-9,1e9> : value to distinguish Da stimulation
}

ASSIGNED {
	v (mV)
	i (nA)
	g (uS)
	factor

	ltd
	ltp
	last_max_da_w
	modulatory_w
}

STATE {
	A (uS)
	B (uS)

	ach (uS)
	da (uS)
	learning_w

	ach_w
	heb_ach_w

	da_w
	heb_da_w
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

	ach = 0
	ach_w = 0
	heb_ach_w = 0

	da = 0
	da_w = 0
	heb_da_w = 0

    modulatory_w = 0
	last_max_da_w = 1e-9 : must be initialized as nonzero
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

	learning_w = learning_w + sigmoid_sat(learning_slope, (-ltd + 2 * ltp) / learning_tau)/8000

	SOLVE state METHOD cnexp
	g = B - A
	i = g*(v - e)

    modulatory_w = (- ach * ((last_max_da_w-da)/last_max_da_w) + da)/1000
    w = w + learning_w * w + modulatory_w * w

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

	ach' = -ach/ach_tau
	da' = -da/da_tau

	ach_w' = -ach_w/ach_tau
	da_w' = -da_w/da_tau

	heb_ach_w' = -heb_ach_w/ach_tau
	heb_da_w' = -heb_da_w/da_tau
}

: All weights must be (0-1)
NET_RECEIVE(weight (uS)) {
    : Da check must be checked before ACh check and Exp2Syn check since da_substractor=2 and ach_substractor=1
    if (weight-da_substractor > 0) { : Da stim.
        da_w = weight-da_substractor
        if (da_w > 1) {
            da_w = 1
        }
        last_max_da_w = da_w

        if (heb_da_w > 0) {
            da = heb_da_w * da_w
            heb_da_w = 0
        }

    } else if (weight-ach_substractor > 0) { : ACh stim
        ach_w = weight-ach_substractor
        if (ach_w > 1) {
            ach_w = 1
        }

        if (heb_ach_w > 0) {
            ach = heb_ach_w * ach_w
            heb_ach_w = 0
        }

    } else { : Ex2Syn stim
        A = A + w*weight*factor
        B = B + w*weight*factor

        if (ach_w > 0) {
            ach = ach_w
            ach_w = 0
        }
        if (da_w > 0) {
            da = da_w
            da_w = 0
        }

        heb_ach_w = 1
        heb_da_w = 1
    }
}

: sigmoid with threshold
FUNCTION sigmoid_thr(slope, value, thr) {
    sigmoid_thr = 1 / (1.0 + pow(slope, -(value-thr)))
}

: sigmoidal saturation
FUNCTION sigmoid_sat(slope, value) {
    sigmoid_sat = 2.0 / (1.0 + pow(slope, -value)) - 1.0 : [-1 move down to -1; 2: move up to 1]
}
