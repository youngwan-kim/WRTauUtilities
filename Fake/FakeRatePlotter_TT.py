from ROOT import *
from utils import *
import array,os

stamp = "20240711_174951"
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


ptbins  = {

    '0' : {
    "tag"                                            : "",
    "TTFakeMeasureRegion_2016"                       : [0,150,190,230,400,1000],
    "TTFakeMeasureRegion_2016preVFP"                 : [0,150,200,300,400,1000],
    "TTFakeMeasureRegion_2016postVFP"                : [0,150,190,230,300,400,500,700,1000],
    "TTFakeMeasureRegion_2017"                       : [0,190,230,300,400,1000],
    "TTFakeMeasureRegion_2018"                       : [0,190,230,500,1000],
    },
    '1' : {
    "tag"                                            : "",
    "TTFakeMeasureRegion_2016"                       : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "TTFakeMeasureRegion_2016preVFP"                 :  [0,150,190,230,270,350,450,1000],
    "TTFakeMeasureRegion_2016postVFP"                : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "TTFakeMeasureRegion_2017"                       : [0,190,230,300,350,400,500,1000],
    "TTFakeMeasureRegion_2018"                       : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000],
    },
    '2' : {
    "tag"                                            : "",
    "TTFakeMeasureRegion_2016"                       : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "TTFakeMeasureRegion_2016preVFP"                 : [0,150,170,190,210,230,250,275,300,325,500,650,1000],
    "TTFakeMeasureRegion_2016postVFP"                : [0,150,170,190,210,230,250,300,350,400,450,500,550,600,700,800,1000,2000],
    "TTFakeMeasureRegion_2017"                       : [0,150,170,190,210,230,250,275,300,350,400,500,750,1000],
    "TTFakeMeasureRegion_2018"                       : [0,150,170,190,210,230,250,275,300,350,400,450,500,550,600,700,800,1000],
    }
    
}

 

savestr += f"_{d_ptbins['tag']}"

l_subtract = ["Subtract"]



l_subtract = ["NonSubtract"]
l_subtract = ["Subtract"]

isnoDY = True
dytag = ""
if isnoDY : dytag = "_TT"

for era in ["2016"]:
    k = 0
    os.system(f"mkdir -p Plots/{savestr}{dytag}/{era}")
    os.system(f"mkdir -p Files/{savestr}{dytag}")
    for genmatch in ["Fake"]:
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
                d_ptbins = ptbins[nj]
                for lep in [""] : #["","_ElTau","_MuTau"]
                    for i,r in enumerate(["TTFakeMeasureRegion"]) : #["BoostedSignalRegionMETInvert","ResolvedSignalRegionMETInvert"]
                        if isPromptRate : d_ptbins = d_ptbins_PR
                        #print(d_ptbins)
                        c = TCanvas("","",1000,1000)
                        h_loose_tmp = f_fake.Get(f"WRTauFake/{r}{lep}/{genmatch}/TauPt_Loose_{eta}_{nj}")
                        if check(f_fake,f"WRTauFake/{r}{lep}/{genmatch}/TauPt_Loose_{eta}_{nj}") :
                            h_loose = h_loose_tmp.Rebin(len(d_ptbins[f"{r}{lep}_{era}"])-1,f"loose{r}",array.array('d',d_ptbins[f"{r}{lep}_{era}"]))
                            h_loose.SetDirectory(0)
                        else : 
                            h_loose = TH1D(f"loose{r}",f"loose{r}",len(d_ptbins[f"{r}{lep}_{era}"])-1,array.array('d',d_ptbins[f"{r}{lep}_{era}"]))
                            h_loose.SetDirectory(0)
                        h_tight_tmp = f_fake.Get(f"WRTauFake/{r}{lep}/{genmatch}/TauPt_Tight_{eta}_{nj}")
                        print(h_tight_tmp)
                        if check(f_fake,f"WRTauFake/{r}{lep}/{genmatch}/TauPt_Tight_{eta}_{nj}") :
                            h_tight = h_tight_tmp.Rebin(len(d_ptbins[f"{r}{lep}_{era}"])-1,f"tight{r}",array.array('d',d_ptbins[f"{r}{lep}_{era}"]))
                            h_tight.SetDirectory(0)
                        else : 
                            h_tight = TH1D(f"tight{r}",f"tight{r}",len(d_ptbins[f"{r}{lep}_{era}"])-1,array.array('d',d_ptbins[f"{r}{lep}_{era}"]))
                            h_tight.SetDirectory(0)
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
    output_file.Close()