import ROOT

rootfile = ROOT.TFile("../Inputs/signal_hists.root", "UPDATE")

def delete(hist):
    rootfile.Delete(hist+";*")
    rootfile.Write()
    rootfile.Close()

def newhist(sys):

    err_summed = ROOT.TH1F(sys+"_largesummed", sys+"_largesummed", 100, 0, 100)

    err_hist = rootfile.Get("mass_large/signal_sys_"+sys)
    Sig_hist = rootfile.Get("mass_large/signal;1")
    
    for bin in range(1, err_hist.GetNbinsX() + 1):
        err_summed.SetBinContent(bin, Sig_hist.GetBinContent(bin)+err_hist.GetBinContent(bin))

    err_summed.Write()


newhist("TRIG__1up")
newhist("TRIG__1down")
newhist("EG_RESOLUTION_ALL__1down")
newhist("EG_RESOLUTION_ALL__1up")
newhist("EG_SCALE_ALL__1down")
newhist("EG_SCALE_ALL__1up")
newhist("PH_RECOeta")
newhist("PH_PIDeta")
