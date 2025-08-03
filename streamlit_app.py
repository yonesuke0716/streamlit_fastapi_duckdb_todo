import streamlit as st
import httpx

API_URL = "http://localhost:8000/todos"
st.set_page_config(
    page_title="📝 Todoアプリ (FastAPI + DuckDB + Streamlit)", layout="wide"
)
st.title("📝 Todoアプリ (FastAPI + DuckDB + Streamlit)")


# Todo取得
@st.cache_data(ttl=5)
def get_todos():
    try:
        r = httpx.get(API_URL)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error(f"取得失敗: {e}")
        return []


todos = get_todos()

# 新規追加
with st.form("add_todo"):
    st.subheader("新しいTodoを追加")
    title = st.text_input("タイトル")
    description = st.text_area("説明")
    priority = st.number_input(
        "優先度（1=低, 5=高）", min_value=1, max_value=5, value=1, step=1
    )
    date = st.date_input("日付", value=None)
    submitted = st.form_submit_button("追加")
    if submitted and title:
        try:
            date_str = date.isoformat() if date else None
            r = httpx.post(
                API_URL,
                json={
                    "title": title,
                    "description": description,
                    "priority": priority,
                    "date": date_str,
                },
            )
            r.raise_for_status()
            st.success("追加しました！")
            st.cache_data.clear()
            st.rerun()
        except Exception as e:
            st.error(f"追加失敗: {e}")

st.divider()

# Todo一覧・編集・削除
st.subheader("Todo一覧")
for todo in todos:
    with st.expander(
        f"{todo['title']} (優先度: {todo.get('priority', 1)}) "
        f"({'完了' if todo['completed'] else '未完了'})",
        expanded=False,
    ):
        st.write(f"説明: {todo['description']}")
        st.write(f"日付: {todo.get('date', '') or ''}")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("完了切替", key=f"toggle_{todo['id']}"):
                try:
                    r = httpx.put(
                        f"{API_URL}/{todo['id']}",
                        json={"completed": not todo["completed"]},
                    )
                    r.raise_for_status()
                    st.success("更新しました！")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"更新失敗: {e}")
        with col2:
            new_title = st.text_input(
                "タイトル編集", value=todo["title"], key=f"edit_title_{todo['id']}"
            )
            new_desc = st.text_area(
                "説明編集", value=todo["description"], key=f"edit_desc_{todo['id']}"
            )
            new_priority = st.number_input(
                "優先度編集（1=低, 5=高）",
                min_value=1,
                max_value=5,
                value=todo.get("priority", 1),
                step=1,
                key=f"edit_priority_{todo['id']}",
            )
            import datetime

            try:
                default_date = (
                    datetime.date.fromisoformat(todo.get("date"))
                    if todo.get("date")
                    else None
                )
            except Exception:
                default_date = None
            new_date = st.date_input(
                "日付編集",
                value=default_date or datetime.date.today(),
                key=f"edit_date_{todo['id']}",
            )
            if st.button("保存", key=f"save_{todo['id']}"):
                try:
                    date_str = new_date.isoformat() if new_date else None
                    r = httpx.put(
                        f"{API_URL}/{todo['id']}",
                        json={
                            "title": new_title,
                            "description": new_desc,
                            "priority": new_priority,
                            "date": date_str,
                        },
                    )
                    r.raise_for_status()
                    st.success("保存しました！")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"保存失敗: {e}")
        with col3:
            if st.button("削除", key=f"delete_{todo['id']}"):
                try:
                    r = httpx.delete(f"{API_URL}/{todo['id']}")
                    r.raise_for_status()
                    st.success("削除しました！")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"削除失敗: {e}")
