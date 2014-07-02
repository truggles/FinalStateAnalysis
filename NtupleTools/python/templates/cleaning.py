'''

Ntuple branch template sets for applying cleaning and extra object vetoes

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Muon
i.e. daughter(1) or somesuch.

Author: Evan K. Friis

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

# Vetos on extra stuff in the event
vetos = PSet(
    #MUON VETOS
    muVetoPt5 = 'vetoMuons(0.4, "pt > 5 & abs(eta) < 2.4").size()',
    muGlbIsoVetoPt10 = 'vetoMuons(0.4, "isGlobalMuon & isTrackerMuon & pt > 10 & abs(eta) < 2.4 & (userIso(0) + max(photonIso + neutralHadronIso - 0.5*puChargedHadronIso, 0))/pt < 0.4").size()',
    muVetoZH = 'vetoMuons(0.4, "isGlobalMuon & isTrackerMuon & pfCandidateRef.isNonnull & pt > 10 & abs(eta) < 2.4 & (userIso(0) + max(photonIso + neutralHadronIso - 0.5*puChargedHadronIso, 0))/pt < 0.3").size()',
    muVetoPt5IsoIdVtx = 'vetoMuons(0.4, "pt > 5 & abs(eta) < 2.4 & userInt(\'tightID\') > 0.5 & ((userIso(0) + max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()) < 0.15 & userFloat(\'dz\') < 0.2").size()',
    muVetoPt15IsoIdVtx = 'vetoMuons(0.4, "pt > 15 & abs(eta) < 2.4 & userInt(\'tightID\') > 0.5 & ((userIso(0) + max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()) < 0.15 & userFloat(\'dz\') < 0.2").size()',
    muTightCountZH = 'countMuons(0.1, "isGlobalMuon & isTrackerMuon & pfCandidateRef.isNonnull & pt > 10 & abs(eta) < 2.4 & (userIso(0) + max(photonIso + neutralHadronIso - 0.5*puChargedHadronIso, 0))/pt < 0.3").size()',
    
    #TAU VETOS
    tauVetoPt20 = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byLooseIsolationMVA\')").size()',
    tauHpsVetoPt20 = 'vetoTaus(0.3, "pt > 20 & abs(eta) < 2.3 & tauID(\'decayModeFinding\') & tauID(\'againstElectronLoose\') & tauID(\'againstMuonLoose\') & tauID(\'byMediumCombinedIsolationDeltaBetaCorr\')").size()',
    tauVetoZH = 'vetoTaus(0.1, "pt > 15 & abs(eta) < 2.3 & tauID(\'decayModeFinding\') & userFloat(\'dz\') < 0.1").size()',
    tauVetoPt20LooseMVAVtx  = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byLooseIsolationMVA\') & userFloat(\'dz\') < 0.2").size()',
    tauVetoPt20LooseMVA2Vtx = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byLooseIsolationMVA2\') & userFloat(\'dz\') < 0.2").size()',
    tauVetoPt20Loose3HitsVtx = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byLooseCombinedIsolationDeltaBetaCorr3Hits\') & userFloat(\'dz\') < 0.2").size()',
    tauVetoPt20VLooseHPSVtx = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byVLooseCombinedIsolationDeltaBetaCorr\') & userFloat(\'dz\') < 0.2").size()',
    tauTightCountZH = 'countTaus(0.1, "pt > 15 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byLooseCombinedIsolationDeltaBetaCorr3Hits\') & userFloat(\'dz\') < 0.1").size()',
    
    #ELECTRON VETOS
    eVetoMVAIsoVtx = 'vetoElectrons(0.4, "pt > 10 & abs(eta) < 2.5 & userInt(\'mvaidwp\') > 0.5 & ((userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt) < 0.3 & userFloat(\'dz\') < 0.2").size()',
    eVetoMVAIso = 'vetoElectrons(0.4, "pt > 10 & abs(eta) < 2.5 & userInt(\'mvaidwp\') > 0.5 & (userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt < 0.3").size()',
    eVetoZH = 'vetoElectrons(0.1, "pt > 10 & abs(eta) < 2.5 & (userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt < 0.3 & ( ( abs(eta) < 0.8 & electronID(\'mvaNonTrigV0\') > 0.5 ) || ( abs(eta) > 0.8 & abs(eta) < 1.479 & electronID(\'mvaNonTrigV0\') > 0.12 ) || ( abs(eta) > 1.479 & electronID(\'mvaNonTrigV0\') > 0.6 ))").size()',
    eVetoZH_smallDR = 'vetoElectrons(0.0001, "pt > 10 & abs(eta) < 2.5 & (userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt < 0.3 & ( ( abs(eta) < 0.8 & electronID(\'mvaNonTrigV0\') > 0.5 ) || ( abs(eta) > 0.8 & abs(eta) < 1.479 & electronID(\'mvaNonTrigV0\') > 0.12 ) || ( abs(eta) > 1.479 & electronID(\'mvaNonTrigV0\') > 0.6 ))").size()',
    eVetoCicTightIso = 'vetoElectrons(0.4, "pt > 10 & abs(eta) < 2.5 &  test_bit(electronID(\'cicTight\'), 0) > 0.5 & (userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt < 0.3").size()',
    eTightCountZH = 'countElectrons(0.1, "pt > 10 & abs(eta) < 2.5 & (userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt < 0.3 & ( ( abs(eta) < 0.8 & electronID(\'mvaNonTrigV0\') > 0.5 ) || ( abs(eta) > 0.8 & abs(eta) < 1.479 & electronID(\'mvaNonTrigV0\') > 0.12 ) || ( abs(eta) > 1.479 & electronID(\'mvaNonTrigV0\') > 0.6 ))").size()',    

    #B-JET Vetos
    bjetVeto = 'vetoJets(0.4, "pt > 20 & abs(eta) < 2.4  & userInt(\'fullIdLoose\') & bDiscriminator(\'\') > 3.3").size()',
    bjetCSVVeto = 'vetoJets(0.4, "pt > 20 & abs(eta) < 2.4 & userInt(\'fullIdLoose\') & bDiscriminator(\'combinedSecondaryVertexBJetTags\') > 0.679").size()',
    bjetCSVVetoZHLike = 'vetoJets(0.4, "pt > 20 & abs(eta) < 2.4 & userInt(\'fullIdLoose\') & bDiscriminator(\'combinedSecondaryVertexBJetTags\') > 0.898").size()',
    bjetCSVVetoZHLikeNoJetId = 'vetoJets(0.4, "pt > 20 & abs(eta) < 2.4 & bDiscriminator(\'combinedSecondaryVertexBJetTags\') > 0.898").size()',
    bjetCSVVetoZHLikeNoJetId_2 = 'vetoJets(0.4, "pt > 20 & abs(eta) < 2.4 & bDiscriminator(\'combinedSecondaryVertexBJetTags\') > 0.679").size()',
    bjetCSVVeto30 = 'vetoJets(0.4, "pt > 30 & abs(eta) < 2.4 & userInt(\'fullIdLoose\') & bDiscriminator(\'combinedSecondaryVertexBJetTags\') > 0.679").size()',
    bjetTightCountZH = 'countJets(0.4, "pt > 20 & abs(eta) < 2.4 & bDiscriminator(\'combinedSecondaryVertexBJetTags\') > 0.679").size()',

    #JET VETOS
    jetVeto20 = 'vetoJets(0.4, "pt > 20 & abs(eta) < 5.0 & userInt(\'fullIdLoose\')").size()',
    jetVeto20_DR05 = 'vetoJets(0.5, "pt > 20 & abs(eta) < 5.0 & userInt(\'fullIdLoose\')").size()',
    jetVeto30 = 'vetoJets(0.4, "pt > 30 & abs(eta) < 5.0 & userInt(\'fullIdLoose\')").size()',
    jetVeto30_DR05 = 'vetoJets(0.5, "pt > 30 & abs(eta) < 5.0 & userInt(\'fullIdLoose\')").size()',
    jetVeto40 = 'vetoJets(0.4, "pt > 40 & abs(eta) < 5.0 & userInt(\'fullIdLoose\')").size()',
    jetVeto40_DR05 = 'vetoJets(0.5, "pt > 40 & abs(eta) < 5.0 & userInt(\'fullIdLoose\')").size()',
    #leadingJetPt = '? (vetoJets(0.4, "abs(eta) < 5.0 & userInt(\'fullIdLoose\')").size() > 0) ? vetoJets(0.4, "abs(eta) < 5.0 & userInt(\'fullIdLoose\')").at(0).pt() : -1.',
)

overlaps = PSet(
    objectMuOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 5").size()',
    objectElecOverlap = 'overlapElectrons({object_idx}, 0.4, "pt > 10").size()',
    objectCiCTightElecOverlap = 'overlapElectrons({object_idx}, 0.4, "pt > 10 & test_bit(electronID(\'cicTight\'), 0)").size()',
    objectMuOverlapZHTight = 'overlapMuons({object_idx}, 0.1, "isGlobalMuon & isTrackerMuon & pfCandidateRef.isNonnull & pt > 10 & abs(eta) < 2.4 & (userIso(0) + max(photonIso + neutralHadronIso - 0.5*puChargedHadronIso, 0))/pt < 0.3").size()',
    objectElecOverlapZHTight = 'overlapElectrons({object_idx}, 0.1, "pt > 10 & abs(eta) < 2.5 & (userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt < 0.3 & ( ( abs(eta) < 0.8 & electronID(\'mvaNonTrigV0\') > 0.5 ) || ( abs(eta) > 0.8 & abs(eta) < 1.479 & electronID(\'mvaNonTrigV0\') > 0.12 ) || ( abs(eta) > 1.479 & electronID(\'mvaNonTrigV0\') > 0.6 ))").size()',
    objectMuOverlapZHLoose = 'overlapMuons({object_idx}, 0.1, "pt > 10 & abs(eta) < 2.4 & (isGlobalMuon || isTrackerMuon)").size()',
    objectElecOverlapZHLoose = 'overlapElectrons({object_idx}, 0.1, "pt > 10 & abs(eta) < 2.5").size()',

)
