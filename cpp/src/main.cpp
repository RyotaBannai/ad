#include <adept.h>
#include <adept_source.h>
#include <iostream>

using adept::adouble;

int main()
{
  adept::Stack stack;
  adouble x = 2;
  stack.new_recording();
  adouble y = (x + 3) * (4 * x);
  y.set_gradient(1.0);
  stack.reverse();
  std::cout << y.value() << "," << x.get_gradient() << std::endl;
}