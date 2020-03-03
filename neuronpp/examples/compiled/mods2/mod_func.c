#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _exc_sigma3exp2syn_reg();
extern void _exc_sigma3exp2syn_ach_da_reg();
extern void _inh_sigma3exp2syn_reg();

void modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," exc_sigma3exp2syn.mod");
fprintf(stderr," exc_sigma3exp2syn_ach_da.mod");
fprintf(stderr," inh_sigma3exp2syn.mod");
fprintf(stderr, "\n");
    }
_exc_sigma3exp2syn_reg();
_exc_sigma3exp2syn_ach_da_reg();
_inh_sigma3exp2syn_reg();
}
