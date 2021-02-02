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
	//TH1F * h_jetPT   = new TH1F("h_jetPT","h_jetPT",10000,0,7000);
	//TH1F * h_jetEta  = new TH1F("h_jetEta","h_jetEta",1000,-10,10);
	TH1F * h_jetBTag		= new TH1F("h_jetBTag","Number of b-tagged jets",20,0,10);
	TH1F * h_Njet			= new TH1F("h_Njet","Number of jets",1000,0,20);
	TH1F * h_Mass_fatjet	= new TH1F("h_Mass_fatjet","Sum of Jet mass",10000,0,7000);
	TH1F * h_ScalarHT		= new TH1F("h_ScalarHT","HT",10000,0,10000);
	
	TH1F * h_srjetBTag		= new TH1F("h_srjetBTag","Number of b-tagged jets",20,0,10);
	TH1F * h_srNjet			= new TH1F("h_srNjet","Number of jets",1000,0,20);
	TH1F * h_srMass_fatjet  = new TH1F("h_srMass_fatjet","Sum of Jet mass",10000,0,7000);
	TH1F * h_srScalarHT		= new TH1F("h_srScalarHT","HT",10000,0,10000);
	

	// INpu files
	for(int iFile = 2; iFile<argc; iFile++) {
        cout << "### InFile " << iFile-1 << " " << argv[iFile] << endl;
        inChain->Add(argv[iFile]);
	}

	// Copy Jet class from delphesclasses.h
	TClonesArray* FatJetTCA    = new TClonesArray("Jet");		inChain->SetBranchAddress("FatJet",&FatJetTCA);
	TClonesArray *FatJetSelTCA =  new TClonesArray("Jet");
	
	TClonesArray* JetTCA       = new TClonesArray("Jet");		inChain->SetBranchAddress("Jet",&JetTCA);
	TClonesArray *JetSelTCA =  new TClonesArray("Jet");

	TClonesArray* HtTCA		   = new TClonesArray("ScalarHT");	inChain->SetBranchAddress("ScalarHT",&HtTCA);


	int total_event = inChain->GetEntries();
	int per99		= total_event/99;
	int per100		=0;
	int Signal_region = 0;
	int Baseline_region = 0;

	cout << "tot: " << total_event << endl;

	// --Evt Loop	
	cout <<" Start Event Loop " << endl;
	for(int eventLoop=0; eventLoop < total_event; eventLoop++){
		inChain->GetEntry(eventLoop); // load data in tree
		if((eventLoop%per99) ==0) cout << "Run" << per100++ << " %" << endl; // Showing progress 
	

		JetSelTCA->Clear("C");


		int Njet=0;
		int NBtag=0;


		//cout << " Jet Loop " << endl;
		// --Jet Loop
        //cout << JetTCA->GetEntries() << endl;
		for(int jetLoop=0; jetLoop < JetTCA->GetEntries(); jetLoop++){
			Jet* jetPtr = (Jet*)JetTCA->At(jetLoop);
			
			if(abs(jetPtr->Eta) > 2.4 ) continue;
			if( jetPtr->PT <= 30 ) continue;
			
			
		
			//h_jetPT ->Fill(jetPtr->PT);  
			//h_jetEta->Fill(jetPtr->Eta);
			//h_jetBTag->Fill(jetPtr->BTag);
			Njet +=1;	 // N jet coutn 
			
			if(jetPtr->BTag == 1){
				NBtag+=1;

			}

			new((*JetSelTCA)[(int)JetSelTCA->GetEntries()]) Jet(*jetPtr);

		}
		//h_Njet->Fill(Njet);
		
		//cout << " FatJet Loop " << endl;
		// --FatJet Loop
	
		double sumFatJet=0;
		for(int fatjetLoop=0; fatjetLoop < FatJetTCA->GetEntries(); fatjetLoop++){
			Jet* fatjetPtr = (Jet*)FatJetTCA->At(fatjetLoop);
			
			if(fatjetPtr->PT <= 30 ) continue;
			//h_Mass_fatjet->Fill(fatjetPtr->Mass);
			sumFatJet += fatjetPtr->Mass ; 			

			new((*FatJetSelTCA)[(int)FatJetSelTCA->GetEntries()]) Jet(*fatjetPtr);
		}

		// --HT Loop
	//	for(int HTLoop=0; HTLoop < HtTCA->GetEntries(); HTLoop++){
	//		ScalarHT* HTPtr = (ScalarHT*)HtTCA->At(HTLoop);			
	//		//h_ScalarHT->Fill(HTPtr->HT);

	//	}

		//cout << " Baseline selection " << endl;
			// ---- Baseline selectioa
			

		// -- Basline Selection
			if(JetSelTCA->GetEntries() < 4) continue;
		
	
			ScalarHT* HTPtr = (ScalarHT*)HtTCA->At(0);
		
			if(sumFatJet < 500	) continue;
			if(HTPtr->HT < 1500) continue; 
			if(NBtag < 1) continue;
		
			h_jetBTag->Fill(NBtag);
			h_Njet->Fill(Njet);
			h_Mass_fatjet->Fill(sumFatJet);
			h_ScalarHT->Fill(HTPtr->HT);
		
			Baseline_region+=1;

		// -- Signal region
			
			if(JetSelTCA->GetEntries() < 8) continue;
			if(sumFatJet <= 800	) continue;
			if(NBtag < 3) continue;
			
	
			h_srjetBTag		->Fill(NBtag)		;
            h_srNjet		->Fill(Njet)		;
            h_srMass_fatjet ->Fill(sumFatJet)	;
            h_srScalarHT	->Fill(HTPtr->HT)	;
	
		    Signal_region+=1 ;

	}//-Evt Loop

	cout << "Baseline region: " << Baseline_region << endl;
	cout << "Total Signal region: " << Signal_region << endl;

	outFile->Write();
}
