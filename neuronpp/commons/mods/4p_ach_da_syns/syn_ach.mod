  NEURON {
      POINT_PROCESS SynACh
      RANGE w, last_max_w, flag_D
  }

  UNITS {
      (nA) = (nanoamp)
      (mV) = (millivolt)
      (uS) = (microsiemens)
  }

  ASSIGNED {
    flag_D
    last_max_w
    w (uS)
  }

  INITIAL {
      last_max_w = 1e-9 : must be nonzero for 4p synapse
      flag_D = -1
  }

  NET_RECEIVE(weight (uS)) {
    w = weight
    last_max_w = weight
    flag_D = 1
  }