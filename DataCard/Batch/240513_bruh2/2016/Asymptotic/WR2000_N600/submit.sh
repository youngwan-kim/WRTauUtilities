universe = vanilla
getenv   = True
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
request_memory = 24000
executable = run_Asymptotic.sh
log = WR2000_N600_Asymptotic.log
output = WR2000_N600_Asymptotic.out
error = WR2000_N600_Asymptotic.err
transfer_output_files = higgsCombineTest.AsymptoticLimits.mH120.root
transfer_output_remaps = "higgsCombineTest.AsymptoticLimits.mH120.root = output/WR2000_N600_Asymptotic.root"
queue
