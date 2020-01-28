Neuron++ wraps NEURON (http://www.neuron.yale.edu) with easy to use Python objects.

## Key features

  * Fast prototyping environment to use NEURON with Python with OOP paradigm in the first place.

  * Precisely define models of a single cell and connect them together to create a small network.
  
  * Perform tidius tasks in a single line of code, eg.: 
    * Manage synaptic signaling
    * Dendritic spines creation
    * Defining experimental protocols (eg. STDP paradigms)
  
  * Provide helpful exception messages and guidelines of how to use NEURON functions without errors
    
This is a pre-Alpha version

## Prerequisites

* Install NEURON from the instruction: https://github.com/ziemowit-s/neuron_netpyne_get_started
* Install requirements.txt

## Repository

https://github.com/ziemowit-s/neuronpp

## Installation

* Locally:
```bash
python setup.py bdist_wheel
```

* Through pip and GitHub:
```bash
pip install git+https://github.com/ziemowit-s//neuronpp
```
* Bear in mind that if you install the library through the pip and you want to use provided model cells (from other publications) you need to copy commons/ folder from this repository to your working directory.

## MOD compilation
Before run you must compile mod files of your model (if it provides specialised mod features)

### Automatic (recommended)
`Cell()` object has a `compile_path` param which allows to specify paths which contain mod files to compile.

In most cases you don't need to compile files externally, if you provided appropriate pathways - it will be done automatically before each run.

### Manual

If you want to compile mods manually this is how to do it:

```bash
nrmivmodl
```

* To help with manual compilation use compile_mod.py or CompileMOD class:

  * It will compile all mods inside the source folder (you can specify many source folders)
  * copy compiled folder to the `compiled/` folder inside the target folder 
  
 ```bash
 python utils/compile_mod.py --sources [SOURCE_FOLDER_WITH_MOD_FILES] --target [TARGET_FOLDER]
 ``` 

  * By default it works on Linux but you can change default params so that they express your OS params:
    * compiled_folder_name="x86_64"
    * mod_compile_command="nrnivmodl"
    
## Predefined Cells
This repository contains the basic cell model `Cell` object as well predefined cell models from ModelDB (https://senselab.med.yale.edu/modeldb)
  * All of those models are located in the cells/ folder. 
  * If you want to create your own model it is recommended to use `Cell` object.
  
The list of predefined cell models:
  * Ebner et al. 2019
  * Custom implementation of Ebner et. al 2019 with ACh/DA modulation
  * Combe et al. 2018
  * Graham et al. 2014
  * Hay et al. 2011
  
MOD files to all of those models are located in the commons/mods/ folder. Combe 2018 model and Graham 2014 model additionaly have hoc files located in the commons/hocmodels/ folder 
  


## Importing HOC model
There is an experimental Cell model `HocCell` which is not a part of `Cell`, however it allows to import HOC files and load its model to the Cell object.
Currently it allows only to import a single HOC cell from the single HOC entry file. If your HOC file/files define more than a single cell - import all of them manually and separately through `HocCell`.
In the future the factory method will create as many Cells as required based on HOC code.
* `HocCell` is located in the core/cell folder.

## Introduction to NEURON++
The full example used in this introduction is located in: examples/basic_example.py
There are other examples in the folder.

### Basics

  * create a cell:
   ```python
    cell = Cell(name="cell")
   ```

  * load SWC/ASC or HOC morphology:
   ```python
    cell.load_morpho(filepath='commons/morphologies/asc/cell2.asc')
   ```

  * create and connect sections:
   ```python
    cell.make_sec("soma", diam=20, l=20, nseg=10)
    cell.make_sec("dend", diam=2, l=100, nseg=10)
    cell.connect_secs(source="dend", target="soma")
   ```

  * add NEURON mechanisms (default or MOD-based):
   ```python
    cell.insert("pas")
    cell.insert("hh")
   ```

  * define simulation and run:
   ```python
    sim = RunSim(init_v=-65, warmup=20)
    sim.run(runtime=500)
   ```
  * add IClamp:
   ```python
   sections = cell.filter_secs("soma")
   soma = sections[0]

   ic = IClamp(segment=soma.hoc(0.5))
   ic.stim(delay=100, dur=10, amp=0.1)
   ```

### Filters
You can filter any part of the cell by string or regular expression filters
  
  * filter section of the cell by string:
  ```python
    # Assuming you have sections dend[0]...dend[100] it will return all of them
    sections = cell.filter_secs(name="dend")
  ```

  * filter section of the cell by regular expression:
  ```python
    # Assuming you have sections dend[0]...dend[100] and apic[0]...apic[100] it will return all of them
    sections = cell.filter_secs(name="regex:(apic)|(basal)")
  ```

  * return synapses of type 'ExpSyn' located in all heads sections
   ```python
    cell.filter_synapses(mod_name="ExpSyn", name="head")
   ```

There are many more filter functions. Check each one of them to discover each filter params.
The main cell object `Cell` contains all filter methods inside.

### More features

  * add synapses:
   ```python
    cell = Cell(name="cell")
    cell.make_sypanses(source=None, weight=0.01, mod_name="Syn4P", target_sec="soma", target_loc=0.5, delay=1)
   ```

  * add spines:
   ```python
   cell.make_spines(spine_number=10, head_nseg=10, neck_nseg=10, sec='dend')
   ```

  * define NetStim (or VecStim) and pass it to synapses while creating:
  ```python
    netstim = NetStimCell(name="netst")
    stim = netstim.make_netstim(start=300, number=5, interval=10)
    cell.make_sypanses(source=stim, weight=0.01, mod_name="Syn4P", target_sec="soma", target_loc=0.5, delay=1)
  ```

  * add synapses with spines in a single function:
   ```python
    syns = cell.make_spine_with_synapse(source=stim, weight=0.01, mod="ExpSyn",
                                        target_sec="dend", delay=1, head_nseg=10, neck_nseg=10, number=10)
   ```
   
   * Make synaptic event: 
     * every synapse can be stimulated by making event
     * but good practice is to define source=None 
     * it will return the synapse which an empty source, which can be stimulated externally
   ```python
    syns = cell.make_sypanses(source=None, weight=0.01, mod_name=SYNAPSE_MECH, target_sec="soma", 
                              target_loc=0.5, delay=1)
                              
    sim = RunSim(init_v=-55, warmup=20)
    
    syns[0].make_event(10)
    syns[0].make_event(20)
    
    sim.run(runtime=100)
   ```

  * Add source to previously created synapse:
  ```python
    syn.add_source(source=stim, weight=weight, threshold=threshold, delay=delay)
  ```

  * make spike detector for the cell:
  ```python
    cell.make_spike_detector()

    sim = RunSim(init_v=-65)
    sim.run(runtime=500)

    cell.plot_spikes()
   ```

  * record variables from sections and point_processes:
   ```python
    # record section's voltage
    secs = cell.filter_secs(name="soma")
    rec_v = Record(secs, locs=0.5, variables="v")

    # record synaptic (point_process) wariables (weight 'w')
    point_processes = cell.filter_point_processes(mod_name="Syn4P", name="dend")
    rec_syn = Record(point_processes, variables="w") 

    sim = RunSim(init_v=-65, warmup=20, with_neuron_gui=True)
    sim.run(runtime=500)
   ```

  * make plots and export to CSV recorded variables
   ```python
    rec_v.plot()
    rec_syn.plot()
    plt.show()

    rec_v.to_csv("vrec.csv")
   ```
  
  * make shape plot in NEURON GUI:
   ```python
   # show 'cai' propagation in range 0-0.01 uM 
   make_shape_plot(variable="cai", min_val=0, max_val=0.01)

   # show 'v' propagation in range -70-40 mV
   make_shape_plot(variable="v", min_val=-70, max_val=40)
   ```

  * define experimetal protocols, eg. STDP protocol:
  ```python
    soma = cell.filter_secs("soma")[0]
    syn = cell.filter_synapses(tag="my_synapse")

    stdp = Experiment()
    stdp.make_protocol("3xEPSP[int=10] 3xAP[int=10,dur=3,amp=1.6]", start=1, isi=10, iti=3000,
                       epsp_synapse=syn, i_clamp_section=soma)
   ```

  * create a population:
    * This is an experimental feature so may not be so easy to use
  ```python
    # Define a new Population class. 
    # You need to implement abstract method make_cell() and make_conn() for each new Population 
    class ExcitatoryPopulation(Population):
        def make_cell(self, **kwargs) -> Cell:
            cell = Cell(name="cell")
            cell.load_morpho(filepath='../commons/morphologies/swc/my.swc')
            cell.insert("pas")
            cell.insert("hh")
            return cell

        def make_conn(self, cell: Cell, source, source_loc=None, weight=1, **kwargs) -> list:
            syns, heads = cell.make_spine_with_synapse(source=source, mod_name="Exp2Syn",
                                                       source_loc=source_loc, weight=weight, target_sec="dend")
            return syns

    # Create NetStim
    stim = NetStimCell("stim").make_netstim(start=21, number=10, interval=10)

    # Create population 1
    pop1 = ExcitatoryPopulation("pop")
    pop1.create(2)
    pop1.connect(sources=stim, rule='all', weight=0.01)
    pop1.record()

    # Create population 2
    pop2 = ExcitatoryPopulation("pop2")
    pop2.create(2)
    pop2.connect(sources=pop1, rule='all', source_sec_name="soma", source_loc=0.5, weight=0.01)
    pop2.record()

    # Run
    sim = RunSim(init_v=-70, warmup=20)
    for i in range(1000):
        sim.run(runtime=1)
        pop1.plot(animate=True)
        pop2.plot(animate=True)
   ```

  * and more...


