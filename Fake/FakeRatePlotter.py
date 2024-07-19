from ROOT import *
from utils import *
import array,os

stamp = "20240623_232843"
filename = f"TauFake_{stamp}"
savestr = filename.split("_",1)[1]
#f_fake = TFile(f"Inputs/{stamp}/{filename}.root")

c = TCanvas("","",1000,1000)


d_ptbins = {

    "tag"                                : "TailFatBinning",
    "Inclusive_2017"                     : [0] + list(range(190, 400, 20)) + list(range(400, 1500, 100)),
    "BoostedSignalRegionMETInvert_2017"  : [0] + list(range(190, 400, 20)) + list(range(400, 1500, 100)),
    "ResolvedSignalRegionMETInvert_2017" : [0] + list(range(190, 400, 20)) + list(range(400, 1500, 100)),
    "Inclusive_2018"                     : [0] + list(range(190, 400, 20)) + list(range(400, 1500, 100)),
    "BoostedSignalRegionMETInvert_2018"  : [0] + list(range(190, 400, 20)) + list(range(400, 1500, 100)),
    "ResolvedSignalRegionMETInvert_2018" : [0] + list(range(190, 400, 20)) + list(range(400, 1500, 100))


}


d_ptbins  = {

    "tag"                                      : "BinOptv2_FlavourSplit",
    "Inclusive_2016"                           : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvertMTSame_2016"        : [0,150,190,210,230,270,310,335,400,450,550,1000], # gof 1.06 deg 2 [0,190,210,230,270,310,335,360,380,400,450,500,1000]
    "ResolvedSignalRegionMETInvertMTSame_2016"       : [0,150,190,230,270,320,360,400,480,525,1000],
    "Inclusive_2017"                                 : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvertMTSame_2017"        : [0,190,210,230,270,300,330,380,450,1000], # gof 0.93 deg 2 = [0,190,210,230,270,300,330,380,450,1000] #[0,190,210,230,270,310,340,380,450,1000]
    "ResolvedSignalRegionMETInvertMTSame_2017"       : [0,190,210,230,270,300,320,350,380,450,1000],#[0,190,230,270,320,360,400,480,1000],
    "Inclusive_2018"                                 : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvertMTSame_2018"        : [0,190,210,230,270,310,335,400,450,550,1000], # gof 1.06 deg 2 [0,190,210,230,270,310,335,360,380,400,450,500,1000]
    "ResolvedSignalRegionMETInvertMTSame_2018"       : [0,190,230,270,320,360,400,480,525,1000],
    "Inclusive_ElTau_2016"                           : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvertMTSame_ElTau_2016"  : [0,150,170,190,210,230,250,300,350,1000], # gof 0.93 deg 2 = [0,190,210,230,270,300,330,380,450,1000] #[0,190,210,230,270,310,340,380,450,1000]
    "ResolvedSignalRegionMETInvertMTSame_ElTau_2016" : [0,150,170,190,210,230,250,300,350,1000],
    "Inclusive_ElTau_2017"                           : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvertMTSame_ElTau_2017"  : [0,190,210,230,275,350,1000], # gof 0.93 deg 2 = [0,190,210,230,270,300,330,380,450,1000] #[0,190,210,230,270,310,340,380,450,1000]
    "ResolvedSignalRegionMETInvertMTSame_ElTau_2017" : [0,190,250,350,1000],
    "Inclusive_ElTau_2018"                           : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvertMTSame_ElTau_2018"  : [0,190,210,230,270,335,400,1000], # gof 1.06 deg 2 [0,190,210,230,270,310,335,360,380,400,450,500,1000]
    "ResolvedSignalRegionMETInvertMTSame_ElTau_2018" : [0,190,250,400,1000],
    "Inclusive_MuTau_2016"                           : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvertMTSame_MuTau_2016"  : [0,150,190,250,300,1000], # gof 0.93 deg 2 = [0,190,210,230,270,300,330,380,450,1000] #[0,190,210,230,270,310,340,380,450,1000]
    "ResolvedSignalRegionMETInvertMTSame_MuTau_2016" : [0,150,170,190,210,230,250,300,350,1000],
    "Inclusive_MuTau_2017"                           : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvertMTSame_MuTau_2017"  : [0,190,250,350,1000], # gof 0.93 deg 2 = [0,190,210,230,270,300,330,380,450,1000] #[0,190,210,230,270,310,340,380,450,1000]
    "ResolvedSignalRegionMETInvertMTSame_MuTau_2017" : [0,190,220,250,300,400,1000],#[0,190,230,270,320,360,400,480,1000],
    "Inclusive_MuTau_2018"                           : [0] + list(range(190, 1500, 10)),
    "BoostedSignalRegionMETInvertMTSame_MuTau_2018"  : [0,190,250,400,1000], # gof 1.06 deg 2 [0,190,210,230,270,310,335,360,380,400,450,500,1000]
    "ResolvedSignalRegionMETInvertMTSame_MuTau_2018" : [0,190,220,250,300,400,1000]#[0,190,230,270,320,360,400,480,525,1000]
    # [0,190,210,230,250,270,300,320,340,360,400,480,525,1500]

}


# [0,190,210,230,250,270,320,800] 
d_ptbins_PR = {

    "tag"                                      : "BinOptv2_FlavourSplit",
    "Inclusive_2016"                           : [0,190,220,250,350,1000],
    "Inclusive_2017"                           : [0,190,220,250,350,1000],
    "Inclusive_2018"                           : [0,190,220,250,350,1000],
    "Inclusive_ElTau_2016"                     : [0,190,220,250,350,1000],
    "Inclusive_ElTau_2017"                     : [0,190,220,250,350,1000],
    "Inclusive_ElTau_2018"                     : [0,190,220,250,350,1000], 
    "Inclusive_MuTau_2016"                     : [0,190,220,250,350,1000],
    "Inclusive_MuTau_2017"                     : [0,190,220,250,350,1000],
    "Inclusive_MuTau_2018"                     : [0,190,220,250,350,1000],
    "BoostedSignalRegionMETInvertMTSame_2016"        : [0,150,250,1000], 
    "ResolvedSignalRegionMETInvertMTSame_2016"       : [0,190,220,250,350,1000],
    "BoostedSignalRegionMETInvertMTSame_2017"        : [0,190,220,250,350,1000],
    "ResolvedSignalRegionMETInvertMTSame_2017"       : [0,190,220,250,350,1000],
    "BoostedSignalRegionMETInvertMTSame_2018"        : [0,190,220,250,350,1000],
    "ResolvedSignalRegionMETInvertMTSame_2018"       : [0,190,220,250,350,1000],
    ####
    "BoostedSignalRegionMETInvertMTSame_ElTau_2016"  : [0,150,1000],
    "ResolvedSignalRegionMETInvertMTSame_ElTau_2016" : [0,150,250,1000],
    "BoostedSignalRegionMETInvertMTSame_ElTau_2017"  : [0,190,350,1000],
    "ResolvedSignalRegionMETInvertMTSame_ElTau_2017" : [0,190,350,1000],
    "BoostedSignalRegionMETInvertMTSame_ElTau_2018"  : [0,190,250,350,1000],
    "ResolvedSignalRegionMETInvertMTSame_ElTau_2018" : [0,190,1000],
    "BoostedSignalRegionMETInvertMTSame_MuTau_2016"  : [0,150,300,1000],
    "ResolvedSignalRegionMETInvertMTSame_MuTau_2016" : [0,150,200,1000],
    "BoostedSignalRegionMETInvertMTSame_MuTau_2017"  : [0,190,220,250,350,1000],
    "ResolvedSignalRegionMETInvertMTSame_MuTau_2017" : [0,190,1000],
    "BoostedSignalRegionMETInvertMTSame_MuTau_2018"  : [0,190,1000],
    "ResolvedSignalRegionMETInvertMTSame_MuTau_2018" : [0,190,220,250,350,1000],
    ####

}

savestr += f"_{d_ptbins['tag']}"

l_subtract = ["Subtract"]



l_subtract = ["NonSubtract"]
l_subtract = ["Subtract"]

isnoDY = False
dytag = ""
if isnoDY : dytag = "_noDY"

for era in ["2016preVFP","2016postVFP","2017","2018"]:
    k = 0
    os.system(f"mkdir -p Plots/{savestr}{dytag}/{era}")
    os.system(f"mkdir -p Files/{savestr}{dytag}")
    for genmatch in ["Prompt"]:
    #for genmatch in ["Prompt"]: # Switch for prompt rate 
        output_file = TFile(f"Files/{savestr}{dytag}/{era}_{genmatch}.root", "RECREATE")
        isDataDriven = genmatch == "Data"
        isPromptRate = genmatch == "Prompt"
        os.system(f"mkdir -p Plots/{savestr}{dytag}/{era}/Prompt")
        f_fake = TFile(f"Inputs/{stamp}/{era}/{filename}{dytag}.root")
        if isDataDriven : 
            f_fake   = TFile(f"Inputs/{stamp}/{era}/Data/{filename}.root")
            f_prompt = TFile(f"Inputs/{stamp}/{era}/{filename}{dytag}.root")
        for eta in d_geoTag :
            for nj in d_njtag :
                for lep in ["_ElTau","_MuTau"] : #["","_ElTau","_MuTau"]
                    for i,r in enumerate(["BoostedSignalRegionMETInvertMTSame","ResolvedSignalRegionMETInvertMTSame"]) : #["BoostedSignalRegionMETInvert","ResolvedSignalRegionMETInvert"]
                        if isPromptRate : d_ptbins = d_ptbins_PR
                        #print(d_ptbins)
                        c = TCanvas("","",1000,1000)
                        h_loose_tmp = f_fake.Get(f"WRTauFake/{r}{lep}/{genmatch}/TauPt_Loose_{eta}_{nj}")
                        if h_loose_tmp :
                            h_loose = h_loose_tmp.Rebin(len(d_ptbins[f"{r}{lep}_{era}"])-1,f"loose{r}",array.array('d',d_ptbins[f"{r}{lep}_{era}"]))
                            h_loose.SetDirectory(0)
                        h_tight_tmp = f_fake.Get(f"WRTauFake/{r}{lep}/{genmatch}/TauPt_Tight_{eta}_{nj}")
                        if h_tight_tmp :
                            h_tight = h_tight_tmp.Rebin(len(d_ptbins[f"{r}{lep}_{era}"])-1,f"tight{r}",array.array('d',d_ptbins[f"{r}{lep}_{era}"]))
                            h_tight.SetDirectory(0)
                        if isDataDriven : 
                            h_loose_prompt_tmp = f_prompt.Get(f"WRTauFake/{r}{lep}/Prompt/TauPt_Loose_{eta}_{nj}")
                            if h_loose_prompt_tmp :
                                h_loose_prompt = h_loose_prompt_tmp.Rebin(len(d_ptbins[f"{r}{lep}_{era}"])-1,f"ddps_loose{r}",array.array('d',d_ptbins[f"{r}{lep}_{era}"]))
                                h_loose_prompt.SetDirectory(0)
                            h_tight_prompt_tmp = f_prompt.Get(f"WRTauFake/{r}{lep}/Prompt/TauPt_Tight_{eta}_{nj}")
                            if h_tight_prompt_tmp :
                                h_tight_prompt = h_tight_prompt_tmp.Rebin(len(d_ptbins[f"{r}{lep}_{era}"])-1,f"ddps_tight{r}",array.array('d',d_ptbins[f"{r}{lep}_{era}"]))
                                h_tight_prompt.SetDirectory(0)
                            h_loose = h_loose - h_loose_prompt 
                            h_tight = h_tight - h_tight_prompt
                        h_fr = h_tight.Clone(f"{r}{lep}_{d_genmatch[genmatch]}{l_subtract[k]}_{eta}_{nj}")
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
                        drawLatex(f"{r}_{lep}",era,genmatch)
                        drawTagLatex(eta,nj)
                        c.Update()
                        if isPromptRate :
                            line = TLine(0,1,1000,1)
                            line.SetLineStyle(3)
                            line.SetLineWidth(2)
                            line.Draw("same")
                            c.Update()
                            c.SaveAs(f"Plots/{savestr}{dytag}/{era}/Prompt/Tau{d_genmatch[genmatch]}{l_subtract[k]}_{r}{lep}_{eta}_{nj}.png")
                            c.SaveAs(f"Plots/{savestr}{dytag}/{era}/Prompt/Tau{d_genmatch[genmatch]}{l_subtract[k]}_{r}{lep}_{eta}_{nj}.pdf")
                        else :
                            c.SaveAs(f"Plots/{savestr}{dytag}/{era}/Tau{d_genmatch[genmatch]}{l_subtract[k]}_{r}{lep}_{eta}_{nj}.png")
                            c.SaveAs(f"Plots/{savestr}{dytag}/{era}/Tau{d_genmatch[genmatch]}{l_subtract[k]}_{r}{lep}_{eta}_{nj}.pdf")


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
                        drawLatex("Inclusive",era,genmatch)
                        drawTagLatex(eta,nj)
                        drawLine(h_fr)
                        c.Update()
                        c.SaveAs(f"Plots/{savestr}/{era}/Tau{d_genmatch[genmatch]}{l_subtract[k]}_Inclusive_{eta}_{nj}.png")
                        c.SaveAs(f"Plots/{savestr}/{era}/Tau{d_genmatch[genmatch]}{l_subtract[k]}_Inclusive_{eta}_{nj}.pdf")
                        c.Close()
        k += 1
    output_file.Close()