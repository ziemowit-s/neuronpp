  NEURON {
      POINT_PROCESS SynDa
      RANGE w, last_max_w, tau, flag_D
  }

  UNITS {
      (nA) = (nanoamp)
      (mV) = (millivolt)
      (uS) = (microsiemens)
  }

  PARAMETER {
      tau = 400 (ms) <1e-9, 1e9>
  }

  ASSIGNED {
    flag_D
    last_max_w
  }

  STATE {
      w (uS)
  }

  INITIAL {
      w = 0
      last_max_w = 1e-9 : must be nonzero for 4p synapse
      flag_D = -1
  }

  BREAKPOINT {
    SOLVE state METHOD cnexp
  }

  DERIVATIVE state {
    : Check if there is a presynaptic event
    if(flag_D == 1) {
  	    flag_D = -1
  	}

  	w' = -w/tau
  }

  NET_RECEIVE(weight (uS)) {
    w = 1 * weight
    last_max_w = weight
    flag_D = 1
  }