from ROOT import *
import os
import array
from math import sqrt
from .tools import getLumiSyst

class SystCalculator:
    def __init__(self, stamp, samplename, era, varKey, VarDic, binN):
        self.stamp = stamp
        self.samplename = samplename
        self.era = era
        self.varKey = varKey
        self.VarDic = VarDic
        self.binN = binN
        self.systDir = f"{os.getenv('WRTau_Output')}/{self.stamp}/{self.era}/RunSyst"
        self.systFile = TFile(f"{self.systDir}/WRTau_Analyzer_{self.samplename}.root")
        self.d_global = {"Luminosity": 0.0}

    def __del__(self):
        if self.systFile.IsOpen():
            self.systFile.Close()

    def get_syst_list(self):
        systList = []
        for key in self.systFile.GetListOfKeys():
            obj = key.ReadObj()
            if obj.InheritsFrom("TDirectory"):
                systName = obj.GetName()
                if systName != "Central":
                    systList.append(systName)

        out = []
        for syst in systList:
            if "Up" in syst:
                out.append(syst.replace("Up", ""))
            elif "Down" in syst:
                out.append(syst.replace("Down", ""))

        return list(set(out))

    def get_syst_error(self):
        systList = self.get_syst_list()
        systDict = {key: [] for key in systList}

        h_central_ = self.systFile.Get(f"Central/__PromptTau__PromptLepton/{self.varKey}")
        h_central = self.rebin_histogram(h_central_, "Central")

        nCentral = h_central.GetBinContent(self.binN)

        for syst in systList:
            if nCentral == 0:
                systDict[syst] = [0.0, 0.0, 0.0]
                continue

            h_up_ = self.systFile.Get(f"{syst}Up/__PromptTau__PromptLepton/{self.varKey}")
            h_down_ = self.systFile.Get(f"{syst}Down/__PromptTau__PromptLepton/{self.varKey}")
            h_up = self.rebin_histogram(h_up_, f"{syst}Up")
            h_down = self.rebin_histogram(h_down_, f"{syst}Down")

            nUp = h_up.GetBinContent(self.binN)
            nDown = h_down.GetBinContent(self.binN)

            systDict[syst] = [max((nUp - nCentral), (nCentral - nDown)),
                              max((nUp - nCentral) / nCentral, (nCentral - nDown) / nCentral),
                              nCentral]

            for h in [h_up, h_down]:
                del h

        for syst_global in self.d_global:
            self.d_global["Luminosity"] = getLumiSyst(self.era) - 1.0
            n_ = systDict[systList[0]][2]
            if n_ == 0:
                systDict[syst_global] = [0.0, 0.0, 0.0]
            else:
                systDict[syst_global] = [n_ * self.d_global[syst_global],
                                         self.d_global[syst_global],
                                         n_]

        del h_central_
        del h_central
        return systDict

    def rebin_histogram(self, hist, name):
        gROOT.cd()
        if len(self.VarDic[self.varKey]) == 8:
            return hist.Clone(name).Rebin(len(self.VarDic[self.varKey][6]) - 1,
                                          name, array.array('d', self.VarDic[self.varKey][6]))
        else:
            return hist.Clone(name).Rebin(self.VarDic[self.varKey][1])

    def get_total_syst_error(self):
        systDict = self.get_syst_error()
        unc = 0.0

        print(f"{self.varKey} Bin #{self.binN} Syst. Unc. Summary")
        for syst, values in systDict.items():
            unc += values[0] ** 2
            print(f"\t {syst} : {values[2]} +/- {abs(values[0])} ({abs(values[1]) * 100}%)")

        if systDict[syst][2] != 0:
            unc_r = sqrt(unc) / systDict[syst][2] * 100
        else:
            unc_r = 0

        print(f"\t\t Total Syst. Unc. = {systDict[syst][2]} +/- {sqrt(unc)} ({unc_r}%)")
        del systDict
        return sqrt(unc)

# Usage Example:
# calculator = SystCalculator(stamp, samplename, era, varKey, VarDic, binN)
# total_syst_error = calculator.get_total_syst_error()
