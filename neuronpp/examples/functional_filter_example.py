import os

from neuron import h
from neuronpp.cells.cell import Cell

path = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(path, "..",
                        "commons/morphologies/asc/cell1.asc")
cell = Cell("cell")
cell.load_morpho(filepath=filepath)
soma = cell.filter_secs("soma")

# Filter sections by distance to the soma (return only those distance > 1000 um)
far_secs = cell.filter_secs(hoc=lambda s: h.distance(soma(0.5).hoc, s(0.5)) > 1000)

# Create a list of distances to check if it works well
distances = [(h.distance(soma(0.5).hoc, s(0.5).hoc), s.name) for s in far_secs]

# Print results
print(len(far_secs))
for d in distances:
    print(d)
