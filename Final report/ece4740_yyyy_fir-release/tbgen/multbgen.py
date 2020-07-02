#=========================================================================
# ECE4740 Multiplier signal_gen Veriloga generator : python multbgen [options]
#=========================================================================
#  -h --help                Display this message
#  -m <module>              Set Module Name
#
# Signal_gen Veriloga generator
# Author : Yixiao Du
# Date : 5/19/2020

import argparse
import os
import sys
import random

class ArgumentParserWithCustomError(argparse.ArgumentParser):
  def error( s, msg = "" ):
    if ( msg ): print("\n ERROR: %s" % msg)
    print("")
    file = open( sys.argv[0] )
    for ( lineno, line ) in enumerate( file ):
      if ( line[0] != '#' ): sys.exit(msg != "")
      print( line[1:].rstrip("\n") )

#------------------------------------------------------------------------
# Standard command line arguments
#------------------------------------------------------------------------
def parse_cmdline():
  p = ArgumentParserWithCustomError( add_help = False )
 
  p.add_argument( "-h", "--help",     action="store_true"     )
  p.add_argument( "-m",               action="store"          )    

  
  opts = p.parse_args()
  if opts.help: p.error()
  return opts

def hex_decode(hbw,val):
  hstr = '0x{0:0{1}X}'.format(val,hbw)
  ret_str = ''
  for i in range(hbw):
    hchar = hstr[i+2]
    if hchar == '0':
      ret_str = '`H0,' + ret_str
    elif hchar == '1':
      ret_str = '`H1,' + ret_str
    elif hchar == '2':
      ret_str = '`H2,' + ret_str
    elif hchar == '3':
      ret_str = '`H3,' + ret_str
    elif hchar == '4':
      ret_str = '`H4,' + ret_str
    elif hchar == '5':
      ret_str = '`H5,' + ret_str
    elif hchar == '6':
      ret_str = '`H6,' + ret_str
    elif hchar == '7':
      ret_str = '`H7,' + ret_str
    elif hchar == '8':
      ret_str = '`H8,' + ret_str
    elif hchar == '9':
      ret_str = '`H9,' + ret_str
    elif hchar == 'A':
      ret_str = '`HA,' + ret_str
    elif hchar == 'B':
      ret_str = '`HB,' + ret_str
    elif hchar == 'C':
      ret_str = '`HC,' + ret_str
    elif hchar == 'D':
      ret_str = '`HD,' + ret_str
    elif hchar == 'E':
      ret_str = '`HE,' + ret_str
    elif hchar == 'F':
      ret_str = '`HF,' + ret_str
    else :
      print('[ERROR] Unsupported Hexdicemal Value!')
      raise ValueError
  return '{' + ret_str[:-1] + '};'


def puts_header(output_file):
  output_file.write('// VerilogA for ece4740_yyyy_fir, multb_sigen, veriloga\n')
  output_file.write('`include "constants.vams"\n')
  output_file.write('`include "disciplines.vams"\n')
  output_file.write('\n')
  output_file.write('// hexdecimal codebook \n')
  output_file.write('`define H0  lo,lo,lo,lo\n') 
  output_file.write('`define H1  hi,lo,lo,lo\n') 
  output_file.write('`define H2  lo,hi,lo,lo\n') 
  output_file.write('`define H3  hi,hi,lo,lo\n') 
  output_file.write('`define H4  lo,lo,hi,lo\n') 
  output_file.write('`define H5  hi,lo,hi,lo\n') 
  output_file.write('`define H6  lo,hi,hi,lo\n') 
  output_file.write('`define H7  hi,hi,hi,lo\n') 
  output_file.write('`define H8  lo,lo,lo,hi\n') 
  output_file.write('`define H9  hi,lo,lo,hi\n') 
  output_file.write('`define HA  lo,hi,lo,hi\n') 
  output_file.write('`define HB  hi,hi,lo,hi\n') 
  output_file.write('`define HC  lo,lo,hi,hi\n') 
  output_file.write('`define HD  hi,lo,hi,hi\n') 
  output_file.write('`define HE  lo,hi,hi,hi\n') 
  output_file.write('`define HF  hi,hi,hi,hi\n')
  output_file.write('\n')

def puts_module(output_file,cp,mname):
  # cp has the unit of ns
  output_file.write(f'module {mname}(A,B);\n')
  output_file.write( '\toutput [0:15] A;\n')
  output_file.write( '\toutput [0:7] B;\n')
  output_file.write( '\tvoltage [0:15] A;\n')
  output_file.write( '\tvoltage [0:7] B;\n')
  output_file.write( '\tparameter real hi = 1.2;\n')
  output_file.write( '\tparameter real lo = 0.0;\n')
  output_file.write( '\tparameter real tr = 10p from (0:inf);\n')
  output_file.write( '\tparameter real tf = 10p from (0:inf);\n')
  output_file.write(f'\tparameter real cp = {cp}n  from (0:inf);\n')
  output_file.write( '\treal Atemp[0:15];\n')
  output_file.write( '\treal Btemp[0:7];\n')
  output_file.write('\n')

def puts_caselist(output_file,caselist):
  output_file.write('\t//----------------------------------------------------------\n')
  output_file.write('\t// test case list\n')
  output_file.write('\t//----------------------------------------------------------\n')
  # caselist = [[name,AAAA,BB],]
  for (i,case) in enumerate(caselist):
    output_file.write(f'\t//k{i}: {case[0]}\n')
    output_file.write(f'\treal k{i}_A[0:15] =') 
    output_file.write(hex_decode(4,case[1]) + '\n')
    output_file.write(f'\treal k{i}_B[0:7] =') 
    output_file.write(hex_decode(2,case[2]) + '\n')
  output_file.write('\n')

def puts_caseseq(output_file,caselist):
  output_file.write('\t//----------------------------------------------------------\n')
  output_file.write('\t// test case sequence\n')
  output_file.write('\t//----------------------------------------------------------\n')
  for i in range(len(caselist)):
    if i == len(caselist)-1:
      output_file.write(f'\treal k{i}_next = {0};\n')
    else:
      output_file.write(f'\treal k{i}_next = {i+1};\n')
  output_file.write('\n')

def puts_testsrc(output_file,caselist):
  output_file.write( '\t//----------------------------------------------------------\n')
  output_file.write( '\t// test source\n')
  output_file.write( '\t//----------------------------------------------------------\n')
  output_file.write( '\t// case counter\n')
  output_file.write( '\treal k = 0;\n')
  output_file.write( '\tgenvar i;\n')
  output_file.write( '\tinteger x;\n')
  output_file.write( '\tanalog begin\n')
  output_file.write('\n')

  output_file.write( '\t\t// initial value and reset\n')
  output_file.write( '\t\t@(initial_step) begin\n')
  output_file.write( '\t\t\tfor(x=0;x<16;x=x+1) begin\n')
  output_file.write( '\t\t\t\tAtemp[x] = lo;\n')
  output_file.write( '\t\t\tend\n')
  output_file.write( '\t\t\tfor(x=0;x<8;x=x+1) begin\n')
  output_file.write( '\t\t\t\tBtemp[x] = lo;\n')
  output_file.write( '\t\t\tend\n')
  output_file.write( '\t\t\tk = 999;\n')
  output_file.write( '\t\tend\n')
  output_file.write('\n')

  output_file.write( '\t\t// test stimulus\n')
  output_file.write( '\t\t@(timer(0n,cp))	begin\n')
  output_file.write( '\t\t\tcase(k)\n')
  for i in range(len(caselist)):
    output_file.write(f'\t\t\t{i}: begin\n')
    output_file.write( '\t\t\t\tfor(x=0;x<16;x=x+1) begin\n')
    output_file.write(f'\t\t\t\t\tAtemp[x] = k{i}_A[x];\n')
    output_file.write( '\t\t\t\tend\n')
    output_file.write( '\t\t\t\tfor(x=0;x<8;x=x+1) begin\n')
    output_file.write(f'\t\t\t\t\tBtemp[x] = k{i}_B[x];\n')
    output_file.write( '\t\t\t\tend\n')
    output_file.write(f'\t\t\t\tk = k{i}_next;\n')
    output_file.write( '\t\t\tend\n')
  output_file.write( '\t\t\tdefault: begin // used for reset\n')
  output_file.write( '\t\t\t\tfor(x=0;x<16;x=x+1) begin\n')
  output_file.write( '\t\t\t\t\tAtemp[x] = lo;\n')
  output_file.write( '\t\t\t\tend\n')
  output_file.write( '\t\t\t\tfor(x=0;x<8;x=x+1) begin\n')
  output_file.write( '\t\t\t\t\tBtemp[x] = lo;\n')
  output_file.write( '\t\t\t\tend\n')
  output_file.write( '\t\t\t\tk = 0;\n')
  output_file.write( '\t\t\tend\n')
  output_file.write( '\t\t\tendcase\n') # case-endcase
  output_file.write( '\t\tend\n') # @timer() begin-end
  output_file.write('\n')

  output_file.write( '\t\t// output DAC\n')
  output_file.write( '\t\tfor(i=0;i<16;i=i+1) begin\n')
  output_file.write( '\t\t\tV(A[i]) <+ transition(Atemp[i], 0, tr, tf);\n')
  output_file.write( '\t\tend\n')
  output_file.write( '\t\tfor(i=0;i<8;i=i+1) begin\n')
  output_file.write( '\t\t\tV(B[i]) <+ transition(Btemp[i], 0, tr, tf);\n')
  output_file.write( '\t\tend\n')
  output_file.write('\n')

  output_file.write( '\tend\n') # analog begin-end
  output_file.write('\n')

def puts_endmodule(output_file):
  output_file.write( 'endmodule\n') # module-endmodule  


def main():
  opts = parse_cmdline()
  file_name = opts.m + '.txt'
  output_file = open(file_name,'w')
  caselist = [
    # name          AAAA     BB
    [ 'basic0',   0x1234,  0x01],
    [ 'basic1',   0x7216,  0x12],
    [ 'basic2',   0xdead,  0x33],
    [ 'basic3',   0xbeef,  0xff],
    [ 'basic4',   0xface,  0x00],
    [ 'basic5',   0xffff,  0xff],
    [ 'basic6',   0x32de,  0x49],
    [ 'basic7',   0x1874,  0x99],
    [ 'basic8',   0x1573,  0xaa],
    [ 'basic9',   0xdeca,  0xac],
  ]

  for i in range(10):
    caselist.append(
      [ f'random{i}',random.randint(0,0xffff),random.randint(0,0xff)]
    )

  puts_header(output_file)
  puts_module(output_file,10,opts.m)
  puts_caselist(output_file,caselist)
  puts_caseseq(output_file,caselist)
  puts_testsrc(output_file,caselist)
  puts_endmodule(output_file)  

main()