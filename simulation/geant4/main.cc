// MuonScope Geant4 demonstration — NOT the original 2026 production scan engine.
// Physics: mu- at 3 GeV, simplified cos^2 zenith intensity, FTFP_BERT,
// two plastic scintillator panels and an optional 5 cm Pb cube.
// Event-level output includes scintillator energy deposits; no optical photons,
// PMT detection, amplifier, discriminator or dead time is simulated here.
#include <cmath>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>

#include "FTFP_BERT.hh"
#include "G4Box.hh"
#include "G4Event.hh"
#include "G4PhysicalConstants.hh"
#include "G4LogicalVolume.hh"
#include "G4MuonMinus.hh"
#include "G4NistManager.hh"
#include "G4PVPlacement.hh"
#include "G4ParticleGun.hh"
#include "G4RunManager.hh"
#include "G4SDManager.hh"
#include "G4Step.hh"
#include "G4SystemOfUnits.hh"
#include "G4ThreeVector.hh"
#include "G4UserEventAction.hh"
#include "G4VPhysicalVolume.hh"
#include "G4VUserDetectorConstruction.hh"
#include "G4VUserPrimaryGeneratorAction.hh"
#include "G4VSensitiveDetector.hh"
#include "Randomize.hh"

struct Config {
    int events = 10000;
    int seed = 2026;
    double upperGapMM = 50.;
    double lowerGapMM = 50.;
    double panelSideMM = 100.;
    double panelThicknessMM = 10.;
    double cubeSideMM = 50.;
    bool withCube = true;
    std::string output = "geant4_hits.csv";
};

class EventRecorder : public G4UserEventAction {
public:
    explicit EventRecorder(const std::string& path) : file(path) {
        if (!file) throw std::runtime_error("Could not open output CSV: " + path);
        file << "event_id,top_edep_mev,bottom_edep_mev,top_x_mm,top_y_mm,"
                "bottom_x_mm,bottom_y_mm,both_edep_positive\n";
    }
    void BeginOfEventAction(const G4Event*) override {
        energy[0] = energy[1] = 0.;
        first[0] = first[1] = false;
        x[0] = x[1] = y[0] = y[1] = 0.;
    }
    void Deposit(int plane, G4double edep, const G4ThreeVector& position) {
        if (plane < 0 || plane > 1) return;
        energy[plane] += edep;
        if (!first[plane]) {
            x[plane] = position.x()/mm;
            y[plane] = position.y()/mm;
            first[plane] = true;
        }
    }
    void EndOfEventAction(const G4Event* event) override {
        file << event->GetEventID() << ',' << energy[0]/MeV << ',' << energy[1]/MeV
             << ',' << x[0] << ',' << y[0] << ',' << x[1] << ',' << y[1] << ','
             << (energy[0] > 0 && energy[1] > 0 ? 1 : 0) << '\n';
    }
private:
    std::ofstream file;
    G4double energy[2]{};
    double x[2]{}, y[2]{};
    bool first[2]{};
};

class PanelSD : public G4VSensitiveDetector {
public:
    explicit PanelSD(EventRecorder* recorder) : G4VSensitiveDetector("PanelSD"), recorder(recorder) {}
    G4bool ProcessHits(G4Step* step, G4TouchableHistory*) override {
        const double e = step->GetTotalEnergyDeposit();
        if (e <= 0) return false;
        const int copy = step->GetPreStepPoint()->GetTouchableHandle()->GetCopyNumber();
        recorder->Deposit(copy, e, step->GetPreStepPoint()->GetPosition());
        return true;
    }
private:
    EventRecorder* recorder;
};

class GeometryBuilder : public G4VUserDetectorConstruction {
public:
    GeometryBuilder(Config c, EventRecorder* recorder) : c(c), recorder(recorder) {}
    G4VPhysicalVolume* Construct() override {
        auto* nist = G4NistManager::Instance();
        auto* worldMat = nist->FindOrBuildMaterial("G4_AIR");
        auto* scint = nist->FindOrBuildMaterial("G4_POLYSTYRENE");
        auto* lead = nist->FindOrBuildMaterial("G4_Pb");
        auto* worldSolid = new G4Box("world", 2*m,2*m,2*m);
        auto* worldLV = new G4LogicalVolume(worldSolid,worldMat,"world");
        auto* worldPV = new G4PVPlacement(nullptr,{},worldLV,"world",nullptr,false,0);
        auto* panelSolid=new G4Box("panel",c.panelSideMM*mm/2,c.panelSideMM*mm/2,
                                    c.panelThicknessMM*mm/2);
        panelLV=new G4LogicalVolume(panelSolid,scint,"scintillatorPanel");
        const double upper = (c.cubeSideMM/2+c.upperGapMM+c.panelThicknessMM/2)*mm;
        const double lower = -(c.cubeSideMM/2+c.lowerGapMM+c.panelThicknessMM/2)*mm;
        new G4PVPlacement(nullptr,G4ThreeVector(0,0,upper),panelLV,"top",worldLV,false,0);
        new G4PVPlacement(nullptr,G4ThreeVector(0,0,lower),panelLV,"bottom",worldLV,false,1);
        if (c.withCube) {
            auto* solid = new G4Box("leadCube",c.cubeSideMM*mm/2,c.cubeSideMM*mm/2,
                                    c.cubeSideMM*mm/2);
            auto* logical = new G4LogicalVolume(solid,lead,"leadCube");
            new G4PVPlacement(nullptr,{},logical,"cube",worldLV,false,0);
        }
        return worldPV;
    }
    void ConstructSDandField() override {
        auto* sensitive=new PanelSD(recorder);
        G4SDManager::GetSDMpointer()->AddNewDetector(sensitive);
        panelLV->SetSensitiveDetector(sensitive);
    }
private:
    Config c;
    EventRecorder* recorder;
    G4LogicalVolume* panelLV=nullptr;
};

class Generator : public G4VUserPrimaryGeneratorAction {
public:
    explicit Generator(Config c) : c(c), gun(new G4ParticleGun(1)) {
        gun->SetParticleDefinition(G4MuonMinus::Definition());
        gun->SetParticleEnergy(3*GeV); // controlled benchmark, NOT realistic energy spectrum
    }
    void GeneratePrimaries(G4Event* event) override {
        const double cosTheta=std::pow(G4UniformRand(),0.25);
        const double sinTheta=std::sqrt(1-cosTheta*cosTheta);
        const double phi=2*CLHEP::pi*G4UniformRand();
        gun->SetParticleMomentumDirection(G4ThreeVector(sinTheta*std::cos(phi),
                                                    sinTheta*std::sin(phi),-cosTheta));
        gun->SetParticlePosition(G4ThreeVector(
            (G4UniformRand()-.5)*c.panelSideMM*mm,
            (G4UniformRand()-.5)*c.panelSideMM*mm,
            (c.cubeSideMM/2+c.upperGapMM+c.panelThicknessMM+1.)*mm));
        gun->GeneratePrimaryVertex(event);
    }
private:
    Config c;
    std::unique_ptr<G4ParticleGun> gun;
};

int main(int argc, char** argv) {
    Config c;
    for (int i=1;i<argc;i++) {
        const std::string arg(argv[i]);
        if (i+1>=argc) { std::cerr << "Missing value for " << arg << '\n';return 2; }
        const std::string value(argv[++i]);
        try {
            if (arg=="--events") c.events=std::stoi(value);
            else if (arg=="--seed") c.seed=std::stoi(value);
            else if (arg=="--upper-gap-mm") c.upperGapMM=std::stod(value);
            else if (arg=="--lower-gap-mm") c.lowerGapMM=std::stod(value);
            else if (arg=="--panel-mm") c.panelSideMM=std::stod(value);
            else if (arg=="--target") c.withCube=(value=="lead");
            else if (arg=="--output") c.output=value;
            else {std::cerr << "Unknown argument: " << arg << '\n';return 2;}
        } catch (const std::exception& e) {std::cerr<<e.what()<<'\n';return 2;}
    }
    if(c.events<1 || c.upperGapMM<=0 || c.lowerGapMM<=0 || c.panelSideMM<=0) {
        std::cerr<<"Invalid geometry/event count\n";return 2;
    }
    G4Random::setTheSeed(c.seed);
    auto* recorder=new EventRecorder(c.output);
    auto manager=std::make_unique<G4RunManager>(); // single-threaded reproducible demonstration
    manager->SetUserInitialization(new GeometryBuilder(c,recorder));
    manager->SetUserInitialization(new FTFP_BERT);
    manager->SetUserAction(new Generator(c));
    manager->SetUserAction(recorder); // run manager owns EventRecorder
    manager->Initialize();
    manager->BeamOn(c.events);
    return 0;
}
