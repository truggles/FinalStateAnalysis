#include "FinalStateAnalysis/DataAlgos/interface/CollectionFilter.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

// Function cache
namespace {

typedef StringCutObjectSelector<reco::Candidate, true> CandFunc;
typedef std::map<std::string, CandFunc> CandFuncCache;
static CandFuncCache functions_;

const CandFunc& getFunction(const std::string& function) {
  CandFuncCache::iterator findFunc = functions_.find(function);
  // Build it if we haven't made it
  if (findFunc == functions_.end()) {
    functions_.insert(std::make_pair(function, CandFunc(function)));
    findFunc = functions_.find(function);
  }
  return findFunc->second;
}

}

// Get objects at least [minDeltaR] away from hardScatter objects
std::vector<const reco::Candidate*> getVetoObjects(
    const std::vector<const reco::Candidate*>& hardScatter,
    const std::vector<const reco::Candidate*>& vetoCollection,
    double minDeltaR,
    const std::string& filter) {
  std::vector<const reco::Candidate*> output;

  const CandFunc& filterFunc = getFunction(filter);

  for (size_t i = 0; i < vetoCollection.size(); ++i) {
    const reco::Candidate* ptr = vetoCollection[i];
    bool awayFromEverything = true;
    for (size_t j = 0; j < hardScatter.size(); ++j) {
      double deltaR = reco::deltaR(ptr->p4(), hardScatter[j]->p4());
     // std::cout << "Delta R = " << deltaR << std::endl; // was used for debugging
      
      if (deltaR < minDeltaR) {
        awayFromEverything = false;
        break;
      }
    }
    if (awayFromEverything && (filterFunc)(*ptr)) {
      output.push_back(ptr);
    }
  }

  /*// also consider the final state leptons. This makes it
  // not really a "veto" anymore, since some of the final
  // state objects will probably pass the filter
  for (size_t k = 0; k < hardScatter.size(); ++k) {
    const reco::Candidate* ptr = hardScatter[k];
    if ((filterFunc)(*ptr)) {
      output.push_back(ptr);
    }
  }
  */

  return output;
}

// Get objects within [minDeltaR] from [object] passing [filter]
std::vector<const reco::Candidate*> getOverlapObjects(
    const reco::Candidate& candidate,
    const std::vector<const reco::Candidate*>& overlapCollection,
    double minDeltaR,
    const std::string& filter) {
  std::vector<const reco::Candidate*> output;

  const CandFunc& filterFunc = getFunction(filter);

  for (size_t i = 0; i < overlapCollection.size(); ++i) {
    const reco::Candidate* ptr = overlapCollection[i];
    double deltaR = reco::deltaR(ptr->p4(), candidate.p4());
    if (deltaR < minDeltaR) {
      if ((filterFunc)(*ptr)) {
        output.push_back(ptr);
      }
    }
  }
  return output;
}

// Count the number of events in a specified collection that
// pass the given filter
std::vector<const reco::Candidate*> getCollectionCount(
    const std::vector<const reco::Candidate*>& hardScatter,
    const std::vector<const reco::Candidate*>& vetoCollection,
    double minDeltaR,
    const std::string& filter) {

  std::vector<const reco::Candidate*> output;
  const CandFunc& filterFunc = getFunction(filter);

  for (size_t i = 0; i < vetoCollection.size(); ++i) {
    const reco::Candidate* ptr = vetoCollection[i];
    bool awayFromEverything = true;
    for (size_t j = 0; j < hardScatter.size(); ++j) {
      double deltaR = reco::deltaR(ptr->p4(), hardScatter[j]->p4());
     // std::cout << "Delta R = " << deltaR << std::endl; // was used for debugging
      //if (deltaR == 0 && (filterFunc)(*ptr)) {std::cout<<"booyakesha"<<std::endl;}
      if (deltaR < minDeltaR && deltaR != 0) {
        // consider the final state objects themselves (deltaR == 0)
        awayFromEverything = false;
        break;
      }   
    }   
    if (awayFromEverything && (filterFunc)(*ptr)) {
      output.push_back(ptr);
    }   
  }

  /*// also consider the final state leptons. This is really
  // the only difference between this method and 'getVetoObjects'
  for (size_t k = 0; k < hardScatter.size(); ++k) {
    const reco::Candidate* ptr = hardScatter[k];
    if ((filterFunc)(*ptr)) {
      output.push_back(ptr);
    }
  }*/
  

  return output;
 
}

