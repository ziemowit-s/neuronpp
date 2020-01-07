#!/bin/bash

# first param is dir from which to copy files fo current_mods.
# Don't forget to add /* at the end
# eg. sh compile_mods.sh mods/4p_ach_da_syns/*

rm -R x86_64;
cp $1 current_mods/
cd current_mods;
nrnivmodl;
mv x86_64 ../