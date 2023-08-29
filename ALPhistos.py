import ROOT

def delete(hist):
    destination_file = ROOT.TFile("../Inputs/signal_hists.root", "UPDATE")
    destination_file.Delete(hist+";*")
    destination_file.Write()

def mkhist(var):

    # Open the ROOT file containing the ntuple
    file = ROOT.TFile("../Inputs/ALP_samples/axion_ma"+var+".root", "READ")

    # Get the ntuple from the file
    tree = file.Get("nominal")

    # Create a histogram
    num_bins = 100
    bin_min = 0
    bin_max = 100
    histogram = ROOT.TH1F("massScaled"+var, "mass", num_bins, bin_min, bin_max)

    # Fill the histogram with the ntuple
    tree.Draw("Mass>>massScaled"+var, "weight*(aco<0.01)")  # Replace variable_name with the variable you want to use

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
for i in range(5,21):
    mkhist("%d" % i)
for i in range(21,30):    
    mkhist("%d" % i)
for i in range(30,110,10):
    mkhist("%d" % i)


