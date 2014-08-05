#include <complex>
#include <Eigen/Eigen>
#include <vector>

#define TMPSIZE 10
#define TMPTIMESTEPS 1000

using std::cout;
using std::cerr;
using std::endl;

class Parameters {
private:
  Eigen::MatrixXcd Ham_; // Hamiltonian
  std::vector<Eigen::VectorXcd> Psi_; // wavefunction over time
  std::vector<Eigen::MatrixXcd> Rho_; // density matrix over time

public:
  Parameters(); // default constructor

  Eigen::MatrixXcd Ham(); // gives Ham_
  std::complex<double> Ham(int r, int c); // gives Ham_(r,c)
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

Eigen::MatrixXcd Parameters::Ham() {
  return Ham_;
}

std::complex<double> Parameters::Ham(int r, int c) {
  if (r > (Ham_.rows() - 1)) {
    cerr << "ERROR: row " << r << "beyond bounds of Hamiltonian." << endl;
  }
  if (c > (Ham_.cols() - 1)) {
    cerr << "ERROR: column " << c << "beyond bounds of Hamiltonian." << endl;
  }
  return Ham_(r,c);
}