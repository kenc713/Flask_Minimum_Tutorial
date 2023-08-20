# Flask + venv instruction
- 仮想環境venv内にFlaskをインストールして使用する方法を解説する。
- コマンドは、`myproject`>`virtual_env`ディレクトリに仮想環境用のディレクトリを作ることを想定した例である。
- 動作確認環境
  - Windows10
  - VScode
  - Powershell

## venvの作成
1. ターミナルを開き、プロジェクト用ディレクトリを作成したい位置に移動する。
2. 以下のコマンドを実行し、仮想環境を作成する。
```
$ mkdir myproject             # プロジェクト用ディレクトリの作成
$ cd myproject               
$ python -m venv virtual_env  # 仮想環境virtual_envの作成
```

> **venv内のPythonのバージョン：**
> - venv内のPythonのバージョンは、マシンにインストールされたPythonのバージョンに依存する。
> - マシン内の全てのpythonのパス一覧は、以下のコマンドで確認できる。
> ```
> $ py --list-paths
> ### Sample output ###
>  -V:3.11 *        C:\Python\Python311\python.exe
>  -V:3.9           C:\Python\Python39\python.exe
> ######
> ```
> - `*`がついているのがデフォルトのバージョンであり、異なるバージョンを利用する場合は、以下のようにvenvを作成する。
> ```
> $ py -3.9 -m venv virtual_env
> ```

## venvの有効化
- `virtual_env`の親ディレクトリである`myproject`内で以下のコマンドを実行し、venvを有効化する。
```
virtual_env\Scripts\activate
```
> **Excution Policyに関するエラー**
> - 以下のようなセキュリティに関するエラーが出る場合がある。
> ```
> venv\Scripts\activate : このシステムではスクリプトの実行が無効になっているため、ファイル C:\Users\myproject\venv\Scripts\Activate.ps1 を読み込むことができません。詳細については、「about_Execution_Policies」(https://go.microsoft.com/fwlink/?LinkID=1
> 1)     を参照してください。
> 発生場所 行:1 文字:1
> + venv\Scripts\activate
> + ~~~~~~~~~~~~~~~~~~~~~
>    + CategoryInfo          : セキュリティ エラー: (: ) []、PSSecurityException
>     + FullyQualifiedErrorId : UnauthorizedAccess
> ```
> - この場合は、以下を実行して、Execution_Policyを変更してから、有効化を行う。
> ```
> Set-ExecutionPolicy RemoteSigned -Scope Process
> ```
> - `-Scope Process`は、現在立ち上げている環境でのみExecution_Policyを変更するという意味がある。

## flaskのインストール
- venvを有効化したら、`flask`をインストールする。
```
$ pip install flask
```
- データベース操作用の`flask-sqlalchemy`もインストールしておく。

## flask動作確認
1. `app.py`を新規作成し、以下をコピぺする。

```python
#coding:utf-8
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug = True)
```

> **vscodeでのインタープリタの選択**
> - flaskのimportにエラー（`Import "flask" could not be resolved from source Pylance(reportMissingModuleSource)`）が生じている場合がある。
> - この場合は、vscodeでインタープリタを変更する必要がある。
> 1. F1キーを押す。
> 2. 'Python:Select Interpreterで検索する。
> 3. venv環境を選択する。

2. ターミナルで以下を実行し、表示されたURL（http://127.0.0.1:5000）にアクセスする。
```
$ python app.py
### Sample output ###
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 137-901-349
######
```
> **DEBUGモード：**
> - `app.run(debug = True)`でDEBUGモードとなる。
> - DEBUGモードでは、Webページでエラーが発生した際、どこで問題が生じたかを示すエラー画面が出る。
> - また、再実行しなくても変更がされる。

## データベースの作成
1. `app.py`内でデータベースを定義する。
   - 具体的な作成方法は、サンプルの`app.py`を参照
2. ターミナルで以下を実行して、`app.py`があるディレクトリで、Pythonを対話モードで起動
```
python
```
3. 以下を実行してデータベースを作成
```
>>> from app import app, db
>>> with app.app_context():
...   db.create_all()
```
- 成功した場合、`instance`ディレクトリ内に、拡張子が`.db`のファイルが作成される。

## 参考資料
https://tech-diary.net/flask-introduction/#index_id0
https://teratail.com/questions/rgcmdk8o0z2ksa