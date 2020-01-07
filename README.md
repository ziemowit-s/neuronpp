Morphological model of neuron with RxD ionic diffusion. Based on NEURON.

## Prerequisites

* Install requirements.txt
* Install NEURON

## Repository

https://github.com/ziemowit-s/neuronpp

## Pip installation
```bash
pip install git+https://github.com/ziemowit-s/neuronpp
```
## MOD compilation
* Before run you must compile mod files and copy compiled folder to the main folder (where run Python files are located)
```bash
nrmivmodl
```

* To help with compilation use compile_mods.sh (Linux only)
  * first param is folder from which to copy files fo current_mods folder
  * Don't forget to add /* at the end, eg.:
```bash
sh compile_mods.sh mods/4p_ach_da_syns/*
``` 
  * If you auto-run from PyCharm - you can config to run compile_mods.sh before each run


## Run examples

### ebner_ach_da
* Shows how Ebner2019 cell works with additional ACh and DA 
```bash
python ebner_ach_da_run.py
```