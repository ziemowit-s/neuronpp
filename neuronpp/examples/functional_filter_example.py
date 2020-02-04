from neuron import h
from neuronpp.cells.cell import Cell

cell = Cell("cell")
cell.load_morpho(filepath='../commons/morphologies/asc/cell1.asc')

soma = cell.filter_secs("soma")[0]
# Filter sections by distance to the soma (return only those distance > 1000 um)
far_secs = cell.filter_secs(hoc=lambda s: h.distance(soma.hoc(0.5), s(0.5)) > 1000)

distances = [(h.distance(soma.hoc(0.5), s.hoc(0.5)), s.name) for s in far_secs]
print(len(far_secs))
for d in distances:
    print(d)
