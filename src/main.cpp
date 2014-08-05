#include <Eigen/Eigen>
#include <iostream>

#include "Parameters.hpp"

#define DEBUG

using std::cout;
using std::endl;

int main(int argc, char ** argv) {
  // initialize parameters /////////////////////////////////////////////////////
  Parameters p;

#ifdef DEBUG
  cout << "Memory usage of p: " << sizeof(p) << " bytes." << endl;
#endif

  // propagate /////////////////////////////////////////////////////////////////

  return 0;
}