import ROOT
from ROOT import TCanvas, TGraph, TGraphAsymmErrors
from ROOT import gROOT
from array import array
import atlasplots as aplt
import yaml

def load_values(yaml_file_path, value_key, x_key, multiplier=1):
    values = []
    x_values = []

    with open(yaml_file_path, "r") as yaml_file:
        data = yaml.safe_load(yaml_file)

        for item in data:
            if value_key in item and x_key in item:
                values.append(multiplier * item[value_key])
                x_values.append(item[x_key])

    return x_values, values

def create_sigma_graphs():
    sigma_graphs = []
    for i in range(1, 14):
        sigma = i * i
        sigma_graph = TGraph(2, array('d', [0, 3]), array('d', [sigma, sigma]))
        sigma_graph.SetLineWidth(2)
        sigma_graph.SetLineStyle(ROOT.kDashed)
        sigma_graph.SetLineColor(ROOT.kAzure + 7)
        sigma_graphs.append(sigma_graph)
    return sigma_graphs

def TestTextPlacement():
    sigma_texts = []
    sigma_graphs = create_sigma_graphs()
    for sigma_graph in sigma_graphs:
        sigma_text = ROOT.TLatex(3.02, sigma_graph.GetY()[0], f"{sigma_graphs.index(sigma_graph)+1}#sigma")
        sigma_text.SetTextSize(0.03)
        sigma_text.SetNDC(False)
        sigma_text.SetTextAlign(12)
        sigma_text.SetTextColor(ROOT.kAzure + 7)
        sigma_text.Draw("same")
        sigma_texts.append(sigma_text)

        print(f"Sigma {sigma_graphs.index(sigma_graph)+1} text coordinates: X={sigma_text.GetX()}, Y={sigma_text.GetY()}")
    return sigma_texts

        



def Plots():
    gROOT.SetStyle("ATLAS")
    c1 = TCanvas('c1', 'Scan of profile likelihood', 200, 10, 400, 400)

    observed_x_values, observed_values = load_values("LbyL/LHoodPlots/NLLscan_mu.yaml", "minusdeltaNLL", "X", 2)
    expected_x_values, expected_values = load_values("LbyLexp/LHoodPlots/NLLscan_mu.yaml", "minusdeltaNLL", "X", 2)

    exp_Graph = TGraph(len(expected_x_values), array('d', expected_x_values), array('d', expected_values))
    obs_Graph = TGraph(len(observed_x_values), array('d', observed_x_values), array('d', observed_values))
  
    exp_Graph.SetLineStyle(ROOT.kDashed)
    exp_Graph.SetLineColor(ROOT.kRed)
    obs_Graph.SetLineWidth(2)
    exp_Graph.SetLineWidth(2)

    obs_Graph.Draw("AC")
    exp_Graph.Draw("C same")

    aplt.atlas_label(0.4, 0.89, text="Internal")

    legend = ROOT.TLegend(0.5, 0.62, 0.7, 0.72)
    legend.SetTextSize(0.025)
    legend.SetBorderSize(0)
    legend.SetFillColorAlpha(0, 0)
    legend.AddEntry(exp_Graph, "Expected", "l")
    legend.AddEntry(obs_Graph, "Observed", "l")
    legend.Draw()

    latex1 = ROOT.TLatex(0.4, 0.85, "Pb+Pb #sqrt{s_{NN}} = 5.02 TeV, 2.222 nb^{-1}")
    latex1.SetTextSize(0.04)
    latex1.SetNDC()
    latex1.Draw("same")

    sigma_graphs = create_sigma_graphs()
    for sigma_graph in sigma_graphs:
        sigma_graph.Draw("C same")

    
    
    sigma_texts = TestTextPlacement()
    for sigma_text in sigma_texts:
        sigma_text.Draw("same")


    obs_Graph.GetXaxis().SetTitle("\mu_{\gamma\gamma \\rightarrow \gamma\gamma}")  # Set the x-axis title
    obs_Graph.GetYaxis().SetTitle("-2\Delta ln L")  # Set the y-axis title

    obs_Graph.GetXaxis().SetRangeUser(0, 3)
    
    # Set the font size of the axis titles
    obs_Graph.GetXaxis().SetTitleSize(0.03)  # Adjust the value as needed
    obs_Graph.GetYaxis().SetTitleSize(0.03)  # Adjust the value as needed

    # Set the font size of the axis label numbers
    obs_Graph.GetXaxis().SetLabelSize(0.03)  # Adjust the value as needed
    obs_Graph.GetYaxis().SetLabelSize(0.03)  # Adjust the value as needed

    c1.Update()
    c1.Print("../Outputs/LHscanplot.pdf")

Plots()
