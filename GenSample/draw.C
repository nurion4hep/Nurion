#include "TMath.h"

void draw() {

double XMIN = -1;
double XMAX = -1;
long YMAX   = 100;

// --Lumi and xsec
	const double Lumi         = 36000.0;
	const double xsecSignal   = 0.0130;
	const double xsecBKG2000   = 20.24;

	int gensig = 5990;
	int genBKG2000 = 40049;

	int rebin =1;


// --read file,hist
	TFile *fSignal		   = TFile::Open("sig.root")     ;
	TFile *fBKG2000	       = TFile::Open("bkg.root")         ;
	

// --hist name, X range Y range
	TString histname = "h_Mass_fatjet"; XMAX=3000; XMIN=0; rebin=100; YMAX=10000000;
	//TString histname = "h_Njet"; XMAX=12; XMIN=0; rebin=12; YMAX=1000000;
	//TString histname = "h_jetEta"; XMAX=5; XMIN=-5; rebin=10; YMAX=1000000;
	//TString histname = "h_jetPT"; XMAX=7000; XMIN=0; rebin=100; YMAX=10000000;
	//TString histname = "h_jetBTag"; XMAX=2.5; XMIN=0; rebin=1; YMAX=100000000;
	
// --Normalize 	
	TH1F *hSignal	  = (TH1F*)fSignal	  ->Get(histname); hSignal    ->Scale(xsecSignal/gensig*Lumi) ;
	TH1F *hBKG2000	  = (TH1F*)fBKG2000	  ->Get(histname); hBKG2000	  ->Scale(xsecBKG2000/genBKG2000*Lumi) ;

// --Combine BKGs
	TH1F *hBKG = new TH1F(*hBKG2000);
	hBKG->Add(hBKG2000);

	cout << hSignal->Integral() << "##" << endl;
	cout << hBKG->Integral() << "##" << endl;



// --histrogram design	
	
	hSignal->SetLineWidth(3); hSignal->SetLineColor(2);
	hBKG->SetFillColor(38); 
	


// --rebinning
	hSignal->Rebin(rebin);
	hBKG->Rebin(rebin);

// --Pad Design
   gStyle->SetOptStat(0);
   gStyle->SetCanvasColor(0);
   gStyle->SetCanvasBorderMode(0);
   gStyle->SetPadBorderMode(0);
   gStyle->SetPadColor(0);
   gStyle->SetFrameBorderMode(0);


	double binwidth= hBKG->GetBinWidth(1);



	TCanvas* c1 = new TCanvas("c1", "c1", 500, 500);
		TPad *pad1 = new TPad("pad1", "pad1", 0.0, 0.0001, 1.0, 1.0);
		//   pad1->SetBottomMargin(0.01);
		pad1->SetGrid();
		   pad1->SetLogy();
		pad1->Draw();
		pad1->cd();
		TH2F *null1 = new TH2F("null1","", 2, XMIN, XMAX, 2, 0.09,YMAX);
		null1->GetYaxis()->SetTitle(Form("Number of events / %3.1f GeV",binwidth));
		null1->GetXaxis()->SetTitle(histname);
		null1->GetYaxis()->SetTitleOffset(1.8);
		null1->GetXaxis()->SetTitleOffset(1.2);
		null1->GetYaxis()->SetTitleSize(0.03);
		null1->GetYaxis()->SetLabelSize(0.03);
		null1->Draw();
		 
	// ----------Drwa here with same option
		 hBKG->Draw("hist same");
		 hSignal->Draw("hist same");

// --legend	
	TLegend *l0 = new TLegend(0.65,0.89,0.90,0.65);
		l0->SetFillStyle(0);
		l0->SetBorderSize(0);
		l0->SetTextSize(0.03);

	  TLegendEntry* l01 = l0->AddEntry(hSignal,"Signal"   ,"l"  );    l01->SetTextColor(hSignal->GetLineColor());  
	  TLegendEntry* l02 = l0->AddEntry(hBKG,"Background"     ,"f"  ); l02->SetTextColor(hBKG->GetLineColor());
	  
	  //TLegendEntry* l01 = l0->AddEntry(hSignal,"Signal"   ,"l"  );    l01->SetTextColor(sigfit->GetLineColor());  
	  //TLegendEntry* l02 = l0->AddEntry(hBKG,"Background"     ,"l"  ); l02->SetTextColor(bkgfit->GetLineColor());
	  
	 // TLegendEntry* l03 = l0->AddEntry(glbfit,"GlobalFit"     ,"l"  ); l03->SetTextColor(glbfit->GetLineColor());
	
		l0->Draw();

		pad1->cd();
			TLatex latex;
			latex.SetNDC();
			latex.SetTextSize(0.04);
			latex.SetTextAlign(11);
			latex.DrawLatex(0.6,0.91,Form("%.1f fb^{-1} (13 TeV)", Lumi/1000.0));


	TString outname = histname +".png";
	c1->Print(outname);



}
