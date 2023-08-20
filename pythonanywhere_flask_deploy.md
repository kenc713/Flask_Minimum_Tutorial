# Git管理のFlaskアプリをPythonanywhereにDeployする方法

## 参考サイト
- 基本的には下記のサイトを見ればできる。
- https://techium.hatenablog.com/entry/2018/02/01/214332

## 注意点
- Pythonanywhereでは`venv`とはまた違う仮想環境が使われている。
  - `venv`作成時と全くコマンドが違うので注意
- Source code:やWorking directory:に入力するPATHは、Console上で確認すると間違いにくい。(pwdの使用)
- WSGI configuration file:の中身のproject_homeが正しいか確認すること。
- 作成した仮想環境へのPATHは`which`コマンドでわかる。
  - 以下の場合、`/home/test_app/.virtualenvs/virtual_env`が仮想環境へのPATHである。
```
which python
# Ex:/home/test_app/.virtualenvs/virtual_env/bin/python
```
- Static Files:の指定も忘れずに行う。