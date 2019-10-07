#include <iostream>
#include "TClonesArray.h"
#include "TFile.h"
#include "TChain.h"
#include "TCanvas.h"
#include "TH1F.h"
#include "TH2F.h"
#include "classes/DelphesClasses.h"




using namespace std;
int main(int argc, char** argv) {

    //gSystem->Load("libDelphes.so"); 
	TFile* outFile = new TFile(argv[1],"recreate");
	TChain* inChain = new TChain("Delphes");
	
	// Output histogram name: h_hatjet
	TH1F * h_fatjet = new TH1F("h_fatjet","h_fatjet",10000,0,2000);


	// Input files
	for(int iFile = 2; iFile<argc; iFile++) {
        cout << "### InFile " << iFile-1 << " " << argv[iFile] << endl;
        inChain->Add(argv[iFile]);
	}

	// Copy Jet class from delphesclasses.h
	TClonesArray* FatJetTCA = new TClonesArray("Jet");inChain->SetBranchAddress("FatJet",&FatJetTCA);
	TClonesArray* FatJetSelTCA = new TClonesArray("Jet");
	

	int total_event = inChain->GetEntries();
	int per99		= total_event/99;
	int per100		=0;

	cout << "tot: " << total_event << endl;

	
	int Gen_evt= total_event;
	int PreSel_evt=0;



	// --Evt Loop	
	for(int eventLoop=0; eventLoop < total_event; eventLoop++){
		inChain->GetEntry(eventLoop); // load data in tree
		if((eventLoop%per99) ==0) cout << "Run" << per100++ << " %" << endl; // Showing progress 
		
		

		// --Object Selection
		for(int fatjetLoop=0; fatjetLoop<FatJetTCA->GetEntries(); fatjetLoop++){
			Jet *fatjetptr = (Jet*)FatJetTCA->At(fatjetLoop);
	
			if(fabs(fatjetptr->Eta) > 2.) continue;
			if(fabs(fatjetptr->PT) < 200.) continue;

			new((*FatJetSelTCA)[(int)FatJetSelTCA->GetEntries()]) Jet(*fatjetptr);
		}


		// --Baseline Selection		
		if(FatJetSelTCA->GetEntries() < 3) continue;
		Jet * fatjetptr1 = (Jet*)FatJetSelTCA->At(0);
		if(fatjetptr1->PT < 440) continue;
		PreSel_evt++;
	} //--Evt Loop Ended

	cout << "Gen Evt: "<< Gen_evt << endl;
	cout << "PreSel Evt: "<< PreSel_evt << endl;

	//outFile->Write();


}
