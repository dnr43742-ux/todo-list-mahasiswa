import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# ---------- Konfigurasi ----------
st.set_page_config(page_title="📅 To-Do List Mahasiswa Teknik Industri", page_icon="📘", layout="centered")
DATA_FILE = "tugas_streamlit.csv"

# ---------- Fungsi ----------
def load_tasks():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        return pd.DataFrame(columns=["Tugas", "Deadline", "Status"])

def save_tasks(df):
    df.to_csv(DATA_FILE, index=False)

def add_task(task, deadline):
    new_task = pd.DataFrame([[task, deadline, "Belum selesai"]], columns=["Tugas", "Deadline", "Status"])
    df = load_tasks()
    df = pd.concat([df, new_task], ignore_index=True)
    save_tasks(df)

def mark_done(index):
    df = load_tasks()
    df.loc[index, "Status"] = "✅ Selesai"
    save_tasks(df)

def delete_task(index):
    df = load_tasks()
    df = df.drop(index)
    save_tasks(df)

def check_deadlines(df):
    now = datetime.now().date()
    upcoming = df[df["Status"] != "✅ Selesai"]
    messages = []
    for _, row in upcoming.iterrows():
        try:
            deadline = datetime.strptime(row["Deadline"], "%Y-%m-%d").date()
            if timedelta(days=0) <= (deadline - now) <= timedelta(days=1):
                messages.append(f"🔔 *{row['Tugas']}* akan mencapai deadline besok ({deadline})")
        except:
            continue
    return messages

# ---------- UI ----------
st.title("📘 To-Do List Mahasiswa Teknik Industri")
st.write("Catat, pantau, dan selesaikan tugasmu dengan mudah!")

tab1, tab2 = st.tabs(["📋 Daftar Tugas", "➕ Tambah Tugas"])

# TAB 1: DAFTAR TUGAS
with tab1:
    df = load_tasks()
    if df.empty:
        st.info("Belum ada tugas, yuk tambahkan di tab *Tambah Tugas*! ✍️")
    else:
        st.dataframe(df, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            index_done = st.number_input("Tandai selesai (masukkan nomor baris)", min_value=0, step=1, value=0)
            if st.button("✅ Tandai Selesai"):
                if index_done < len(df):
                    mark_done(index_done)
                    st.success("Tugas berhasil ditandai selesai!")
        with col2:
            index_delete = st.number_input("Hapus tugas (masukkan nomor baris)", min_value=0, step=1, value=0)
            if st.button("🗑️ Hapus Tugas"):
                if index_delete < len(df):
                    delete_task(index_delete)
                    st.warning("Tugas berhasil dihapus!")

# TAB 2: TAMBAH TUGAS
with tab2:
    st.subheader("Tambah Tugas Baru 📌")
    task = st.text_input("Nama Tugas")
    deadline = st.date_input("Pilih Deadline", datetime.now().date())
    if st.button("Tambah"):
        if task.strip() != "":
            add_task(task, str(deadline))
            st.success(f"Tugas *{task}* berhasil ditambahkan!")
        else:
            st.error("Nama tugas tidak boleh kosong!")

# 🔔 Reminder deadline
df = load_tasks()
messages = check_deadlines(df)
if messages:
    st.warning("### Pengingat Deadline ⏰")
    for msg in messages:
        st.markdown(msg)