COMMENT
Two state kinetic scheme described by rise time tau1,
and decay time constant tau2. The normalized peak current is 1nA.
Decay time MUST be greater than rise time.

The solution of A->G->bath with rate constants 1/tau1 and 1/tau2 is
 A = a*exp(-t/tau1) and
 G = a*tau2/(tau2-tau1)*(-exp(-t/tau1) + exp(-t/tau2))
	where tau1 < tau2

If tau2-tau1 -> 0 then we have a alpha-function.
and if tau1 -> 0 then we have just single exponential decay.

The factor is evaluated in the
initial block such that an event of weight 1 generates a
peak current of 1.

Because the solution is a sum of exponentials, the
coupled equations can be solved as a pair of independent equations
by the more efficient cnexp method.

Adapted and modified from the original Exp2Syn mod file.
M.Migliore Jun 2003
ENDCOMMENT

NEURON {
	POINT_PROCESS Exp2i
	RANGE tau1, tau2, i, g
	ELECTRODE_CURRENT i

	GLOBAL total
}

UNITS {
	(nA) = (nanoamp)
}

PARAMETER {
	tau1=.1 (ms) <1e-9,1e9>
	tau2 = 10 (ms) <1e-9,1e9>
}

ASSIGNED {
	i (nA)
	g (nA)
	factor
	total (nA)
}

STATE {
	A (nA)
	B (nA)
}

INITIAL {
	LOCAL tp
	total = 0
	if (tau1/tau2 > .9999) {
		tau1 = .9999*tau2
	}
	A = 0
	B = 0
	tp = (tau1*tau2)/(tau2 - tau1) * log(tau2/tau1)
	factor = -exp(-tp/tau1) + exp(-tp/tau2)
	factor = 1/factor
}

BREAKPOINT {
	SOLVE state METHOD cnexp
	g = B - A
	i = g
}

DERIVATIVE state {
	A' = -A/tau1
	B' = -B/tau2
}

NET_RECEIVE(weight (nA)) {
	state_discontinuity(A, A + weight*factor)
	state_discontinuity(B, B + weight*factor)
	total = total+weight
}
