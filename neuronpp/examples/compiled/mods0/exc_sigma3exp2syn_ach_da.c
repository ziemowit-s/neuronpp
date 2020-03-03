/* Created by Language version: 7.7.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib_ansi.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__ExcSigma3Exp2SynAchDa
#define _nrn_initial _nrn_initial__ExcSigma3Exp2SynAchDa
#define nrn_cur _nrn_cur__ExcSigma3Exp2SynAchDa
#define _nrn_current _nrn_current__ExcSigma3Exp2SynAchDa
#define nrn_jacob _nrn_jacob__ExcSigma3Exp2SynAchDa
#define nrn_state _nrn_state__ExcSigma3Exp2SynAchDa
#define _net_receive _net_receive__ExcSigma3Exp2SynAchDa 
#define state state__ExcSigma3Exp2SynAchDa 
 
#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define tau1 _p[0]
#define tau2 _p[1]
#define e _p[2]
#define ltd_sigmoid_half _p[3]
#define learning_slope _p[4]
#define learning_tau _p[5]
#define w _p[6]
#define ach_tau _p[7]
#define da_tau _p[8]
#define ach_substractor _p[9]
#define da_substractor _p[10]
#define i _p[11]
#define g _p[12]
#define ltd _p[13]
#define ltp _p[14]
#define last_max_da_w _p[15]
#define modulatory_w _p[16]
#define A _p[17]
#define B _p[18]
#define ach _p[19]
#define da _p[20]
#define learning_w _p[21]
#define ach_w _p[22]
#define heb_ach_w _p[23]
#define da_w _p[24]
#define heb_da_w _p[25]
#define factor _p[26]
#define DA _p[27]
#define DB _p[28]
#define Dach _p[29]
#define Dda _p[30]
#define Dlearning_w _p[31]
#define Dach_w _p[32]
#define Dheb_ach_w _p[33]
#define Dda_w _p[34]
#define Dheb_da_w _p[35]
#define v _p[36]
#define _g _p[37]
#define _tsav _p[38]
#define _nd_area  *_ppvar[0]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 /* declaration of user functions */
 static double _hoc_sigmoid_sat();
 static double _hoc_sigmoid_thr();
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern Prop* nrn_point_prop_;
 static int _pointtype;
 static void* _hoc_create_pnt(_ho) Object* _ho; { void* create_point_process();
 return create_point_process(_pointtype, _ho);
}
 static void _hoc_destroy_pnt();
 static double _hoc_loc_pnt(_vptr) void* _vptr; {double loc_point_process();
 return loc_point_process(_pointtype, _vptr);
}
 static double _hoc_has_loc(_vptr) void* _vptr; {double has_loc_point();
 return has_loc_point(_vptr);
}
 static double _hoc_get_loc_pnt(_vptr)void* _vptr; {
 double get_loc_point_process(); return (get_loc_point_process(_vptr));
}
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 }
 static void _hoc_setdata(void* _vptr) { Prop* _prop;
 _prop = ((Point_process*)_vptr)->_prop;
   _setdata(_prop);
 }
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 0,0
};
 static Member_func _member_func[] = {
 "loc", _hoc_loc_pnt,
 "has_loc", _hoc_has_loc,
 "get_loc", _hoc_get_loc_pnt,
 "sigmoid_sat", _hoc_sigmoid_sat,
 "sigmoid_thr", _hoc_sigmoid_thr,
 0, 0
};
#define sigmoid_sat sigmoid_sat_ExcSigma3Exp2SynAchDa
#define sigmoid_thr sigmoid_thr_ExcSigma3Exp2SynAchDa
 extern double sigmoid_sat( _threadargsprotocomma_ double , double );
 extern double sigmoid_thr( _threadargsprotocomma_ double , double , double );
 /* declare global and static user variables */
#define ltp_sigmoid_half ltp_sigmoid_half_ExcSigma3Exp2SynAchDa
 double ltp_sigmoid_half = -40;
#define ltp_theshold ltp_theshold_ExcSigma3Exp2SynAchDa
 double ltp_theshold = -45;
#define ltd_theshold ltd_theshold_ExcSigma3Exp2SynAchDa
 double ltd_theshold = -60;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "ach_substractor", 1e-009, 1e+009,
 "ach_tau", 1e-009, 1e+009,
 "da_substractor", 1e-009, 1e+009,
 "da_tau", 1e-009, 1e+009,
 "ltp_sigmoid_half_ExcSigma3Exp2SynAchDa", 1e-009, 1e+009,
 "ltp_theshold_ExcSigma3Exp2SynAchDa", 1e-009, 1e+009,
 "ltd_theshold_ExcSigma3Exp2SynAchDa", 1e-009, 1e+009,
 "ltd_sigmoid_half", 1e-009, 1e+009,
 "tau2", 1e-009, 1e+009,
 "tau1", 1e-009, 1e+009,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "ltd_theshold_ExcSigma3Exp2SynAchDa", "mV",
 "ltp_theshold_ExcSigma3Exp2SynAchDa", "mV",
 "ltp_sigmoid_half_ExcSigma3Exp2SynAchDa", "mV",
 "tau1", "ms",
 "tau2", "ms",
 "e", "mV",
 "ltd_sigmoid_half", "mV",
 "ach_tau", "ms",
 "da_tau", "ms",
 "ach_substractor", "1e-9",
 "da_substractor", "1e-9",
 "A", "uS",
 "B", "uS",
 "ach", "uS",
 "da", "uS",
 "i", "nA",
 "g", "uS",
 0,0
};
 static double A0 = 0;
 static double B0 = 0;
 static double ach_w0 = 0;
 static double ach0 = 0;
 static double delta_t = 0.01;
 static double da_w0 = 0;
 static double da0 = 0;
 static double heb_da_w0 = 0;
 static double heb_ach_w0 = 0;
 static double learning_w0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "ltd_theshold_ExcSigma3Exp2SynAchDa", &ltd_theshold_ExcSigma3Exp2SynAchDa,
 "ltp_theshold_ExcSigma3Exp2SynAchDa", &ltp_theshold_ExcSigma3Exp2SynAchDa,
 "ltp_sigmoid_half_ExcSigma3Exp2SynAchDa", &ltp_sigmoid_half_ExcSigma3Exp2SynAchDa,
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(_NrnThread*, _Memb_list*, int);
static void nrn_state(_NrnThread*, _Memb_list*, int);
 static void nrn_cur(_NrnThread*, _Memb_list*, int);
static void  nrn_jacob(_NrnThread*, _Memb_list*, int);
 static void _hoc_destroy_pnt(_vptr) void* _vptr; {
   destroy_point_process(_vptr);
}
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(_NrnThread*, _Memb_list*, int);
static void _ode_matsol(_NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[2]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"ExcSigma3Exp2SynAchDa",
 "tau1",
 "tau2",
 "e",
 "ltd_sigmoid_half",
 "learning_slope",
 "learning_tau",
 "w",
 "ach_tau",
 "da_tau",
 "ach_substractor",
 "da_substractor",
 0,
 "i",
 "g",
 "ltd",
 "ltp",
 "last_max_da_w",
 "modulatory_w",
 0,
 "A",
 "B",
 "ach",
 "da",
 "learning_w",
 "ach_w",
 "heb_ach_w",
 "da_w",
 "heb_da_w",
 0,
 0};
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
  if (nrn_point_prop_) {
	_prop->_alloc_seq = nrn_point_prop_->_alloc_seq;
	_p = nrn_point_prop_->param;
	_ppvar = nrn_point_prop_->dparam;
 }else{
 	_p = nrn_prop_data_alloc(_mechtype, 39, _prop);
 	/*initialize range parameters*/
 	tau1 = 0.1;
 	tau2 = 10;
 	e = 0;
 	ltd_sigmoid_half = -55;
 	learning_slope = 1.3;
 	learning_tau = 20;
 	w = 1;
 	ach_tau = 10;
 	da_tau = 10;
 	ach_substractor = 1;
 	da_substractor = 2;
  }
 	_prop->param = _p;
 	_prop->param_size = 39;
  if (!nrn_point_prop_) {
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 3, _prop);
  }
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _net_receive(Point_process*, double*, double);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _exc_sigma3exp2syn_ach_da_reg() {
	int _vectorized = 1;
  _initlists();
 	_pointtype = point_register_mech(_mechanism,
	 nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init,
	 hoc_nrnpointerindex, 1,
	 _hoc_create_pnt, _hoc_destroy_pnt, _member_func);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 39, 3);
  hoc_register_dparam_semantics(_mechtype, 0, "area");
  hoc_register_dparam_semantics(_mechtype, 1, "pntproc");
  hoc_register_dparam_semantics(_mechtype, 2, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 pnt_receive[_mechtype] = _net_receive;
 pnt_receive_size[_mechtype] = 1;
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 ExcSigma3Exp2SynAchDa C:/Users/Wladek/Documents/GitHub/neuronpp/neuronpp/examples/compiled/mods0/exc_sigma3exp2syn_ach_da.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[9], _dlist1[9];
 static int state(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset = 0; {
   DA = - A / tau1 ;
   DB = - B / tau2 ;
   Dlearning_w = - learning_w / 4.0 ;
   Dach = - ach / ach_tau ;
   Dda = - da / da_tau ;
   Dach_w = - ach_w / ach_tau ;
   Dda_w = - da_w / da_tau ;
   Dheb_ach_w = - heb_ach_w / ach_tau ;
   Dheb_da_w = - heb_da_w / da_tau ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
 DA = DA  / (1. - dt*( ( - 1.0 ) / tau1 )) ;
 DB = DB  / (1. - dt*( ( - 1.0 ) / tau2 )) ;
 Dlearning_w = Dlearning_w  / (1. - dt*( ( - 1.0 ) / 4.0 )) ;
 Dach = Dach  / (1. - dt*( ( - 1.0 ) / ach_tau )) ;
 Dda = Dda  / (1. - dt*( ( - 1.0 ) / da_tau )) ;
 Dach_w = Dach_w  / (1. - dt*( ( - 1.0 ) / ach_tau )) ;
 Dda_w = Dda_w  / (1. - dt*( ( - 1.0 ) / da_tau )) ;
 Dheb_ach_w = Dheb_ach_w  / (1. - dt*( ( - 1.0 ) / ach_tau )) ;
 Dheb_da_w = Dheb_da_w  / (1. - dt*( ( - 1.0 ) / da_tau )) ;
  return 0;
}
 /*END CVODE*/
 static int state (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) { {
    A = A + (1. - exp(dt*(( - 1.0 ) / tau1)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau1 ) - A) ;
    B = B + (1. - exp(dt*(( - 1.0 ) / tau2)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau2 ) - B) ;
    learning_w = learning_w + (1. - exp(dt*(( - 1.0 ) / 4.0)))*(- ( 0.0 ) / ( ( - 1.0 ) / 4.0 ) - learning_w) ;
    ach = ach + (1. - exp(dt*(( - 1.0 ) / ach_tau)))*(- ( 0.0 ) / ( ( - 1.0 ) / ach_tau ) - ach) ;
    da = da + (1. - exp(dt*(( - 1.0 ) / da_tau)))*(- ( 0.0 ) / ( ( - 1.0 ) / da_tau ) - da) ;
    ach_w = ach_w + (1. - exp(dt*(( - 1.0 ) / ach_tau)))*(- ( 0.0 ) / ( ( - 1.0 ) / ach_tau ) - ach_w) ;
    da_w = da_w + (1. - exp(dt*(( - 1.0 ) / da_tau)))*(- ( 0.0 ) / ( ( - 1.0 ) / da_tau ) - da_w) ;
    heb_ach_w = heb_ach_w + (1. - exp(dt*(( - 1.0 ) / ach_tau)))*(- ( 0.0 ) / ( ( - 1.0 ) / ach_tau ) - heb_ach_w) ;
    heb_da_w = heb_da_w + (1. - exp(dt*(( - 1.0 ) / da_tau)))*(- ( 0.0 ) / ( ( - 1.0 ) / da_tau ) - heb_da_w) ;
   }
  return 0;
}
 
static void _net_receive (_pnt, _args, _lflag) Point_process* _pnt; double* _args; double _lflag; 
{  double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _thread = (Datum*)0; _nt = (_NrnThread*)_pnt->_vnt;   _p = _pnt->_prop->param; _ppvar = _pnt->_prop->dparam;
  if (_tsav > t){ extern char* hoc_object_name(); hoc_execerror(hoc_object_name(_pnt->ob), ":Event arrived out of order. Must call ParallelContext.set_maxstep AFTER assigning minimum NetCon.delay");}
 _tsav = t; {
   if ( _args[0] - da_substractor > 0.0 ) {
       if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = da_w;
    double __primary = (_args[0] - da_substractor) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / da_tau ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / da_tau ) - __primary );
    da_w += __primary;
  } else {
 da_w = _args[0] - da_substractor ;
       }
 if ( da_w > 1.0 ) {
         if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = da_w;
    double __primary = (1.0) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / da_tau ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / da_tau ) - __primary );
    da_w += __primary;
  } else {
 da_w = 1.0 ;
         }
 }
     last_max_da_w = da_w ;
     if ( heb_da_w > 0.0 ) {
         if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = da;
    double __primary = (heb_da_w * da_w) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / da_tau ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / da_tau ) - __primary );
    da += __primary;
  } else {
 da = heb_da_w * da_w ;
         }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = heb_da_w;
    double __primary = (0.0) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / da_tau ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / da_tau ) - __primary );
    heb_da_w += __primary;
  } else {
 heb_da_w = 0.0 ;
         }
 }
     }
   else if ( _args[0] - ach_substractor > 0.0 ) {
       if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = ach_w;
    double __primary = (_args[0] - ach_substractor) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / ach_tau ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / ach_tau ) - __primary );
    ach_w += __primary;
  } else {
 ach_w = _args[0] - ach_substractor ;
       }
 if ( ach_w > 1.0 ) {
         if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = ach_w;
    double __primary = (1.0) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / ach_tau ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / ach_tau ) - __primary );
    ach_w += __primary;
  } else {
 ach_w = 1.0 ;
         }
 }
     if ( heb_ach_w > 0.0 ) {
         if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = ach;
    double __primary = (heb_ach_w * ach_w) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / ach_tau ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / ach_tau ) - __primary );
    ach += __primary;
  } else {
 ach = heb_ach_w * ach_w ;
         }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = heb_ach_w;
    double __primary = (0.0) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / ach_tau ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / ach_tau ) - __primary );
    heb_ach_w += __primary;
  } else {
 heb_ach_w = 0.0 ;
         }
 }
     }
   else {
       if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = A;
    double __primary = (A + _args[0] * factor) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / tau1 ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / tau1 ) - __primary );
    A += __primary;
  } else {
 A = A + _args[0] * factor ;
       }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = B;
    double __primary = (B + _args[0] * factor) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / tau2 ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / tau2 ) - __primary );
    B += __primary;
  } else {
 B = B + _args[0] * factor ;
       }
 if ( ach_w > 0.0 ) {
         if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = ach;
    double __primary = (ach_w) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / ach_tau ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / ach_tau ) - __primary );
    ach += __primary;
  } else {
 ach = ach_w ;
         }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = ach_w;
    double __primary = (0.0) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / ach_tau ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / ach_tau ) - __primary );
    ach_w += __primary;
  } else {
 ach_w = 0.0 ;
         }
 }
     if ( da_w > 0.0 ) {
         if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = da;
    double __primary = (da_w) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / da_tau ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / da_tau ) - __primary );
    da += __primary;
  } else {
 da = da_w ;
         }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = da_w;
    double __primary = (0.0) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / da_tau ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / da_tau ) - __primary );
    da_w += __primary;
  } else {
 da_w = 0.0 ;
         }
 }
       if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = heb_ach_w;
    double __primary = (1.0) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / ach_tau ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / ach_tau ) - __primary );
    heb_ach_w += __primary;
  } else {
 heb_ach_w = 1.0 ;
       }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = heb_da_w;
    double __primary = (1.0) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / da_tau ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / da_tau ) - __primary );
    heb_da_w += __primary;
  } else {
 heb_da_w = 1.0 ;
       }
 }
   } }
 
double sigmoid_thr ( _threadargsprotocomma_ double _lslope , double _lvalue , double _lthr ) {
   double _lsigmoid_thr;
 _lsigmoid_thr = 1.0 / ( 1.0 + pow ( _lslope , - ( _lvalue - _lthr ) ) ) ;
   
return _lsigmoid_thr;
 }
 
static double _hoc_sigmoid_thr(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  sigmoid_thr ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) , *getarg(3) );
 return(_r);
}
 
double sigmoid_sat ( _threadargsprotocomma_ double _lslope , double _lvalue ) {
   double _lsigmoid_sat;
 _lsigmoid_sat = 2.0 / ( 1.0 + pow ( _lslope , - _lvalue ) ) - 1.0 ;
   
return _lsigmoid_sat;
 }
 
static double _hoc_sigmoid_sat(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  sigmoid_sat ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) );
 return(_r);
}
 
static int _ode_count(int _type){ return 9;}
 
static void _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
     _ode_spec1 (_p, _ppvar, _thread, _nt);
 }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 9; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 (_p, _ppvar, _thread, _nt);
 }
 
static void _ode_matsol(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
 _ode_matsol_instance1(_threadargs_);
 }}

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
  A = A0;
  B = B0;
  ach_w = ach_w0;
  ach = ach0;
  da_w = da_w0;
  da = da0;
  heb_da_w = heb_da_w0;
  heb_ach_w = heb_ach_w0;
  learning_w = learning_w0;
 {
   double _ltp ;
 if ( tau1 / tau2 > 0.9999 ) {
     tau1 = 0.9999 * tau2 ;
     }
   if ( tau1 / tau2 < 1e-9 ) {
     tau1 = tau2 * 1e-9 ;
     }
   A = 0.0 ;
   B = 0.0 ;
   _ltp = ( tau1 * tau2 ) / ( tau2 - tau1 ) * log ( tau2 / tau1 ) ;
   factor = - exp ( - _ltp / tau1 ) + exp ( - _ltp / tau2 ) ;
   factor = 1.0 / factor ;
   ltd = 0.0 ;
   ltp = 0.0 ;
   learning_w = 0.0 ;
   ach = 0.0 ;
   ach_w = 0.0 ;
   heb_ach_w = 0.0 ;
   da = 0.0 ;
   da_w = 0.0 ;
   heb_da_w = 0.0 ;
   modulatory_w = 0.0 ;
   last_max_da_w = 1e-9 ;
   }
 
}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _tsav = -1e20;
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
 initmodel(_p, _ppvar, _thread, _nt);
}
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   if ( v - ltd_theshold > 0.0 ) {
     ltd = sigmoid_thr ( _threadargscomma_ learning_slope , v , ltd_sigmoid_half ) ;
     }
   else {
     ltd = 0.0 ;
     }
   if ( v - ltp_theshold > 0.0 ) {
     ltp = sigmoid_thr ( _threadargscomma_ learning_slope , v , ltp_sigmoid_half ) ;
     }
   else {
     ltp = 0.0 ;
     }
   learning_w = learning_w + sigmoid_sat ( _threadargscomma_ learning_slope , ( - ltd + 2.0 * ltp ) / learning_tau ) / 8000.0 ;
   g = B - A ;
   i = g * ( v - e ) ;
   modulatory_w = ( - ach * ( ( last_max_da_w - da ) / last_max_da_w ) + da ) / 1000.0 ;
   w = w + learning_w + modulatory_w ;
   if ( w > 5.0 ) {
     w = 5.0 ;
     }
   if ( w < 0.0 ) {
     w = 0.0001 ;
     }
   }
 _current += i;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
 	}
 _g = (_g - _rhs)/.001;
 _g *=  1.e2/(_nd_area);
 _rhs *= 1.e2/(_nd_area);
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}
 
}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}
 
}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
 {   state(_p, _ppvar, _thread, _nt);
  }}}

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(A) - _p;  _dlist1[0] = &(DA) - _p;
 _slist1[1] = &(B) - _p;  _dlist1[1] = &(DB) - _p;
 _slist1[2] = &(learning_w) - _p;  _dlist1[2] = &(Dlearning_w) - _p;
 _slist1[3] = &(ach) - _p;  _dlist1[3] = &(Dach) - _p;
 _slist1[4] = &(da) - _p;  _dlist1[4] = &(Dda) - _p;
 _slist1[5] = &(ach_w) - _p;  _dlist1[5] = &(Dach_w) - _p;
 _slist1[6] = &(da_w) - _p;  _dlist1[6] = &(Dda_w) - _p;
 _slist1[7] = &(heb_ach_w) - _p;  _dlist1[7] = &(Dheb_ach_w) - _p;
 _slist1[8] = &(heb_da_w) - _p;  _dlist1[8] = &(Dheb_da_w) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "exc_sigma3exp2syn_ach_da.mod";
static const char* nmodl_file_text = 
  "COMMENT\n"
  "Two state kinetic scheme synapse described by rise time tau1,\n"
  "and decay time constant tau2. The normalized peak conductance is 1.\n"
  "Decay time MUST be greater than rise time.\n"
  "\n"
  "The solution of A->G->bath with rate constants 1/tau1 and 1/tau2 is\n"
  " A = a*exp(-t/tau1) and\n"
  " G = a*tau2/(tau2-tau1)*(-exp(-t/tau1) + exp(-t/tau2))\n"
  "	where tau1 < tau2\n"
  "\n"
  "If tau2-tau1 is very small compared to tau1, this is an alphasynapse with time constant tau2.\n"
  "If tau1/tau2 is very small, this is single exponential decay with time constant tau2.\n"
  "\n"
  "The factor is evaluated in the initial block\n"
  "such that an event of weight 1 generates a\n"
  "peak conductance of 1.\n"
  "\n"
  "Because the solution is a sum of exponentials, the\n"
  "coupled equations can be solved as a pair of independent equations\n"
  "by the more efficient cnexp method.\n"
  "\n"
  "Neuromodulatory mechanism:\n"
  "---------------------------\n"
  "All weights must be (0-1). To distinguish general weight, ACh and Da weights from single real value in NET_RECEIVE block\n"
  "it assumes that:\n"
  "* general weight is (0-1)\n"
  "* ACh weight is (1-2)\n"
  "* Da weight is (2-3)\n"
  "\n"
  "Then substraction are performed to distinguish which signal is passed:\n"
  "* general weight - no substraction\n"
  "* ACh weight which fo distinguish purpose is substracted by ach_substractor\n"
  "* Da weight which fo distinguish purpose is substracted by da_substractor\n"
  "\n"
  "The key assumption here is Thread safety, the other approach is to use POINTER (which is not thread safe)\n"
  "and artificial ionic concetration. For more info see discussion:\n"
  "https://www.neuron.yale.edu/phpBB/viewtopic.php?f=31&t=4239\n"
  "\n"
  "ENDCOMMENT\n"
  "\n"
  "NEURON {\n"
  "	POINT_PROCESS ExcSigma3Exp2SynAchDa\n"
  "	RANGE tau1, tau2, e, i\n"
  "\n"
  "	RANGE ach, ach_w, ach_tau, ach_substractor\n"
  "	RANGE da, da_w, da_tau, da_substractor, last_max_da_w\n"
  "	RANGE heb_ach_w, heb_da_w\n"
  "	RANGE modulatory_w\n"
  "\n"
  "	RANGE ltd, ltp, learning_slope, learning_tau\n"
  "	RANGE ltd_sigmoid_half, ltp_threshold\n"
  "	RANGE w, learning_w\n"
  "\n"
  "	NONSPECIFIC_CURRENT i\n"
  "\n"
  "	RANGE g\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(nA) = (nanoamp)\n"
  "	(mV) = (millivolt)\n"
  "	(uS) = (microsiemens)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	tau1 = 0.1 (ms) <1e-9,1e9>\n"
  "	tau2 = 10 (ms) <1e-9,1e9>\n"
  "	e=0	(mV)\n"
  "\n"
  "    ltd_theshold = -60 (mV) <1e-9,1e9>\n"
  "	ltp_theshold = -45 (mV) <1e-9,1e9>\n"
  "\n"
  "    ltd_sigmoid_half = -55 (mV) <1e-9,1e9>\n"
  "	ltp_sigmoid_half = -40 (mV) <1e-9,1e9>\n"
  "\n"
  "	learning_slope = 1.3\n"
  "	learning_tau = 20\n"
  "	w = 1.0\n"
  "\n"
  "	ach_tau = 10 (ms) <1e-9,1e9>\n"
  "	da_tau = 10 (ms) <1e-9,1e9>\n"
  "	ach_substractor = 1 <1e-9,1e9> : value to distinguish ACh stimulation\n"
  "	da_substractor = 2 <1e-9,1e9> : value to distinguish Da stimulation\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	v (mV)\n"
  "	i (nA)\n"
  "	g (uS)\n"
  "	factor\n"
  "\n"
  "	ltd\n"
  "	ltp\n"
  "	last_max_da_w\n"
  "	modulatory_w\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	A (uS)\n"
  "	B (uS)\n"
  "\n"
  "	ach (uS)\n"
  "	da (uS)\n"
  "	learning_w\n"
  "\n"
  "	ach_w\n"
  "	heb_ach_w\n"
  "\n"
  "	da_w\n"
  "	heb_da_w\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	LOCAL tp\n"
  "	if (tau1/tau2 > 0.9999) {\n"
  "		tau1 = 0.9999*tau2\n"
  "	}\n"
  "	if (tau1/tau2 < 1e-9) {\n"
  "		tau1 = tau2*1e-9\n"
  "	}\n"
  "	A = 0\n"
  "	B = 0\n"
  "	tp = (tau1*tau2)/(tau2 - tau1) * log(tau2/tau1)\n"
  "	factor = -exp(-tp/tau1) + exp(-tp/tau2)\n"
  "	factor = 1/factor\n"
  "\n"
  "    ltd = 0\n"
  "	ltp = 0\n"
  "	learning_w = 0\n"
  "\n"
  "	ach = 0\n"
  "	ach_w = 0\n"
  "	heb_ach_w = 0\n"
  "\n"
  "	da = 0\n"
  "	da_w = 0\n"
  "	heb_da_w = 0\n"
  "\n"
  "    modulatory_w = 0\n"
  "	last_max_da_w = 1e-9 : must be initialized as nonzero\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "    if(v-ltd_theshold > 0) {\n"
  "        ltd = sigmoid_thr(learning_slope, v, ltd_sigmoid_half)\n"
  "    } else {\n"
  "        ltd = 0\n"
  "    }\n"
  "    if(v-ltp_theshold > 0) {\n"
  "	    ltp = sigmoid_thr(learning_slope, v, ltp_sigmoid_half)\n"
  "	} else {\n"
  "	    ltp = 0\n"
  "	}\n"
  "\n"
  "	learning_w = learning_w + sigmoid_sat(learning_slope, (-ltd + 2 * ltp) / learning_tau)/8000\n"
  "\n"
  "	SOLVE state METHOD cnexp\n"
  "	g = B - A\n"
  "	i = g*(v - e)\n"
  "\n"
  "    modulatory_w = (- ach * ((last_max_da_w-da)/last_max_da_w) + da)/1000\n"
  "    w = w + learning_w + modulatory_w\n"
  "\n"
  "	if (w > 5) {\n"
  "	    w = 5\n"
  "	}\n"
  "	if (w < 0) {\n"
  "	    w = 0.0001\n"
  "	}\n"
  "}\n"
  "\n"
  "DERIVATIVE state {\n"
  "	A' = -A/tau1\n"
  "	B' = -B/tau2\n"
  "	learning_w' = -learning_w/4\n"
  "\n"
  "	ach' = -ach/ach_tau\n"
  "	da' = -da/da_tau\n"
  "\n"
  "	ach_w' = -ach_w/ach_tau\n"
  "	da_w' = -da_w/da_tau\n"
  "\n"
  "	heb_ach_w' = -heb_ach_w/ach_tau\n"
  "	heb_da_w' = -heb_da_w/da_tau\n"
  "}\n"
  "\n"
  ": All weights must be (0-1)\n"
  "NET_RECEIVE(weight (uS)) {\n"
  "    : Da check must be checked before ACh check and Exp2Syn check since da_substractor=2 and ach_substractor=1\n"
  "    if (weight-da_substractor > 0) { : Da stim.\n"
  "        da_w = weight-da_substractor\n"
  "        if (da_w > 1) {\n"
  "            da_w = 1\n"
  "        }\n"
  "        last_max_da_w = da_w\n"
  "\n"
  "        if (heb_da_w > 0) {\n"
  "            da = heb_da_w * da_w\n"
  "            heb_da_w = 0\n"
  "        }\n"
  "\n"
  "    } else if (weight-ach_substractor > 0) { : ACh stim\n"
  "        ach_w = weight-ach_substractor\n"
  "        if (ach_w > 1) {\n"
  "            ach_w = 1\n"
  "        }\n"
  "\n"
  "        if (heb_ach_w > 0) {\n"
  "            ach = heb_ach_w * ach_w\n"
  "            heb_ach_w = 0\n"
  "        }\n"
  "\n"
  "    } else { : Ex2Syn stim\n"
  "        A = A + weight*factor\n"
  "        B = B + weight*factor\n"
  "\n"
  "        if (ach_w > 0) {\n"
  "            ach = ach_w\n"
  "            ach_w = 0\n"
  "        }\n"
  "        if (da_w > 0) {\n"
  "            da = da_w\n"
  "            da_w = 0\n"
  "        }\n"
  "\n"
  "        heb_ach_w = 1\n"
  "        heb_da_w = 1\n"
  "    }\n"
  "}\n"
  "\n"
  ": sigmoid with threshold\n"
  "FUNCTION sigmoid_thr(slope, value, thr) {\n"
  "    sigmoid_thr = 1 / (1.0 + pow(slope, -(value-thr)))\n"
  "}\n"
  "\n"
  ": sigmoidal saturation\n"
  "FUNCTION sigmoid_sat(slope, value) {\n"
  "    sigmoid_sat = 2.0 / (1.0 + pow(slope, -value)) - 1.0 : [-1 move down to -1; 2: move up to 1]\n"
  "}\n"
  ;
#endif
