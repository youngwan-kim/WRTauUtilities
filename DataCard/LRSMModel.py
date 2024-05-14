# Place it at CombineTool/CMSSW_10_2_13/python/HiggsAnalysis/CombinedLimit

from HiggsAnalysis.CombinedLimit.PhysicsModel import *

class LRSMModel(PhysicsModel):
    def doParametersOfInterest(self):
        self.modelBuilder.doVar("r[0,0,10]")
        self.modelBuilder.doSet("POI", ",".join(['r']))
        self.modelBuilder.factory_("expr::r2(\"(@0)*(@0)\", r)")

    def getYieldScale(self, bin, process):
        if process == "signal" :
            return 'r'
        else:
            return 1


LRSMModel_ = LRSMModel()