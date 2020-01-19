from neuron import h


def get_netstim(start, number, interval, noise):
    stim = h.NetStim()
    stim.start = start
    stim.number = number
    stim.interval = interval
    stim.noise = noise
    return stim


def get_vecstim(ping_array):
    stim = h.VecStim()
    vec = h.Vector(ping_array)
    stim.play(vec)

    return stim, vec


def make_conn(source, target, source_sec=None, delay=None, weight=None, threshold=None):
    if source_sec is None:
        con = h.NetCon(source, target)
    else:
        con = h.NetCon(source, target, sec=source_sec)
    if delay:
        con.delay = delay
    if weight:
        con.weight[0] = weight
    if threshold:
        con.threshold = threshold
    return con
