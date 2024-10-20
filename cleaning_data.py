import pandas as pd
import openpyxl as op # thư viện cho phép đọc và ghi file
import os             # thao tác với file
import re             #cung cap các biểu thức chính quy để thao tác với chuỗi


# Hàm để làm sạch dữ liệu trong cột Title
def clean_title(title):
    if isinstance(title, str):
        cleaned_title = re.sub(r'[ýÿáàâãäåçèéêëíìîïñóòôõöúùûü,¿½ï,.,/,(,-,|]+', '', title)
        return cleaned_title.strip()
    return title

# Hàm đọc dữ liệu từ file CSV
def load_data(csv_path):
    return pd.read_csv(csv_path, encoding='latin1')

# Hàm làm sạch cột Youtuber
def clean_youtuber_column(df):
    df = df.drop_duplicates(subset='Youtuber', keep=False)
    df['Youtuber'] = df['Youtuber'].apply(lambda x: re.sub(r'[^\w\s]', '', str(x))) 
    df['Youtuber'] = df['Youtuber'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', str(x)))
    df = df[df['Youtuber'].str.strip().astype(bool)]
    df['Youtuber'] = df['Youtuber'].astype(str)
    df = df.dropna(subset=['Youtuber'])
    df = df[df['Youtuber'].str.len() > 2]
    return df

# Hàm làm sạch cột Subscribers
def clean_subscribers_column(df):
    df['subscribers'] = pd.to_numeric(df['subscribers'], errors='coerce')
    return df

# Hàm làm sạch cột Category
def clean_category_column(df):
    df = df.dropna(subset=['category'])
    return df

# Hàm làm sạch cột Title
def clean_title_column(df):
    df["Title"] = df["Title"].apply(clean_title)
    df['Title'] = df['Title'].str.title()
    return df

# Hàm làm sạch cột Country
def clean_country_column(df):
    df = df.dropna(subset=['Country'])
    df['Country'] = df['Country'].str.title()
    return df

# Hàm xử lý các cột có giá trị rỗng
def check_missing_values(df):
    df['channel_type_rank'].fillna(0, inplace=True)
    df['video_views_for_the_last_30_days'].fillna(0, inplace=True)
    df['lowest_monthly_earnings'].fillna(0, inplace=True)
    df['highest_monthly_earnings'].fillna(0, inplace=True)
    df['lowest_yearly_earnings'].fillna(0, inplace=True)
    df['highest_yearly_earnings'].fillna(0, inplace=True)
    df['subscribers_for_last_30_days'].fillna(0, inplace=True)
    df['country_rank'].fillna(0, inplace=True)
    
    return df

# Hàm làm sạch các cột khác (ví dụ: video_views_rank, channel_type, created_year, Population)
def check_other_columns(df):
    df = df.dropna(subset=['video_views_rank'])
    df = df.dropna(subset=['channel_type'])
    df = df.dropna(subset=['created_year'])
    df = df.dropna(subset=['Population'])
    return df



# Hàm kiểm tra và lọc các ngày không hợp lệ
def check_invalid_dates(df):
    df = df[df['created_date'] <= 31]
    return df

# Hàm để đánh số lại cột 'rank'
def reset_rank_column(df, rank='rank'):
    df[rank] = range(1, len(df) + 1)
    return df


# Hàm lưu file csv
def save_data(df, csv_path):
    df.to_csv(csv_path, index=False, encoding="latin1")


def main():
    csv_path = r"C:\Users\Admin\Desktop\project-python\Data_Src.csv"
    
    df = load_data(csv_path)
    
    # Làm sạch các cột
    df = clean_youtuber_column(df)
    df = clean_subscribers_column(df)
    df = clean_category_column(df)
    df = clean_title_column(df)
    df = clean_country_column(df)
    df = check_missing_values(df)
    df = check_other_columns(df)
    df = check_invalid_dates(df)
    df = reset_rank_column(df,'rank')
    
    
    save_data(df, csv_path)
    
    #print(df.iloc[1:50])

if __name__ == "__main__":
    main()
