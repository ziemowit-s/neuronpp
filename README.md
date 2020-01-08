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

* To help with compilation use compile_mod.py or CompileMOD class:
  * It will compile all mods recursively (if it contains other folders) inside the source folder and
  * copy compiled folder to the target folder 
```bash
python compile_mod.py --source [SOURCE_FOLDER_WITH_MOD_FILES] --target [TARGET_FOLDER]
``` 
  * By default it works on Linux but you can change default params so that they express your OS params:
    * compiled_folder_name="x86_64"
    * mod_compile_command="nrnivmodl"


## Run examples

### ebner_ach_da
* Shows how Ebner2019 cell works with additional ACh and DA 
```bash
python ebner_ach_da_run.py
```