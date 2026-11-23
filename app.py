import streamlit as st
import pandas as pd
import joblib

paket = joblib.load('csgo_model.joblib')
model = paket['model']
scaler = paket['scaler']
sutunlar = paket['sutunlar']

st.title('CS:GO Raunt Kazanma Tahmini')
st.caption("Harita, taraf, ekonomi farkı ve kaybetme serisine göre raunt kazanma olasılığı simülatörü")

harita_sozlugu = {
    "Agency": "cs_agency", "Assault": "cs_assault", "Insertion": "cs_insertion",
    "Italy": "cs_italy", "Office": "cs_office", "Austria": "de_austria",
    "Aztec": "de_aztec", "Blackgold": "de_blackgold", "Cache": "de_cache",
    "Canals": "de_canals", "Cobblestone": "de_cbble", "Dust": "de_dust",
    "Dust 2": "de_dust2", "Inferno": "de_inferno", "Mirage": "de_mirage",
    "Nuke": "de_nuke", "Overpass": "de_overpass", "Shipped": "de_shipped",
    "Thrill": "de_thrill", "Train": "de_train", "Vertigo": "de_vertigo"
}

secilen_isim = st.selectbox("Harita Seçin", harita_sozlugu)
harita = harita_sozlugu[secilen_isim]

taraf = st.radio("Takım A Tarafı", ["CT", "T"], horizontal=True)
eq_diff = st.slider("Ekipman Değeri Farkı (A - B) ($)", -25000, 25000, 0, step=500)
a_val = st.session_state.get("a_box", 0)
b_val = st.session_state.get("b_box", 0)

a_streak = st.number_input("Takım A Kaybetme Serisi", min_value=0, max_value=15, value=0, key="a_box", disabled=(b_val > 0))
b_streak = st.number_input("Takım B Kaybetme Serisi", min_value=0, max_value=15, value=0, key="b_box", disabled=(a_val > 0))

if st.button("Kazanma Olasılığını Hesapla"):
    # 1. Eğitimdeki 44 sütunun tamamını 0 ile başlat
    girdi_df = pd.DataFrame(0, index=[0], columns=sutunlar)

    # 2. Sayısal girdileri gerçek sütun adlarına yerleştir
    girdi_df["a_eq_diff"] = eq_diff
    girdi_df["a_prev_streak"] = a_streak
    girdi_df["b_prev_streak"] = b_streak

    # 3. Harita + Taraf birleşik sütununu 1 yap (örn: "map_side_de_mirage_CT")
    birlesik_sutun = f"map_side_{harita}_{taraf}"
    if birlesik_sutun in girdi_df.columns:
        girdi_df[birlesik_sutun] = 1

    # 4. Ölçekle ve olasılık hesapla
    girdi_scaled = scaler.transform(girdi_df)
    olasilik = model.predict_proba(girdi_scaled)[0][1]

    # 5. Sonucu iki sütunlu temiz kartlar halinde yazdır
    st.divider()
    rakip_taraf = "T" if taraf == "CT" else "CT"
    olasilik_b = 1 - olasilik

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f"Takım A ({taraf})", value=f"%{olasilik * 100:.1f}")
    with col2:
        st.metric(label=f"Takım B ({rakip_taraf})", value=f"%{olasilik_b * 100:.1f}")

    st.progress(float(olasilik))