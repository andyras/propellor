#include <Eigen/Eigen>
#include <iostream>

#include "Parameters.hpp"

#define DEBUG

using std::cout;
using std::cerr;
using std::endl;

int main(int argc, char ** argv) {
  // initialize parameters /////////////////////////////////////////////////////
  Parameters p;

#ifdef DEBUG
  cout << "Memory usage of p: " << sizeof(p) << " bytes." << endl;

  Eigen::MatrixXcd H = p.Ham();

  cout << "size of Hamiltonian: " << H.rows() << "x" << H.cols() << endl;
  cout << "Hamiltonian: " << H << endl;
  cout << "Second element of Hamiltonian: " << p.Ham(0,1) << endl;
#endif

  // propagate /////////////////////////////////////////////////////////////////

  return 0;
}