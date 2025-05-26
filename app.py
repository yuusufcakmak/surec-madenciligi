import streamlit as st
import pandas as pd
import os
from process_miner import (
    load_data,
    calculate_case_durations,
    most_frequent_activities,
    average_process_completion_time,
    most_frequent_transitions,
    plot_activity_frequencies,
    plot_process_flow
)

st.set_page_config(page_title="Süreç Madenciliği Analiz Aracı", layout="wide", initial_sidebar_state="expanded")

st.sidebar.title("Süreç Madenciliği ✨")
st.sidebar.markdown("---_Bu araç, CSV log dosyalarınızı analiz ederek süreçleriniz hakkında değerli bilgiler sunar._---")

OUTPUT_DIR = "streamlit_outputs"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

st.sidebar.header("Veri Yükleme Alanı 📤")
uploaded_file = st.sidebar.file_uploader("Lütfen süreç loglarınızı içeren .CSV dosyasını buraya yükleyin:", type=["csv"])
st.sidebar.markdown("**Örnek CSV Formatı:**")
st.sidebar.code("Case ID,Activity Name,Start Time,End Time\n1,Aktivite A,2023-01-01 09:00:00,2023-01-01 09:05:00\n...")

st.title("📊 Süreç Madenciliği Analiz Paneli")
st.markdown("Hoş geldiniz! Süreçlerinizi keşfetmek ve iyileştirmek için CSV dosyanızı kenar çubuğundan yükleyerek başlayın.")
st.markdown("---_Analiz sonuçları aşağıda görüntülenecektir._---")

if uploaded_file is not None:
    temp_file_path = os.path.join(OUTPUT_DIR, uploaded_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"🎉 **'__{uploaded_file.name}__'** başarıyla yüklendi! Analizler yapılıyor...")
    
    df_orj = load_data(temp_file_path)

    if df_orj is not None and not df_orj.empty:
        st.info("Veri başarıyla doğrulandı. İşte analiz sonuçlarınız:")
        
        df = df_orj.copy()
        
        st.header("📈 Temel Analiz Sonuçları")

        with st.expander("1️⃣ Her Vaka (Case ID) için Toplam Süreler", expanded=True):
            case_durations = calculate_case_durations(df.copy())
            if not case_durations.empty:
                st.dataframe(case_durations)
            else:
                st.warning("Vaka süreleri hesaplanamadı.")

        with st.expander("2️⃣ En Sık Gerçekleşen Adımlar ve Frekansları", expanded=True):
            frequent_activities = most_frequent_activities(df.copy())
            if not frequent_activities.empty:
                st.dataframe(frequent_activities)
                
                activity_freq_img_path = plot_activity_frequencies(frequent_activities, output_dir=OUTPUT_DIR, filename="st_activity_frequencies.png")
                if activity_freq_img_path and os.path.exists(activity_freq_img_path):
                    st.image(activity_freq_img_path, caption="Adım Frekansları Bar Grafiği")
                else:
                    st.warning("Adım frekansları grafiği oluşturulamadı.")
            else:
                st.warning("En sık gerçekleşen adımlar bulunamadı.")

        with st.expander("3️⃣ Ortalama Süreç Tamamlanma Süresi", expanded=True):
            avg_completion_time = average_process_completion_time(df.copy())
            if avg_completion_time:
                st.metric(label="Ortalama Süreç Tamamlanma Süresi", value=str(avg_completion_time))
            else:
                st.warning("Ortalama süreç tamamlanma süresi hesaplanamadı.")
            
        with st.expander("4️⃣ En Sık Adım Geçişleri ve Süreç Akışı", expanded=True):
            frequent_transitions = most_frequent_transitions(df.copy())
            if not frequent_transitions.empty:
                st.dataframe(frequent_transitions)
                
                process_flow_img_path = plot_process_flow(frequent_transitions, output_dir=OUTPUT_DIR, filename="st_process_flow") 
                if process_flow_img_path and os.path.exists(process_flow_img_path):
                    st.image(process_flow_img_path, caption="Basit Süreç Akış Diyagramı (Graphviz)")
                else:
                    st.warning("Süreç akış diyagramı oluşturulamadı. Graphviz'in sisteminizde kurulu ve PATH'e ekli olduğundan emin olun.")
            else:
                st.warning("Adım geçişleri bulunamadı.")
            
    elif df_orj is None:
        st.error("❌ Veri yüklenirken bir hata oluştu. Lütfen CSV dosyanızı kontrol edin ve teknik detaylar için terminal çıktısını inceleyin.")
    else: 
        st.warning("⚠️ Yüklenen CSV dosyası boş veya geçerli süreç verisi içermiyor gibi görünüyor.")

else:
    st.info("💡 Analizleri başlatmak için lütfen sol kenar çubuğundan bir .CSV dosyası yükleyin.")

st.markdown("""--- 
Geliştiren: M.Yusuf Çakmak""") 