import ROOT

def delete(hist):
    destination_file = ROOT.TFile("../Inputs/signal_hists.root", "UPDATE")
    destination_file.Delete(hist+";*")
    destination_file.Write()

def mkhist(var, branch):

    # Open the ROOT file containing the ntuple
    file = ROOT.TFile("../Inputs/ALP_samples/axion_ma"+var+".root", "READ")

    # Get the ntuple from the file
    tree = file.Get(branch)

    # Create a histogram
    num_bins = 100
    bin_min = 0
    bin_max = 100
    histogram = ROOT.TH1F(branch+"massScaled"+var, "mass", num_bins, bin_min, bin_max)

    # Fill the histogram with the ntuple
    tree.Draw("Mass>>"+branch+"massScaled"+var, "weight*(aco<0.01)")  # Replace variable_name with the variable you want to use

    # Optionally, set the histogram properties
    histogram.GetXaxis().SetTitle("m_{a} [GeV]")
    histogram.GetYaxis().SetTitle("Events/GeV")
    histogram.SetLineColor(ROOT.kRed)
    histogram.SetFillColor(ROOT.kWhite)


    destination_file = ROOT.TFile("../Inputs/signal_hists.root", "UPDATE")
    destination_file.cd()
    histogram.Write()
    destination_file.Write()
    destination_file.Close()

    # Close the file
    file.Close()

# Open the ROOT file for writing
destination_file = ROOT.TFile("../Inputs/signal_hists.root", "UPDATE")
destination_file.Close()

# Generate histograms and save them
for tr in ["EG_RESOLUTION_ALL__1down", "EG_RESOLUTION_ALL__1up", "EG_SCALE_AF2__1down", "EG_SCALE_AF2__1up", "EG_SCALE_ALL__1down", "EG_SCALE_ALL__1up", "TRIG_1up", "TRIG_1down", "PH_RECOeta", "PH_PIDeta"]:
    for i in range(5,21):
        mkhist("%d" % i, tr)
    for i in range(21,30):    
        mkhist("%d" % i, tr)
    for i in range(30,110,10):
        mkhist("%d" % i, tr)
