import pandas as pd
import matplotlib.pyplot as plt
import os
import graphviz

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        required_columns = ['Case ID', 'Activity Name', 'Start Time', 'End Time']
        if not all(col in df.columns for col in required_columns):
            print(f"Hata: CSV dosyası şu sütunları içermelidir: {', '.join(required_columns)}")
            return None
        
        df['Start Time'] = df['Start Time'].astype(str).str.strip()
        df['End Time'] = df['End Time'].astype(str).str.strip()

        try:
            df['Start Time'] = pd.to_datetime(df['Start Time'])
            df['End Time'] = pd.to_datetime(df['End Time'])
        except Exception as e:
            print(f"Hata: Zaman sütunları okunamadı. Lütfen doğru formatta olduğundan emin olun (örn: YYYY-MM-DD HH:MM:SS). Detay: {e}")
            return None

        return df
    except FileNotFoundError:
        print(f"Hata: '{file_path}' dosyası bulunamadı.")
        return None
    except Exception as e:
        print(f"Hata: Dosya okunurken bir sorun oluştu: {e}")
        return None

def calculate_case_durations(df):
    if df.empty or not all(col in df.columns for col in ['Case ID', 'Start Time', 'End Time']):
        print("Hata: calculate_case_durations için yetersiz veri veya sütunlar.")
        return pd.DataFrame()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    case_overall_durations = df.groupby('Case ID').agg(
        Min_Start_Time=('Start Time', 'min'),
        Max_End_Time=('End Time', 'max')
    ).reset_index()
    case_overall_durations['Total Case Duration'] = case_overall_durations['Max_End_Time'] - case_overall_durations['Min_Start_Time']
    return case_overall_durations[['Case ID', 'Total Case Duration']]

def most_frequent_activities(df):
    activity_counts = df['Activity Name'].value_counts().reset_index()
    activity_counts.columns = ['Activity Name', 'Frequency']
    return activity_counts

def average_process_completion_time(df):
    case_durations = df.groupby('Case ID').agg(
        start_time=('Start Time', 'min'),
        end_time=('End Time', 'max')
    )
    case_durations['Total Duration'] = case_durations['end_time'] - case_durations['start_time']
    average_time = case_durations['Total Duration'].mean()
    return average_time

def most_frequent_transitions(df):
    df_sorted = df.sort_values(by=['Case ID', 'Start Time'])
    df_sorted['Next Activity'] = df_sorted.groupby('Case ID')['Activity Name'].shift(-1)
    transitions = df_sorted.dropna(subset=['Next Activity'])
    transition_counts = transitions.groupby(['Activity Name', 'Next Activity']).size().reset_index(name='Frequency')
    transition_counts = transition_counts.sort_values(by='Frequency', ascending=False)
    return transition_counts

def plot_activity_frequencies(activity_df, output_dir=".", filename="activity_frequencies.png"):
    if activity_df.empty or not all(col in activity_df.columns for col in ['Activity Name', 'Frequency']):
        print("Hata: plot_activity_frequencies için yetersiz veri veya sütunlar.")
        return None

    plt.figure(figsize=(10, 6))
    plt.bar(activity_df['Activity Name'], activity_df['Frequency'], color='skyblue')
    plt.xlabel("Aktivite Adı")
    plt.ylabel("Frekans")
    plt.title("Aktivite Frekansları")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    
    filepath = os.path.join(output_dir, filename)
    try:
        plt.savefig(filepath)
        print(f"\nGrafik '{filepath}' olarak kaydedildi.")
        return filepath
    except Exception as e:
        print(f"Hata: Grafik kaydedilemedi: {e}")
        return None
    finally:
        plt.close()

def plot_process_flow(transitions_df, output_dir=".", filename="process_flow"):
    if transitions_df.empty or not all(col in transitions_df.columns for col in ['Activity Name', 'Next Activity', 'Frequency']):
        print("Hata: plot_process_flow için yetersiz veri veya sütunlar.")
        return None

    dot = graphviz.Digraph(comment='Süreç Akışı', format='png')
    dot.attr(rankdir='LR')

    activities = pd.concat([transitions_df['Activity Name'], transitions_df['Next Activity']]).unique()
    for activity in activities:
        dot.node(activity, activity)

    for _, row in transitions_df.iterrows():
        dot.edge(row['Activity Name'], row['Next Activity'], label=str(row['Frequency']))

    output_path = os.path.join(output_dir, filename)
    try:
        rendered_path = dot.render(output_path, view=False, cleanup=True)
        print(f"\nSüreç akış diyagramı '{rendered_path}' olarak kaydedildi.")
        return rendered_path
    except Exception as e:
        print(f"Hata: Süreç akış diyagramı oluşturulamadı/kaydedilemedi. Graphviz kurulu ve PATH'te mi? Detay: {e}")
        return None

def main():
    file_path = input("Lütfen .csv dosyasının yolunu girin: ")
    df = load_data(file_path)

    if df is not None:
        print("\n--- Analiz Sonuçları ---")

        case_durations = calculate_case_durations(df.copy())
        print("\n1. Her Case ID için Toplam Süre (İlk aktiviteden son aktiviteye kadar geçen süre):")
        print(case_durations)

        frequent_activities = most_frequent_activities(df.copy())
        print("\n2. En Sık Gerçekleşen Adımlar:")
        print(frequent_activities)
        if not frequent_activities.empty:
            activity_freq_img_path = plot_activity_frequencies(frequent_activities)
            if activity_freq_img_path:
                pass

        avg_completion_time = average_process_completion_time(df.copy())
        print("\n3. Ortalama Süreç Tamamlanma Süresi:")
        print(avg_completion_time)

        frequent_transitions = most_frequent_transitions(df.copy())
        print("\n4. En Sık Adım Geçişleri:")
        print(frequent_transitions)
        if not frequent_transitions.empty:
            process_flow_img_path = plot_process_flow(frequent_transitions)
            if process_flow_img_path:
                pass

if __name__ == "__main__":
    main() 