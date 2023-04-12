# Automatic differentiation (自動微分)
## 実行環境
- Arm でも動く
- Adept: C++ 向けの自動微分ライブラリ
 - Adept のinstall [参考](http://www.met.reading.ac.uk/clouds/adept/adept_documentation.pdf)
 - 参考pdf より、install に必要なライブラリ：
  - openblas, LAPACK など. compile するにあたり他にもエラーで必要になるライブラリがあるが適宜brew する.
- コンパイル
 - cmake を使う
 - `src` で `cmake -S . -B build && cmake --build build && ./build/a.out`
 - CMakeLists.txt
  - `include_directories` に`include_directories` に必要なライブラリが入っている場合は追加する
  - Intel 版のbrew で入れたものを使いたいなら`/usr/local/include`、Arm 版のbrew で入れたものを使いたいなら`/opt/homebrew/opt`
  - `add_executable` の第一引数に実行ファイル名、二つ目をコンパイル対象のファイルとする
  - その他、brew で入れにくいpackage はcmake に任せる. `matplot` など　[参考](https://stackoverflow.com/questions/72860530/matplot-linking-issue)
## 留意点など
- unix 以外のplatform で実行するときには、ファイルに`#include <adept_source.h>` も追加しないといけない！
- jpeg, tiff が入っていないと可視化されない. `brew install jpeg tiff`
## 参考・リンク等
- cmake
 - [How to properly add include directories with CMake](https://stackoverflow.com/questions/13703647/how-to-properly-add-include-directories-with-cmake)
- matplotplusplus
 - [C++でグラフ描画をするならmatplotlib-cppを使ってみる？](https://hirlab.net/nblog/category/programming/art_826/)
- odeint 
 - [Boost を使って微分方程式を解く](https://sochigusa.bitbucket.io/tips/boost_odeint.html)
## その他
```c++

enum class line_style {
  none,          // no line
  solid_line,    // "-"
  dashed_line,   // "--"
  dotted_line,   // ":"
  dash_dot_line, // "-."
};

enum class marker_style {
  none,      // "" -> gnuplot linetype -1
  plus_sign, // "+" -> gnuplot linetype 1
  circle,    // "o" -> gnuplot linetype 6
  asterisk,  // "*" -> gnuplot linetype 3
  point,     // "." -> gnuplot linetype 7
  cross,     // "x" -> gnuplot linetype 2
  square,    // "s" / "square" -> gnuplot linetype 4 / 5
  diamond,   // "d" / "diamond" -> gnuplot linetype 12 / 13
  upward_pointing_triangle,   // "^" -> gnuplot linetype 8 / 9
  downward_pointing_triangle, // "v" -> gnuplot linetype 10 / 11
  right_pointing_triangle,    // ">" -> gnuplot linetype (doest not
                              // exist)
  left_pointing_triangle, // "<" -> gnuplot linetype (does not exist)
  pentagram, // "p" / "pentagram" -> gnuplot linetype 14 / 15
  hexagram,  // "h" / "hexagram" -> gnuplot linetype (does not exist)
  custom, // https://stackoverflow.com/questions/16189187/gnuplot-using-custom-point-shapes-with-legend-entry
};
```