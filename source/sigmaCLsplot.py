import ROOT
from ROOT import TCanvas, TGraph, TGraphAsymmErrors
from ROOT import gROOT
from array import array
import atlasplots as aplt

def log_labels(axis):
    axis.SetMoreLogLabels()
    axis.SetLabelSize(0.035)

# Initialize lists to store extracted values
observed_upperlimits = []
expected_upperlimits = []
expected_upperlimit_plus1sigma = []
expected_upperlimit_plus2sigma = []
expected_upperlimit_minus1sigma = []
expected_upperlimit_minus2sigma = [] 

def extract_values(mass):
    # Open the ROOT file
    file = ROOT.TFile.Open("ALP"+mass+"/Limits/asymptotics/myLimit_CL95.root")

    # Get the TTree from the file
    tree = file.Get("stats")

    h= ROOT.TH1F("h", "h", 100, 0, 100)
    h1= ROOT.TH1F("h1", "h1", 100, 0, 100)
    h2= ROOT.TH1F("h2", "h2", 100, 0, 100)
    h3= ROOT.TH1F("h3", "h3", 100, 0, 100)
    h4= ROOT.TH1F("h4", "h4", 100, 0, 100)
    h5= ROOT.TH1F("h5", "h5", 100, 0, 100)
    tree.Draw("obs_upperlimit>>h")
    tree.Draw("exp_upperlimit>>h1")
    tree.Draw("exp_upperlimit_plus1>>h2")
    tree.Draw("exp_upperlimit_plus2>>h3")
    tree.Draw("exp_upperlimit_minus1>>h4")
    tree.Draw("exp_upperlimit_minus2>>h5")

    # Extract the values from the branches
    observed_upperlimit = h.GetMean()
    expected_upperlimit = h1.GetMean()
    expected_upperlimit_plus1 = h2.GetMean()
    expected_upperlimit_plus2 = h3.GetMean()
    expected_upperlimit_minus1 = h4.GetMean()
    expected_upperlimit_minus2 = h5.GetMean()

    # Store the extracted values in the lists
    observed_upperlimits.append(observed_upperlimit)
    expected_upperlimits.append(expected_upperlimit)
    expected_upperlimit_plus1sigma.append(expected_upperlimit_plus1)
    expected_upperlimit_plus2sigma.append(expected_upperlimit_plus2)
    expected_upperlimit_minus1sigma.append(expected_upperlimit_minus1)
    expected_upperlimit_minus2sigma.append(expected_upperlimit_minus2)

    
for i in (6, 7, 8 ,9, 11, 12, 13, 14, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 40, 50, 60, 70, 80, 90, 100):
    extract_values("%d" % i)

print (observed_upperlimits, expected_upperlimits, expected_upperlimit_plus1sigma, expected_upperlimit_plus2sigma, expected_upperlimit_minus1sigma, expected_upperlimit_minus2sigma)

sigma_values = []

with open(r"../Inputs/alpgeneratedcrosssection.dat") as datFile:
    for index, data in enumerate(datFile):
        if index not in [0, 1, 6, 11, 15, 16,]:  # Exclude the first, 6th, 9th, and 11th value
            value = float(data.split()[1])
            sigma_values.append(value)
            #if index not in [0, 5, 8, 10, 17]: 

print("Values from datFile:", sigma_values)

obs_sigma_CLs = []
for x in range(0, len(sigma_values)):
    obs_sigma_CLs.append(sigma_values[x] * observed_upperlimits[x])

print(obs_sigma_CLs)

exp_sigma_CLs = []
for x in range(0, len(sigma_values)):
    exp_sigma_CLs.append(sigma_values[x] * expected_upperlimits[x])

print(exp_sigma_CLs)

exp_sigma_CLs_p1 = []
for x in range(0, len(sigma_values)):
    exp_sigma_CLs_p1.append(sigma_values[x] * (expected_upperlimit_plus1sigma[x] - expected_upperlimits[x]))

print(exp_sigma_CLs_p1)

exp_sigma_CLs_p2 = []
for x in range(0, len(sigma_values)):
    exp_sigma_CLs_p2.append(sigma_values[x] * (expected_upperlimit_plus2sigma[x] - expected_upperlimits[x]))

print(exp_sigma_CLs_p2)

exp_sigma_CLs_m1 = []
for x in range(0, len(sigma_values)):
    exp_sigma_CLs_m1.append(sigma_values[x] * (expected_upperlimits[x] - expected_upperlimit_minus1sigma[x]))

print(exp_sigma_CLs_m1)

exp_sigma_CLs_m2 = []
for x in range(0, len(sigma_values)):
    exp_sigma_CLs_m2.append(sigma_values[x] * (expected_upperlimits[x] - expected_upperlimit_minus2sigma[x]))

print(exp_sigma_CLs_m2)

def CLsplots():

    gROOT.SetStyle("ATLAS")
    c1 = TCanvas( 'c1', 'Control Limits of ALPs production cross section', 200, 10, 800, 600 )

    x = [6, 7, 8 ,9, 11, 12, 13, 14, 16, 17, 18, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 40, 50, 60, 70, 80, 90, 100]

    sigma1Graph = TGraphAsymmErrors(len(x), array('d', x), array('d', exp_sigma_CLs), array('d', [0.0] * len(x)), array('d', [0.0] * len(x)), array('d', exp_sigma_CLs_m1), array('d', exp_sigma_CLs_p1))
    
    sigma2Graph = TGraphAsymmErrors(len(x), array('d', x), array('d', exp_sigma_CLs), array('d', [0.0] * len(x)), array('d', [0.0] * len(x)), array('d', exp_sigma_CLs_m2), array('d', exp_sigma_CLs_p2))

    # Create a TGraph object and fill it with x and y values
    obs_graph = TGraph(len(x), array('d', x), array('d', obs_sigma_CLs))
    exp_graph = TGraph(len(x), array('d', x), array('d', exp_sigma_CLs))

    sigma1Graph.SetLineWidth(0)
    sigma1Graph.SetFillColorAlpha(ROOT.kGreen, 1)

    sigma2Graph.SetLineWidth(0)
    sigma2Graph.SetFillColorAlpha(ROOT.kYellow, 1)

    exp_graph.SetLineStyle(ROOT.kDashed)

    sigma2Graph.Draw("3AL")
    sigma1Graph.Draw("3L same")
    obs_graph.Draw("L same")
    exp_graph.Draw("L same")

    aplt.atlas_label(0.51, 0.86, text="Internal")

    latex = ROOT.TLatex(18, 125, "#scale[0.8]{Pb+Pb #sqrt{s_{NN}} = 5.02 TeV, 2.222 nb^{-1}}")

    # Create a TLegend
    legend = ROOT.TLegend(0.5, 0.6, 0.7, 0.8)  # Adjust the coordinates as needed

    # Add entries to the legend
    legend.AddEntry(exp_graph, "Expected Limit", "l")
    legend.AddEntry(obs_graph, "Observed", "l")
    legend.AddEntry(sigma2Graph, "#pm2#sigma unc. band", "f")
    legend.AddEntry(sigma1Graph, "#pm1#sigma unc. band", "f")
    
    

    # Set the legend style
    legend.SetTextSize(0.025)
    legend.SetBorderSize(0)
    legend.SetFillColorAlpha(0, 0)

    # Draw the legend
    legend.Draw()

    sigma2Graph.SetTitle("Asymmetric Error Bands")
    sigma2Graph.GetXaxis().SetTitle("m_{a} [GeV]")  # Set the x-axis title
    sigma2Graph.GetYaxis().SetTitle("95% CLs limit on \sigma [nb]")  # Set the y-axis title

    # TCanvas.Update() draws the latex.Draw("same")frame, after which one can change it
    c1.SetLogy()
    c1.SetLogx()

    latex.Draw("same")

    sigma2Graph.GetYaxis().SetRangeUser(0.4, 400)

    log_labels(sigma2Graph.GetXaxis())
    

    # Set the font size of the axis titles
    sigma2Graph.GetXaxis().SetTitleSize(0.03)  # Adjust the value as needed
    sigma2Graph.GetYaxis().SetTitleSize(0.03)  # Adjust the value as needed

    # Set the font size of the axis label numbers
    sigma2Graph.GetXaxis().SetLabelSize(0.03)  # Adjust the value as needed
    sigma2Graph.GetYaxis().SetLabelSize(0.03)  # Adjust the value as needed

    

    c1.Update()

    c1.Print("../Outputs/CLsOnCrossSection.pdf")

CLsplots()



