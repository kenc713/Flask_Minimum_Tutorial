# todo管理アプリケーション
# app.pyでは、routing（どのURLでどんな処理をするのか）とDB定義を行う。


from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

"""
- Flask             :appインスタンス作成用
- render_template   :templatesディレクトリ内のHTMLファイルを表示する関数
- request           :GET,POSTの判定用
- redirect          :指定のURLへのリダイレクト用
- SQLAlchemy        :SQLデータベースをPythonオブジェクト的に扱うためのもの
"""


# appインスタンスを作成
app = Flask(__name__)

# データベースの接続先設定(ここでは、'todo.db'という名前のデータベースを設定)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

# データベースのインスタンスを作成
db = SQLAlchemy(app)


### データベースの定義 ###
#ここでは、id、タスクタイトル、詳細説明、期日の4項目からなるデータベースを定義している。
class Post(db.Model):
    """
    id      :整数、主キー(データを一意に識別するための項目)
    title   :30文字以内の文字列、必須項目(null禁止)
    detail  :100文字以内の文字列
    due     :日付型、必須項目
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    detail = db.Column(db.String(100))
    due = db.Column(db.DateTime, nullable=False)
### ###


### 各URLのページでの動作を指定 ###

# @app.route('[URL]')以下に、関数の形で動作を記述する。
# 

# トップページ
# GETリクエスト受信時   ：todoリスト表示
# POSTリクエスト受信時  ：todo追加
# 可能なリクエスト方法を表すmethodsはデフォルトではGETのみなのでPOSTを追加しておく。
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':

        # 全データ取得
        posts = Post.query.all()

        # 全データ(todoタスク)締め切り順にソート
        posts = Post.query.order_by(Post.due).all()

        # 全データをindex.htmlに渡して表示
        return render_template('index.html', posts=posts)

    else:
        # トップページ(/)でフォーム送信のボタンが押されると、
        # POSTリクエストが送信される。⇒フォームの情報を取得&処理

        # 入力フォームから情報を取得
        title = request.form.get('title')
        detail = request.form.get('detail')
        due = request.form.get('due')
        
        # 期日を成形
        due = datetime.strptime(due, '%Y-%m-%d')

        # 新たなレコードを用意
        new_post = Post(title=title, detail=detail, due=due)

        # データベースに追加＆反映
        db.session.add(new_post)    
        db.session.commit()

        # topページに戻る
        return redirect('/')

# タスク作成ページ
@app.route('/create')
def create():
    return render_template('create.html')

# タスク詳細表示ページ
# URLに変数が含まれている例(index.htmlを一緒に見るとわかりやすい)
# URLの変数が引数となっている。
@app.route('/detail/<int:id>')
def read(id):
    # 特定のレコード（タスク）を取得
    post = Post.query.get(id)

    return render_template('detail.html', post=post)

# タスク削除ページ
@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)

    # 投稿の削除&反映
    db.session.delete(post)     
    db.session.commit()
    return redirect('/')

# タスク編集ページ
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')

        db.session.commit()     # 既存のレコードを変更するだけなのでcommitのみ
        return redirect('/')    # トップページにリダイレクト

### ###

if __name__ == "__main__":
    app.run(debug=True)     # appの起動