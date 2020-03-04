from neuronpp.cells.cell import Cell
from neuronpp.utils.record import Record
from neuronpp.utils.run_sim import RunSim
import matplotlib.pylab as plt

if __name__ == '__main__':
    # Prepare cell
    cell = Cell("cell", compile_paths='../commons/mods/sigma3syn')
    soma = cell.add_sec("soma", diam=20, l=20, nseg=10)
    cell.insert('pas')
    cell.insert('hh')

    w = 0.003  # LTP
    #w = 0.0022  # LTD
    syn = cell.add_synapse(source=None, netcon_weight=w, seg=soma(0.5), mod_name="ExcSigma3Exp2SynAchDa")
    pp = syn.point_process
    ach_netcon = cell.add_netcon(source=None, point_process=pp,
                                 netcon_weight=0.1+pp.hoc.ach_substractor, delay=1)
    da_netcon = cell.add_netcon(source=None, point_process=syn.point_process,
                                netcon_weight=0.1+pp.hoc.da_substractor, delay=1)
    # prepare plots and spike detector
    rec_v = Record(soma(0.5), variables="v")
    rec_w = Record(syn, variables="w")

    # run
    sim = RunSim(init_v=-68, warmup=5)
    syn.make_event(5)
    da_netcon.make_event(7)

    syn.make_event(50)
    ach_netcon.make_event(52)
    sim.run(runtime=100)

    # plot
    rec_w.plot()
    rec_v.plot()
    plt.show()
