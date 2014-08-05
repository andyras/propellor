#include <Eigen/Eigen>
#include <vector>

#define TMPSIZE 10
#define TMPTIMESTEPS 1000

class Parameters {
private:
  Eigen::MatrixXcd Ham_; // Hamiltonian
  std::vector<Eigen::VectorXcd> Psi_; // wavefunction over time
  std::vector<Eigen::MatrixXcd> Rho_; // density matrix over time

public:
  Parameters();
};

Parameters::Parameters() {
  // resize Hamiltonian ////////////////////////////////////////////////////////
  Ham_.resize(TMPSIZE,TMPSIZE);

  // fill in Hamiltonian ///////////////////////////////////////////////////////
  // energies
  for (unsigned int ii = 0; ii < Ham_.rows(); ii++) {
    Ham_(ii,ii) = ii*0.001;
  }
  // couplings
  for (unsigned int ii = 0; ii < (Ham_.rows() - 1); ii++) {
    Ham_(ii,ii+1) = 0.001;
    Ham_(ii+1,ii) = 0.001;
  }

  // resize wavefunction
  Psi_.resize(TMPTIMESTEPS + 1);
  for (unsigned int ii = 0; ii < Psi_.size(); ii++) {
    Psi_[ii].resize(TMPSIZE,1);
  }

  // fill in wavefunction at t = 0
  Psi_[0](0,0) = 1.0;

  // resize density matrix
  Rho_.resize(TMPTIMESTEPS + 1);
  for (unsigned int ii = 0; ii < Rho_.size(); ii++) {
    Rho_[ii].resize(TMPSIZE,TMPSIZE);
  }
}