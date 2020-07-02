%% Before running, set up the testbench cell name, input and output table, clock period etc. In the "EDIT BELOW/ABOVE ACCORDING TO YOUR DUT" block
% (c) 2019 Oscar Castaneda, Olalekan Afuye, Charles Jeon & Christoph Studer
% Modified by Yixiao Du (yd383@cornell.edu)
% ECE4740 logic module test tool.

clear


% vvvvvvvvvvvvvvvvvvvvvvvvvvv EDIT BELOW ACCORDING TO YOUR DUT vvvvvvvvvvvvvvvvvvvvvvvvvvv
% set up the name and parameters of your testbench cell
tb_name = 'FIR_GL_tb';
% set whether to check the results or only print them
check_enable = 1;
% set up inputs and outputs, MSB is on the left, use ... to contiune a line
input_nbr = 16+8*4+1;
input_table = {
  'X\<15\>','X\<14\>','X\<13\>','X\<12\>','X\<11\>','X\<10\>','X\<9\>','X\<8\>','X\<7\>','X\<6\>','X\<5\>','X\<4\>','X\<3\>','X\<2\>','X\<1\>','X\<0\>',...
  'B0\<7\>','B0\<6\>','B0\<5\>','B0\<4\>','B0\<3\>','B0\<2\>','B0\<1\>','B0\<0\>',...
  'B1\<7\>','B1\<6\>','B1\<5\>','B1\<4\>','B1\<3\>','B1\<2\>','B1\<1\>','B1\<0\>',...
  'B2\<7\>','B2\<6\>','B2\<5\>','B2\<4\>','B2\<3\>','B2\<2\>','B2\<1\>','B2\<0\>',...
  'B3\<7\>','B3\<6\>','B3\<5\>','B3\<4\>','B3\<3\>','B3\<2\>','B3\<1\>','B3\<0\>',...
  'RST_N'};
output_nbr = 18; 
output_table = {
  'Y\<17\>','Y\<16\>','Y\<15\>','Y\<14\>','Y\<13\>','Y\<12\>','Y\<11\>','Y\<10\>','Y\<9\>','Y\<8\>','Y\<7\>','Y\<6\>','Y\<5\>','Y\<4\>','Y\<3\>','Y\<2\>','Y\<1\>','Y\<0\>'};

% define total test case numbers
sample_nbr = 18; 
% define period (in ps)
cp  =  1e7;
% define rise and fall time (in ps)
t_rf = 10;
% initial setup time
t_ini = cp;
% maximum propagation delay (in ps)
max_tp = 10000;
% ^^^^^^^^^^^^^^^^^^^^^^^^^^^ EDIT ABOVE ACCORDING TO YOUR DUT ^^^^^^^^^^^^^^^^^^^^^^^^^^^


% set up cds_srr function
addpath('/opt/cadence/MMSIM151/tools.lnx86/spectre/matlab/64bit');

% directory that contains the simulation outputs
directory = sprintf('%s/Cadence/simulation/%s/spectre/schematic/psf', getenv('HOME'), tb_name);

% set up basic parameters
Vdd = 1.2;

% total simulation data length
a = cds_srr(directory, 'tran-tran', input_table{1}, 0);
data_len = max(size(a.V));

% get input signals
input_mtx = zeros(data_len,input_nbr);
for i = 1:input_nbr
  a = cds_srr(directory, 'tran-tran', input_table{i}, 0); 
  % extract voltages of signals
  input_mtx(:,i) = a.V;
end

% convert time into ps
t_ps = a.time*1e12;

% get output signals
output_mtx = [];
for i=1:output_nbr
  y = cds_srr(directory, 'tran-tran', output_table{i}, 0);
  output_mtx = [output_mtx y.V];
end

% we sample the inputs at the middle of a cycle
t_ps_sample_in = t_ini + cp/2 + (0:sample_nbr-1)*cp;

% we sample the outputs tp_max after an input changes (each cp),
t_ps_sample_out = t_ini + max_tp + (0:sample_nbr-1)*cp;

%% DUT output
% create base for expected output waveform
input_vec_bits = [];
for i = 1:input_nbr
  input_vec_bits = [input_vec_bits (input_mtx(:,i) > (Vdd/2))];  
end


% vvvvvvvvvvvvvvvvvvvvvvvvvvv EDIT BELOW ACCORDING TO YOUR DUT vvvvvvvvvvvvvvvvvvvvvvvvvvv
% define the functionality of DUT
input_X_bw = 16;
input_B0_bw = 8;
input_B1_bw = 8;
input_B2_bw = 8;
input_B3_bw = 8;
input_RST_N_bw = 1;
idx = 1;
input_X_dec = bi2de(input_vec_bits(:,(idx:idx+input_X_bw-1)),'left-msb');
idx = idx + input_X_bw;
input_B0_dec = bi2de(input_vec_bits(:,(idx:idx+input_B0_bw-1)),'left-msb');
idx = idx + input_B0_bw;
input_B1_dec = bi2de(input_vec_bits(:,(idx:idx+input_B1_bw-1)),'left-msb');
idx = idx + input_B1_bw;
input_B2_dec = bi2de(input_vec_bits(:,(idx:idx+input_B2_bw-1)),'left-msb');
idx = idx + input_B2_bw;
input_B3_dec = bi2de(input_vec_bits(:,(idx:idx+input_B3_bw-1)),'left-msb');
idx = idx + input_B3_bw;
input_RST_dec = bi2de(input_vec_bits(:,(idx:idx+input_RST_N_bw-1)),'left-msb');
idx = idx + input_RST_N_bw;
% ^^^^^^^^^^^^^^^^^^^^^^^^^^^ EDIT ABOVE ACCORDING TO YOUR DUT ^^^^^^^^^^^^^^^^^^^^^^^^^^^


%Check each one of the sampling points
err_flag = 0;
dut_output = zeros(sample_nbr,output_nbr);
x_input = zeros(sample_nbr,1);
sample_pt = t_ps_sample_out;
disp('Y(n) = B0*X(n) + B1*X(n-1) + B2*X(n-2) + B3*X(n-3)')
fbits_b = 6;
fbits_x = 10;
fbits_s = 8;
fbits_y = 6;
t_ps_idx_in = find(t_ps-t_ps_sample_in(1)>=0,1);
blist = [input_B0_dec(t_ps_idx_in)/(2^fbits_b),input_B1_dec(t_ps_idx_in)/(2^fbits_b),input_B2_dec(t_ps_idx_in)/(2^fbits_b),input_B3_dec(t_ps_idx_in)/(2^fbits_b)];
msg = sprintf('B0: %f[%x] B1: %f[%x] B2: %f[%x] B3: %f[%x]',...
             input_B0_dec(t_ps_idx_in)/(2^fbits_b),input_B0_dec(t_ps_idx_in),...
             input_B1_dec(t_ps_idx_in)/(2^fbits_b),input_B1_dec(t_ps_idx_in),...
             input_B2_dec(t_ps_idx_in)/(2^fbits_b),input_B2_dec(t_ps_idx_in),...
             input_B3_dec(t_ps_idx_in)/(2^fbits_b),input_B3_dec(t_ps_idx_in)...
             );
disp(msg)
for i=1:sample_nbr
    % find t_ps closest (from the right) to the t_ps_sample_in and _out
    t_ps_idx_in  = find(t_ps-t_ps_sample_in(i)>=0,1);
    t_ps_idx_out = find(t_ps-t_ps_sample_out(i)>=0,1);
    
    % measure the outputs and declare 1 if it is greater than Vdd/2    
    dut_output(i,:) = output_mtx(t_ps_idx_out,:) > (Vdd/2);

    x_input(i) = input_X_dec(t_ps_idx_in);

    % vvvvvvvvvvvvvvvvvvvvvvvvvvv EDIT BELOW ACCORDING TO YOUR DUT vvvvvvvvvvvvvvvvvvvvvvvvvvv
    % interpret UDT outputs
    s_result  = bi2de(dut_output(:,1:18),'left-msb');
    y_result  = bi2de(dut_output(:,1:16),'left-msb');
    
    msg = sprintf('%2d  -------------------------------------------------',i);
    disp(msg)
    msg = sprintf('18-bit:%f[%x],16-bit:%f[%x]',...
                  s_result(i)/(2^fbits_s),s_result(i),y_result(i)/(2^fbits_y),y_result(i)...
                  );
    disp(msg)

    % ^^^^^^^^^^^^^^^^^^^^^^^^^^^ EDIT ABOVE ACCORDING TO YOUR DUT ^^^^^^^^^^^^^^^^^^^^^^^^^^^
end
disp('---------------------------------------------------')
disp('[WARNING] Auto Verify has been disabled, please verify by inspection!')

%% plotting

input_wfm = x_input;
output_wfm = y_result;

input_wfm = input_wfm./(2^fbits_x);
output_wfm = output_wfm./(2^fbits_y);

blist_fp = [0.138336181640625,0.354217529296875,0.354217529296875,0.138336181640625];
output_ideal = [];
    for i = 1:sample_nbr+3
      if i == 1
        output_ideal = [output_ideal;blist_fp(1)*input_wfm(i)];
      elseif i == 2
        output_ideal = [output_ideal;blist_fp(1)*input_wfm(i) + blist_fp(2)*input_wfm(i-1)];
      elseif i == 3
        output_ideal = [output_ideal;blist_fp(1)*input_wfm(i) + blist_fp(2)*input_wfm(i-1) + blist_fp(3)*input_wfm(i-2)];
      elseif i == sample_nbr + 1
        output_ideal = [output_ideal;blist_fp(2)*input_wfm(i-1) + blist_fp(3)*input_wfm(i-2) + blist_fp(4)*input_wfm(i-3)];
      elseif i == sample_nbr + 2
        output_ideal = [output_ideal;blist_fp(3)*input_wfm(i-2) + blist_fp(4)*input_wfm(i-3)];
      elseif i == sample_nbr + 3
        output_ideal = [output_ideal;blist_fp(4)*input_wfm(i-3)];
      else
        output_ideal = [output_ideal;blist_fp(1)*input_wfm(i) + blist_fp(2)*input_wfm(i-1) + blist_fp(3)*input_wfm(i-2) + blist_fp(4)*input_wfm(i-3)];
      end
    end

figure(1)
subplot(2,1,1)
stem(input_wfm,'r')
subplot(2,1,2)
hold on
stem(output_wfm,'b')
plot(output_ideal,'k--')
hold off

[h,w] = freqz(blist,[1],1024);
mag = abs(h);
mag = 20*log(mag);
pha = angle(h);
[h_ref,w_ref] = freqz(blist_fp,[1],1024);
mag_ref = abs(h_ref);
mag_ref = 20*log(mag_ref);
pha_ref = angle(h_ref);

figure(2)
subplot(2,1,1)
hold on
plot(w,mag,'r')
plot(w,mag_ref,'k--')
hold off
subplot(2,1,2)
hold on
plot(w,pha,'r')
plot(w,pha_ref,'k--')
hold off

