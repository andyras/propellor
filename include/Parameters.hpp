#include <Eigen/Eigen>
#include <vector>

class Parameters {
private:
  Eigen::MatrixXcd Ham; // Hamiltonian
  std::vector<Eigen::VectorXcd> Psi; // wavefunction over time
  std::vector<Eigen::MatrixXcd> Rho; // density matrix over time

public:
};