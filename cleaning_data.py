import pandas as pd
import openpyxl as op  # thư viện cho phép đọc và ghi file
import os             # thao tác với file
import re             # cung cấp các biểu thức chính quy để thao tác với chuỗi

#  Hàm để làm sạch dữ liệu trong cột Title
def clean_title(title):
    if isinstance(title, str):
        cleaned_title = re.sub(r'[ýÿáàâãäåçèéêëíìîïñóòôõöúùûü,¿½ï,.,/,(,-,|]+', '', title)
        return cleaned_title.strip()
    return title

# Hàm để làm sạch các cột
def clean_data_columns(df):
    # Làm sạch cột Youtuber
    df = df.drop_duplicates(subset='Youtuber', keep=False)
    df['Youtuber'] = df['Youtuber'].apply(lambda x: re.sub(r'[^\w\s]', '', str(x)))
    df['Youtuber'] = df['Youtuber'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', str(x)))
    df = df[df['Youtuber'].str.strip().astype(bool)]
    df['Youtuber'] = df['Youtuber'].astype(str)
    df = df.dropna(subset=['Youtuber'])
    df = df[df['Youtuber'].str.len() > 2]

    # Làm sạch cột Subscribers
    df['subscribers'] = pd.to_numeric(df['subscribers'], errors='coerce')

    # Làm sạch cột Category
    df = df.dropna(subset=['category'])

    # Làm sạch cột Title
    df["Title"] = df["Title"].apply(clean_title)
    df['Title'] = df['Title'].str.title()

    # Làm sạch cột Country
    df = df.dropna(subset=['Country'])
    df['Country'] = df['Country'].str.title()

    return df

# Hàm kiểm tra và xử lý các cột có giá trị rỗng
def handle_missing_values_and_columns(df):
    df['channel_type_rank'] = df['channel_type_rank'].fillna(0)
    df['video_views_for_the_last_30_days'] = df['video_views_for_the_last_30_days'].fillna(0)
    df['lowest_monthly_earnings'] = df['lowest_monthly_earnings'].fillna(0)
    df['highest_monthly_earnings'] = df['highest_monthly_earnings'].fillna(0)
    df['lowest_yearly_earnings'] = df['lowest_yearly_earnings'].fillna(0)
    df['highest_yearly_earnings'] = df['highest_yearly_earnings'].fillna(0)
    df['subscribers_for_last_30_days'] = df['subscribers_for_last_30_days'].fillna(0)
    df['country_rank'] = df['country_rank'].fillna(0)

    # Kiểm tra các cột khác
    df = df.dropna(subset=['video_views_rank', 'channel_type', 'created_year',])
    return df

# Hàm kiểm tra và lọc các ngày không hợp lệ
def check_invalid_dates(df):
    df = df[df['created_date'] <= 31]
    return df

# hàm xóa các cột không liên quan
# def erase_column(df):
#     columns_to_drop = ['Gross tertiary education enrollment (%)', 'Population',
#     'Unemployment rate', 'Urban_population', 'Latitude', 'Longitude']
#     df = df.drop(columns=columns_to_drop, errors='ignore')
#     return df
    
# Hàm để đánh số lại cột 'rank'
def reset_rank_column(df, rank='rank'):
    df[rank] = range(1, len(df) + 1)
    return df

# Hàm lưu file csv
def save_data(df, csv_path):
    df.to_csv(csv_path, index=False, encoding="latin1")

def main():
    csv_path = r"C:\Users\Admin\Desktop\project-python\Data_Src.csv"
    
    df = pd.read_csv(csv_path, encoding='latin1')

    df = clean_data_columns(df)
    df = handle_missing_values_and_columns(df)
    df = check_invalid_dates(df)
    df = reset_rank_column(df, 'rank')
    # df = erase_column(df)
   
    save_data(df, csv_path)

if __name__ == "__main__":
    main()
