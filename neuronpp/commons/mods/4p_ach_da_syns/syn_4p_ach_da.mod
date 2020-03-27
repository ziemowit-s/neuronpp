COMMENT
  Implementation of a four-pathway phenomenological synaptic plasticity rule
  See Ebner et al. (2019)
  https://doi.org/10.1016/j.celrep.2019.11.068
ENDCOMMENT
  
  NEURON {
  	POINT_PROCESS Syn4PAChDa
  	: Pointers for ACh and DA synapses
  	POINTER ACh_w
  	POINTER Da_w
  	POINTER flag_D_ACh
  	POINTER flag_D_Da

  	POINTER last_max_w_ACh
  	POINTER last_max_w_Da

  	:ACh/DA params
  	RANGE ACh, ACh_tau, A_ACh, stdp_ach, ach_stdp
  	RANGE Da, Da_tau, A_Da, stdp_da, da_stdp

  	: Parameters & variables of the original Exp2Syn
  	RANGE tau_a, tau_b, e, i

  	NONSPECIFIC_CURRENT i

  	: Parameters & variables of the plasticity rule
  	RANGE A_LTD_pre, A_LTP_pre, A_LTD_post, A_LTP_post
  	RANGE tau_G_a, tau_G_b, m_G
  	RANGE w_pre, w_post, w_pre_init, w_post_init, w
  	RANGE s_ampa, s_nmda

  	RANGE tau_u_T, theta_u_T, m_T
  	RANGE theta_u_N, tau_Z_a, tau_Z_b, m_Z, tau_N_alpha, tau_N_beta, m_N_alpha, m_N_beta, theta_N_X
  	RANGE theta_u_C, theta_C_minus, theta_C_plus, tau_K_alpha, tau_K_gamma, m_K_alpha, m_K_beta, s_K_beta

  	RANGE E, LTD_pre, LTP_pre, LTD_post, LTP_post
  }

  UNITS {
  	(nA) = (nanoamp)
  	(mV) = (millivolt)
  	(uS) = (microsiemens)
  }

  PARAMETER {
    ACh_tau = 50 (ms) <1e-9, 1e9>
    Da_tau = 50 (ms) <1e-9, 1e9>

    A_ACh = 1e-4 : amplitude of ACh
    A_Da = 1e-4 : amplitude of Da

  	: Parameters of the original Exp2Syn
  	tau_a = 0.2 (ms) <1e-9,1e9>			: time constant of EPSP rise // used for AMPAR currents
  	tau_b = 2 (ms) <1e-9,1e9>			: time constant of EPSP decay
  	e = 0 (mV)							: reversal potential

  	w_pre_init = 0.5					: pre factor initial value
  	w_post_init = 2.0					: post factor initial value

  	s_ampa = 0.5						: contribution of AMPAR currents
  	s_nmda = 0.5						: contribution of NMDAR currents

  	: Parameters of the plasticity rule
  	tau_G_a = 2 (ms) <1e-9,1e9>			: time constant of presynaptic event G (rise) // also used for NMDAR currents
  	tau_G_b = 50 (ms) <1e-9,1e9>		: time constant of presynaptic event G (decay)
  	m_G = 10							: slope of the saturation function for G

  	A_LTD_pre = 8.5e-7					: amplitude of pre-LTD
  	A_LTP_pre = 8.5e-7					: amplitude of pre-LTP
  	A_LTD_post = 3.6e-7					: amplitude of post-LTD
  	A_LTP_post = 5.5e-5					: amplitude of post-LTP

  	tau_u_T = 10 (ms) <1e-9,1e9>		: time constant for filtering u to calculate T
  	theta_u_T = -60						: voltage threshold applied to u to calculate T
  	m_T = 1.7							: slope of the saturation function for T

  	theta_u_N = -30						: voltage threshold applied to u to calculate N
  	tau_Z_a = 1	(ms) <1e-9,1e9>			: time constant of presynaptic event Z (rise)
  	tau_Z_b = 15 (ms) <1e-9,1e9>		: time constant of presynaptic event Z (decay)
  	m_Z = 6								: slope of the saturation function for Z
  	tau_N_alpha = 7.5 (ms) <1e-9,1e9>	: time constant for calculating N-alpha
  	tau_N_beta = 30	(ms) <1e-9,1e9>		: time constant for calculating N-beta
  	m_N_alpha = 2						: slope of the saturation function for N_alpha
  	m_N_beta = 10						: slope of the saturation function for N_beta
  	theta_N_X = 0.2						: threshold for N to calculate X

  	theta_u_C = -68						: voltage threshold applied to u to calculate C
  	theta_C_minus = 15					: threshold applied to C for post-LTD (P activation)
  	theta_C_plus = 35					: threshold applied to C for post-LTP (K-alpha activation)
  	tau_K_alpha = 15 (ms) <1e-9,1e9>	: time constant for filtering K_alpha to calculate K_alpha_bar
  	tau_K_gamma = 20 (ms) <1e-9,1e9>	: time constant for filtering K_beta to calculate K_gamma
  	m_K_alpha = 1.5						: slope of the saturation function for K_alpha
  	m_K_beta = 1.7						: slope of the saturation function for K_beta
  	s_K_beta = 100						: scaling factor for calculation of K_beta

  	LTD_pre = 0
  	LTP_pre = 0
  	LTD_post = 0
  	LTP_post = 0
  }

  ASSIGNED {
  	v (mV)
  	i (nA)
  	g (uS)
  	g_ampa (uS)
  	g_nmda (uS)
  	epsilon
  	epsilon_G
  	epsilon_Z
  	C
  	T
  	G
  	E
  	P
  	K_alpha
  	Rho
  	K_beta
  	K
  	N
  	X
  	Z
  	flag_D
  	w_pre
  	w_post
  	w
  	A_n
  	B_n
  	last_weight

    ACh_w
    Da_w
  	flag_D_ACh
  	flag_D_Da
  	last_max_w_ACh
  	last_max_w_Da
  }

  STATE {
  	A (uS)
  	B (uS)

  	Da (uS)
  	stdp_da (uS)
  	da_stdp (uS)

  	ACh (uS)
  	stdp_ach (uS)
  	ach_stdp (uS)

  	G_a
  	G_b
  	u_bar
  	K_alpha_bar
  	K_gamma
  	Z_a
  	Z_b
  	N_alpha_bar
  	N_beta_bar
  }

  INITIAL {
  	LOCAL omega, omega_G, omega_Z
  	g = 0
  	g_ampa = 0
  	g_nmda = 0
  	u_bar = 0
  	K_alpha_bar = 0
  	K_gamma = 0
  	flag_D = -1
  	N_alpha_bar = 0
  	N_beta_bar = 0
  	w_pre = w_pre_init
  	w_post = w_post_init
  	w = w_pre * w_post
  	last_weight = 0

  	Da = 0
  	stdp_da = 0
  	da_stdp = 0

  	ACh = 0
  	stdp_ach = 0
  	ach_stdp = 0

  	: Calculations taken from the original Exp2Syn
  	: AMPAR-EPSP
  	if (tau_a/tau_b > .9999) {
  		tau_a = .9999*tau_b
  	}
  	A = 0
  	B = 0
  	omega = (tau_a*tau_b)/(tau_b - tau_a) * log(tau_b/tau_a)
  	epsilon = -exp(-omega/tau_a) + exp(-omega/tau_b)
  	epsilon = 1/epsilon

  	: G
  	if (tau_G_a/tau_G_b > .9999) {
  		tau_G_a = .9999*tau_G_b
  	}
  	G_a = 0
  	G_b = 0
  	omega_G = (tau_G_a*tau_G_b)/(tau_G_b - tau_G_a) * log(tau_G_b/tau_G_a)
  	epsilon_G = -exp(-omega_G/tau_G_a) + exp(-omega_G/tau_G_b)
  	epsilon_G = 1/epsilon_G

  	: Z
  	if (tau_Z_a/tau_Z_b > .9999) {
  		tau_Z_a = .9999*tau_Z_b
  	}
  	Z_a = 0
  	Z_b = 0
  	omega_Z = (tau_Z_a*tau_Z_b)/(tau_Z_b - tau_Z_a) * log(tau_Z_b/tau_Z_a)
  	epsilon_Z = -exp(-omega_Z/tau_Z_a) + exp(-omega_Z/tau_Z_b)
  	epsilon_Z = 1/epsilon_Z
  }

  BREAKPOINT {
  	SOLVE state METHOD cnexp
  	G = sigmoid_sat(m_G, G_b - G_a)			: G presynaptic signal
  	Z = sigmoid_sat(m_Z, Z_b - Z_a)			: Z presynaptic signal

  	g_ampa = s_ampa * w_post * (B - A)							: AMPAR conductance
  	g_nmda = s_nmda * w_post_init * (B_n - A_n) * mgblock(v)	: NMDAR conductance

  	g = w_pre * (g_ampa + g_nmda)			: average conductance, as w_pre is not actually modeled as a probability
  	i = g * (v - e)
  }

  DERIVATIVE state {
  	LOCAL D, u, Eta, g_update, N_alpha, N_beta, N

    : if Hebbian
  	if(flag_D == 1) {
  		D = 1
  	    flag_D = -1
  	    if(ach_stdp > 0) {
  	        ACh = ach_stdp * w
  	        ach_stdp = 0
  	    } else {
  	        stdp_ach = 1
  	    }
  	    if(da_stdp > 0){
  	        Da = da_stdp * w
  	        da_stdp = 0
  	    } else {
  	        stdp_da = 1
  	    }
  	}
  	else {
  	    D = 0
  	}

    : If ACh
	if(flag_D_ACh == 1) {
  	    flag_D_ACh = -1

  	    if(stdp_ach > 0){
  	        ACh = stdp_ach * ACh_w * w
  	        stdp_ach = 0
  	        ach_stdp = 0
        } else {
            ach_stdp = ACh_w
        }
        ACh_w = 0
  	}

  	: If Da
  	if(flag_D_Da == 1) {
  	    flag_D_Da = -1

  	    if(stdp_da > 0){
  	        Da = stdp_da * Da_w * w
  	        stdp_da = 0
  	        da_stdp = 0
        } else {
            da_stdp = Da_w
        }
        Da_w = 0
  	}


    : Ensures that ACh/Da are between 0 and 1
    if(ACh > 1.0) {
  		ACh = 1.0
  	}
  	if(ACh < 0.0) {
  		ACh = 0.0
  	}
    if(Da > 1.0) {
  		Da = 1.0
  	}
  	if(Da < 0.0) {
  		Da = 0.0
  	}

  	UNITSOFF
  	u = v		: read local voltage
  	Eta = dt	: learning rate
  	UNITSON

    stdp_ach' = -stdp_ach/ACh_tau
    ach_stdp' = -ach_stdp/ACh_tau
    ACh' = -ACh/ACh_tau

    stdp_da' = -stdp_da/Da_tau
    da_stdp' = -da_stdp/Da_tau
    Da' = -Da/Da_tau

  	: Calculations for pre-LTD
  	u_bar' = (- u_bar + positive(u - theta_u_T)) / tau_u_T
  	T = sigmoid_sat(m_T, u_bar)  : between -1 and 1: 2/(1+m_T**-u_bar)-1 [-1 move down to -1; 2: move up to 1]

  	: Calculations for pre-LTP
  	N_alpha_bar' = (- N_alpha_bar + positive(u - theta_u_N)) / tau_N_alpha
  	N_beta_bar'	= (- N_beta_bar + N_alpha_bar) / tau_N_beta
  	N_alpha = sigmoid_sat(m_N_alpha, N_alpha_bar)
  	N_beta = sigmoid_sat(m_N_beta, N_beta_bar)
  	N = positive(N_alpha * N_beta - theta_N_X)
  	X = Z * N

  	: Calculations for post-LTD
  	C = G * positive(u - theta_u_C)
  	P = positive(C - theta_C_minus) * positive(theta_C_plus - C) / pow((theta_C_plus - theta_C_minus) / 2, 2)

  	: Calculations for post-LTP
  	K_alpha = sigmoid_sat(m_K_alpha, positive(C - theta_C_plus)) * Rho
  	K_alpha_bar' = (- K_alpha_bar + K_alpha) / tau_K_alpha
  	K_beta = sigmoid_sat(m_K_beta, (K_alpha_bar * s_K_beta))
  	Rho = 1.0 - K_beta
  	K_gamma' = (- K_gamma + K_beta) / tau_K_gamma
  	K = K_alpha * K_beta * K_gamma

  	: Pathway outcomes
  	LTP_pre	= A_LTP_pre * X * Eta			: apply Eta to make values invariant to changes in dt
  	LTD_post = - A_LTD_post * P * Eta

    : ACh acts on LTD_pre; DA blocks LTD_pre
    : DA acts on LTP_post; ACh has no effect on LTP_post

    E = D * T
    LTD_pre  = - (A_LTD_pre  * E) - (A_ACh * ACh * (last_max_w_Da-Da)/last_max_w_Da * Eta): Eta only for ACh/Da
  	LTP_post =   ( (A_LTP_post * K) + (A_Da * Da) ) * Eta : Eta for all params

  	: Update weights
  	w_pre = w_pre + LTD_pre + LTP_pre
  	if(w_pre > 1.0) {
  		w_pre = 1.0
  	}
  	if(w_pre < 0.0) {
  		w_pre = 0.0
  	}
  	w_post = w_post + LTD_post + LTP_post
  	if(w_post > 5.0) {
  		w_post = 5.0
  	}
  	if(w_post < 0.0) {
  		w_post = 0.0
  	}
  	w = w_pre * w_post
  
  	A' = -A / tau_a
  	B' = -B / tau_b
  	G_a' = -G_a / tau_G_a
  	G_b' = -G_b / tau_G_b
  	A_n = G_a * last_weight	: use time course of the G signal to model NMDAR activation
  	B_n = G_b * last_weight
  	Z_a' = -Z_a / tau_Z_a
  	Z_b' = -Z_b / tau_Z_b
  }
  
  NET_RECEIVE(weight (uS)) {
  	: printf(\Received weight = %f at t = %f\\, weight, t)
  	A = A + weight * epsilon	: AMPAR component
  	B = B + weight * epsilon
  	G_a = G_a + epsilon_G
  	G_b = G_b + epsilon_G
  	Z_a = Z_a + epsilon_Z
  	Z_b = Z_b + epsilon_Z
  	flag_D = 1
  	last_weight = weight	: used to scale NMDAR component
  }
  
  FUNCTION positive(value) {	: rectification function
  	if(value < 0) {
  		positive = 0
  	}
  	else {
  		positive = value
  	}
  }

  : between -1 and 1
  FUNCTION sigmoid_sat(slope, value) {	: sigmoidal saturation
  	sigmoid_sat = 2.0 / (1.0 + pow(slope, -value)) - 1.0 : [-1 move down to -1; 2: move up to 1]
  }
  
  FUNCTION mgblock(v(mV)) {	: Mg2+ block
  	LOCAL u
  	UNITSOFF
  	u = v
  	UNITSON
  	: Modified from Jahr & Stevens (1990)
  	mgblock = 1 / (1 + exp(0.080 * -u) * (1.0 / 3.57))
  }