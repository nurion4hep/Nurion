#include <iostream>
#include "TClonesArray.h"
#include "TFile.h"
#include "TChain.h"
#include "TCanvas.h"
#include "TH1F.h"
#include "TH2F.h"

// --Path of your delphesclasses.h
#include "/hcp/data/data02/jwkim2/WORK/Delphes/classes/DelphesClasses.h"




using namespace std;
int main(int argc, char** argv) {

    //gSystem->Load("libDelphes.so"); 
	TFile* outFile = new TFile(argv[1],"recreate");
	TChain* inChain = new TChain("Delphes");
	
	// Output histogram name: h_hatjet
	TH1F * h_jetPT   = new TH1F("h_jetPT","h_jetPT",10000,0,7000);
	TH1F * h_jetEta  = new TH1F("h_jetEta","h_jetEta",1000,-10,10);
	TH1F * h_jetBTag = new TH1F("h_jetBTag","h_jeBTag",20,0,10);
	TH1F * h_Njet    = new TH1F("h_Njet","h_Njet",1000,0,12);
	TH1F * h_Mass_fatjet  = new TH1F("h_Mass_fatjet","h_Mass_fatjet",10000,0,7000);
	TH1F * h_ScalarHT  = new TH1F("h_ScalarHT","h_ScalarHT",10000,0,7000);
	

	// INpu files
	for(int iFile = 2; iFile<argc; iFile++) {
        cout << "### InFile " << iFile-1 << " " << argv[iFile] << endl;
        inChain->Add(argv[iFile]);

	}

	// Copy Jet class from delphesclasses.h
	TClonesArray* FatJetTCA    = new TClonesArray("Jet");		inChain->SetBranchAddress("FatJet",&FatJetTCA);
	
	TClonesArray* JetTCA       = new TClonesArray("Jet");		inChain->SetBranchAddress("Jet",&JetTCA);

	TClonesArray* HtTCA		   = new TClonesArray("ScalarHT");	inChain->SetBranchAddress("ScalarHT",&HtTCA);
	


	int total_event = inChain->GetEntries();
	int per99		= total_event/99;
	int per100		=0;

	cout << "tot: " << total_event << endl;

	// --Evt Loop	
	for(int eventLoop=0; eventLoop < total_event; eventLoop++){
		inChain->GetEntry(eventLoop); // load data in tree
		if((eventLoop%per99) ==0) cout << "Run" << per100++ << " %" << endl; // Showing progress 
	


		int Njet=0;
		// --Jet Loop
        //cout << JetTCA->GetEntries() << endl;
		for(int jetLoop=0; jetLoop < JetTCA->GetEntries(); jetLoop++){
			Jet* jetPtr = (Jet*)JetTCA->At(jetLoop);
			
			if(abs(jetPtr->Eta) > 2.4 ) continue;
					
			h_jetPT ->Fill(jetPtr->PT);  
			h_jetEta->Fill(jetPtr->Eta);
			h_jetBTag->Fill(jetPtr->BTag);
			Njet +=1;	 // N jet coutn 
		}
		h_Njet->Fill(Njet);
		
		// --FatJet Loop
        //cout << FatJetTCA->GetEntries() << endl;
		for(int fatjetLoop=0; fatjetLoop < FatJetTCA->GetEntries(); fatjetLoop++){
			Jet* fatjetPtr = (Jet*)FatJetTCA->At(fatjetLoop);			
			h_Mass_fatjet->Fill(fatjetPtr->Mass);
		}

		// --HT Loop
		for(int HTLoop=0; HTLoop < HtTCA->GetEntries(); HTLoop++){
			ScalarHT* HTPtr = (ScalarHT*)HtTCA->At(HTLoop);			
			h_ScalarHT->Fill(HTPtr->HT);
		}
	}

	outFile->Write();
}
