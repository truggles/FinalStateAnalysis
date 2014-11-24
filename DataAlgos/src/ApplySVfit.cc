///////////
// imp of function getSVfitMass
// based on standalone SVfit instructions
// https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012#SVFit_Christian_Lorenzo_Aram_Rog
//
// S.Z. Shalhout (sshalhou@CERN.CH) Nov 20, 2012
/////////


#include "DataFormats/Provenance/interface/EventID.h"
#include "FinalStateAnalysis/DataAlgos/interface/ApplySVfit.h"
#include "TauAnalysis/CandidateTools/interface/NSVfitStandaloneAlgorithm.h"
#include "TLorentzVector.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/Math/interface/Vector3D.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "FinalStateAnalysis/DataAlgos/interface/Hash.h"
#include <iostream>
#include <iomanip>
#include <map>
#include <stdio.h>
#include <string>
#include <math.h>


namespace ApplySVfit {

  using NSVfitStandalone::Vector;
  using NSVfitStandalone::LorentzVector;
  using NSVfitStandalone::MeasuredTauLepton;

  // Caching and translation layer
  typedef std::map<size_t, std::vector<double> > SVFitCache;
  static SVFitCache theCache;
  static edm::EventID lastSVfitEvent; // last processed event

  std::vector<double> getSVfitMass(std::vector<reco::CandidatePtr>& cands,
      const pat::MET& met, const TMatrixD& covMET, unsigned int verbosity,
      const edm::EventID& evtId, int adjust) {

    std::vector<double> four_vec;

    // Check if this a new event
    if (evtId != lastSVfitEvent) {
      theCache.clear();
    }
    lastSVfitEvent = evtId;

    // Hash our candidates - NB cands will be sorted in place
    // Hack to create a unique hash for TES +/- and no adjust
    size_t hash = (hashCandsByContent(cands) + adjust);
    //std::cout << "EvtID: " << evtId << " Hash: " << hash << " adjust: " << adjust << std::endl; 

    // Check if we've already computed it
    SVFitCache::const_iterator lookup = theCache.find(hash);
    if (lookup != theCache.end()) {
      return lookup->second;
    }

    // No pain no gain
    Vector measuredMET = met.momentum();
    double measuredMETphi = met.phi();
    
    // vector to store our adjusted Pt values and later adjust MET
    std::vector<std::pair<double,double>> deltaPxPy;
    std::vector<MeasuredTauLepton> measuredTauLeptons;

    for (size_t dau = 0; dau < cands.size(); ++dau) {
      int pdgId = std::abs(cands[dau]->pdgId());
      if (pdgId == 11 || pdgId == 13)
        measuredTauLeptons.push_back(
            MeasuredTauLepton(NSVfitStandalone::kLepDecay,cands[dau]->p4()));
      else if (pdgId == 15) {
        LorentzVector tAdj = cands[dau]->p4();
        if (adjust == 1) {
          double dPx;
          double dPy;
          dPx = (cos( tAdj.Phi() ))*( tAdj.Pt()*0.03 );
          dPy = (sin( tAdj.Phi() ))*( tAdj.Pt()*0.03 );
          //std::cout << "measuredMET_i" << measuredMET<< std::endl;
          //std::cout << "measuredMETphi_i " << measuredMETphi << std::endl;
          //std::cout<<"Px = "<<tAdj.Px()<<" dPx = "<<dPx<<" Phi = "<<tAdj.Phi() << std::endl;
          //std::cout<<"Py = "<<tAdj.Py()<<" dPy = "<<dPy<<" Phi = "<<tAdj.Phi() << std::endl;
          deltaPxPy.push_back(std::make_pair(dPx, dPy));
          
          TLorentzVector TtauAdjust;
          TtauAdjust.SetPtEtaPhiE( tAdj.Pt()*1.03, tAdj.Eta(), tAdj.Phi(), tAdj.E()*1.03 );
          tAdj.SetPxPyPzE( TtauAdjust.Px(), TtauAdjust.Py(), TtauAdjust.Pz(), TtauAdjust.E() );
        }
        else if (adjust == -1) {
          double dPx;
          double dPy;
          dPx = (cos( tAdj.Phi() ))*( tAdj.Pt()*(-0.03) );
          dPy = (sin( tAdj.Phi() ))*( tAdj.Pt()*(-0.03) );
          //std::cout << "measuredMET_i" << measuredMET<< std::endl;
          //std::cout << "measuredMETphi_i " << measuredMETphi << std::endl;
          //std::cout<<"Px = "<<tAdj.Px()<<" dPx = "<<dPx<<" Phi = "<<tAdj.Phi() << std::endl;
          //std::cout<<"Py = "<<tAdj.Py()<<" dPy = "<<dPy<<" Phi = "<<tAdj.Phi() << std::endl;
          deltaPxPy.push_back(std::make_pair(dPx, dPy));

          TLorentzVector TtauAdjust;
          TtauAdjust.SetPtEtaPhiE( tAdj.Pt()*0.97, tAdj.Eta(), tAdj.Phi(), tAdj.E()*0.97 );
          tAdj.SetPxPyPzE( TtauAdjust.Px(), TtauAdjust.Py(), TtauAdjust.Pz(), TtauAdjust.E() );
        }
        //std::cout << "Given Adjustment = " << adjust << std::endl;
        measuredTauLeptons.push_back(
            MeasuredTauLepton(NSVfitStandalone::kHadDecay,tAdj ));
        }      
      else
        throw cms::Exception("BadPdgId") << "I don't understand PDG id: "
          << pdgId << ", sorry." << std::endl;
    }

    // Adjusted MET vector
    Vector adjMET= met.momentum();
    for (auto& element : deltaPxPy) {
      //std::cout << "dPxPhi Loop: " << element.first << " : " << element.second << std::endl;
      double adjMETx = 0;
      double adjMETy = 0;
      adjMETx = adjMET.x() - element.first;
      //std::cout << "dMETx = MET.x() - element.first " << adjMETx << std::endl;
      adjMETy = adjMET.y() - element.second;
      //std::cout << "dMETy = MET.y() - element.second " << adjMETy << std::endl;
      adjMET.SetXYZ(adjMETx, adjMETy, 0);
      //std::cout << adjMET<< std::endl;
    }
    //std::cout << "Final adjMET" << adjMET<< std::endl;
    //std::cout << "Final measuredMET" << measuredMET<< std::endl;


    NSVfitStandaloneAlgorithm algo(measuredTauLeptons,
        adjMET, covMET, verbosity);
    algo.addLogM(false);
    algo.integrateMarkovChain();

    four_vec.push_back( algo.pt() );
    four_vec.push_back( algo.eta() );
    four_vec.push_back( algo.phi() );

    double mass = algo.mass(); // mass uncertainty not implemented yet
    four_vec.push_back( mass );
    theCache[hash] = four_vec;
    //theCache.insert(hash, std::vector<double>());
    //theCache[hash] = four_vec;
    //theCache[hash] = mass;
    //return mass;
    return four_vec;
  }

} // namespace ApplySVfit
