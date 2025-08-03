# FastAPI + DuckDB + Streamlit Todoアプリケーション - シーケンス図

## システム概要

このアプリケーションは以下のコンポーネントで構成されています：
- **Streamlit Frontend**: ユーザーインターフェース
- **FastAPI Backend**: REST APIサーバー
- **DuckDB Database**: データストレージ
- **SQLAlchemy ORM**: データベース操作

## 1. アプリケーション起動時の処理フロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant Streamlit as Streamlit App
    participant FastAPI as FastAPI Server
    participant ORM as SQLAlchemy ORM
    participant Database as DuckDB Database

    Note over User,Database: アプリケーション起動時
    
    User->>Streamlit: ブラウザでアクセス
    Streamlit->>FastAPI: GET /todos (httpx.get)
    FastAPI->>ORM: SessionLocal() 作成
    ORM->>Database: データベース接続
    FastAPI->>ORM: db.query(TodoModel).all()
    ORM->>Database: SELECT * FROM todos
    Database-->>ORM: データ返却
    ORM-->>FastAPI: TodoModel オブジェクト
    FastAPI->>FastAPI: Todo.model_validate() でPydantic変換
    FastAPI-->>Streamlit: JSON レスポンス
    Streamlit->>Streamlit: データをキャッシュ (st.cache_data)
    Streamlit-->>User: Todo一覧を表示
```

## 2. 新規Todo作成の処理フロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant Streamlit as Streamlit App
    participant FastAPI as FastAPI Server
    participant ORM as SQLAlchemy ORM
    participant Database as DuckDB Database

    Note over User,Database: 新規Todo作成
    
    User->>Streamlit: フォーム入力（タイトル、説明、優先度、日付）
    User->>Streamlit: 「追加」ボタンクリック
    Streamlit->>Streamlit: バリデーション（タイトル必須）
    Streamlit->>FastAPI: POST /todos (httpx.post)
    Note right of Streamlit: JSON: {title, description, priority, date}
    
    FastAPI->>FastAPI: Todo Pydanticモデルでバリデーション
    FastAPI->>ORM: SessionLocal() 作成
    ORM->>Database: データベース接続
    FastAPI->>ORM: TodoModel インスタンス作成
    FastAPI->>ORM: db.add(db_todo)
    FastAPI->>ORM: db.commit()
    ORM->>Database: INSERT INTO todos
    Database-->>ORM: 成功レスポンス
    FastAPI->>ORM: db.refresh(db_todo)
    ORM->>Database: 最新データ取得
    Database-->>ORM: 作成されたデータ
    ORM-->>FastAPI: TodoModel オブジェクト
    FastAPI->>FastAPI: Todo.model_validate() でPydantic変換
    FastAPI-->>Streamlit: JSON レスポンス（作成されたTodo）
    
    Streamlit->>Streamlit: st.cache_data.clear() でキャッシュクリア
    Streamlit->>Streamlit: st.rerun() でページ再読み込み
    Streamlit-->>User: 成功メッセージ表示
```

## 3. Todo更新の処理フロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant Streamlit as Streamlit App
    participant FastAPI as FastAPI Server
    participant ORM as SQLAlchemy ORM
    participant Database as DuckDB Database

    Note over User,Database: Todo更新（完了切替・編集）
    
    User->>Streamlit: 「完了切替」または「保存」ボタンクリック
    Streamlit->>FastAPI: PUT /todos/{todo_id} (httpx.put)
    Note right of Streamlit: JSON: {completed: true/false} または {title, description, priority, date}
    
    FastAPI->>FastAPI: Todo Pydanticモデルでバリデーション
    FastAPI->>ORM: SessionLocal() 作成
    ORM->>Database: データベース接続
    FastAPI->>ORM: db.query(TodoModel).filter(id == todo_id).first()
    ORM->>Database: SELECT * FROM todos WHERE id = ?
    Database-->>ORM: TodoModel オブジェクト
    
    alt Todoが見つからない場合
        FastAPI->>FastAPI: HTTPException(404, "Todo not found")
        FastAPI-->>Streamlit: 404 エラーレスポンス
        Streamlit-->>User: エラーメッセージ表示
    else Todoが見つかった場合
        FastAPI->>ORM: フィールド更新（title, description, completed, priority, date）
        FastAPI->>ORM: db.commit()
        ORM->>Database: UPDATE todos SET ... WHERE id = ?
        Database-->>ORM: 成功レスポンス
        FastAPI->>ORM: db.refresh(db_todo)
        ORM->>Database: 最新データ取得
        Database-->>ORM: 更新されたデータ
        ORM-->>FastAPI: TodoModel オブジェクト
        FastAPI->>FastAPI: Todo.model_validate() でPydantic変換
        FastAPI-->>Streamlit: JSON レスポンス（更新されたTodo）
        
        Streamlit->>Streamlit: st.cache_data.clear() でキャッシュクリア
        Streamlit->>Streamlit: st.rerun() でページ再読み込み
        Streamlit-->>User: 成功メッセージ表示
    end
```

## 4. Todo削除の処理フロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant Streamlit as Streamlit App
    participant FastAPI as FastAPI Server
    participant ORM as SQLAlchemy ORM
    participant Database as DuckDB Database

    Note over User,Database: Todo削除
    
    User->>Streamlit: 「削除」ボタンクリック
    Streamlit->>FastAPI: DELETE /todos/{todo_id} (httpx.delete)
    
    FastAPI->>ORM: SessionLocal() 作成
    ORM->>Database: データベース接続
    FastAPI->>ORM: db.query(TodoModel).filter(id == todo_id).first()
    ORM->>Database: SELECT * FROM todos WHERE id = ?
    Database-->>ORM: TodoModel オブジェクト
    
    alt Todoが見つからない場合
        FastAPI->>FastAPI: HTTPException(404, "Todo not found")
        FastAPI-->>Streamlit: 404 エラーレスポンス
        Streamlit-->>User: エラーメッセージ表示
    else Todoが見つかった場合
        FastAPI->>ORM: db.delete(db_todo)
        FastAPI->>ORM: db.commit()
        ORM->>Database: DELETE FROM todos WHERE id = ?
        Database-->>ORM: 成功レスポンス
        FastAPI-->>Streamlit: JSON レスポンス {"result": "success"}
        
        Streamlit->>Streamlit: st.cache_data.clear() でキャッシュクリア
        Streamlit->>Streamlit: st.rerun() でページ再読み込み
        Streamlit-->>User: 成功メッセージ表示
    end
```

## 5. データベース初期化の処理フロー

```mermaid
sequenceDiagram
    participant App as Application
    participant Database as database.py
    participant ORM as SQLAlchemy ORM
    participant DuckDB as DuckDB File

    Note over App,DuckDB: アプリケーション起動時（データベース初期化）
    
    App->>Database: import database
    Database->>Database: create_engine("sqlite:///duckdb.db")
    Database->>ORM: declarative_base()
    Database->>ORM: sessionmaker()
    Database->>ORM: Base.metadata.create_all(bind=engine)
    ORM->>DuckDB: CREATE TABLE IF NOT EXISTS todos (...)
    DuckDB-->>ORM: テーブル作成完了
    ORM-->>Database: 初期化完了
    Database-->>App: データベース接続準備完了
```

## 6. エラーハンドリングの処理フロー

```mermaid
sequenceDiagram
    participant User as ユーザー
    participant Streamlit as Streamlit App
    participant FastAPI as FastAPI Server
    participant Database as DuckDB Database

    Note over User,Database: エラーハンドリング
    
    User->>Streamlit: 操作実行
    Streamlit->>FastAPI: HTTP リクエスト
    
    alt ネットワークエラー
        FastAPI-->>Streamlit: 接続エラー
        Streamlit->>Streamlit: st.error("取得失敗: {e}")
        Streamlit-->>User: エラーメッセージ表示
    else データベースエラー
        FastAPI->>Database: データベース操作
        Database-->>FastAPI: エラーレスポンス
        FastAPI->>FastAPI: HTTPException 生成
        FastAPI-->>Streamlit: エラーレスポンス
        Streamlit->>Streamlit: st.error("操作失敗: {e}")
        Streamlit-->>User: エラーメッセージ表示
    else バリデーションエラー
        FastAPI->>FastAPI: Pydantic バリデーション
        FastAPI->>FastAPI: ValidationError 発生
        FastAPI-->>Streamlit: 422 エラーレスポンス
        Streamlit->>Streamlit: st.error("バリデーション失敗: {e}")
        Streamlit-->>User: エラーメッセージ表示
    end
```

## 7. システム全体のアーキテクチャ図

```mermaid
graph TB
    subgraph "フロントエンド"
        A[ユーザー]
        B[Streamlit App]
    end
    
    subgraph "バックエンド"
        C[FastAPI Server]
        D[SQLAlchemy ORM]
    end
    
    subgraph "データストレージ"
        E[DuckDB Database]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> D
    D --> C
    C --> B
    B --> A
```

## 技術的な詳細

### データフロー
1. **ユーザー操作** → Streamlit UI
2. **HTTP リクエスト** → FastAPI Server
3. **データベース操作** → SQLAlchemy ORM → DuckDB
4. **レスポンス** → FastAPI → Streamlit → ユーザー

### キャッシュ戦略
- Streamlitは `@st.cache_data(ttl=5)` で5秒間キャッシュ
- データ変更時は `st.cache_data.clear()` でキャッシュクリア
- `st.rerun()` でページ再読み込み

### セッション管理
- 各APIリクエストで新しいデータベースセッションを作成
- `try-finally` ブロックでセッションの適切なクローズを保証

### バリデーション
- **Pydantic**: API リクエスト/レスポンスのバリデーション
- **SQLAlchemy**: データベーススキーマの制約
- **Streamlit**: フロントエンドでの入力検証 