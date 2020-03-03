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
 
#define nrn_init _nrn_init__Syn4P
#define _nrn_initial _nrn_initial__Syn4P
#define nrn_cur _nrn_cur__Syn4P
#define _nrn_current _nrn_current__Syn4P
#define nrn_jacob _nrn_jacob__Syn4P
#define nrn_state _nrn_state__Syn4P
#define _net_receive _net_receive__Syn4P 
#define state state__Syn4P 
 
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
#define tau_a _p[0]
#define tau_b _p[1]
#define e _p[2]
#define w_pre_init _p[3]
#define w_post_init _p[4]
#define s_ampa _p[5]
#define s_nmda _p[6]
#define tau_G_a _p[7]
#define tau_G_b _p[8]
#define m_G _p[9]
#define A_LTD_pre _p[10]
#define A_LTP_pre _p[11]
#define A_LTD_post _p[12]
#define A_LTP_post _p[13]
#define tau_u_T _p[14]
#define theta_u_T _p[15]
#define m_T _p[16]
#define theta_u_N _p[17]
#define tau_Z_a _p[18]
#define tau_Z_b _p[19]
#define m_Z _p[20]
#define tau_N_alpha _p[21]
#define tau_N_beta _p[22]
#define m_N_alpha _p[23]
#define m_N_beta _p[24]
#define theta_N_X _p[25]
#define theta_u_C _p[26]
#define theta_C_minus _p[27]
#define theta_C_plus _p[28]
#define tau_K_alpha _p[29]
#define tau_K_gamma _p[30]
#define m_K_alpha _p[31]
#define m_K_beta _p[32]
#define s_K_beta _p[33]
#define i _p[34]
#define w_pre _p[35]
#define w_post _p[36]
#define w _p[37]
#define A _p[38]
#define B _p[39]
#define G_a _p[40]
#define G_b _p[41]
#define u_bar _p[42]
#define K_alpha_bar _p[43]
#define K_gamma _p[44]
#define Z_a _p[45]
#define Z_b _p[46]
#define N_alpha_bar _p[47]
#define N_beta_bar _p[48]
#define g _p[49]
#define g_ampa _p[50]
#define g_nmda _p[51]
#define epsilon _p[52]
#define epsilon_G _p[53]
#define epsilon_Z _p[54]
#define C _p[55]
#define T _p[56]
#define G _p[57]
#define E _p[58]
#define P _p[59]
#define K_alpha _p[60]
#define Rho _p[61]
#define K_beta _p[62]
#define K _p[63]
#define N _p[64]
#define X _p[65]
#define Z _p[66]
#define flag_D _p[67]
#define A_n _p[68]
#define B_n _p[69]
#define last_weight _p[70]
#define DA _p[71]
#define DB _p[72]
#define DG_a _p[73]
#define DG_b _p[74]
#define Du_bar _p[75]
#define DK_alpha_bar _p[76]
#define DK_gamma _p[77]
#define DZ_a _p[78]
#define DZ_b _p[79]
#define DN_alpha_bar _p[80]
#define DN_beta_bar _p[81]
#define v _p[82]
#define _g _p[83]
#define _tsav _p[84]
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
 static double _hoc_mgblock();
 static double _hoc_positive();
 static double _hoc_sigmoid_sat();
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
 "mgblock", _hoc_mgblock,
 "positive", _hoc_positive,
 "sigmoid_sat", _hoc_sigmoid_sat,
 0, 0
};
#define mgblock mgblock_Syn4P
#define positive positive_Syn4P
#define sigmoid_sat sigmoid_sat_Syn4P
 extern double mgblock( _threadargsprotocomma_ double );
 extern double positive( _threadargsprotocomma_ double );
 extern double sigmoid_sat( _threadargsprotocomma_ double , double );
 /* declare global and static user variables */
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 "tau_K_gamma", 1e-009, 1e+009,
 "tau_K_alpha", 1e-009, 1e+009,
 "tau_N_beta", 1e-009, 1e+009,
 "tau_N_alpha", 1e-009, 1e+009,
 "tau_Z_b", 1e-009, 1e+009,
 "tau_Z_a", 1e-009, 1e+009,
 "tau_u_T", 1e-009, 1e+009,
 "tau_G_b", 1e-009, 1e+009,
 "tau_G_a", 1e-009, 1e+009,
 "tau_b", 1e-009, 1e+009,
 "tau_a", 1e-009, 1e+009,
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "tau_a", "ms",
 "tau_b", "ms",
 "e", "mV",
 "tau_G_a", "ms",
 "tau_G_b", "ms",
 "tau_u_T", "ms",
 "tau_Z_a", "ms",
 "tau_Z_b", "ms",
 "tau_N_alpha", "ms",
 "tau_N_beta", "ms",
 "tau_K_alpha", "ms",
 "tau_K_gamma", "ms",
 "A", "uS",
 "B", "uS",
 "i", "nA",
 0,0
};
 static double A0 = 0;
 static double B0 = 0;
 static double G_b0 = 0;
 static double G_a0 = 0;
 static double K_gamma0 = 0;
 static double K_alpha_bar0 = 0;
 static double N_beta_bar0 = 0;
 static double N_alpha_bar0 = 0;
 static double Z_b0 = 0;
 static double Z_a0 = 0;
 static double delta_t = 0.01;
 static double u_bar0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
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
"Syn4P",
 "tau_a",
 "tau_b",
 "e",
 "w_pre_init",
 "w_post_init",
 "s_ampa",
 "s_nmda",
 "tau_G_a",
 "tau_G_b",
 "m_G",
 "A_LTD_pre",
 "A_LTP_pre",
 "A_LTD_post",
 "A_LTP_post",
 "tau_u_T",
 "theta_u_T",
 "m_T",
 "theta_u_N",
 "tau_Z_a",
 "tau_Z_b",
 "m_Z",
 "tau_N_alpha",
 "tau_N_beta",
 "m_N_alpha",
 "m_N_beta",
 "theta_N_X",
 "theta_u_C",
 "theta_C_minus",
 "theta_C_plus",
 "tau_K_alpha",
 "tau_K_gamma",
 "m_K_alpha",
 "m_K_beta",
 "s_K_beta",
 0,
 "i",
 "w_pre",
 "w_post",
 "w",
 0,
 "A",
 "B",
 "G_a",
 "G_b",
 "u_bar",
 "K_alpha_bar",
 "K_gamma",
 "Z_a",
 "Z_b",
 "N_alpha_bar",
 "N_beta_bar",
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
 	_p = nrn_prop_data_alloc(_mechtype, 85, _prop);
 	/*initialize range parameters*/
 	tau_a = 0.2;
 	tau_b = 2;
 	e = 0;
 	w_pre_init = 0.5;
 	w_post_init = 2;
 	s_ampa = 0.5;
 	s_nmda = 0.5;
 	tau_G_a = 2;
 	tau_G_b = 50;
 	m_G = 10;
 	A_LTD_pre = 8.5e-007;
 	A_LTP_pre = 8.5e-007;
 	A_LTD_post = 3.6e-007;
 	A_LTP_post = 5.5e-005;
 	tau_u_T = 10;
 	theta_u_T = -60;
 	m_T = 1.7;
 	theta_u_N = -30;
 	tau_Z_a = 1;
 	tau_Z_b = 15;
 	m_Z = 6;
 	tau_N_alpha = 7.5;
 	tau_N_beta = 30;
 	m_N_alpha = 2;
 	m_N_beta = 10;
 	theta_N_X = 0.2;
 	theta_u_C = -68;
 	theta_C_minus = 15;
 	theta_C_plus = 35;
 	tau_K_alpha = 15;
 	tau_K_gamma = 20;
 	m_K_alpha = 1.5;
 	m_K_beta = 1.7;
 	s_K_beta = 100;
  }
 	_prop->param = _p;
 	_prop->param_size = 85;
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

 void _syn_4p_reg() {
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
  hoc_register_prop_size(_mechtype, 85, 3);
  hoc_register_dparam_semantics(_mechtype, 0, "area");
  hoc_register_dparam_semantics(_mechtype, 1, "pntproc");
  hoc_register_dparam_semantics(_mechtype, 2, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 pnt_receive[_mechtype] = _net_receive;
 pnt_receive_size[_mechtype] = 1;
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 Syn4P C:/Users/Wladek/Documents/GitHub/neuronpp/neuronpp/examples/compiled/mods1/syn_4p.mod\n");
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
 static int _slist1[11], _dlist1[11];
 static int state(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset = 0; {
   double _lD , _lu , _lEta , _lLTD_pre , _lLTP_pre , _lLTD_post , _lLTP_post , _lg_update , _lN_alpha , _lN_beta , _lN ;
 if ( flag_D  == 1.0 ) {
     _lD = 1.0 ;
     flag_D = - 1.0 ;
     }
   else {
     _lD = 0.0 ;
     }
    _lu = v ;
   _lEta = dt ;
    Du_bar = ( - u_bar + positive ( _threadargscomma_ _lu - theta_u_T ) ) / tau_u_T ;
   T = sigmoid_sat ( _threadargscomma_ m_T , u_bar ) ;
   E = _lD * T ;
   DN_alpha_bar = ( - N_alpha_bar + positive ( _threadargscomma_ _lu - theta_u_N ) ) / tau_N_alpha ;
   DN_beta_bar = ( - N_beta_bar + N_alpha_bar ) / tau_N_beta ;
   _lN_alpha = sigmoid_sat ( _threadargscomma_ m_N_alpha , N_alpha_bar ) ;
   _lN_beta = sigmoid_sat ( _threadargscomma_ m_N_beta , N_beta_bar ) ;
   _lN = positive ( _threadargscomma_ _lN_alpha * _lN_beta - theta_N_X ) ;
   X = Z * _lN ;
   C = G * positive ( _threadargscomma_ _lu - theta_u_C ) ;
   P = positive ( _threadargscomma_ C - theta_C_minus ) * positive ( _threadargscomma_ theta_C_plus - C ) / pow ( ( theta_C_plus - theta_C_minus ) / 2.0 , 2.0 ) ;
   K_alpha = sigmoid_sat ( _threadargscomma_ m_K_alpha , positive ( _threadargscomma_ C - theta_C_plus ) ) * Rho ;
   DK_alpha_bar = ( - K_alpha_bar + K_alpha ) / tau_K_alpha ;
   K_beta = sigmoid_sat ( _threadargscomma_ m_K_beta , ( K_alpha_bar * s_K_beta ) ) ;
   Rho = 1.0 - K_beta ;
   DK_gamma = ( - K_gamma + K_beta ) / tau_K_gamma ;
   K = K_alpha * K_beta * K_gamma ;
   _lLTD_pre = - A_LTD_pre * E ;
   _lLTP_pre = A_LTP_pre * X * _lEta ;
   _lLTD_post = - A_LTD_post * P * _lEta ;
   _lLTP_post = A_LTP_post * K * _lEta ;
   w_pre = w_pre + _lLTD_pre + _lLTP_pre ;
   if ( w_pre > 1.0 ) {
     w_pre = 1.0 ;
     }
   if ( w_pre < 0.0 ) {
     w_pre = 0.0 ;
     }
   w_post = w_post + _lLTD_post + _lLTP_post ;
   if ( w_post > 5.0 ) {
     w_post = 5.0 ;
     }
   if ( w_post < 0.0 ) {
     w_post = 0.0 ;
     }
   w = w_pre * w_post ;
   DA = - A / tau_a ;
   DB = - B / tau_b ;
   DG_a = - G_a / tau_G_a ;
   DG_b = - G_b / tau_G_b ;
   A_n = G_a * last_weight ;
   B_n = G_b * last_weight ;
   DZ_a = - Z_a / tau_Z_a ;
   DZ_b = - Z_b / tau_Z_b ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
 double _lD , _lu , _lEta , _lLTD_pre , _lLTP_pre , _lLTD_post , _lLTP_post , _lg_update , _lN_alpha , _lN_beta , _lN ;
 if ( flag_D  == 1.0 ) {
   _lD = 1.0 ;
   flag_D = - 1.0 ;
   }
 else {
   _lD = 0.0 ;
   }
  _lu = v ;
 _lEta = dt ;
  Du_bar = Du_bar  / (1. - dt*( ( ( - 1.0 ) ) / tau_u_T )) ;
 T = sigmoid_sat ( _threadargscomma_ m_T , u_bar ) ;
 E = _lD * T ;
 DN_alpha_bar = DN_alpha_bar  / (1. - dt*( ( ( - 1.0 ) ) / tau_N_alpha )) ;
 DN_beta_bar = DN_beta_bar  / (1. - dt*( ( ( - 1.0 ) ) / tau_N_beta )) ;
 _lN_alpha = sigmoid_sat ( _threadargscomma_ m_N_alpha , N_alpha_bar ) ;
 _lN_beta = sigmoid_sat ( _threadargscomma_ m_N_beta , N_beta_bar ) ;
 _lN = positive ( _threadargscomma_ _lN_alpha * _lN_beta - theta_N_X ) ;
 X = Z * _lN ;
 C = G * positive ( _threadargscomma_ _lu - theta_u_C ) ;
 P = positive ( _threadargscomma_ C - theta_C_minus ) * positive ( _threadargscomma_ theta_C_plus - C ) / pow ( ( theta_C_plus - theta_C_minus ) / 2.0 , 2.0 ) ;
 K_alpha = sigmoid_sat ( _threadargscomma_ m_K_alpha , positive ( _threadargscomma_ C - theta_C_plus ) ) * Rho ;
 DK_alpha_bar = DK_alpha_bar  / (1. - dt*( ( ( - 1.0 ) ) / tau_K_alpha )) ;
 K_beta = sigmoid_sat ( _threadargscomma_ m_K_beta , ( K_alpha_bar * s_K_beta ) ) ;
 Rho = 1.0 - K_beta ;
 DK_gamma = DK_gamma  / (1. - dt*( ( ( - 1.0 ) ) / tau_K_gamma )) ;
 K = K_alpha * K_beta * K_gamma ;
 _lLTD_pre = - A_LTD_pre * E ;
 _lLTP_pre = A_LTP_pre * X * _lEta ;
 _lLTD_post = - A_LTD_post * P * _lEta ;
 _lLTP_post = A_LTP_post * K * _lEta ;
 w_pre = w_pre + _lLTD_pre + _lLTP_pre ;
 if ( w_pre > 1.0 ) {
   w_pre = 1.0 ;
   }
 if ( w_pre < 0.0 ) {
   w_pre = 0.0 ;
   }
 w_post = w_post + _lLTD_post + _lLTP_post ;
 if ( w_post > 5.0 ) {
   w_post = 5.0 ;
   }
 if ( w_post < 0.0 ) {
   w_post = 0.0 ;
   }
 w = w_pre * w_post ;
 DA = DA  / (1. - dt*( ( - 1.0 ) / tau_a )) ;
 DB = DB  / (1. - dt*( ( - 1.0 ) / tau_b )) ;
 DG_a = DG_a  / (1. - dt*( ( - 1.0 ) / tau_G_a )) ;
 DG_b = DG_b  / (1. - dt*( ( - 1.0 ) / tau_G_b )) ;
 A_n = G_a * last_weight ;
 B_n = G_b * last_weight ;
 DZ_a = DZ_a  / (1. - dt*( ( - 1.0 ) / tau_Z_a )) ;
 DZ_b = DZ_b  / (1. - dt*( ( - 1.0 ) / tau_Z_b )) ;
  return 0;
}
 /*END CVODE*/
 static int state (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) { {
   double _lD , _lu , _lEta , _lLTD_pre , _lLTP_pre , _lLTD_post , _lLTP_post , _lg_update , _lN_alpha , _lN_beta , _lN ;
 if ( flag_D  == 1.0 ) {
     _lD = 1.0 ;
     flag_D = - 1.0 ;
     }
   else {
     _lD = 0.0 ;
     }
    _lu = v ;
   _lEta = dt ;
     u_bar = u_bar + (1. - exp(dt*(( ( - 1.0 ) ) / tau_u_T)))*(- ( ( ( positive ( _threadargscomma_ _lu - theta_u_T ) ) ) / tau_u_T ) / ( ( ( - 1.0 ) ) / tau_u_T ) - u_bar) ;
   T = sigmoid_sat ( _threadargscomma_ m_T , u_bar ) ;
   E = _lD * T ;
    N_alpha_bar = N_alpha_bar + (1. - exp(dt*(( ( - 1.0 ) ) / tau_N_alpha)))*(- ( ( ( positive ( _threadargscomma_ _lu - theta_u_N ) ) ) / tau_N_alpha ) / ( ( ( - 1.0 ) ) / tau_N_alpha ) - N_alpha_bar) ;
    N_beta_bar = N_beta_bar + (1. - exp(dt*(( ( - 1.0 ) ) / tau_N_beta)))*(- ( ( ( N_alpha_bar ) ) / tau_N_beta ) / ( ( ( - 1.0 ) ) / tau_N_beta ) - N_beta_bar) ;
   _lN_alpha = sigmoid_sat ( _threadargscomma_ m_N_alpha , N_alpha_bar ) ;
   _lN_beta = sigmoid_sat ( _threadargscomma_ m_N_beta , N_beta_bar ) ;
   _lN = positive ( _threadargscomma_ _lN_alpha * _lN_beta - theta_N_X ) ;
   X = Z * _lN ;
   C = G * positive ( _threadargscomma_ _lu - theta_u_C ) ;
   P = positive ( _threadargscomma_ C - theta_C_minus ) * positive ( _threadargscomma_ theta_C_plus - C ) / pow ( ( theta_C_plus - theta_C_minus ) / 2.0 , 2.0 ) ;
   K_alpha = sigmoid_sat ( _threadargscomma_ m_K_alpha , positive ( _threadargscomma_ C - theta_C_plus ) ) * Rho ;
    K_alpha_bar = K_alpha_bar + (1. - exp(dt*(( ( - 1.0 ) ) / tau_K_alpha)))*(- ( ( ( K_alpha ) ) / tau_K_alpha ) / ( ( ( - 1.0 ) ) / tau_K_alpha ) - K_alpha_bar) ;
   K_beta = sigmoid_sat ( _threadargscomma_ m_K_beta , ( K_alpha_bar * s_K_beta ) ) ;
   Rho = 1.0 - K_beta ;
    K_gamma = K_gamma + (1. - exp(dt*(( ( - 1.0 ) ) / tau_K_gamma)))*(- ( ( ( K_beta ) ) / tau_K_gamma ) / ( ( ( - 1.0 ) ) / tau_K_gamma ) - K_gamma) ;
   K = K_alpha * K_beta * K_gamma ;
   _lLTD_pre = - A_LTD_pre * E ;
   _lLTP_pre = A_LTP_pre * X * _lEta ;
   _lLTD_post = - A_LTD_post * P * _lEta ;
   _lLTP_post = A_LTP_post * K * _lEta ;
   w_pre = w_pre + _lLTD_pre + _lLTP_pre ;
   if ( w_pre > 1.0 ) {
     w_pre = 1.0 ;
     }
   if ( w_pre < 0.0 ) {
     w_pre = 0.0 ;
     }
   w_post = w_post + _lLTD_post + _lLTP_post ;
   if ( w_post > 5.0 ) {
     w_post = 5.0 ;
     }
   if ( w_post < 0.0 ) {
     w_post = 0.0 ;
     }
   w = w_pre * w_post ;
    A = A + (1. - exp(dt*(( - 1.0 ) / tau_a)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_a ) - A) ;
    B = B + (1. - exp(dt*(( - 1.0 ) / tau_b)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_b ) - B) ;
    G_a = G_a + (1. - exp(dt*(( - 1.0 ) / tau_G_a)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_G_a ) - G_a) ;
    G_b = G_b + (1. - exp(dt*(( - 1.0 ) / tau_G_b)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_G_b ) - G_b) ;
   A_n = G_a * last_weight ;
   B_n = G_b * last_weight ;
    Z_a = Z_a + (1. - exp(dt*(( - 1.0 ) / tau_Z_a)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_Z_a ) - Z_a) ;
    Z_b = Z_b + (1. - exp(dt*(( - 1.0 ) / tau_Z_b)))*(- ( 0.0 ) / ( ( - 1.0 ) / tau_Z_b ) - Z_b) ;
   }
  return 0;
}
 
static void _net_receive (_pnt, _args, _lflag) Point_process* _pnt; double* _args; double _lflag; 
{  double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _thread = (Datum*)0; _nt = (_NrnThread*)_pnt->_vnt;   _p = _pnt->_prop->param; _ppvar = _pnt->_prop->dparam;
  if (_tsav > t){ extern char* hoc_object_name(); hoc_execerror(hoc_object_name(_pnt->ob), ":Event arrived out of order. Must call ParallelContext.set_maxstep AFTER assigning minimum NetCon.delay");}
 _tsav = t; {
     if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = A;
    double __primary = (A + _args[0] * epsilon) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / tau_a ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / tau_a ) - __primary );
    A += __primary;
  } else {
 A = A + _args[0] * epsilon ;
     }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = B;
    double __primary = (B + _args[0] * epsilon) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / tau_b ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / tau_b ) - __primary );
    B += __primary;
  } else {
 B = B + _args[0] * epsilon ;
     }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = G_a;
    double __primary = (G_a + epsilon_G) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / tau_G_a ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / tau_G_a ) - __primary );
    G_a += __primary;
  } else {
 G_a = G_a + epsilon_G ;
     }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = G_b;
    double __primary = (G_b + epsilon_G) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / tau_G_b ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / tau_G_b ) - __primary );
    G_b += __primary;
  } else {
 G_b = G_b + epsilon_G ;
     }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = Z_a;
    double __primary = (Z_a + epsilon_Z) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / tau_Z_a ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / tau_Z_a ) - __primary );
    Z_a += __primary;
  } else {
 Z_a = Z_a + epsilon_Z ;
     }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = Z_b;
    double __primary = (Z_b + epsilon_Z) - __state;
     __primary += ( 1. - exp( 0.5*dt*( ( - 1.0 ) / tau_Z_b ) ) )*( - ( 0.0 ) / ( ( - 1.0 ) / tau_Z_b ) - __primary );
    Z_b += __primary;
  } else {
 Z_b = Z_b + epsilon_Z ;
     }
 flag_D = 1.0 ;
   last_weight = _args[0] ;
   } }
 
double positive ( _threadargsprotocomma_ double _lvalue ) {
   double _lpositive;
 if ( _lvalue < 0.0 ) {
     _lpositive = 0.0 ;
     }
   else {
     _lpositive = _lvalue ;
     }
   
return _lpositive;
 }
 
static double _hoc_positive(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  positive ( _p, _ppvar, _thread, _nt, *getarg(1) );
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
 
double mgblock ( _threadargsprotocomma_ double _lv ) {
   double _lmgblock;
 double _lu ;
  _lu = _lv ;
    _lmgblock = 1.0 / ( 1.0 + exp ( 0.080 * - _lu ) * ( 1.0 / 3.57 ) ) ;
   
return _lmgblock;
 }
 
static double _hoc_mgblock(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  mgblock ( _p, _ppvar, _thread, _nt, *getarg(1) );
 return(_r);
}
 
static int _ode_count(int _type){ return 11;}
 
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
	for (_i=0; _i < 11; ++_i) {
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
  G_b = G_b0;
  G_a = G_a0;
  K_gamma = K_gamma0;
  K_alpha_bar = K_alpha_bar0;
  N_beta_bar = N_beta_bar0;
  N_alpha_bar = N_alpha_bar0;
  Z_b = Z_b0;
  Z_a = Z_a0;
  u_bar = u_bar0;
 {
   double _lomega , _lomega_G , _lomega_Z ;
 g = 0.0 ;
   g_ampa = 0.0 ;
   g_nmda = 0.0 ;
   u_bar = 0.0 ;
   K_alpha_bar = 0.0 ;
   K_gamma = 0.0 ;
   flag_D = - 1.0 ;
   N_alpha_bar = 0.0 ;
   N_beta_bar = 0.0 ;
   w_pre = w_pre_init ;
   w_post = w_post_init ;
   w = w_pre * w_post ;
   last_weight = 0.0 ;
   if ( tau_a / tau_b > .9999 ) {
     tau_a = .9999 * tau_b ;
     }
   A = 0.0 ;
   B = 0.0 ;
   _lomega = ( tau_a * tau_b ) / ( tau_b - tau_a ) * log ( tau_b / tau_a ) ;
   epsilon = - exp ( - _lomega / tau_a ) + exp ( - _lomega / tau_b ) ;
   epsilon = 1.0 / epsilon ;
   if ( tau_G_a / tau_G_b > .9999 ) {
     tau_G_a = .9999 * tau_G_b ;
     }
   G_a = 0.0 ;
   G_b = 0.0 ;
   _lomega_G = ( tau_G_a * tau_G_b ) / ( tau_G_b - tau_G_a ) * log ( tau_G_b / tau_G_a ) ;
   epsilon_G = - exp ( - _lomega_G / tau_G_a ) + exp ( - _lomega_G / tau_G_b ) ;
   epsilon_G = 1.0 / epsilon_G ;
   if ( tau_Z_a / tau_Z_b > .9999 ) {
     tau_Z_a = .9999 * tau_Z_b ;
     }
   Z_a = 0.0 ;
   Z_b = 0.0 ;
   _lomega_Z = ( tau_Z_a * tau_Z_b ) / ( tau_Z_b - tau_Z_a ) * log ( tau_Z_b / tau_Z_a ) ;
   epsilon_Z = - exp ( - _lomega_Z / tau_Z_a ) + exp ( - _lomega_Z / tau_Z_b ) ;
   epsilon_Z = 1.0 / epsilon_Z ;
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
   G = sigmoid_sat ( _threadargscomma_ m_G , G_b - G_a ) ;
   Z = sigmoid_sat ( _threadargscomma_ m_Z , Z_b - Z_a ) ;
   g_ampa = s_ampa * w_post * ( B - A ) ;
   g_nmda = s_nmda * w_post_init * ( B_n - A_n ) * mgblock ( _threadargscomma_ v ) ;
   g = w_pre * ( g_ampa + g_nmda ) ;
   i = g * ( v - e ) ;
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
 _slist1[0] = &(u_bar) - _p;  _dlist1[0] = &(Du_bar) - _p;
 _slist1[1] = &(N_alpha_bar) - _p;  _dlist1[1] = &(DN_alpha_bar) - _p;
 _slist1[2] = &(N_beta_bar) - _p;  _dlist1[2] = &(DN_beta_bar) - _p;
 _slist1[3] = &(K_alpha_bar) - _p;  _dlist1[3] = &(DK_alpha_bar) - _p;
 _slist1[4] = &(K_gamma) - _p;  _dlist1[4] = &(DK_gamma) - _p;
 _slist1[5] = &(A) - _p;  _dlist1[5] = &(DA) - _p;
 _slist1[6] = &(B) - _p;  _dlist1[6] = &(DB) - _p;
 _slist1[7] = &(G_a) - _p;  _dlist1[7] = &(DG_a) - _p;
 _slist1[8] = &(G_b) - _p;  _dlist1[8] = &(DG_b) - _p;
 _slist1[9] = &(Z_a) - _p;  _dlist1[9] = &(DZ_a) - _p;
 _slist1[10] = &(Z_b) - _p;  _dlist1[10] = &(DZ_b) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "syn_4p.mod";
static const char* nmodl_file_text = 
  "COMMENT\n"
  "Implementation of a four-pathway phenomenological synaptic plasticity rule\n"
  "See Ebner et al. (2019)\n"
  "https://doi.org/10.1016/j.celrep.2019.11.068\n"
  "ENDCOMMENT\n"
  "\n"
  "NEURON {\n"
  "	POINT_PROCESS Syn4P\n"
  "	: Parameters & variables of the original Exp2Syn\n"
  "	RANGE tau_a, tau_b, e, i\n"
  "\n"
  "	NONSPECIFIC_CURRENT i\n"
  "	: Parameters & variables of the plasticity rule\n"
  "	RANGE A_LTD_pre, A_LTP_pre, A_LTD_post, A_LTP_post\n"
  "	RANGE tau_G_a, tau_G_b, m_G\n"
  "	RANGE w_pre, w_post, w_pre_init, w_post_init, w\n"
  "	RANGE s_ampa, s_nmda\n"
  "	\n"
  "	RANGE tau_u_T, theta_u_T, m_T\n"
  "	RANGE theta_u_N, tau_Z_a, tau_Z_b, m_Z, tau_N_alpha, tau_N_beta, m_N_alpha, m_N_beta, theta_N_X\n"
  "	RANGE theta_u_C, theta_C_minus, theta_C_plus, tau_K_alpha, tau_K_gamma, m_K_alpha, m_K_beta, s_K_beta\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(nA) = (nanoamp)\n"
  "	(mV) = (millivolt)\n"
  "	(uS) = (microsiemens)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	: Parameters of the original Exp2Syn\n"
  "	tau_a = 0.2 (ms) <1e-9,1e9>			: time constant of EPSP rise // used for AMPAR currents\n"
  "	tau_b = 2 (ms) <1e-9,1e9>			: time constant of EPSP decay\n"
  "	e = 0 (mV)							: reversal potential\n"
  "	\n"
  "	w_pre_init = 0.5					: pre factor initial value\n"
  "	w_post_init = 2.0					: post factor initial value\n"
  "	\n"
  "	s_ampa = 0.5						: contribution of AMPAR currents\n"
  "	s_nmda = 0.5						: contribution of NMDAR currents\n"
  "\n"
  "	: Parameters of the plasticity rule\n"
  "	tau_G_a = 2 (ms) <1e-9,1e9>			: time constant of presynaptic event G (rise) // also used for NMDAR currents\n"
  "	tau_G_b = 50 (ms) <1e-9,1e9>		: time constant of presynaptic event G (decay)\n"
  "	m_G = 10							: slope of the saturation function for G\n"
  "	\n"
  "	A_LTD_pre = 8.5e-7					: amplitude of pre-LTD\n"
  "	A_LTP_pre = 8.5e-7					: amplitude of pre-LTP\n"
  "	A_LTD_post = 3.6e-7					: amplitude of post-LTD\n"
  "	A_LTP_post = 5.5e-5					: amplitude of post-LTP\n"
  "	\n"
  "	tau_u_T = 10 (ms) <1e-9,1e9>		: time constant for filtering u to calculate T\n"
  "	theta_u_T = -60						: voltage threshold applied to u to calculate T\n"
  "	m_T = 1.7							: slope of the saturation function for T\n"
  "	\n"
  "	theta_u_N = -30						: voltage threshold applied to u to calculate N\n"
  "	tau_Z_a = 1	(ms) <1e-9,1e9>			: time constant of presynaptic event Z (rise)\n"
  "	tau_Z_b = 15 (ms) <1e-9,1e9>		: time constant of presynaptic event Z (decay)\n"
  "	m_Z = 6								: slope of the saturation function for Z\n"
  "	tau_N_alpha = 7.5 (ms) <1e-9,1e9>	: time constant for calculating N-alpha\n"
  "	tau_N_beta = 30	(ms) <1e-9,1e9>		: time constant for calculating N-beta\n"
  "	m_N_alpha = 2						: slope of the saturation function for N_alpha\n"
  "	m_N_beta = 10						: slope of the saturation function for N_beta\n"
  "	theta_N_X = 0.2						: threshold for N to calculate X\n"
  "	\n"
  "	theta_u_C = -68						: voltage threshold applied to u to calculate C\n"
  "	theta_C_minus = 15					: threshold applied to C for post-LTD (P activation)\n"
  "	theta_C_plus = 35					: threshold applied to C for post-LTP (K-alpha activation)\n"
  "	tau_K_alpha = 15 (ms) <1e-9,1e9>	: time constant for filtering K_alpha to calculate K_alpha_bar\n"
  "	tau_K_gamma = 20 (ms) <1e-9,1e9>	: time constant for filtering K_beta to calculate K_gamma\n"
  "	m_K_alpha = 1.5						: slope of the saturation function for K_alpha\n"
  "	m_K_beta = 1.7						: slope of the saturation function for K_beta\n"
  "	s_K_beta = 100						: scaling factor for calculation of K_beta\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	v (mV)\n"
  "	i (nA)\n"
  "	g (uS)\n"
  "	g_ampa (uS)\n"
  "	g_nmda (uS)\n"
  "	epsilon\n"
  "	epsilon_G\n"
  "	epsilon_Z\n"
  "	C\n"
  "	T\n"
  "	G\n"
  "	E\n"
  "	P\n"
  "	K_alpha\n"
  "	Rho\n"
  "	K_beta\n"
  "	K\n"
  "	N\n"
  "	X\n"
  "	Z\n"
  "	flag_D\n"
  "	w_pre\n"
  "	w_post\n"
  "	w\n"
  "	A_n\n"
  "	B_n\n"
  "	last_weight\n"
  "}\n"
  "\n"
  "STATE {\n"
  "	A (uS)\n"
  "	B (uS)\n"
  "	G_a\n"
  "	G_b\n"
  "	u_bar\n"
  "	K_alpha_bar\n"
  "	K_gamma\n"
  "	Z_a\n"
  "	Z_b\n"
  "	N_alpha_bar\n"
  "	N_beta_bar\n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "	LOCAL omega, omega_G, omega_Z\n"
  "	g = 0\n"
  "	g_ampa = 0\n"
  "	g_nmda = 0\n"
  "	u_bar = 0\n"
  "	K_alpha_bar = 0\n"
  "	K_gamma = 0\n"
  "	flag_D = -1\n"
  "	N_alpha_bar = 0\n"
  "	N_beta_bar = 0\n"
  "	w_pre = w_pre_init\n"
  "	w_post = w_post_init\n"
  "	w = w_pre * w_post\n"
  "	last_weight = 0\n"
  "	\n"
  "	: Calculations taken from the original Exp2Syn\n"
  "	: AMPAR-EPSP\n"
  "	if (tau_a/tau_b > .9999) {\n"
  "		tau_a = .9999*tau_b\n"
  "	}\n"
  "	A = 0\n"
  "	B = 0\n"
  "	omega = (tau_a*tau_b)/(tau_b - tau_a) * log(tau_b/tau_a)\n"
  "	epsilon = -exp(-omega/tau_a) + exp(-omega/tau_b)\n"
  "	epsilon = 1/epsilon\n"
  "	\n"
  "	: G\n"
  "	if (tau_G_a/tau_G_b > .9999) {\n"
  "		tau_G_a = .9999*tau_G_b\n"
  "	}\n"
  "	G_a = 0\n"
  "	G_b = 0\n"
  "	omega_G = (tau_G_a*tau_G_b)/(tau_G_b - tau_G_a) * log(tau_G_b/tau_G_a)\n"
  "	epsilon_G = -exp(-omega_G/tau_G_a) + exp(-omega_G/tau_G_b)\n"
  "	epsilon_G = 1/epsilon_G\n"
  "	\n"
  "	: Z\n"
  "	if (tau_Z_a/tau_Z_b > .9999) {\n"
  "		tau_Z_a = .9999*tau_Z_b\n"
  "	}\n"
  "	Z_a = 0\n"
  "	Z_b = 0\n"
  "	omega_Z = (tau_Z_a*tau_Z_b)/(tau_Z_b - tau_Z_a) * log(tau_Z_b/tau_Z_a)\n"
  "	epsilon_Z = -exp(-omega_Z/tau_Z_a) + exp(-omega_Z/tau_Z_b)\n"
  "	epsilon_Z = 1/epsilon_Z\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE state METHOD cnexp\n"
  "	G = sigmoid_sat(m_G, G_b - G_a)			: G presynaptic signal\n"
  "	Z = sigmoid_sat(m_Z, Z_b - Z_a)			: Z presynaptic signal\n"
  "	\n"
  "	g_ampa = s_ampa * w_post * (B - A)							: AMPAR conductance\n"
  "	g_nmda = s_nmda * w_post_init * (B_n - A_n) * mgblock(v)	: NMDAR conductance\n"
  "	\n"
  "	g = w_pre * (g_ampa + g_nmda)			: average conductance, as w_pre is not actually modeled as a probability\n"
  "	i = g * (v - e)\n"
  "}\n"
  "\n"
  "DERIVATIVE state {\n"
  "	LOCAL D, u, Eta, LTD_pre, LTP_pre, LTD_post, LTP_post, g_update, N_alpha, N_beta, N\n"
  "	\n"
  "	if(flag_D == 1) {	: Check if there is a presynaptic event\n"
  "		D = 1\n"
  "	    flag_D = -1\n"
  "	}\n"
  "	else {\n"
  "	    D = 0\n"
  "	}\n"
  "	\n"
  "	UNITSOFF\n"
  "	u = v		: read local voltage\n"
  "	Eta = dt	: learning rate\n"
  "	UNITSON\n"
  "	\n"
  "	: Calculations for pre-LTD\n"
  "	u_bar' = (- u_bar + positive(u - theta_u_T)) / tau_u_T\n"
  "	T = sigmoid_sat(m_T, u_bar)									\n"
  "	E = D * T													\n"
  "	\n"
  "	: Calculations for pre-LTP\n"
  "	N_alpha_bar' = (- N_alpha_bar + positive(u - theta_u_N)) / tau_N_alpha\n"
  "	N_beta_bar'	= (- N_beta_bar + N_alpha_bar) / tau_N_beta\n"
  "	N_alpha = sigmoid_sat(m_N_alpha, N_alpha_bar)\n"
  "	N_beta = sigmoid_sat(m_N_beta, N_beta_bar)\n"
  "	N = positive(N_alpha * N_beta - theta_N_X)\n"
  "	X = Z * N\n"
  "	\n"
  "	: Calculations for post-LTD\n"
  "	C = G * positive(u - theta_u_C)\n"
  "	P = positive(C - theta_C_minus) * positive(theta_C_plus - C) / pow((theta_C_plus - theta_C_minus) / 2, 2)\n"
  "	\n"
  "	: Calculations for post-LTP\n"
  "	K_alpha = sigmoid_sat(m_K_alpha, positive(C - theta_C_plus)) * Rho\n"
  "	K_alpha_bar' = (- K_alpha_bar + K_alpha) / tau_K_alpha\n"
  "	K_beta = sigmoid_sat(m_K_beta, (K_alpha_bar * s_K_beta))\n"
  "	Rho = 1.0 - K_beta\n"
  "	K_gamma' = (- K_gamma + K_beta) / tau_K_gamma\n"
  "	K = K_alpha * K_beta * K_gamma\n"
  "	\n"
  "	: Pathway outcomes\n"
  "	LTD_pre = - A_LTD_pre * E\n"
  "	LTP_pre	= A_LTP_pre * X * Eta			: apply Eta to make values invariant to changes in dt\n"
  "	LTD_post = - A_LTD_post * P * Eta\n"
  "	LTP_post = A_LTP_post * K * Eta\n"
  "	\n"
  "	: Update weights\n"
  "	w_pre = w_pre + LTD_pre + LTP_pre\n"
  "	if(w_pre > 1.0) {\n"
  "		w_pre = 1.0\n"
  "	}\n"
  "	if(w_pre < 0.0) {\n"
  "		w_pre = 0.0\n"
  "	}\n"
  "	w_post = w_post + LTD_post + LTP_post\n"
  "	if(w_post > 5.0) {\n"
  "		w_post = 5.0\n"
  "	}\n"
  "	if(w_post < 0.0) {\n"
  "		w_post = 0.0\n"
  "	}\n"
  "	w = w_pre * w_post\n"
  "	\n"
  "	A' = -A / tau_a\n"
  "	B' = -B / tau_b\n"
  "	G_a' = -G_a / tau_G_a\n"
  "	G_b' = -G_b / tau_G_b\n"
  "	A_n = G_a * last_weight	: use time course of the G signal to model NMDAR activation\n"
  "	B_n = G_b * last_weight\n"
  "	Z_a' = -Z_a / tau_Z_a\n"
  "	Z_b' = -Z_b / tau_Z_b\n"
  "}\n"
  "\n"
  "NET_RECEIVE(weight (uS)) {\n"
  "	: printf(\"Received weight = %f at t = %f\\n\", weight, t)\n"
  "	A = A + weight * epsilon	: AMPAR component\n"
  "	B = B + weight * epsilon\n"
  "	G_a = G_a + epsilon_G\n"
  "	G_b = G_b + epsilon_G\n"
  "	Z_a = Z_a + epsilon_Z\n"
  "	Z_b = Z_b + epsilon_Z\n"
  "	flag_D = 1\n"
  "	last_weight = weight	: used to scale NMDAR component\n"
  "}\n"
  "\n"
  "FUNCTION positive(value) {	: rectification function\n"
  "	if(value < 0) {\n"
  "		positive = 0\n"
  "	}\n"
  "	else {\n"
  "		positive = value\n"
  "	}\n"
  "}\n"
  "\n"
  "FUNCTION sigmoid_sat(slope, value) {	: sigmoidal saturation\n"
  "	sigmoid_sat = 2.0 / (1.0 + pow(slope, -value)) - 1.0\n"
  "}\n"
  "\n"
  "FUNCTION mgblock(v(mV)) {	: Mg2+ block\n"
  "	LOCAL u\n"
  "	UNITSOFF\n"
  "	u = v\n"
  "	UNITSON\n"
  "	: Modified from Jahr & Stevens (1990)\n"
  "	mgblock = 1 / (1 + exp(0.080 * -u) * (1.0 / 3.57))\n"
  "}\n"
  ;
#endif
