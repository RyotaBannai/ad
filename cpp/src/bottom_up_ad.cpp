#include <iostream>

struct ad
{
  double x, dx; // fと、f'の計算結果を保持
};

ad operator+(const ad &f, const ad &g)
{
  return ad{f.x + g.x, f.dx + g.dx};
}
// 積の微分
ad operator*(const ad &f, const ad &g)
{
  return ad{f.x * g.x, f.x * g.dx + f.dx * g.x};
}
// 関数の値と導関数の値を [f,df/dx] と括弧表記する
int main()
{
  // 微分する変数はx, その導関数は1 -> [2,1]
  // 多変数の場合f(x0,x1,x2..,xn)
  // それぞれの変数で偏導関数の値を１にして毎回計算する（もしくは、偏導関数の値を並べて同時に計算？）-> 計算の無駄が多い.
  // -> トップダウン型自動微分
  ad x{2, 1}, a{3, 0}, b{4, 0};
  ad y = (x + a) * (b * x);
  std::cout << y.x << "," << y.dx << std::endl; // 40,28
}