#=========================================================================
# ECE4740 FIR Filter signal_gen Veriloga generator : python multbgen [options]
#=========================================================================
#  -h --help        Display this message
#  -m <module>      Set Module Name
#  -t <test>        Choose Test Case
#                     puls : impulse response
#                     step : step response
#                     freq : frequency respinse
#  -f <freq>        Set the frequency of the sine wave (Unit: kHz) (for "-t freq" only)
#  -ac              Perform AC Analysis (for "-t freq" only)
#  -s <sample rate> Set the Sample Rate (Unit: kHz) (required in "-t freq")
#            
#
# Signal_gen Veriloga generator
# Author : Yixiao Du
# Date : 5/19/2020

import argparse
import os
import sys
import math

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
  p.add_argument( "-t",               default = 'puls',
                                      choices =  ['puls',
                                                  'step',
                                                  'freq']     )
  p.add_argument( "-m",               action="store"          )
  p.add_argument( "-f",               default = 10.0,
                                      action="store",
                                      type = float            )
  p.add_argument( "-ac",              action="store_true"     )
  p.add_argument( "-s",               default = 100.0,
                                      action="store",
                                      type = float            )    

  
  opts = p.parse_args()
  if opts.help: p.error()
  return opts

def hex_decode(hbw,val):
  hstr = '0x{0:0{1}X}'.format(val,hbw)
  hstr = hstr[-hbw:]
  ret_str = ''
  for i in range(hbw):
    hchar = hstr[i]
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
      print('[ERROR] Unsupported Hexdicemal Value!',val)
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
  output_file.write(f'module {mname}(X,RST_N,B0,B1,B2,B3);\n')
  output_file.write( '\toutput [0:15] X;\n')
  output_file.write( '\toutput [0:7] B0;\n')
  output_file.write( '\toutput [0:7] B1;\n')
  output_file.write( '\toutput [0:7] B2;\n')
  output_file.write( '\toutput [0:7] B3;\n')
  output_file.write( '\toutput RST_N;\n')
  output_file.write( '\tvoltage [0:15] X;\n')
  output_file.write( '\tvoltage [0:7] B0;\n')
  output_file.write( '\tvoltage [0:7] B1;\n')
  output_file.write( '\tvoltage [0:7] B2;\n')
  output_file.write( '\tvoltage [0:7] B3;\n')
  output_file.write( '\tvoltage RST_N;\n')
  output_file.write( '\tparameter real hi = 1.2;\n')
  output_file.write( '\tparameter real lo = 0.0;\n')
  output_file.write( '\tparameter real tr = 10p from (0:inf);\n')
  output_file.write( '\tparameter real tf = 10p from (0:inf);\n')
  output_file.write(f'\tparameter real cp = {cp}n  from (0:inf);\n')
  output_file.write( '\treal Xtemp[0:15];\n')
  output_file.write( '\treal B0temp[0:7];\n')
  output_file.write( '\treal B1temp[0:7];\n')
  output_file.write( '\treal B2temp[0:7];\n')
  output_file.write( '\treal B3temp[0:7];\n')
  output_file.write( '\treal RST_Ntemp;\n')
  output_file.write('\n')

def puts_caselist(output_file,caselist,blist):
  output_file.write('\t//----------------------------------------------------------\n')
  output_file.write('\t// test case list\n')
  output_file.write('\t//----------------------------------------------------------\n')
  output_file.write('\t// set bs\n')
  for i in range(4):
    output_file.write(f'\treal v_B{i}[0:7] =') 
    output_file.write(hex_decode(2,blist[i]) + '\n')
  # caselist = [[name,XXXX,RST_N],]
  for (i,case) in enumerate(caselist):
    output_file.write(f'\t//k{i}: {case[0]}\n')
    output_file.write(f'\treal k{i}_X[0:15] =') 
    output_file.write(hex_decode(4,case[1]) + '\n')
    output_file.write(f'\treal k{i}_RST_N =') 
    output_file.write(case[2] + ';\n')
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
  output_file.write( '\t\t\t\tXtemp[x] = lo;\n')
  output_file.write( '\t\t\tend\n')
  output_file.write( '\t\t\tRST_Ntemp = lo;\n')
  output_file.write( '\t\t\tfor(x=0;x<8;x=x+1) begin\n')
  output_file.write( '\t\t\t\tB0temp[x] = v_B0[x];\n')
  output_file.write( '\t\t\t\tB1temp[x] = v_B1[x];\n')
  output_file.write( '\t\t\t\tB2temp[x] = v_B2[x];\n')
  output_file.write( '\t\t\t\tB3temp[x] = v_B3[x];\n')
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
    output_file.write(f'\t\t\t\t\tXtemp[x] = k{i}_X[x];\n')
    output_file.write( '\t\t\t\tend\n')
    output_file.write(f'\t\t\tRST_Ntemp = k{i}_RST_N;\n')
    output_file.write(f'\t\t\t\tk = k{i}_next;\n')
    output_file.write( '\t\t\tend\n')
  output_file.write( '\t\t\tdefault: begin // used for reset\n')
  output_file.write( '\t\t\t\tfor(x=0;x<16;x=x+1) begin\n')
  output_file.write( '\t\t\t\t\tXtemp[x] = lo;\n')
  output_file.write( '\t\t\t\tend\n')
  output_file.write( '\t\t\tRST_Ntemp = lo;\n')
  output_file.write( '\t\t\t\tk = 0;\n')
  output_file.write( '\t\t\tend\n')
  output_file.write( '\t\t\tendcase\n') # case-endcase
  output_file.write( '\t\tend\n') # @timer() begin-end
  output_file.write( '\n')

  output_file.write( '\t\t// output DAC\n')
  output_file.write( '\t\tfor(i=0;i<16;i=i+1) begin\n')
  output_file.write( '\t\t\tV(X[i]) <+ transition(Xtemp[i], 0, tr, tf);\n')
  output_file.write( '\t\tend\n')
  output_file.write( '\t\tfor(i=0;i<8;i=i+1) begin\n')
  output_file.write( '\t\t\tV(B0[i]) <+ transition(B0temp[i], 0, tr, tf);\n')
  output_file.write( '\t\t\tV(B1[i]) <+ transition(B1temp[i], 0, tr, tf);\n')
  output_file.write( '\t\t\tV(B2[i]) <+ transition(B2temp[i], 0, tr, tf);\n')
  output_file.write( '\t\t\tV(B3[i]) <+ transition(B3temp[i], 0, tr, tf);\n')
  output_file.write( '\t\tend\n')
  output_file.write( '\t\tV(RST_N) <+ transition(RST_Ntemp, 0, tr, tf);\n')
  output_file.write( '\n')

  output_file.write( '\tend\n') # analog begin-end
  output_file.write( '\n')

def puts_endmodule(output_file):
  output_file.write( 'endmodule\n') # module-endmodule


def sine_gen(freq,fs,fbits):
  sin_seq = []
  N = math.ceil(4*fs/freq)
  for n in range(N):
    # sample value
    value = 1 + math.sin(2*math.pi*freq*n/fs)
    # convert to integer-represented fixed-point
    a = value*(2**fbits)
    (b,a) = math.modf(a)
    value = int(a)
                   #                        name  XXXX  RST_N
    sin_seq.append([f'sap{fs}k_sine_{freq}k_{n}', value,'hi'])
  return sin_seq

def impulse_gen(freq,fs,fbits):
  puls_seq = [['impluse_0',2**fbits,'hi']]
  N = math.ceil(4*fs/freq)
  for n in range(N-1):
    puls_seq.append([f'impluse_{n+1}',0,'hi'])
  return puls_seq

def step_gen(freq,fs,fbits):
  step_seq = []
  N = math.ceil(4*fs/freq)
  for n in range(N):
    step_seq.append([f'step_{n}',2**fbits,'hi'])
  return step_seq



def main():
  opts = parse_cmdline()
  file_name = opts.m + '.txt'
  output_file = open(file_name,'w')
  fbits_x = 10
  fbits_b = 6

  # initialize b's
  blist = [0,0,0,0]
  blist_fp = [  0.138336181640625,
                0.354217529296875,
                0.354217529296875,
                0.138336181640625,]
  for i in range(4):
    # convert to integer-represented fixed-point
    a = blist_fp[i]*(2**fbits_b)
    (b,a) = math.modf(a)
    blist[i] = int(a)
    # print(blist)
  
  # choose a test list
  caselist = [['reset',0,'lo']] # reset for 1 cycle
  if opts.t == 'puls':
    caselist += impulse_gen(opts.f,opts.s,fbits_x)
  elif opts.t == 'step':
    caselist += step_gen(opts.f,opts.s,fbits_x)
  elif opts.t == 'freq':
    if opts.ac:
      freq_list = [0.01,0.1,0.2,0.5,1,2,5,10,20,50] # in kHz
      for i in range(len(freq_list)):
        caselist += ['reset',0,'lo']
        caselist += sine_gen(opts.f,opts.s,fbits_x)
    else:
      caselist += sine_gen(opts.f,opts.s,fbits_x)
  else:
    print('[ERROR] Unsupported Test Mode!')
    raise ValueError
  
  # set clock frequency
  cp_ns = int(1/(1000*opts.s)*(10**9))

  puts_header(output_file)
  puts_module(output_file,cp_ns,opts.m)
  puts_caselist(output_file,caselist,blist)
  puts_caseseq(output_file,caselist)
  puts_testsrc(output_file,caselist)
  puts_endmodule(output_file)

  output_file.close()  

main()