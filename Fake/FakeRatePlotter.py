from ROOT import *
from utils import *
import array,os

stamp = "20240318_145423"
filename = f"TauFake_{stamp}"
savestr = filename.split("_",1)[1]+"_MCWeight"
#f_fake = TFile(f"Inputs/{stamp}/{filename}.root")

c = TCanvas("","",1000,1000)

d_ptbins = {

    "tag"                           : "TailFatBinning",
    "Inclusive"                     : [0] + list(range(190, 400, 20)) + list(range(400, 1500, 100)),
    "BoostedSignalRegionMETInvert"  : [0] + list(range(190, 400, 20)) + list(range(400, 1500, 100)),
    "ResolvedSignalRegionMETInvert" : [0] + list(range(190, 400, 20)) + list(range(400, 1500, 100))

}

d_ptbins = {

    "tag"                                : "BinOptv1",
    "Inclusive_2017"                     : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvert_2017"  : [0,190,210,230,270,300,330,380,450,1000], # gof 0.93 deg 2 = [0,190,210,230,270,300,330,380,450,1000] #[0,190,210,230,270,310,340,380,450,1000]
    "ResolvedSignalRegionMETInvert_2017" : [0,190,210,230,270,300,320,350,380,450,1000],#[0,190,230,270,320,360,400,480,1000],
    "Inclusive_2018"                     : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvert_2018"  : [0,190,210,230,270,310,335,400,450,550,1000], # gof 1.06 deg 2 [0,190,210,230,270,310,335,360,380,400,450,500,1000]
    "ResolvedSignalRegionMETInvert_2018" : [0,190,230,270,320,360,400,480,525,1000]
    # [0,190,210,230,250,270,300,320,340,360,400,480,525,1500]

}

savestr += f"_{d_ptbins['tag']}"

l_subtract = ["NonSubtract","Subtract"]

for era in ["2017","2018"]:
    k = 0
    os.system(f"mkdir -p Plots/{savestr}/{era}")
    os.system(f"mkdir -p Files/{savestr}")
    #for genmatch in ["Data","Data"]:
    for genmatch in ["Prompt"]:
        output_file = TFile(f"Files/{savestr}/{era}_{genmatch}.root", "RECREATE")
        isDataDriven = genmatch == "Data"
        isPromptRate = genmatch == "Prompt"
        f_fake = TFile(f"Inputs/{stamp}/{era}/{filename}.root")
        if isDataDriven : 
            f_fake   = TFile(f"Inputs/{stamp}/{era}/Data/{filename}.root")
            f_prompt = TFile(f"Inputs/{stamp}/{era}/{filename}.root")
        for eta in d_geoTag :
            for nj in d_njtag :
                for i,r in enumerate(["BoostedSignalRegionMETInvert","ResolvedSignalRegionMETInvert"]) :
                    if isPromptRate : d_ptbins[f"{r}_{era}"] = [0,190,220,250,350,1000]
                    c = TCanvas("","",1000,1000)
                    h_loose_tmp = f_fake.Get(f"WRTauFake/{r}/{genmatch}/TauPt_Loose_{eta}_{nj}")
                    if h_loose_tmp :
                        h_loose = h_loose_tmp.Rebin(len(d_ptbins[f"{r}_{era}"])-1,f"loose{r}",array.array('d',d_ptbins[f"{r}_{era}"]))
                        h_loose.SetDirectory(0)
                    else : continue
                    h_tight_tmp = f_fake.Get(f"WRTauFake/{r}/{genmatch}/TauPt_Tight_{eta}_{nj}")
                    if h_tight_tmp :
                        h_tight = h_tight_tmp.Rebin(len(d_ptbins[f"{r}_{era}"])-1,f"tight{r}",array.array('d',d_ptbins[f"{r}_{era}"]))
                        h_tight.SetDirectory(0)
                    else : continue
                    if isDataDriven : 
                        h_loose_prompt_tmp = f_prompt.Get(f"WRTauFake/{r}/Prompt/TauPt_Loose_{eta}_{nj}")
                        if h_loose_prompt_tmp :
                            h_loose_prompt = h_loose_prompt_tmp.Rebin(len(d_ptbins[f"{r}_{era}"])-1,f"ddps_loose{r}",array.array('d',d_ptbins[f"{r}_{era}"]))
                            h_loose_prompt.SetDirectory(0)
                        else : continue
                        h_tight_prompt_tmp = f_prompt.Get(f"WRTauFake/{r}/Prompt/TauPt_Tight_{eta}_{nj}")
                        if h_tight_prompt_tmp :
                            h_tight_prompt = h_tight_prompt_tmp.Rebin(len(d_ptbins[f"{r}_{era}"])-1,f"ddps_tight{r}",array.array('d',d_ptbins[f"{r}_{era}"]))
                            h_tight_prompt.SetDirectory(0)
                        else : continue
                        if k == 0 :
                            h_loose = h_loose - h_loose_prompt 
                            h_tight = h_tight - h_tight_prompt
                    h_fr = h_tight.Clone(f"{r}_{d_genmatch[genmatch]}{l_subtract[k]}_{eta}_{nj}")
                    h_fr.Divide(h_tight,h_loose,1,1,'B')
                    original_directory = gDirectory.GetPath()
                    output_file.cd()
                    h_fr.Write()
                    gDirectory.cd(original_directory)
                    if isPromptRate : h_fr.GetYaxis().SetRangeUser(0,1.5) 
                    else : h_fr.GetYaxis().SetRangeUser(0,0.6) 
                    h_fr.SetStats(0)
                    h_fr.GetXaxis().SetTitle("p_{T}(#tau_{h})")
                    h_fr.GetYaxis().SetTitleSize(0.05)
                    h_fr.GetYaxis().SetTitle(d_genmatch[genmatch]+"(#tau_{h})")
                    if isDataDriven : h_fr.GetYaxis().SetTitle("FR(#tau_{h})")
                    h_fr.GetYaxis().SetTitleOffset(0.9)
                    h_fr.GetXaxis().SetNdivisions(509)
                    h_fr.SetLineColor(kRed)
                    h_fr.SetLineWidth(3)
                    h_fr.GetXaxis().SetTitleSize(0.05)
                    h_err = h_fr.Clone(f"{r}_FR_err")
                    h_err.SetLineWidth(2)
                    h_err.SetLineColor(kBlack)

                    c.cd()
                    c.SetLeftMargin(0.125)
                    c.SetRightMargin(0.085)
                    c.SetBottomMargin(0.125)
                    #h_fr.Draw("hist")
                    h_err.Draw("e0")
                    h_fr.Draw("hist&same")
                    drawLatex(i,era,genmatch)
                    drawTagLatex(eta,nj)
                    c.Update()
                    drawLine(h_fr)
                    c.Update()
                    c.SaveAs(f"Plots/{savestr}/{era}/Tau{d_genmatch[genmatch]}{l_subtract[k]}_{r}_{eta}_{nj}.png")
                    c.SaveAs(f"Plots/{savestr}/{era}/Tau{d_genmatch[genmatch]}{l_subtract[k]}_{r}_{eta}_{nj}.pdf")


                h_loose_1 = f_fake.Get(f"WRTauFake/BoostedSignalRegionMETInvert/{genmatch}/TauPt_Loose_{eta}_{nj}")
                h_loose_2 = f_fake.Get(f"WRTauFake/ResolvedSignalRegionMETInvert/{genmatch}/TauPt_Loose_{eta}_{nj}")
                h_tight_1 = f_fake.Get(f"WRTauFake/BoostedSignalRegionMETInvert/{genmatch}/TauPt_Tight_{eta}_{nj}")
                h_tight_2 = f_fake.Get(f"WRTauFake/ResolvedSignalRegionMETInvert/{genmatch}/TauPt_Tight_{eta}_{nj}")
                
                if isDataDriven :
                    h_loose_prompt_1 = f_prompt.Get(f"WRTauFake/BoostedSignalRegionMETInvert/{genmatch}/TauPt_Loose_{eta}_{nj}")
                    h_loose_prompt_2 = f_prompt.Get(f"WRTauFake/ResolvedSignalRegionMETInvert/{genmatch}/TauPt_Loose_{eta}_{nj}")
                    h_tight_prompt_1 = f_prompt.Get(f"WRTauFake/BoostedSignalRegionMETInvert/{genmatch}/TauPt_Tight_{eta}_{nj}")
                    h_tight_prompt_2 = f_prompt.Get(f"WRTauFake/ResolvedSignalRegionMETInvert/{genmatch}/TauPt_Tight_{eta}_{nj}")
                    

                if h_loose_1 and h_loose_2 :
                    if h_tight_1 and h_tight_2  :
                        if isDataDriven and h_loose_prompt_1 and h_loose_prompt_2 :
                            h_loose_tmp = h_loose_1 + h_loose_2 - h_loose_prompt_1 - h_loose_prompt_2
                        elif not isDataDriven : h_loose_tmp = h_loose_1+h_loose_2
                        h_loose = h_loose_tmp.Rebin(len(d_ptbins[f"Inclusive_{era}"])-1,f"Inclusive_{genmatch}_{eta}_{nj}_Loose",array.array('d',d_ptbins[f"Inclusive_{era}"]))
                        if eta == "All" and nj == "All" : 
                            original_directory = gDirectory.GetPath()
                            output_file.cd()
                            h_loose.Write()
                            gDirectory.cd(original_directory)
                        if isDataDriven and h_loose_prompt_1 and h_loose_prompt_2 :
                            h_tight_tmp = h_tight_1 + h_tight_2 - h_tight_prompt_1 - h_tight_prompt_2
                        elif not isDataDriven : h_tight_tmp = h_tight_1 + h_tight_2 
                        h_tight = h_tight_tmp.Rebin(len(d_ptbins[f"Inclusive_{era}"])-1,f"Inclusive_{genmatch}_{eta}_{nj}_Tight",array.array('d',d_ptbins[f"Inclusive_{era}"]))
                        if eta == "All" and nj == "All" : 
                            original_directory = gDirectory.GetPath()
                            output_file.cd()
                            h_tight.Write()
                            gDirectory.cd(original_directory)
                        h_fr = h_tight.Clone(f"Inclusive_{d_genmatch[genmatch]}_{eta}_{nj}")
                        h_fr.Divide(h_tight,h_loose,1,1,'B')
                        h_fr.GetYaxis().SetRangeUser(0,1.5)
                        h_fr.SetStats(0)
                        h_fr.GetXaxis().SetTitle("p_{T}(#tau_{h})")
                        h_fr.GetYaxis().SetTitleSize(0.05)
                        h_fr.GetYaxis().SetTitle(d_genmatch[genmatch]+"(#tau_{h})")
                        h_fr.GetYaxis().SetTitleOffset(0.9)
                        h_fr.GetXaxis().SetNdivisions(509)
                        h_fr.SetLineColor(kRed)
                        h_fr.SetLineWidth(3)
                        h_fr.GetXaxis().SetTitleSize(0.05)
                        h_err = h_fr.Clone(f"{r}_FR_err")
                        h_err.SetLineWidth(2)
                        h_err.SetLineColor(kBlack)
                        original_directory = gDirectory.GetPath()
                        output_file.cd()
                        h_fr.Write()
                        gDirectory.cd(original_directory)
                        c.cd()
                        c.SetLeftMargin(0.125)
                        c.SetRightMargin(0.085)
                        c.SetBottomMargin(0.125)
                        #h_fr.Draw("hist")
                        h_err.Draw("e0")
                        h_fr.Draw("hist&same")
                        drawLatex(2,era,genmatch)
                        drawTagLatex(eta,nj)
                        drawLine(h_fr)
                        c.Update()
                        c.SaveAs(f"Plots/{savestr}/{era}/Tau{d_genmatch[genmatch]}{l_subtract[k]}_Inclusive_{eta}_{nj}.png")
                        c.SaveAs(f"Plots/{savestr}/{era}/Tau{d_genmatch[genmatch]}{l_subtract[k]}_Inclusive_{eta}_{nj}.pdf")
                        c.Close()
        k += 1
    output_file.Close()