'''

Build a version of the MVA MET recipe which runs only on objects in
the UW PAT tuple.

Author: Evan K. Friis, UW Madison

'''

import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.producersLayer1.metProducer_cfi import patMETs
from FinalStateAnalysis.Utilities.version import cmssw_major_version

try:
    if cmssw_major_version() == 5:
        from JetMETCorrections.METPUSubtraction.mvaPFMET_leptons_cff import \
                calibratedAK5PFJetsForPFMEtMVA, pfMEtMVA, \
                isomuons, isoelectrons, isotaus

#        from RecoJets.Configuration.RecoPFJets_cff import kt6PFJets as dummy
#        from RecoTauTag.RecoTau.PFRecoTauDiscriminationByHPSSelection_cfi import hpsSelectionDiscriminator
#        from RecoTauTag.RecoTau.TauDiscriminatorTools import requireLeadTrack
        from JetMETCorrections.METPUSubtraction.mvaPFMET_leptons_cfi import \
                isomuonseq, isoelectronseq#, \
#                kt6PFJetsForRhoComputationVoronoiMet, hpsPFTauDiscriminationByDecayModeFinding, \
#                requireDecayMode, hpsPFTauDiscriminationAgainstMuon2, \
#                hpsPFTauDiscriminationByMVAIsolation, isotaus, isotauseq
#                kt6PFJetsForRhoComputationVoronoiMetMvamet, hpsPFTauDiscriminationByDecayModeFinding, \
#                requireDecayModeMvamet, hpsPFTauDiscriminationAgainstMuon2Mvamet, \
#                hpsPFTauDiscriminationByMVAIsolationMvamet, isotaus, isotauseq


    else:
        from JetMETCorrections.METPUSubtraction.mvaPFMET_leptons_42X_cff \
                import calibratedAK5PFJetsForPFMEtMVA, pfMEtMVA, \
                isomuons, isoelectrons, isotaus

    from JetMETCorrections.Configuration.DefaultJEC_cff \
            import ak5PFJetsL1FastL2L3, ak5PFJetsL1FastL2L3Residual

    from JetMETCorrections.Configuration.JetCorrectionServicesAllAlgos_cff \
            import ak5PFL1FastL2L3, ak5PFL1Fastjet, ak5PFL2Relative, \
            ak5PFL3Absolute

    #process.load("JetMETCorrections.Configuration.DefaultJEC_cff")
    # Modify muons
#$#    muon_cut = isomuons.cut
#$#    isomuons = cms.EDFilter(
#$#        "MuonSelector",
#$#        src=cms.InputTag("muons"),
#$#        cut=muon_cut,
#$#        filter=cms.bool(False)
#$#    )
#$#    # Modify electrons
#$#    e_cut = isoelectrons.cut
#$#    isoelectrons = cms.EDFilter(
#$#        "GsfElectronSelector",
#$#        src=cms.InputTag("gsfElectrons"),
#$#        cut=e_cut,
#$#        filter=cms.bool(False)
#$#    )
    # Modify tau test XXX
#~~    t_cut = isotaus.cut
#~~    isotaus = cms.EDFilter(
#~~        "PATTauSelector",
#~~        src=cms.InputTag("selectedPatTaus"),
#~~        cut=t_cut,
#~~        filter=cms.bool(False)
#~~    )
###    # Modify taus
    isotaus = cms.EDFilter(
        "PATTauSelector",
        src=cms.InputTag("selectedPatTaus"),
        cut=cms.string(
            'pt > 19 && abs(eta) < 2.3 && '
            'tauID("decayModeFinding") && '
            'tauID("byIsolationMVAraw") > 0.8 && '
            'tauID("againstElectronLoose") && tauID("againstMuonLoose2")'),
        filter=cms.bool(False)
    )

    patMEtMVA = patMETs.clone(metSource=cms.InputTag("pfMEtMVA"))
    patMEtMVA.addMuonCorrections = False
    pfMEtMVA.verbosity = 0

    print "Built MVA MET sequence"
    pfMEtMVAsequence = cms.Sequence(
        (isomuonseq+isotaus+isoelectronseq)*
        calibratedAK5PFJetsForPFMEtMVA * # XXX
#        isomuons * isoelectrons * isotaus *
        pfMEtMVA * patMEtMVA
    )
except ImportError:
    import sys
    sys.stderr.write(
        "Warning: MVA MET dependencies not installed => MVA MET disabled.\n")
    pfMEtMVAsequence = cms.Sequence()
