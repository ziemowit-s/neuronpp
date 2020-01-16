from neuron import h


def make_shape_plot(variable=None, min_val=-70, max_val=40):
    ps = h.PlotShape(True)
    if variable:
        ps.variable(variable)
        ps.scale(min_val, max_val)
    ps.show(0)
    h.fast_flush_list.append(ps)
    ps.exec_menu('Shape Plot')
    return ps


def connect_net_stim(syn, weight, delay):
    stim = h.NetStim()
    con = h.NetCon(stim, syn)
    con.delay = delay
    con.weight[0] = weight
    return stim, con

