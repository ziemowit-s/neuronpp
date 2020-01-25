Neuron++ is a library which wraps NEURON tool with easy to use Python classes

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

## MOD compilation
Before run you must compile mod files, however `Cell()` object has `compile_path` param which allows to specify paths with mods to compile before each run.
In most cases you don't need to compile files externally, but just add paths to your Cell.

Every cell in the cell/ folder has defined required paths which will work if you run python script from the main folder (as a working directory) which is neuronpp/neuronpp/

However if you want to compile mods manually this is how to do it:

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

### More Features

  * add synapses:
   ```python
    cell = Cell(name="cell")
    cell.make_sypanses(source=None, weight=0.01, mod_name="Syn4P", sec="soma", target_loc=0.5, delay=1)
   ```

  * add spines:
   ```python
   cell.make_spines(spine_number=10, head_nseg=10, neck_nseg=10, sec='dend')
   ```

  * define NetStim (or VecStim) and pass it to synapses:
  ```python
    netstim = NetStimCell(name="netst")
    stim = netstim.make_netstim(start=300, number=5, interval=10)
    cell.make_sypanses(source=stim, weight=0.01, mod_name="Syn4P", sec="soma", target_loc=0.5, delay=1)
  ```

  * add synapses with spines in a single function:
   ```python
    syns = cell.make_spine_with_synapse(source=stim, weight=0.01, mod_name="ExpSyn",
                                        sec="dend", delay=1, head_nseg=10, neck_nseg=10, number=10)
   ```
   
   * Make synaptic event: 
     * every synapse can be stimulated by making event
     * but good practice is to define source=None 
     * it will return the synapse which an empty source, which can be stimulated externally
   ```python
    syns = cell.make_sypanses(source=None, weight=0.01, mod_name=SYNAPSE_MECH, sec="soma", target_loc=0.5, delay=1)
    sim = RunSim(init_v=-55, warmup=20)
    syns[0].make_event(10)
    syns[0].make_event(20)
    sim.run(runtime=100)
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

  * and more...


