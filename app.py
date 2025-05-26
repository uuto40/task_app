import streamlit as st
import requests

# APIのURL
API_URL = "http://localhost:8000"  # Dockerの場合は適宜 http://demo-app:8000 に

st.title("✅ タスク管理アプリ")

# タスクの取得
def fetch_tasks():
    response = requests.get(f"{API_URL}/tasks")
    return response.json() if response.status_code == 200 else []

# タスクの追加
def add_task(title):
    response = requests.post(f"{API_URL}/tasks", json={"title": title})
    return response.ok

# タスクの完了
def complete_task(task_id):
    response = requests.put(f"{API_URL}/tasks/{task_id}/done")
    return response.ok

# タスクの未完了に戻す
def undo_task(task_id):
    response = requests.delete(f"{API_URL}/tasks/{task_id}/done")
    return response.ok

# タスクの削除
def delete_task(task_id):
    response = requests.delete(f"{API_URL}/tasks/{task_id}")
    return response.ok

# タスク追加フォーム
with st.form("add_task_form"):
    title = st.text_input("新しいタスク名")
    submitted = st.form_submit_button("追加")
    if submitted and title:
        if add_task(title):
            st.success("タスクを追加しました")
            st.rerun()
        else:
            st.error("追加に失敗しました")

st.subheader("📋 タスク一覧")

tasks = fetch_tasks()

for task in tasks:
    col1, col2, col3 = st.columns([5, 1, 1])
    with col1:
        task_str = f"✅ {task['title']}" if task["done"] else f"🔲 {task['title']}"
        st.write(task_str)
    with col2:
        btn_label = "戻す" if task["done"] else "完了"
        btn_key = f"toggle-{task['id']}"
        if st.button(btn_label, key=btn_key):
            success = undo_task(task["id"]) if task["done"] else complete_task(task["id"])
            if success:
                st.rerun()
            else:
                st.error("更新に失敗しました")
    with col3:
        if st.button("削除", key=f"delete-{task['id']}"):
            if delete_task(task["id"]):
                st.rerun()
            else:
                st.error("削除に失敗しました")

