import matplotlib.pyplot as plt

from neuronpp.cells.cell import Cell
from neuronpp.utils.record import Record
from neuronpp.utils.run_sim import RunSim

if __name__ == '__main__':
    # Prepare cell
    cell = Cell("cell", compile_paths='../commons/mods/sigma3syn')
    soma = cell.add_sec("soma", diam=20, l=20, nseg=10)
    cell.insert('pas')
    cell.insert('hh')

    syn = cell.add_sypanse(source=None, weight=0.01, seg=soma(0.5), mod_name="Sigma3Exp2Syn")

    # prepare plots and spike detector
    rec_v = Record(soma(0.5), variables="v")
    rec_w = Record(syn, variables="w")

    # run
    sim = RunSim(init_v=-65, warmup=5)
    syn.make_event(5)
    sim.run(runtime=20)

    # plot
    rec_w.plot()
    rec_v.plot()
