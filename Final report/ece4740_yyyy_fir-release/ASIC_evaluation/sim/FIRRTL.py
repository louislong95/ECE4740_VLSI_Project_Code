#=========================================================================
# Wrapper for a Verilog FIR
#=========================================================================

from pymtl3 import *
from pymtl3.passes.backends.verilog import \
    VerilogPlaceholderConfigs, VerilatorImportConfigs, TranslationConfigs

class FIRRTL( Placeholder, Component ):

  # Constructor

  def construct( s ):

    # Interface
    s.clk     = InPort  ()
    s.reset   = InPort  ()
    s.data_in = InPort  (Bits16)
    s.b0      = InPort  (Bits8)
    s.b1      = InPort  (Bits8)
    s.b2      = InPort  (Bits8)
    s.b3      = InPort  (Bits8)

    s.y       = OutPort (Bits16)

    # Configurations

    from os import path
    s.config_placeholder = VerilogPlaceholderConfigs(
      src_file   = path.dirname(__file__) + '/FIRRTL.v',
      top_module = 'lab2_FIRRTL',
      has_clk    = True,
      has_reset  = True,
    )