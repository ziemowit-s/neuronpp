Neuron++ is a wrapper for NEURON (http://www.neuron.yale.edu) with easy to use Python objects. 
The key intention behind this framework was to perform tedious tasks in few lines of code with 
the object-oriented paradigm. 

NEURON allows to create simulations of Biological Neural Networks. The Neuron++ framework was 
designed to match the simplicity of libraries such as Keras library for Artificial Neural Networks.
With Neuron++ you can easily create group of cells, stack them together as populations, 
then stimulate them with external input and collect readouts to perform any task.

## Key features

  * Use for fast prototyping of neural models in NEURON simulator, using Python interface with 
    the object-oriented paradigm (OOP)

  * Precisely define single cell models and connect them together to create a network
  
  * Auto-compilation of all MOD files on the fly
  
  * Auto-load SWC/ASC or HOC morphology for each cell
  
  * Upload HOC defined models and adapt them to your needs
  
  * Define in vitro experimental protocols (eg. STDP paradigms)
  
  * Manage synaptic signaling
  
  * Debug synapses and point processes RANGE values in real time with interactive 
    stimulation from the keyboard
  
  * Create predefined dendritic spines and synapses with ease
  
  * Define populations of neurons and connect them together
  
  * Provide helpful exception messages and guidelines of how to use NEURON functions with Neuron++ 
    wrapper without errors
    
This is the Alpha version.

## Prerequisites

1. Python >= 3.5 (recommended is Python 3.8)
2. Install requirements.txt:
```bash
pip install -r requirements.txt
```

* If not Linux - go to the instruction: https://github.com/ziemowit-s/neuron_get_started
* recommended NEURON version is 7.8.2. Please do not use NEURON version 8.* Neuron++ won't remove correctly NEURON elements. It will be fixed in the future

## Repository

https://github.com/ziemowit-s/neuronpp

## Neuron++ installation

* Locally:
```bash
python setup.py bdist_wheel
```

* Through pip and GitHub:
```bash
pip install git+https://github.com/ziemowit-s//neuronpp
```
* Bear in mind that if you install the library through the pip you will have access to all features 
of NEURON++, however additionally provided cell models from other publications (listed below) will 
not work correctly, unless you download the 'commons/' folder from the GitHub repository and change 
paths in 'examples/' indicating the 'commons/'. 

So if you want to work with those predefined models it is recommended to clone the repository from 
GitHub rather than install through pip.

## Predefined Cell models
This repository contains the basic cell objects: 
  * `Cell` class
  * `HocCell` - the experimental `HOC class which loads HOC based cell model. 
  
The repository also contains some predefined cell models from ModelDB (https://senselab.med.yale.edu/modeldb)
  * All of those models are located in the cells/ folder. 
  * If you want to create your own model it is recommended to use:
    * `Cell`
    * `HocCell` - if you want to reuse existing HOC model
  
The list of predefined cell models:
  * Ebner et al. 2019, https://doi.org/10.1016/j.celrep.2019.11.068
  * Custom implementation of Ebner et. al 2019 with ACh/DA modulation
  * Combe et al. 2018, https://doi.org/10.1523/JNEUROSCI.0449-18.2018
  * Graham et al. 2014, https://doi.org/10.1162/NECO_a_00640
  * Hay et al. 2011, https://doi.org/10.1371/journal.pcbi.1002107
  
MOD files of all of those models are located in the commons/mods/ folder. 
Combe 2018 model and Graham 2014 model additionally have HOC files located in the 
commons/hocmodels/ folder.

## Automatic MOD compilation
### Automatic (recommended)
`Cell()` object has a `compile_path` param which allows to specify paths which contain MOD files.

You don't need to compile files externally, if you provided appropriate pathways it 
will be done automatically before each run.

## Introduction to NEURON++
All examples are located in the examples/ folder

Please bear in mind that due to substantial updates some examples may not work as described here in 
the README, also some additional features have been added which are not listed here. We will update 
readme soon.

### Basics

  * create a cell:
   ```python
    cell = Cell(name="mycell")
   ```

  * load SWCor ASC morphology:
   ```python
    cell.load_morpho(filepath='commons/morphologies/asc/cell2.asc')
   ```
 
  * load HOC-based cell (and HOC-based morphology) model to the `Cell` object:
    * allows to work with most modelDB single cell models
    * it will auto load all sections and point processes for further usage and/or filtering 
    * This is an experimental feature, so currently works ONLY with HOC models which define a 
    single cell
   ```python
    cell = HocCell(name="mycell")
    cell.load_hoc("your_cell_model.hoc")
   ```
   
 * if the HOC cell model is defined as a Template - just specify the `cell_template_name` param:
 ```python
    cell = HocCell(name="mycell")
    cell.load_hoc("Ebner2019_minimum_load/load_model.hoc", hoc_template_name="L5PCtemplate")
   ```
   
  * create and connect sections:
   ```python
    cell.add_seg("soma", diam=20, l=20, nseg=10)
    cell.add_seg("dend", diam=2, l=100, nseg=10)
    cell.connect_secs(child="dend", parent="soma")
   ```

  * add NEURON mechanisms (default or MOD-based):
   ```python
    cell.insert("pas")
    cell.insert("hh")
   ```

  * define simulation and run:
   ```python
    sim = Simulation(init_v=-65, warmup=20)
    sim.run(runtime=500)
   ```
  * add IClamp:
   ```python
   sections = cell.filter_secs("soma")
   soma = sections[0]

   ic = IClamp(segment=soma(0.5))
   ic.debug(delay=100, dur=10, amp=0.1)
   ```

### Easy filters
You can obtain any part of the cell by string or regular expression filtering
  
  * filter section of the cell by string:
  ```python
    # Assuming you have sections dend[0]...dend[100] it will return all of them
    sections = cell.filter_secs(name="dend")
  ```

  * filter by string separated by coma:
  ```python
    # Each coma function as OR between strings
    sections = cell.filter_secs(name="apic[1],apic[50]")
  ```

  * filter section of the cell by regular expression:
  ```python
    # Assuming you have sections dend[0]...dend[100] and apic[0]...apic[100] it will return all of them
    sections = cell.filter_secs(name="regex:(apic)|(basal)")
  ```

  * return synapses of type 'ExpSyn' located in all heads sections (of the dendritic spines)
   ```python
    cell.filter_synapses(mod_name="ExpSyn", name="head")
   ```

  * custom function-based filtering:
    * pass function to the `obj_filter` param.
    eg. (lambda expression) returns sections which name contains 'apic' or their 
    distance > 1000 um from the soma:
  ```python
   soma = cell.filter_secs("soma")
   cell.filter_secs(obj_filter=lambda o: 'apic' in o.name or h.distance(soma(0.5), o(0.5)) > 1000)
  ```
         
  * field-based filtering with custom function.
    eg. (lambda expression) returns sections which parent's name contains less than 10 characters
  ```python
  cell.filter_secs(parent=lambda o: len(o.parent.name) < 10)
  ```

All filter functions available in default cell object `Cell`:
  * filter_secs - obtain sections
  * filter_point_processes - obtain point processes
  * filter_netcons - obtain netcons
  * filter_synapses - obtain single synapse, which is a point_process and netcon wrapper
  * filter_synaptic_group - obtain a group of synapses which is many single synapses grouped together

### Define Synapses
If you define `source` param - it will stimulate synapse based on the stimulation from the source.
If `source` is None - there will be no source and no netcon, however you can add those later or 
use such synapse for the `Experiment`.

  * add single synapse:
   ```python
    cell = Cell(name="cell")
    soma = cell.filter_secs(name="soma")
    cell.add_sypanse(source=None, mod_name="Syn4P", seg=soma(0.5), netcon_weight=0.01, delay=1)
   ```

  * add many spines to the provided sections:
   ```python
   cell = Cell(name="cell")
   dendrites = cell.filter_secs(name="dend")
   cell.add_randuniform_spines(spine_number=10, head_nseg=10, neck_nseg=10, secs=dendrites)
   ```

  * add many synapses with spines (1 synapse/spine) in a single function to the provided sections:
   ```python
    cell = Cell(name="cell")
    dendrites = cell.filter_secs(name="dend")
    syns = cell.add_random_synapses_with_spine(source=None, secs=dendrites, mod="ExpSyn",
                                               netcon_weight=0.01, delay=1, number=10)
   ```
  
  * define NetStim (or VecStim) and pass it to synapses as a source while creating:
  ```python
    netstim = NetStimCell(name="netst")
    stim = netstim.add_netstim(start=300, number=5, interval=10)
    
    cell = Cell(name="cell")
    soma = cell.filter_secs(name="soma")
    cell.add_sypanse(source=stim, seg=soma(0.5), mod_name="ExpSyn", netcon_weight=0.01, delay=1)
  ```
  
   * send external input to the synapse by calling synaptic event: 
     * every synapse can be stimulated by making event, however a good practice is to define 
     source=None for such synapses. 
   ```python
    cell = Cell(name="cell")
    soma = cell.filter_secs(name="soma")
    syns = cell.add_sypanse(source=None, seg=soma(0.5), mod_name="ExpSyn", 
                            netcon_weight=0.01, delay=1)
                              
    sim = Simulation(init_v=-55, warmup=20)
    
    syns[0].make_event(10)
    syns[0].make_event(20)
    
    sim.run(runtime=100)
   ```

  * Add another source to the previously created synapse:
  ```python
    synapse.add_netcon(source=None, weight=0.035, threshold=15, delay=2)
  ```

### Record and plot

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
    soma = cell.filter_secs(name="soma")
    rec_v = Record(soma(0.5), variables="v")

    # record synaptic (point_process) wariables (weight 'w')
    point_processes = cell.filter_point_processes(mod_name="Syn4P", name="dend")
    rec_syn = Record(point_processes, variables="w") 

    sim = Simulation(init_v=-65, warmup=20, with_neuron_gui=True)
    sim.run(runtime=500)
   ```

  * make plots and export recorded variables to CSV:
   ```python
    rec_v.plot()
    rec_syn.plot()
    plt.show()
    rec_v.to_csv("vrec.csv")
   ```
  
  * make shape plot of the cell in NEURON GUI:
   ```python
   # show 'cai' propagation in range 0-0.01 uM 
   make_shape_plot(variable="cai", min_val=0, max_val=0.01)

   # show 'v' propagation in range -70-40 mV
   make_shape_plot(variable="v", min_val=-70, max_val=40)
   ```
   
### Replicate in vitro experiments

  * define experimetal protocols, eg. STDP protocol:
  ```python
    soma = cell.filter_secs("soma")
    syn = cell.filter_synapses(tag="my_synapse")

    experiment = Experiment(iti=40)
    experiment.add_epsp(num=3, synapse=syn, init=20, interval=20, weight=0.02)
    experiment.add_iclamp(num=3, segment=soma(0.5), init=60, interval=20, dur=3, amp=1.6)
    experiment.build()
   ```

### Populations of neurons

Create a population of many neurons of the same type and connect them between populations:

* Create a template cell function:

  ```python
    def cell_function():
        cell = Cell(name="cell")
        morpho_path = os.path.join(path, "..", "commons/morphologies/swc/my.swc")
        cell.load_morpho(filepath=morpho_path)
        cell.insert("pas")
        cell.insert("hh")
        cell.make_spike_detector(seg=cell.filter_secs("soma")(0.5))
        return cell
    ```
  
  * Create stimulation:
  ```python
    # Create NetStim
    netstim = NetStimCell("stim").add_netstim(start=21, number=100, interval=2)
  
    # Define weight distribution for both: NetStim->population1 and population1->population2
    weight_dist = NormalTruncatedDist(mean=0.1, std=0.2)
  ```
  
  * Define  population 1:
  ```python
    pop1 = Population("pop_1")
    pop1.add_cells(num=3, cell_function=cell_function)

    # create 10 synapses on population 2 per NetStim object (single NetStim here)
    connector = pop1.connect(syn_num_per_cell_source=10)
    connector.set_source(netstim)

    # choose all dendrites as potential targets for synaptic choice
    targets = [d(0.5) for c in pop1.cells for d in c.filter_secs("dend")]
    connector.set_target(targets)

    # Make synapse
    syn_adder = connector.add_synapse("Exp2Syn")
    syn_adder.add_netcon(weight=weight_dist)
    # change tau1 and tau2 for Exp2Syn synapses
    syn_adder.add_point_process_params(tau1=0.1, tau2=2)
  ```
  
  * Build connections and define that you want to record from the population
    * By default `record()` method make records of: voltage variable in soma(0.5)
  ```python
    connector.build()
    pop1.record()
  ```
  
  * Create population 2:
  ```python
    pop2 = Population("pop_2")
    pop2.add_cells(num=3, cell_function=cell_function)
  ```
  
  * Define connections between pop1 and pop2 where weights will be chosen 
  from the Normal Truncated Distribution:
  ```python
    # create 5 synapses per single cell in population 1
    connector = pop2.connect(syn_num_per_cell_source=5)

    source = [c.filter_secs("soma")(0.5) for c in pop1.cells]
    connector.set_source(source)

    # choose all dendrites as potential targets for synaptic choice
    targets = [d(0.5) for c in pop2.cells for d in c.filter_secs("dend")]
    connector.set_target(targets)

    # Make synapse
    syn_adder = connector.add_synapse("Exp2Syn")
    syn_adder.add_netcon(weight=weight_dist)
    # change tau1 and tau2 for Exp2Syn synapses
    syn_adder.add_point_process_params(tau1=0.1, tau2=2)
   ```

  * Build connections and define that you want to record from the population
  * By default `record()` method make records of: voltage variable in soma(0.5)
  ```python
    connector.build()
    pop2.record()
  ```
  
  * Ryn simulation and plot activities:
  ```python
    sim = Simulation(init_v=-70, warmup=20)
    for i in range(1000):
        sim.run(runtime=1)
        pop1.plot(animate=True)
        pop2.plot(animate=True)
    ```

  * Create (experimental) interactive graph of connected populations which allows you to see and 
  move nodes in the web browser:
  ```python
  show_connectivity_graph(pop1.cells + pop2.cells)
  ```
![Network Graph](images/conectivity_graph.png) 
  

### Debug synapses and point processes

Debug any cell and synapse on interactive plot. 
  * By pressing a key defined as `stim_key` param (default is w) you can stimulate synapses 
    provided to the Debugger
  * It allows to easily plot synaptic weight (defined as MOD's RANGE variable) to see how 
    the plasticity behaves in real time
  ```python
    from neuronpp.cells.cell import Cell
    from neuronpp.utils.synaptic_debugger import SynapticDebugger
    
    # Prepare cell
    cell = Cell("cell")
    soma = cell.add_sec("soma", diam=20, l=20, nseg=100)
    cell.insert("pas")
    cell.insert("hh")
    
    syn1 = cell.add_synapse(source=None, netcon_weight=0.002, seg=soma(0.1), mod_name="Exp2Syn")
    syn2 = cell.add_synapse(source=None, netcon_weight=0.002, seg=soma(0.9), mod_name="Exp2Syn")
    syn3 = cell.add_synapse(source=None, netcon_weight=0.002, seg=soma(0.5), mod_name="Exp2Syn")
    
    # Debug
    debug = SynapticDebugger(init_v=-70, warmup=10, delay_between_steps=15)
    debug.add_syn(syn1, key_press='1', plot=True, syn_variables='i')
    debug.add_syn(syn2, key_press='2')
    debug.add_syn(syn3, key_press='3')
    debug.add_seg(soma(0.5))
    debug.debug_interactive()
  ```

![Debugger](images/debugger.gif) 
Example of Ebner et al. 2019 model of synaptic weight (variable w) changing based on synaptic stimulation on demand
by pressing key "w" on the keyboard:
* variable w: weight on the synapse.
* variable v: voltage on the soma.
* Pressing "w" on the keyboard produce a synaptic event. 



