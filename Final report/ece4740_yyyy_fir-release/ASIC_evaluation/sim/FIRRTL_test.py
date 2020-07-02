#=========================================================================
# IntMulStageRTL_test
#=========================================================================

import pytest
import random

random.seed(0xdeadbeef)

from pymtl3                               import *
from pymtl3.passes                        import TracingConfigs
from pymtl3.stdlib.test                   import mk_test_case_table
from pymtl3.stdlib.test                   import run_test_vector_sim, config_model
from lab2_xcel.FIRRTL                     import FIRRTL

from pymtl3.passes.backends.verilog import \
    VerilatorImportConfigs, TranslationConfigs
import math

#----------------------------------------------------------------------
# Test Case: sine wave
#----------------------------------------------------------------------


def sine_gen(freq,fs,fbits):
  blist = [0,0,0,0]
  fbits_b = 6
  blist_fp = [  0.138336181640625,
                0.354217529296875,
                0.354217529296875,
                0.138336181640625,]
  for i in range(4):
    # convert to integer-represented fixed-point
    a = blist_fp[i]*(2**fbits_b)
    (b,a) = math.modf(a)
    blist[i] = int(a)
  msg_list = [('data_in b0 b1 b2 b3'),]
  N = math.ceil(4*fs/freq)
  for n in range(N):
    # sample value
    value = 1 + math.sin(2*math.pi*freq*n/fs)
    # convert to integer-represented fixed-point
    a = value*(2**8)
    (b,a) = math.modf(a)
    value = int(a)
                   #                        name  XXXX  RST_N
    msg_list.append([value, blist[0], blist[1], blist[2], blist[3]])
  return msg_list

#-------------------------------------------------------------------------
# Test Case Table
#-------------------------------------------------------------------------
test_case_table = mk_test_case_table([
  (                  "msgs"),
  [ "sine_wave",      sine_gen(10.0, 100.0, 10)],
])

#-------------------------------------------------------------------------
# TestHarness
#-------------------------------------------------------------------------

@pytest.mark.parametrize( **test_case_table )
def test( test_params, dump_vcd, test_verilog ):
  msgs  = test_params.msgs
  run_test_vector_sim( FIRRTL(), msgs, dump_vcd )
