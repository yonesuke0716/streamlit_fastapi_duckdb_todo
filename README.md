# FastAPI + Streamlit Todoアプリケーション

このプロジェクトは、FastAPI、DuckDB、Streamlitを使用して構築されたTodo管理アプリケーションです。

## 機能

- ✅ Todoの作成、読み取り、更新、削除（CRUD操作）
- 📝 タイトル、説明、優先度、日付の管理
- 🎯 完了/未完了の切り替え
- 🎨 直感的なWebインターフェース（Streamlit）
- 🚀 高速なAPI（FastAPI）
- 💾 軽量なデータベース（DuckDB/SQLite）

## 技術スタック

- **バックエンド**: FastAPI
- **データベース**: DuckDB/SQLite
- **フロントエンド**: Streamlit
- **ORM**: SQLModel(SQLAlchemy + Pydantic)

## セットアップ方法

### 前提条件

- Python 3.13以上
- uv（推奨）またはpip

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd streamlit_fastapi_duckdb_todo
```

### 2. 環境変数の設定

プロジェクトルートに`.env`ファイルを作成し、データベース設定を指定します：

```bash
# .envファイル
# DuckDBを使用する場合
DATABASE_URL=duckdb:///todos_duckdb.db

# SQLiteを使用する場合
# DATABASE_URL=sqlite:///todos_sqlite.db
```

### 3. 依存関係のインストール

#### uvを使用する（推奨）

uv syncで依存関係の同期を実施する。

任意でaddを行う。

```bash
# プロジェクトの依存関係を同期
uv sync

# 新しいライブラリを追加する場合
uv add <package-name>

# requirements.txtから依存関係を追加する場合
uv add -r requirements.txt
```

### 4. 仮想環境の起動

#### Windowsの場合

```bash
.\.venv\Scripts\activate  
```

#### macOS/Linuxの場合

```bash
source .venv/bin/activate
```

### 5. アプリケーションの起動

#### バックエンドAPIの起動

```bash
python api_app.py
```

起動に成功したら、以下でSwagger UIを確認。

http://localhost:8000/docs

#### Streamlitアプリケーションの起動

別のターミナルで以下を実行：

```bash
python -m streamlit run streamlit_app.py
```

## 使い方

### APIエンドポイント

アプリケーションが起動すると、以下のAPIエンドポイントが利用可能になります：

- `GET /todos` - すべてのTodoを取得
- `POST /todos` - 新しいTodoを作成
- `PUT /todos/{todo_id}` - 既存のTodoを更新
- `DELETE /todos/{todo_id}` - Todoを削除

### Webインターフェース

1. ブラウザで `http://localhost:8501` にアクセス
2. Streamlitアプリケーションが表示されます
3. 「新しいTodoを追加」セクションでTodoを作成
4. Todo一覧で編集、完了切替、削除が可能

### Todoの作成

1. タイトルを入力（必須、3-100文字）
2. 説明を入力（必須、3-100文字）
3. 優先度を選択（1=低、5=高）
4. 日付を選択（オプション）
5. 「追加」ボタンをクリック

### Todoの編集

1. Todo一覧の各項目を展開
2. タイトル、説明、優先度、日付を編集
3. 「保存」ボタンをクリック

### Todoの完了切替

1. Todo一覧の各項目を展開
2. 「完了切替」ボタンをクリック
3. 完了/未完了の状態が切り替わります

### Todoの削除

1. Todo一覧の各項目を展開
2. 「削除」ボタンをクリック
3. 確認後、Todoが削除されます

## データベース

- DuckDBまたはSQLiteを使用した軽量なデータベース
- `.env`ファイルでデータベースタイプを切り替え可能
- データベースファイル: `todos.db`
- 自動的にテーブルが作成されます

## 開発

### プロジェクト構造

```
fastapi-duckdb/
├── api_app.py          # FastAPIアプリケーション
├── streamlit_app.py    # Streamlitアプリケーション
├── database.py         # データベース設定
├── models.py           # データモデル
├── .env                # 環境変数設定
├── todos.db           # データベースファイル
├── pyproject.toml     # プロジェクト設定
├── requirements.txt    # 依存関係
└── README.md          # このファイル
```

## ライセンス

このプロジェクトは [Apache License 2.0](LICENSE) の下で公開されています。

### ライセンスの概要

- **ライセンス**: Apache License 2.0
- **著作権**: このプロジェクトの貢献者
- **許可事項**: 
  - 商用利用
  - 修正・改変
  - 配布
  - 特許使用
- **条件**: 
  - ライセンスと著作権表示の保持
  - 変更箇所の明記
  - NOTICEファイルの保持（存在する場合）

詳細については [LICENSE](LICENSE) ファイルを参照してください。