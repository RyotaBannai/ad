#include <adept.h>
#include <adept_source.h>
#include <boost/numeric/odeint.hpp>
#include <iostream>
#include <matplot/matplot.h>
#include <random>

using adept::adouble;
namespace odeint = boost::numeric::odeint;
namespace plt = matplot;
using namespace std;

template <class T> vector<T> simulate(const vector<T> init)
{
  typedef std::array<T, 4> state_t;
  state_t x0{init[0], init[1], init[2], init[3]};
  T m = init[4];
  auto system = [&](const state_t &x, state_t &dxdt, T /*t*/) { // 微分方程式を書く
    dxdt[0] = x[2];                                             // u`
    dxdt[1] = x[3];                                             // v`
    T r2 = x[0] * x[0] + x[1] * x[1];
    T r3 = pow(r2, 3.0 / 2.0);
    dxdt[2] = -m * x[0] / r3; // x`
    dxdt[3] = -m * x[1] / r3; // y`
  };

  auto stepper = odeint::controlled_runge_kutta<odeint::runge_kutta_dopri5<state_t, T>>();
  std::vector<T> orbit; // 軌道保存用
  auto observer = [&](const state_t &x, T /*t*/) {
    orbit.push_back(x[0]);
    orbit.push_back(x[1]);
  };
  T t0 = 0.0, t1 = 15.0, dt = 0.1;
  odeint::integrate_const( // 軌道計算する
      stepper, system, x0, t0, t1, dt, observer);
  return orbit;
}

// 二乗平均
template <class T> T error(const vector<T> &orbit, const vector<double> &observed)
{
  size_t n = orbit.size();
  T sum_sqr = 0.0;
  for (size_t i = 0; i < n; ++i) {
    T dv = orbit[i] - observed[i];
    sum_sqr += dv * dv;
  }
  return sum_sqr / n;
}

struct adam {
  size_t dim, k;
  double a = 0.001, b1 = 0.9, b2 = 0.999, e = 1e-8;
  vector<double> m1, m2;
  adam(size_t dim) : dim(dim), k(0), m1(dim), m2(dim) {}
  void operator()(const vector<double> &dx, vector<double> &x)
  {
    double t = static_cast<double>(++k);
    for (size_t i = 0; i < dim; ++i) {
      m1[i] = b1 * m1[i] + (1.0 - b1) * dx[i];
      m2[i] = b2 * m2[i] + (1.0 - b2) * dx[i] * dx[i];
      double c1 = m1[i] / (1.0 - pow(b1, t));
      double c2 = m2[i] / (1.0 - pow(b2, t));
      x[i] -= a * c1 / (sqrt(c2) + e);
    }
  }
};

template <class T> tuple<vector<T>, vector<T>> split_dat(vector<T> v)
{
  vector<double> xs, ys;
  for (size_t i = 0; i < v.size(); ++i) {
    if (i % 2 == 0) {
      xs.push_back(v[i]);
    }
    else {
      ys.push_back(v[i]);
    }
  }
  return make_tuple(xs, ys);
}

// main
int main()
{
  vector<double> _init{
      /*x =*/3.0, /*y =*/0.0, // 座標
      /*u =*/0.3, /*v =*/0.2, // 速度
      /*m =*/1.0              // 太陽の質量
  };
  vector<double> orbit = simulate(_init);
  vector<double> observed = orbit;

  // 推定値にノイズを加えて、観測データっぽくする.
  mt19937 gen(0);                   // include random
  normal_distribution<> d(0, 0.05); // include random
  for (auto &x : observed) {
    x += d(gen);
  }

  // 初期条件の 位置, 速度, 太陽の質量 を推定してみる
  // 目分量でテキトーな初期条件を入れる (全ての変数は最適値ではない)
  vector<double> init{
      /*x =*/10, /*y =*/5,    // 座標
      /*u =*/0.4, /*v =*/0.3, // 速度
      /*m =*/1.3              // 太陽の質量
  };

  size_t dim = init.size();
  auto optimizer = adam(dim);

  for (size_t i = 0; i < 100; ++i) {

    adept::Stack stack;
    std::vector<adept::adouble> init_(dim); // 入力変数
    boost::copy(init, init_.begin());
    stack.new_recording(); // アルゴリズムの記録を開始
    std::vector<adept::adouble> orbit_ = simulate(init_);
    adept::adouble err_ = error(orbit_, observed); // 誤差値
    err_.set_gradient(1.0);                        // 出力変数(誤差値)の勾配を設定
    stack.reverse();                               // トップダウン型自動微分を実行
    std::vector<double> grad(dim);
    for (size_t i = 0; i < dim; ++i)
      grad[i] = init_[i].get_gradient(); // 偏導関数の値
    // adouble err = error(orbit_tmp, observed); // 誤差値
    // cout << 'error' << err << endl;
    // err.set_gradient(1.0); // 出力変数（誤差値）の勾配を設定
    // stack.reverse();       // トップダウン型自動微分
    // vector<double> grad(dim);
    // for (size_t i = 0; i < dim; ++i) {
    //   grad[i] = init_tmp[i].get_gradient(); // 偏導関数の値
    // }
    // optimizer(grad, _init);
    // cout << _init[0] << ',' << _init[1] << "," << endl;
  }

  // auto [xs, ys] = split_dat(observed);
  // plt::subplot(2, 1, 0);
  // plt::plot(xs, ys, "r-+");
  //
  // auto [xs2, ys2] = split_dat(orbit);
  // plt::hold(plt::on);
  // plt::subplot(2, 1, 1);
  // plt::plot(xs2, ys2, "a--o");
  // plt::show();

  // vector<double> orbit_opt = simulate(_init);
  // auto [xs_opt, ys_opt] = split_dat(orbit_opt);
  // plt::hold(plt::on);
  // plt::plot(xs_opt, ys_opt, "a--o");
  // plt::show();
}