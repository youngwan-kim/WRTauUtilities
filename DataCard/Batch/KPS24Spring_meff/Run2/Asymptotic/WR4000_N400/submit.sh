universe = vanilla
getenv   = True
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
request_memory = 24000
executable = run_Asymptotic.sh
log = WR4000_N400_Asymptotic.log
output = WR4000_N400_Asymptotic.out
error = WR4000_N400_Asymptotic.err
transfer_output_files = higgsCombineTest.AsymptoticLimits.mH120.root
transfer_output_remaps = "higgsCombineTest.AsymptoticLimits.mH120.root = output/WR4000_N400_Asymptotic.root"
queue
