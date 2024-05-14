//Place it in /data6/Users/jihkim/HNDiLeptonWorskspace/src/LimitPlotter

#include "Macros.h"
#include "canvas_margin.h"

TString WORKING_DIR = getenv("HNDILEPTONWORKSPACE_DIR");  
TString version = getenv("FLATVERSION");
TString dataset = "";
TString ENV_FILE_PATH = WORKING_DIR;
TString ENV_PLOT_PATH = getenv("PLOT_PATH");
  
TString filepath = ENV_FILE_PATH+dataset+"/Limits/ReadLimits/Shape/out/";
TString plotpath = ENV_FILE_PATH+dataset+"/src/LimitPlotter/out/";

void DrawLimits(TString year="", TString channel=""){

  bool DrawObserved = false;

  setTDRStyle();

  //gStyle->SetOptStat(0);

  TString tag = "_syst_Run23Scaled"; //"_HNL_UL";
  TString method = "Asym"; //"Full";

  vector<TString> myWPs = {"KPS24Spring"};
  for(int i=0; i<myWPs.size(); i++){
    TString myWP = myWPs.at(i);
    TString this_filepath = filepath+myWP+"/"+year+"_"+channel+tag+"_"+method+"_limit.txt";
    TString this_plotpath = plotpath+myWP;

    if( !gSystem->mkdir(this_plotpath, kTRUE) ){
      cout
      << "###################################################" << endl
      << "Directoy " << this_plotpath << " is created" << endl
      << "###################################################" << endl
      << endl;
    }

    TLatex latex_CMSPreliminary, latex_Lumi, latex_title;
    latex_CMSPreliminary.SetNDC();
    latex_Lumi.SetNDC();
    latex_title.SetNDC();

    //=== 13 TeV full Run2
    string elline;
    cout << "Reading "+this_filepath+" ..." << endl;
    ifstream in;
    in.open(this_filepath);
    //int n_central = 24; //FIXME depending on the bins
    int n_central = 28; //FIXME depending on the bins
    double mass[n_central], obs[n_central], limit[n_central], onesig_left[n_central], onesig_right[n_central], twosig_left[n_central], twosig_right[n_central];

    int dummyint=0;
    double max_obs = 0., max_obs_mass = 0.;
    double min_obs = 9999., min_obs_mass = 0.;
    while(getline(in,elline)){
      cout << elline << endl;
      //if(elline.find("7500") != string::npos){
      //  n_central--;
      //  continue; //FIXME JH : 7500 now has a xsec issue...
      //}
      std::istringstream is( elline );
      is >> mass[dummyint];
      is >> obs[dummyint];
      is >> twosig_left[dummyint];
      is >> onesig_left[dummyint];
      is >> limit[dummyint];
      is >> onesig_right[dummyint];
      is >> twosig_right[dummyint];

      //==== skip points below 0
      if(obs[dummyint]<=0 || limit[dummyint]<=0 || onesig_left[dummyint]<=0 || onesig_right[dummyint]<=0 || twosig_left[dummyint]<=0 || twosig_right[dummyint]<=0){
        n_central--;
        continue;
      }
      
      double scale = 0.01;
      //double scale=1.;
      //if(mass[dummyint]<=100) scale *= 0.001; // 0.001 only for low mass (https://cms-talk.web.cern.ch/t/too-large-error-with-hybridnew/32844)
      //else scale *= 0.01; // input signal scaled as V^2 = 0.01 by default

      obs[dummyint] *= scale;

      limit[dummyint] *= scale;
      onesig_left[dummyint] *= scale;
      onesig_right[dummyint] *= scale;
      twosig_left[dummyint] *= scale;
      twosig_right[dummyint] *= scale;

      //==== skip points over 1
      //if(obs[dummyint]>1.0 || limit[dummyint]>1.0){
      //  n_central--;
      //  continue;
      //}

      onesig_left[dummyint] = limit[dummyint]-onesig_left[dummyint];
      onesig_right[dummyint] = onesig_right[dummyint] - limit[dummyint];
      twosig_left[dummyint] = limit[dummyint]-twosig_left[dummyint];
      twosig_right[dummyint] = twosig_right[dummyint] - limit[dummyint];

      if(max_obs<obs[dummyint]){
        max_obs = obs[dummyint];
        max_obs_mass = mass[dummyint];
      }
      if(min_obs>obs[dummyint]){
        min_obs = obs[dummyint];
        min_obs_mass = mass[dummyint];
      }

      dummyint++;
    }

    cout << "N mass points : " << n_central << endl;
    for(unsigned int k = 0; k < n_central ; k++){

      cout << "Mass = " << mass[k] << " expected = " << limit[k] << " + 1sigma = " << onesig_right[k] << " - 1sigma = "  << onesig_left[k] << " + 2sigma = " << twosig_right[k] << " - 2sigma = " << twosig_left[k] << endl;
    }
    
    cout << "Max : " << max_obs_mass << "\t" << max_obs << endl;
    cout << "Min : " << min_obs_mass << "\t" << min_obs << endl;

    //TGraph *gr_13TeV_obs = new TGraph(n_central,mass,obs);
    TGraphAsymmErrors *gr_13TeV_obs = new TGraphAsymmErrors(n_central,mass,obs,0,0,0,0);
    gr_13TeV_obs->SetLineWidth(3);
    gr_13TeV_obs->SetLineColor(kBlack);

    //TGraph *gr_13TeV_exp = new TGraph(n_central,mass,limit);
    TGraphAsymmErrors *gr_13TeV_exp = new TGraphAsymmErrors(n_central,mass,limit,0,0,0,0);
    gr_13TeV_exp->SetLineWidth(3);
    gr_13TeV_exp->SetLineStyle(2);
    //gr_13TeV_exp->SetFillColor(kWhite);

    TGraphAsymmErrors *gr_band_1sigma = new TGraphAsymmErrors(n_central, mass, limit, 0, 0, onesig_left, onesig_right);
    gr_band_1sigma->SetFillColor(kGreen+1);
    gr_band_1sigma->SetLineColor(kGreen+1);
    gr_band_1sigma->SetMarkerColor(kGreen+1);

    TGraphAsymmErrors *gr_band_2sigma = new TGraphAsymmErrors(n_central, mass, limit, 0, 0, twosig_left, twosig_right);
    gr_band_2sigma->SetFillColor(kOrange);
    gr_band_2sigma->SetLineColor(kOrange);
    gr_band_2sigma->SetMarkerColor(kOrange);


    //=== EXO-17-028 overlay
    const int nm_17028 = 20;
    double mass_17028[nm_17028] = {
      100, 125, 150,200,
      250, 300, 400, 500,
      600, 700, 800, 900,
      1000, 1100, 1200, 1300,
      1400, 1500, 1700, 2000,
    };

    double obs_17028[nm_17028], exp_17028[nm_17028];
    vector<double> tempvec_obs_17028, tempvec_exp_17028;
    vector<double> scales_17028;
    if(channel=="MuMu"){
      //tempvec_exp_17028 = {
      //  175.333, 21.5041, 32.925, 56.3397,
      //  70.8081, 99.3095, 20.4264, 42.5126,
      //  60.1695, 116.721, 15.8605, 25.8407,
      //  38.43, 64.346, 100.265, 151.699,
      //  247.709, 340.424, 1340.34
      //}; // these are the DYTypeI results
      tempvec_exp_17028 = {
        175.333, 21.5041, 32.925, 56.3397,
        70.8081, 95.0624, 18.8665, 38.4947,
        42.8618, 74.4406, 8.4652, 12.594,
        16.3718, 23.4646, 32.9925, 43.0679,
        61.6472, 74.073,  135.185, 304.058
      }; // DY+VBF TypeI results
      scales_17028 = {
        0.001, 0.01, 0.01,0.01,
        0.01,0.01,0.1, 0.1,
        0.1,0.1,1,1,
        1,1,1,1,
        1,1,1,1
      };
      //tempvec_obs_17028 = {
      //  215.218, 23.0424,41.8101,49.4399,
      //  57.1134,84.404,39.6932,44.5303,
      //  81.4561,195.31,16.3137,42.605,
      //  61.6358,103.589,150.295,220.286,
      //  365.037, 516.2, 1408.5
      //}; // these are the DYTypeI results
      tempvec_obs_17028 = {
        215.218, 23.0424, 41.8101, 49.4399,
        57.1134, 81.2452, 36.7668, 40.1455,
        56.0452, 122.926, 8.8852,  21.2021,
        27.1287, 38.7571, 48.9324, 63.9919,
        91.9852, 116.982, 142.081, 311.967
      }; // DY+VBF TypeI results
    }
    else   if(channel=="EE"){
      //https://github.com/jedori0228/HiggsAnalysis-CombinedLimit/blob/2016Data_HNDilepton_Limit/data/2016_HNDiLepton/Outputs_Tool/ElEl_Combined/result.txt
      //tempvec_exp_17028 = {
      //  467.448, 65.4099, 90.4068, 159.838,
      //  216.957, 284.563, 59.74, 94.6793, 
      //  104.302, 183.121, 30.189, 47.1442,
      //  72.0759, 117.305, 183.214, 285.811,
      //  434.08, 644.258, 2506.94
      //}; // these are the DYTypeI only results;
      tempvec_exp_17028 = {
        467.448, 65.4099, 90.4068, 159.838,
        216.957, 268.406, 53.8654, 78.1765, 
        76.2341, 118.242, 17.2123, 24.2464,
        31.61,   46.3963, 64.5734, 89.4366,
        115.964, 147.772, 279.822, 632.318
      }; // DY+VBF TypeI results;
      scales_17028 = {
        0.001, 0.01, 0.01,0.01,0.01,0.01,0.1, 0.1,0.1,0.1,1,1,1,1,1,1,1,1,1,1
      };
      //tempvec_obs_17028 = {
      //  368.924, 63.3389, 61.9159, 151.2,
      //  206.654, 254.261, 68.8604, 95.9664, 
      //  123.0, 274.57, 24.8148, 46.0243,
      //  95.1426, 164.011, 252.706, 379.988,
      //  419.316, 631.767, 2486.31
      //}; // these are the DYTypeI only results;
      tempvec_obs_17028 = {
        368.924, 63.3389, 61.9159, 151.2,
        206.654, 235.791, 63.261,  79.9909, 
        91.403,  174.955, 14.6124, 23.4109,
        43.3134, 64.2114, 86.8003, 117.953,
        112.79,  143.465, 276.02,  626.971
      }; // DY+VBF TypeI results
    }
    else   if(channel=="EMu"){
      //https://github.com/jedori0228/HiggsAnalysis-CombinedLimit/blob/2016Data_HNDilepton_Limit/data/2016_HNDiLepton/Outputs_Tool/EE_Combined/result.txt
      tempvec_exp_17028 = {
        410.683, 55.9408, 82.975,  136.932,
        178.214, 218.714, 39.6317, 46.813, 
        88.4598, 123.904, 14.4261, 17.8333,
        26.8884, 33.8577, 46.471,  61.5947,
        82.8097, 124.842, 257.358, 512.365
      }; // DY+VBF
      scales_17028 = {
        0.001, 0.01, 0.01,0.01,0.01,0.01,0.1, 0.1,0.1,0.1,1,1,1,1,1,1,1,1,1,1
      };
      tempvec_obs_17028 = {
        290.008, 33.6466, 62.3902, 187.344,
        168.976, 257.416, 51.8467, 45.2587, 
        90.0862, 134.809, 22.2963, 18.1025,
        28.0044, 34.4163, 46.4722, 61.1279,
        83.0085, 123.863, 245.571, 508.857
      }; // DY+VBF TypeI results
    }
    cout << "Channel : " << channel << endl;
    for(unsigned int j=0; j<tempvec_obs_17028.size(); j++){
      obs_17028[j] = (channel=="EMu") ? scales_17028[j]*tempvec_obs_17028.at(j)*0.01*0.5 : scales_17028[j]*tempvec_obs_17028.at(j)*0.01;
      exp_17028[j] = (channel=="EMu") ? scales_17028[j]*tempvec_exp_17028.at(j)*0.01*0.5 : scales_17028[j]*tempvec_exp_17028.at(j)*0.01;
      //cout << "mN = " << mass_17028[j] << " 17028 obs limit = " <<  scales_17028[j]*tempvec_obs_17028.at(j)*0.01 << endl;
    }

    TGraph *gr_17028_exp = new TGraph(nm_17028, mass_17028, exp_17028);
    gr_17028_exp->SetLineColor(kRed);
    gr_17028_exp->SetLineWidth(3);
    TGraph *gr_17028_obs = new TGraph(nm_17028, mass_17028, obs_17028);
    gr_17028_obs->SetLineColor(kRed);
    gr_17028_obs->SetLineWidth(3);


    //=== trilep overlay
    int temp_n_mass_trilep = 31;
    vector<double> temp_mass_trilep = {
      1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 20, 30, 40, 50, 60, 70, 75, 85, 90, 95, 100, 130, 150, 200, 400, 600, 800, 1000, 1200,
    };
    vector<double> tmpvec_obs_trilep = {
      0.0163199, 0.00182936, 0.00059415, 0.000280499, 0.000149561, 0.000103852, 6.81653E-05, 4.97358E-05, 3.52154E-05, 3.12335E-05, 2.46796E-05, 2.13769E-05, 1.48506E-05, 1.76593E-05, 1.87597E-05, 1.80473E-05, 2.77739E-05, 0.000156184, 0.000742155, 0.00241651, 0.00289491, 0.00345643, 0.00431929, 0.00716543, 0.00796569, 0.00888232, 0.0301448, 0.0835229, 0.20645, 0.441043, 0.847844,
    };

    if(channel=="EE"){
      temp_n_mass_trilep = 30;
      temp_mass_trilep = {
        1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 20, 30, 40, 50, 60, 70, 75, 85, 90, 100, 130, 150, 200, 400, 600, 800, 1000, 1200,
      };
      tmpvec_obs_trilep = {
        0.0135784, 0.00151879, 0.000447416, 0.000223742, 0.00011303, 7.23346E-05, 5.10346E-05, 3.77547E-05, 2.72229E-05, 2.33201E-05, 1.8688E-05, 1.75216E-05, 1.20661E-05, 1.60735E-05, 2.19737E-05, 3.32274E-05, 6.70456E-05, 0.000564676, 0.00186338, 0.00629086, 0.00622036, 0.00652451, 0.010974, 0.014264, 0.0135633, 0.0523753, 0.167425, 0.428148, 0.949388, 1.83977,
      };
    }

    const int n_mass_trilep = temp_n_mass_trilep;
    double mass_trilep[n_mass_trilep];
    double obs_trilep[n_mass_trilep];
    for(unsigned int i=0; i<tmpvec_obs_trilep.size(); i++){
      mass_trilep[i] = temp_mass_trilep.at(i);
      obs_trilep[i] = tmpvec_obs_trilep.at(i);
      //cout << i << "\t" << temp_mass_trilep[i] << "\t" << obs_trilep[i] << endl;
    }
    TGraph *gr_trilepLimit = new TGraph(n_mass_trilep, mass_trilep, obs_trilep);
    gr_trilepLimit->SetLineWidth(3);
    gr_trilepLimit->SetLineStyle(4);
    gr_trilepLimit->SetLineColor(kRed);


    //=== EXO-21-003 overlay
    const int n_mass_21003 = 19;
    double mass_21003[n_mass_21003] = {50,150,300,450,600,750,900,1000,1250,1500,1750,2000,2500,5000,7500,10000,15000,20000,25000};
    double obs_21003[n_mass_21003] = {0.0632,0.0125,0.0070,0.0061,0.0060,0.0066,0.0067,0.0075,0.0086,0.0098,0.0117,0.0136,0.0189,0.0539,0.1081,0.1908,0.4021,0.7433,1.1322};
    double obs_21003_sqrt[n_mass_21003] = {0.2514, 0.1118, 0.0837, 0.0781, 0.0775, 0.0812, 0.0819, 0.0866, 0.0927, 0.099, 0.1082, 0.1166, 0.1375, 0.2322, 0.3288, 0.4368, 0.6341, 0.8621, 1.064}; //xcheck with https://www.hepdata.net/record/131287
    double twolow_21003[n_mass_21003] = {0.0487,0.0100,0.0060,0.0048,0.0048,0.0050,0.0053,0.0057,0.0071,0.0081,0.0092,0.0111,0.0154,0.0438,0.0877,0.1552,0.3264,0.6055,0.9196};
    double onelow_21003[n_mass_21003] = {0.0668,0.0141,0.0076,0.0072,0.0068,0.0075,0.0071,0.0086,0.0102,0.0113,0.0132,0.0152,0.0213,0.0609,0.1220,0.2158,0.4540,0.8421,1.2790};
    double exp_21003[n_mass_21003] = {0.0981,0.0200,0.0112,0.0103,0.0103,0.0107,0.0112,0.0122,0.0142,0.0161,0.0190,0.0229,0.0317,0.0903,0.1812,0.3203,0.6738,1.2500,1.8984};
    double exp_21003_sqrt[n_mass_21003] = { 0.31320920, 0.14142136, 0.10583005, 0.10148892, 0.10148892, 0.10344080, 0.10583005, 0.11045361, 0.11916375, 0.12688578, 0.13784049, 0.15132746, 0.17804494, 0.30049958, 0.42567593, 0.56595053, 0.82085321, 1.1180340, 1.3778244 };
    double onehigh_21003[n_mass_21003] = {0.1459,0.0306,0.0173,0.0152,0.0152,0.0166,0.0166,0.0188,0.0218,0.0251,0.0297,0.0343,0.0477,0.1368,0.2757,0.4863,1.0257,1.9027,2.8822};
    double twohigh_21003[n_mass_21003] = {0.2096,0.0443,0.0255,0.0224,0.0224,0.0239,0.0243,0.0274,0.0321,0.0367,0.0433,0.0501,0.0702,0.2014,0.4058,0.7168,1.5094,2.8000,4.2485};

    TGraph *gr_21003_exp = new TGraph(n_mass_21003, mass_21003, exp_21003_sqrt); // the 21003 must be sqrt-ed.
    gr_21003_exp->SetLineWidth(3);
    gr_21003_exp->SetLineColor(kBlue);
    TGraph *gr_21003_obs = new TGraph(n_mass_21003, mass_21003, obs_21003_sqrt); // the 21003 must be sqrt-ed.
    gr_21003_obs->SetLineWidth(3);
    gr_21003_obs->SetLineColor(kBlue);

//  =======================================

    //==== Double beta decay
    double allxrange[2]= {0.,999999.};
    double dbeta_ee[2];
    for(int i=0; i<2; i++){
      dbeta_ee[i] = 5e-8*allxrange[i];
    }
    TGraph *gr_dbeta = new TGraph(2, allxrange, dbeta_ee);
    gr_dbeta->SetLineColor(kViolet);

    //==== EWPD
    double EWPD_ee[2], EWPD_mm[2];
    for(int i=0; i<2; i++){
      //==== https://journals.aps.org/prd/pdf/10.1103/PhysRevD.78.013010
      //==== 90% CL
      EWPD_ee[i] = 0.003;
      EWPD_mm[i] = 0.003;
      //==== https://www.epj-conferences.org/articles/epjconf/pdf/2013/21/epjconf_lhcp2013_19008.pdf
      //==== 95% CL
      EWPD_ee[i] = 0.041*0.041;
      EWPD_mm[i] = 0.030*0.030;
    }
    TGraph *gr_EWPD_ee = new TGraph(2, allxrange, EWPD_ee);
    TGraph *gr_EWPD_mm = new TGraph(2, allxrange, EWPD_mm);
    gr_EWPD_ee->SetLineColor(kCyan);
    gr_EWPD_mm->SetLineColor(kCyan);
    gr_EWPD_ee->SetLineStyle(2);
    gr_EWPD_mm->SetLineStyle(2);
    gr_EWPD_ee->SetLineWidth(3);
    gr_EWPD_mm->SetLineWidth(3);


    //======================
    //==== Dilepton full Run2 limit
    //======================

    //=== Legend
    cout << "Drawing Dilepton "+year+" limit ..." << endl;
    TLegend *lg = new TLegend(0.48, 0.15, 0.66, 0.45);
    lg->SetBorderSize(0);
    lg->SetFillStyle(0);
    TH1D *hist_emptylegend = new TH1D("hist_emptylegend","",1,0.,1.);
    hist_emptylegend->SetLineColor(0);

    if(DrawObserved) lg->AddEntry(gr_13TeV_obs,"Observed", "l");
    lg->AddEntry(gr_13TeV_exp,"Expected", "l");
    lg->AddEntry(gr_band_1sigma,"68% expected", "f");
    lg->AddEntry(gr_band_2sigma,"95% expected", "f");
    lg->AddEntry(hist_emptylegend,"","l");

    TLegend *lg_Alt = new TLegend(0.65, 0.15, 0.93, 0.48);
    lg_Alt->SetBorderSize(0);
    lg_Alt->SetFillStyle(0);
    if(channel=="MuMu"){
      //lg_Alt->AddEntry(gr_DELPHILimit, "DELPHI prompt", "l");
      //lg_Alt->AddEntry(gr_L3Limit, "L3", "l");
      //lg_Alt->AddEntry(gr_EWPD_mm, "EWPD (90% CL)", "l");
      //lg_Alt->AddEntry(gr_ATLAS_MuMu, "ATLAS 8 TeV", "l");
      //lg_Alt->AddEntry(gr_17028_exp, "CMS 13 TeV dilepton (exp)", "l");
      lg_Alt->AddEntry(gr_17028_exp, "Ref [1]   ", "l");
      //lg_Alt->AddEntry(gr_21003_exp, "CMS 13 TeV SSWW (exp)", "l");
      lg_Alt->AddEntry(gr_21003_exp, "Ref [5]   ", "l");
      //lg_Alt->AddEntry(gr_17028_obs, "CMS 13 TeV dilepton", "l");
      //lg_Alt->AddEntry(gr_trilepLimit, "CMS 13 TeV trilepton", "l");
      //lg_Alt->AddEntry(gr_21003_obs, "CMS 13 TeV SSWW", "l");
      //lg_Alt->AddEntry(gr_EWPD_mm, "EWPD", "l");
    }
    if(channel=="EE"){
      //lg_Alt->AddEntry(gr_DELPHILimit, "DELPHI prompt", "l");
      //lg_Alt->AddEntry(gr_L3_2Limit, "L3", "l");
      //lg_Alt->AddEntry(gr_EWPD_ee, "EWPD (90% CL)", "l");
      //lg_Alt->AddEntry(gr_ATLAS_EE, "ATLAS 8 TeV", "l");
      //lg_Alt->AddEntry(gr_17028_exp, "CMS 13 TeV dilepton", "l");
      //lg_Alt->AddEntry(gr_dbeta, "Neutrino-less double beta dacay", "l");
      //lg_Alt->AddEntry(gr_17028_exp, "CMS 13 TeV dilepton (exp)", "l");
      lg_Alt->AddEntry(gr_17028_exp, "Ref [1]   ", "l");
      //lg_Alt->AddEntry(gr_17028_obs, "CMS 13 TeV dilepton", "l");
      //lg_Alt->AddEntry(gr_trilepLimit, "CMS 13 TeV trilepton", "l");
      //lg_Alt->AddEntry(gr_EWPD_ee, "EWPD", "l");
    }
    if(channel=="EMu"){ //FIXME add 17028 results
      //lg_Alt->AddEntry(gr_8TeV_exp, "CMS 8 TeV", "l");
      //lg_Alt->AddEntry(hist_emptylegend,"#color[0]{CMS 13 TeV trilepton}","l");
      //lg_Alt->AddEntry(hist_emptylegend,"#color[0]{CMS 13 TeV trilepton}","l");
      //lg_Alt->AddEntry(hist_emptylegend,"#color[0]{CMS 13 TeV trilepton}","l");
      //lg_Alt->AddEntry(hist_emptylegend,"#color[0]{CMS 13 TeV trilepton}","l");
      //lg_Alt->AddEntry(hist_emptylegend,"#color[0]{CMS 13 TeV trilepton}","l");
      lg_Alt->AddEntry(gr_17028_exp, "CMS 13 TeV dilepton (exp)", "l");
      //lg_Alt->AddEntry(gr_17028_obs, "CMS 13 TeV dilepton", "l");
    }

    TCanvas *c_Dilep = new TCanvas("c_Dilep", "", 900, 800);
    canvas_margin(c_Dilep);
    c_Dilep->cd();
    c_Dilep->Draw();
    c_Dilep->SetLogx();
    c_Dilep->SetLogy();

    TH1D *dummy = new TH1D("hist", "", 100000, 0., 100000.);
    hist_axis(dummy);
    dummy->GetYaxis()->SetTitleSize(0.06);
    if(channel=="EE") dummy->GetYaxis()->SetTitle("#||{V_{eN}}^{2}");
    if(channel=="MuMu") dummy->GetYaxis()->SetTitle("#||{V_{#muN}}^{2}");
    if(channel=="EMu"){
      dummy->GetYaxis()->SetTitle("#scale[0.8]{#frac{#||{ V_{eN}V_{#muN}^{*}}^{2}}{#||{ V_{eN} }^{2} + #||{ V_{#muN} }^{2}}}");
      dummy->GetYaxis()->SetTitleOffset(1.8);
      dummy->GetYaxis()->SetTitleSize(0.04);
    }
    dummy->GetXaxis()->SetTitle("m_{N} (GeV)");
    //dummy->GetXaxis()->SetRangeUser(90., 25000); //FIXME
    dummy->GetXaxis()->SetRangeUser(90., 65000); //FIXME
    dummy->GetYaxis()->SetRangeUser(1e-4, 1.); //FIXME
    dummy->SetTitle("");
    dummy->Draw("hist");

    // Now draw limits
    gr_band_2sigma->Draw("3same");
    gr_band_1sigma->Draw("3same");
    gr_13TeV_exp->Draw("lsame");
    gr_17028_exp->Draw("lsame");
    //gr_17028_obs->Draw("lsame");
    //gr_8and13TeV_obs->Draw("lsame");
    if(channel=="MuMu"){
      //gr_L3Limit->Draw("lsame");
      //gr_DELPHILimit->Draw("lsame");
      gr_21003_exp->Draw("lsame");
      //gr_21003_obs->Draw("lsame");
      //gr_trilepLimit->Draw("lsame");
      //gr_EWPD_mm->Draw("lsame");
      //gr_ATLAS_MuMu->Draw("lsame");
    }
    if(channel=="EE"){
      //gr_L3_2Limit->Draw("lsame");
      //gr_DELPHILimit->Draw("lsame");
      //gr_trilepLimit->Draw("lsame");
      //gr_EWPD_ee->Draw("lsame");
      //gr_dbeta->Draw("lsame");
      //gr_ATLAS_EE->Draw("lsame");
    }

    if(DrawObserved) gr_13TeV_obs->Draw("lsame");

    lg->Draw();
    lg_Alt->Draw();

    latex_Lumi.SetTextSize(0.035);
    latex_Lumi.SetTextFont(42);
    TString lumi;
    if(year=="2016") lumi = "36.5";
    else if(year=="2016preVFP") lumi = "19.5";
    else if(year=="2016postVFP") lumi = "16.8";
    else if(year=="2017") lumi = "41.5";
    else if(year=="2018") lumi = "59.8";
    else if(year=="Run2") lumi = "137.9";
    if(tag.Contains("Run2")) lumi = "137.9";
    if(tag.Contains("Run23")) lumi = "400";
    
    //latex_CMSPreliminary.DrawLatex(0.16, 0.96, "#scale[0.8]{CMS #bf{#it{Preliminary}}}");
    if(tag.Contains("Run23")) latex_Lumi.DrawLatex(0.734, 0.96, lumi+" fb^{-1} (13.6 TeV)");
    else latex_Lumi.DrawLatex(0.736, 0.96, lumi+" fb^{-1} (13 TeV)");
    latex_title.SetTextSize(0.04);
    latex_title.SetLineWidth(2);
    latex_title.DrawLatex(0.25, 0.84, "#font[41]{95% CL upper limit}");
    latex_title.SetTextSize(0.05);
    //latex_title.DrawLatex(0.25, 0.88, "#font[62]{CMS}");

    dummy->Draw("axissame");
    //c_Dilep->SaveAs(this_plotpath+"/"+year+"_"+channel+"_13TeV_mixing_"+channel+"_"+myWP+".png");
  }

  return;
}

void CompareLimits(TString channel=""){

  setTDRStyle();

  vector<TString> files;
  //files.push_back(filepath+"/SR2HT_SR3l2pt_ChargeSplit/2017_"+channel+"_HNL_UL_Asym_limit.txt");
  //files.push_back(filepath+"/SR2HT_SR3l2pt/2017_"+channel+"_HNL_UL_Asym_limit.txt");
  //files.push_back(filepath+"/NewOpt_HNL_ULID/Run2_"+channel+"_Asym_limit.txt");
  files.push_back(filepath+"/CRtest_HNL_ULID_Syst/2017_"+channel+"_syst_Run2Scaled_Asym_limit.txt");

  vector<vector<double>> masses, obss, limits, onesig_lefts, onesig_rights, twosig_lefts, twosig_rights;
  vector<int> n_centrals;

  for(int i=0; i<files.size(); i++){

    // iterate with each file
    string elline;
    cout << "Reading "+files.at(i)+" ..." << endl;
    ifstream in;
    in.open(files.at(i));
    int n_central = 24; //FIXME depending on the bins
    vector<double> mass, obs, limit, onesig_left, onesig_right, twosig_left, twosig_right;

    int dummyint=0;
    while(getline(in,elline)){
      cout << elline << endl;
      double this_mass, this_obs, this_limit, this_onesig_left, this_onesig_right, this_twosig_left, this_twosig_right;
      std::istringstream is( elline );
      if (is >> this_mass) mass.push_back(this_mass);
      if (is >> this_obs) obs.push_back(this_obs);
      if (is >> this_twosig_left) twosig_left.push_back(this_twosig_left);
      if (is >> this_onesig_left) onesig_left.push_back(this_onesig_left);
      if (is >> this_limit) limit.push_back(this_limit);
      if (is >> this_onesig_right) onesig_right.push_back(this_onesig_right);
      if (is >> this_twosig_right) twosig_right.push_back(this_twosig_right);

      double scale = 0.01;
      //double scale=1.;
      //if(mass[dummyint]<=100) scale *= 0.001; // 0.001 only for low mass (https://cms-talk.web.cern.ch/t/too-large-error-with-hybridnew/32844)
      //else scale *= 0.01; // input signal scaled as V^2 = 0.01 by default

      obs[dummyint] *= scale;

      if(channel=="EMu"){
        if(dummyint < 6){
          limit[dummyint] *= 0.5;
          onesig_left[dummyint]  *= 0.5;
          onesig_right[dummyint] *= 0.5;
          twosig_left[dummyint]  *= 0.5;
          twosig_right[dummyint] *= 0.5;
        } //FIXME This is because the MuE histograms are wrong in BDT Limit input. After fixing the issue, remove these lines.
      }
      limit[dummyint] *= scale;
      onesig_left[dummyint] *= scale;
      onesig_right[dummyint] *= scale;
      twosig_left[dummyint] *= scale;
      twosig_right[dummyint] *= scale;

      //==== skip points
      //if(obs[dummyint]>1. || limit[dummyint]>1.){
      //  n_central--;
      //  continue;
      //}

      onesig_left[dummyint] = limit[dummyint]-onesig_left[dummyint];
      onesig_right[dummyint] = onesig_right[dummyint] - limit[dummyint];
      twosig_left[dummyint] = limit[dummyint]-twosig_left[dummyint];
      twosig_right[dummyint] = twosig_right[dummyint] - limit[dummyint];

      dummyint++;
    }
    
    n_centrals.push_back(n_central);
    masses.push_back(mass);
    obss.push_back(obs);
    limits.push_back(limit);
    onesig_lefts.push_back(onesig_left);
    onesig_rights.push_back(onesig_right);
    twosig_lefts.push_back(twosig_left);
    twosig_rights.push_back(twosig_right);
    //cout << limits.size() << endl;
    //for(int ii=0; ii<limits.size(); ii++) cout << limits.at(ii).at(10) << endl;

  }

  //TGraphAsymmErrors
  TGraphAsymmErrors *gr_obs0 = new TGraphAsymmErrors(n_centrals[0],&masses[0][0],&obss[0][0],0,0,0,0);
  gr_obs0->SetLineWidth(3);
  gr_obs0->SetLineColor(kBlack);

  TGraphAsymmErrors *gr_exp0 = new TGraphAsymmErrors(n_centrals[0],&masses[0][0],&limits[0][0],0,0,0,0);
  gr_exp0->SetLineWidth(3);
  gr_exp0->SetLineStyle(2);
  gr_exp0->SetLineColor(kBlack);

  TGraphAsymmErrors *gr_band_1sigma0 = new TGraphAsymmErrors(n_centrals[0], &masses[0][0], &limits[0][0], 0, 0, &onesig_lefts[0][0], &onesig_rights[0][0]);
  gr_band_1sigma0->SetFillColor(kGreen+1);
  gr_band_1sigma0->SetLineColor(kGreen+1);
  gr_band_1sigma0->SetMarkerColor(kGreen+1);

  TGraphAsymmErrors *gr_band_2sigma0 = new TGraphAsymmErrors(n_centrals[0], &masses[0][0], &limits[0][0], 0, 0, &twosig_lefts[0][0], &twosig_rights[0][0]);
  gr_band_2sigma0->SetFillColor(kOrange);
  gr_band_2sigma0->SetLineColor(kOrange);
  gr_band_2sigma0->SetMarkerColor(kOrange);

  // Use when there are more than two input limits to compare
  //TGraph *gr_exp1 = new TGraph(n_centrals[1],&masses[1][0],&limits[1][0]);
  //gr_exp1->SetLineWidth(3);
  //gr_exp1->SetLineStyle(2);
  //gr_exp1->SetLineColor(kViolet);

  //TGraph *gr_exp2 = new TGraph(n_centrals[2],&masses[2][0],&limits[2][0]);
  //gr_exp2->SetLineWidth(3);
  //gr_exp2->SetLineStyle(2);
  //gr_exp2->SetLineColor(kGreen+2);

  //TGraph *gr_exp3 = new TGraph(n_centrals[3],&masses[3][0],&limits[3][0]);
  //gr_exp3->SetLineWidth(3);
  //gr_exp3->SetLineStyle(2);
  //gr_exp3->SetLineColor(kBlue);


  //=== EXO-17-028 overlay
  const int nm_17028 = 20;
  double mass_17028[nm_17028] = {
    100, 125, 150,200,
    250, 300, 400, 500,
    600, 700, 800, 900,
    1000, 1100, 1200, 1300,
    1400, 1500, 1700, 2000,
  };

  double obs_17028[nm_17028], exp_17028[nm_17028];
  vector<double> tempvec_obs_17028, tempvec_exp_17028;
  vector<double> scales_17028;
  if(channel=="MuMu"){
    //tempvec_exp_17028 = {
    //  175.333, 21.5041, 32.925, 56.3397,
    //  70.8081, 99.3095, 20.4264, 42.5126,
    //  60.1695, 116.721, 15.8605, 25.8407,
    //  38.43, 64.346, 100.265, 151.699,
    //  247.709, 340.424, 1340.34
    //}; // these are the DYTypeI results
    tempvec_exp_17028 = {
      175.333, 21.5041, 32.925, 56.3397,
      70.8081, 95.0624, 18.8665, 38.4947,
      42.8618, 74.4406, 8.4652, 12.594,
      16.3718, 23.4646, 32.9925, 43.0679,
      61.6472, 74.073,  135.185, 304.058
    }; // DY+VBF TypeI results
    scales_17028 = {
      0.001, 0.01, 0.01,0.01,
      0.01,0.01,0.1, 0.1,
      0.1,0.1,1,1,
      1,1,1,1,
      1,1,1,1
    };
    //tempvec_obs_17028 = {
    //  215.218, 23.0424,41.8101,49.4399,
    //  57.1134,84.404,39.6932,44.5303,
    //  81.4561,195.31,16.3137,42.605,
    //  61.6358,103.589,150.295,220.286,
    //  365.037, 516.2, 1408.5
    //}; // these are the DYTypeI results
    tempvec_obs_17028 = {
      215.218, 23.0424, 41.8101, 49.4399,
      57.1134, 81.2452, 36.7668, 40.1455,
      56.0452, 122.926, 8.8852,  21.2021,
      27.1287, 38.7571, 48.9324, 63.9919,
      91.9852, 116.982, 142.081, 311.967
    }; // DY+VBF TypeI results
  }
  else   if(channel=="EE"){
    //https://github.com/jedori0228/HiggsAnalysis-CombinedLimit/blob/2016Data_HNDilepton_Limit/data/2016_HNDiLepton/Outputs_Tool/ElEl_Combined/result.txt
    //tempvec_exp_17028 = {
    //  467.448, 65.4099, 90.4068, 159.838,
    //  216.957, 284.563, 59.74, 94.6793, 
    //  104.302, 183.121, 30.189, 47.1442,
    //  72.0759, 117.305, 183.214, 285.811,
    //  434.08, 644.258, 2506.94
    //}; // these are the DYTypeI only results;
    tempvec_exp_17028 = {
      467.448, 65.4099, 90.4068, 159.838,
      216.957, 268.406, 53.8654, 78.1765, 
      76.2341, 118.242, 17.2123, 24.2464,
      31.61,   46.3963, 64.5734, 89.4366,
      115.964, 147.772, 279.822, 632.318
    }; // DY+VBF TypeI results;
    scales_17028 = {
      0.001, 0.01, 0.01,0.01,0.01,0.01,0.1, 0.1,0.1,0.1,1,1,1,1,1,1,1,1,1,1
    };
    //tempvec_obs_17028 = {
    //  368.924, 63.3389, 61.9159, 151.2,
    //  206.654, 254.261, 68.8604, 95.9664, 
    //  123.0, 274.57, 24.8148, 46.0243,
    //  95.1426, 164.011, 252.706, 379.988,
    //  419.316, 631.767, 2486.31
    //}; // these are the DYTypeI only results;
    tempvec_obs_17028 = {
      368.924, 63.3389, 61.9159, 151.2,
      206.654, 235.791, 63.261,  79.9909, 
      91.403,  174.955, 14.6124, 23.4109,
      43.3134, 64.2114, 86.8003, 117.953,
      112.79,  143.465, 276.02,  626.971
    }; // DY+VBF TypeI results
  }
  else   if(channel=="EMu"){
    //https://github.com/jedori0228/HiggsAnalysis-CombinedLimit/blob/2016Data_HNDilepton_Limit/data/2016_HNDiLepton/Outputs_Tool/EE_Combined/result.txt
    tempvec_exp_17028 = {
      410.683, 55.9408, 82.975,  136.932,
      178.214, 218.714, 39.6317, 46.813, 
      88.4598, 123.904, 14.4261, 17.8333,
      26.8884, 33.8577, 46.471,  61.5947,
      82.8097, 124.842, 257.358, 512.365
    }; // DY+VBF
    scales_17028 = {
      0.001, 0.01, 0.01,0.01,0.01,0.01,0.1, 0.1,0.1,0.1,1,1,1,1,1,1,1,1,1,1
    };
    tempvec_obs_17028 = {
      290.008, 33.6466, 62.3902, 187.344,
      168.976, 257.416, 51.8467, 45.2587, 
      90.0862, 134.809, 22.2963, 18.1025,
      28.0044, 34.4163, 46.4722, 61.1279,
      83.0085, 123.863, 245.571, 508.857
    }; // DY+VBF TypeI results
  }
  cout << "Channel : " << channel << endl;
  for(unsigned int j=0; j<tempvec_obs_17028.size(); j++){
    obs_17028[j] = (channel=="EMu") ? scales_17028[j]*tempvec_obs_17028.at(j)*0.01*0.5 : scales_17028[j]*tempvec_obs_17028.at(j)*0.01;
    exp_17028[j] = (channel=="EMu") ? scales_17028[j]*tempvec_exp_17028.at(j)*0.01*0.5 : scales_17028[j]*tempvec_exp_17028.at(j)*0.01;
    //cout << "mN = " << mass_17028[j] << " 17028 obs limit = " <<  scales_17028[j]*tempvec_obs_17028.at(j)*0.01 << endl;
  }

  TGraph *gr_17028_exp = new TGraph(nm_17028, mass_17028, exp_17028);
  gr_17028_exp->SetLineColor(kRed);
  gr_17028_exp->SetLineWidth(3);
  TGraph *gr_17028_obs = new TGraph(nm_17028, mass_17028, obs_17028);
  gr_17028_obs->SetLineColor(kRed);
  gr_17028_obs->SetLineWidth(3);

  //=== EXO-21-003 overlay
  const int n_mass_21003 = 19;
  double mass_21003[n_mass_21003] = {50,150,300,450,600,750,900,1000,1250,1500,1750,2000,2500,5000,7500,10000,15000,20000,25000};
  double obs_21003[n_mass_21003] = {0.0632,0.0125,0.0070,0.0061,0.0060,0.0066,0.0067,0.0075,0.0086,0.0098,0.0117,0.0136,0.0189,0.0539,0.1081,0.1908,0.4021,0.7433,1.1322};
  double obs_21003_sqrt[n_mass_21003] = {0.2514, 0.1118, 0.0837, 0.0781, 0.0775, 0.0812, 0.0819, 0.0866, 0.0927, 0.099, 0.1082, 0.1166, 0.1375, 0.2322, 0.3288, 0.4368, 0.6341, 0.8621, 1.064}; //xcheck with https://www.hepdata.net/record/131287
  double twolow_21003[n_mass_21003] = {0.0487,0.0100,0.0060,0.0048,0.0048,0.0050,0.0053,0.0057,0.0071,0.0081,0.0092,0.0111,0.0154,0.0438,0.0877,0.1552,0.3264,0.6055,0.9196};
  double onelow_21003[n_mass_21003] = {0.0668,0.0141,0.0076,0.0072,0.0068,0.0075,0.0071,0.0086,0.0102,0.0113,0.0132,0.0152,0.0213,0.0609,0.1220,0.2158,0.4540,0.8421,1.2790};
  double exp_21003[n_mass_21003] = {0.0981,0.0200,0.0112,0.0103,0.0103,0.0107,0.0112,0.0122,0.0142,0.0161,0.0190,0.0229,0.0317,0.0903,0.1812,0.3203,0.6738,1.2500,1.8984};
  double exp_21003_sqrt[n_mass_21003] = { 0.31320920, 0.14142136, 0.10583005, 0.10148892, 0.10148892, 0.10344080, 0.10583005, 0.11045361, 0.11916375, 0.12688578, 0.13784049, 0.15132746, 0.17804494, 0.30049958, 0.42567593, 0.56595053, 0.82085321, 1.1180340, 1.3778244 };
  double onehigh_21003[n_mass_21003] = {0.1459,0.0306,0.0173,0.0152,0.0152,0.0166,0.0166,0.0188,0.0218,0.0251,0.0297,0.0343,0.0477,0.1368,0.2757,0.4863,1.0257,1.9027,2.8822};
  double twohigh_21003[n_mass_21003] = {0.2096,0.0443,0.0255,0.0224,0.0224,0.0239,0.0243,0.0274,0.0321,0.0367,0.0433,0.0501,0.0702,0.2014,0.4058,0.7168,1.5094,2.8000,4.2485};

  TGraph *gr_21003_exp = new TGraph(n_mass_21003, mass_21003, exp_21003_sqrt); // the 21003 must be sqrt-ed.
  gr_21003_exp->SetLineWidth(3);
  gr_21003_exp->SetLineColor(kBlue);
  TGraph *gr_21003_obs = new TGraph(n_mass_21003, mass_21003, obs_21003_sqrt); // the 21003 must be sqrt-ed.
  gr_21003_obs->SetLineWidth(3);
  gr_21003_obs->SetLineColor(kBlue);

  // ratio for charge split vs inclusive
  //double ratio_ChargeSplit[23];
  //for(int i=0; i<23; i++) ratio_ChargeSplit[i] = limits[1][i]/limits[0][i];

  // ratio with EXO-17-028 expected //FIXME this is mass dependent.
  double mass_comp_17028[17] = {100,150,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1500,1700,2000};
  int index_comp_17028[17] = {0,2,3,5,6,7,8,9,10,11,12,13,14,15,17,18,19};
  int index_comp_limit[17] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16};
  double ratio_17028[17];
  for(int i=0; i<17; i++) ratio_17028[i] = exp_17028[index_comp_17028[i]]/limits[0][index_comp_limit[i]];

  // ratio with EXO-21-003 expected //FIXME this is mass dependent.
  double mass_comp_21003[13] = {150,300,600,900,1000,1500,2000,2500,5000,7500,10000,15000,20000};
  double obs_comp_21003[13] = {0.1118, 0.0837, 0.0775, 0.0819, 0.0866, 0.099, 0.1166, 0.1375, 0.2322, 0.3288, 0.4368, 0.6341, 0.8621}; //xcheck with https://www.hepdata.net/record/131287
  double exp_comp_21003[13] = {0.14142136, 0.10583005, 0.10148892, 0.10583005, 0.11045361, 0.12688578, 0.15132746, 0.17804494, 0.30049958, 0.42567593, 0.56595053, 0.82085321, 1.1180340 };
  double ratio_21003[13];
  ratio_21003[0] = exp_comp_21003[0]/limits[0][1];
  ratio_21003[1] = exp_comp_21003[1]/limits[0][3];
  ratio_21003[2] = exp_comp_21003[2]/limits[0][6];
  ratio_21003[3] = exp_comp_21003[3]/limits[0][9];
  ratio_21003[4] = exp_comp_21003[4]/limits[0][10];
  ratio_21003[5] = exp_comp_21003[5]/limits[0][14];
  ratio_21003[6] = exp_comp_21003[6]/limits[0][16];
  ratio_21003[7] = exp_comp_21003[7]/limits[0][17];
  ratio_21003[8] = exp_comp_21003[8]/limits[0][19];
  ratio_21003[9] = exp_comp_21003[9]/limits[0][20];
  ratio_21003[10] = exp_comp_21003[10]/limits[0][21];
  ratio_21003[11] = exp_comp_21003[11]/limits[0][22];
  ratio_21003[12] = exp_comp_21003[12]/limits[0][23];

  //==== CANVAS
  TCanvas *c1 = new TCanvas("c1", "", 1000, 1000);
  c1->cd();

  //==== PAD : drawing distribution
  TPad *c_up = new TPad("c_up", "", 0, 0.25, 1, 1);
  c_up->SetTopMargin(0.08);
  c_up->SetBottomMargin(0.017);
  c_up->SetLeftMargin(0.14);
  c_up->SetRightMargin(0.04);
  c_up->SetLogx();
  c_up->SetLogy();
  c_up->Draw();
  c_up->cd();

  TH1D *dummy = new TH1D("hist", "", 100000, 0., 100000.);
  hist_axis(dummy);
  dummy->GetYaxis()->SetTitleSize(0.06);
  if(channel=="MuMu") dummy->GetYaxis()->SetTitle("#||{V_{#muN}}^{2}");
  else if(channel=="EE") dummy->GetYaxis()->SetTitle("#||{V_{eN}}^{2}");
  else if(channel=="EMu"){
    dummy->GetYaxis()->SetTitle("#scale[0.8]{#frac{#||{ V_{eN}V_{#muN}^{*}}^{2}}{#||{ V_{eN} }^{2} + #||{ V_{#muN} }^{2}}}");
    dummy->GetYaxis()->SetTitleOffset(1.5);
    dummy->GetYaxis()->SetTitleSize(0.04);
  }
  dummy->GetXaxis()->SetTitle("m_{N} (GeV)");
  dummy->GetXaxis()->SetLabelSize(0);
  dummy->GetXaxis()->SetRangeUser(90., 25000);
  dummy->GetYaxis()->SetRangeUser(1e-4, 1.); //FIXME
  dummy->SetTitle("");
  dummy->Draw("hist");

  TLegend *lg = new TLegend(0.48, 0.15, 0.7, 0.45);
  lg->SetBorderSize(0);
  lg->SetFillStyle(0);

  if(channel=="MuMu") lg->AddEntry(gr_exp0,"2017 Expected #mu#mu", "l");
  else if(channel=="EE") lg->AddEntry(gr_exp0,"2017 Expected ee", "l");
  //lg->AddEntry(gr_exp0,"2017 Expected #mu#mu ChargeSpl.", "l");
  //lg->AddEntry((TObject*)0,"(scaled to Run2 lumi)", "");
  lg->AddEntry(gr_band_1sigma0,"68% expected", "f");
  lg->AddEntry(gr_band_2sigma0,"95% expected", "f");

  TLegend *lg_Alt = new TLegend(0.7, 0.15, 0.93, 0.48);
  lg_Alt->SetBorderSize(0);
  lg_Alt->SetFillStyle(0);

  //lg_Alt->AddEntry((TObject*)0,"", "");
  //lg_Alt->AddEntry(gr_exp1, "2017 Expected #mu#mu ChargeInc.", "l");
  //lg_Alt->AddEntry(gr_exp2, "2017 Expected ee", "l");
  //lg_Alt->AddEntry(gr_exp3, "2017 Expected e#mu", "l");
  lg_Alt->AddEntry(gr_17028_exp, "CMS 13 TeV dilepton (exp)", "l");
  if(channel=="MuMu") lg_Alt->AddEntry(gr_21003_exp, "CMS 13 TeV SSWW (exp)", "l");
  //lg_Alt->AddEntry(gr_17028_obs, "CMS 13 TeV dilepton", "l");
  //lg_Alt->AddEntry(gr_21003_obs, "CMS 13 TeV SSWW", "l");

  gr_band_2sigma0->Draw("3same");
  gr_band_1sigma0->Draw("3same");
  gr_exp0->Draw("lsame");
  //gr_exp1->Draw("lsame");
  //gr_exp2->Draw("lsame");
  //gr_exp3->Draw("lsame");
  gr_17028_exp->Draw("lsame");
  if(channel=="MuMu") gr_21003_exp->Draw("lsame");
  //gr_17028_obs->Draw("lsame");
  //gr_21003_obs->Draw("lsame");

  // Axis, tickles
  dummy->Draw("axissame");

  lg->Draw();
  lg_Alt->Draw();

  TLatex latex_CMSPreliminary, latex_Lumi, latex_title;
  latex_CMSPreliminary.SetNDC();
  latex_Lumi.SetNDC();
  latex_title.SetNDC();

  latex_Lumi.SetTextSize(0.035);
  latex_Lumi.SetTextFont(42);
  //TString lumi = "41.5"; //FIXME
  TString lumi = "137.9"; //FIXME
  
  latex_CMSPreliminary.DrawLatex(0.14, 0.93, "#scale[0.8]{CMS #bf{#it{Preliminary}}}");
  latex_Lumi.DrawLatex(0.76, 0.93, lumi+" fb^{-1} (13 TeV)");
  latex_title.SetTextSize(0.04);
  latex_title.SetLineWidth(2);
  latex_title.DrawLatex(0.25, 0.79, "#font[41]{95% CL upper limit}");
  latex_title.SetTextSize(0.05);
  latex_title.DrawLatex(0.25, 0.83, "#font[62]{CMS}");


  c1->cd();
  // PAD : drawing ratio
  TPad *c_down = new TPad("c_down", "", 0, 0, 1, 0.25);
  c_down->SetTopMargin(0.03);
  c_down->SetBottomMargin(0.2);
  c_down->SetLeftMargin(0.14);
  c_down->SetRightMargin(0.04);
  c_down->SetLogx();
  c_down->SetLogy();
  c_down->SetGridx();
  c_down->SetGridy();
  c_down->Draw();
  c_down->cd();


  TH1D *dummy2 = new TH1D("hist2", "", 100000, 0., 100000.);
  dummy2->GetYaxis()->SetTitleSize(0.1);
  dummy2->GetYaxis()->SetTitleOffset(0.5);
  if(channel=="MuMu") dummy2->GetYaxis()->SetTitle("#frac{limits}{Run2 #mu#mu}");
  else if(channel=="EE") dummy2->GetYaxis()->SetTitle("#frac{limits}{Run2 ee}");
  else if(channel=="EMu") dummy2->GetYaxis()->SetTitle("#frac{limits}{Run2 e#mu}");
  dummy2->GetYaxis()->SetLabelSize(0.07);
  dummy2->GetXaxis()->SetTitleSize(0.1);
  dummy2->GetXaxis()->SetTitleOffset(0.4);
  dummy2->GetXaxis()->SetTitle("m_{N} (GeV)");
  dummy2->GetXaxis()->SetLabelSize(0.07);
  dummy2->GetXaxis()->SetRangeUser(90., 25000);
  dummy2->GetYaxis()->SetRangeUser(0.85, 15);
  dummy2->SetTitle("");
  dummy2->Draw("hist");

  //vector<vector<double>> ratios;
  //for(int i=0; i<limits.size(); i++){
  //  vector<double> this_ratio;
  //  for(int j=0; j<limits.at(i).size(); j++){
  //    this_ratio.push_back(limits[i][j]/limits[0][j]);
  //  }
  //  ratios.push_back(this_ratio);
  //}

  //TGraph *gr_rat0 = new TGraph(n_centrals[0],&masses[0][0],&ratios[0][0]);
  //gr_rat0->Draw("psame");
  //TGraph *gr_rat1 = new TGraph(n_centrals[1],&masses[1][0],&ratios[1][0]);
  //gr_rat1->SetMarkerColor(kRed);
  //gr_rat1->Draw("psame");
  //TGraph *gr_rat2 = new TGraph(n_centrals[2],&masses[2][0],&ratios[2][0]);
  //gr_rat2->SetMarkerColor(kGreen+2);
  //gr_rat2->Draw("psame");
  //TGraph *gr_rat3 = new TGraph(n_centrals[3],&masses[3][0],&ratios[3][0]);
  //gr_rat3->SetMarkerColor(kBlue);
  //gr_rat3->Draw("psame");

  TGraph *gr_ratio_17028 = new TGraph(15,mass_comp_17028,ratio_17028);
  gr_ratio_17028->SetMarkerColor(kRed);
  gr_ratio_17028->Draw("psame");
  if(channel=="MuMu"){
    TGraph *gr_ratio_21003 = new TGraph(12,mass_comp_21003,ratio_21003);
    gr_ratio_21003->SetMarkerColor(kBlue);
    gr_ratio_21003->Draw("psame");
  }
  //TGraph *gr_ratio_ChargeSplit = new TGraph(23,&masses[0][0],ratio_ChargeSplit);
  //gr_ratio_ChargeSplit->SetMarkerColor(kViolet);
  //gr_ratio_ChargeSplit->Draw("psame");

  gSystem->mkdir(plotpath+"/CRtest_HNL_ULID_Syst/", kTRUE); // recursive option
  c1->SaveAs(plotpath+"/CRtest_HNL_ULID_Syst/2017_"+channel+"_syst_Run2Scaled_Asym_limit_comp.png");
}