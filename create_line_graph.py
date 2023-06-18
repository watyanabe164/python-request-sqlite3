import sqlite3
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite3 database
# カレントディレクトリ内にあるdata.dbを開いて、接続する
# cursorオブジェクトを作成する（これつかってSQL文を実行する）
conn = sqlite3.connect("data.db")
c = conn.cursor()

# Retrieve the data from the table for the specified date range
# もともとは、datetimeを使って、日付を指定していたが、これだとなぜか2022/1/1～2023/1/1のデータがとれちゃったので困った
# なので、文字列で指定することにした
#start_date = datetime.datetime(2022, 4, 1)
#end_date = datetime.datetime(2023, 4, 1)
#c.execute("SELECT * FROM data WHERE date >= ? AND date <= ?", (start_date.strftime("%Y/%m/%d"), end_date.strftime("%Y/%m/%d")))
start_date="2022/4/1"
end_date="2023/4/1"
c.execute("SELECT * FROM data WHERE date >= ? AND date <= ?", (start_date,end_date))
# もちろん↓↓のようなやり方でもうまくいくけど、これだと、都度修正するときに不便なので上のようにした
#c.execute("SELECT * FROM data WHERE date BETWEEN '2022/4/1' AND '2023/4/1'")
rows = c.fetchall()

# Extract the dates and cases from the data
# 抽出したデータをdatesとcasesにそれぞれ格納する
# 1列目は日付、2列目はPCR検査数
dates = []
cases = []
for row in rows:
    if row[0]:
        dates.append(datetime.datetime.strptime(row[0], "%Y/%m/%d"))
        if row[1]:
            cases.append(int(row[1])//1000)
        else:
            cases.append(0)


## Create a Pandas DataFrame with the dates and cases
# PandasのDataFrameを作成する
# indexは日付、casesはPCR検査数
df = pd.DataFrame({"cases": cases}, index=dates)

# Resample the data to daily frequency
# 日付が飛んでいるところは0で埋める
# resample("D")は日付を1日ごとにするという意味
# asfreq()は日付が飛んでいるところを0で埋めるという意味
df = df.resample("D").asfreq()

# Fill missing values with 0
df = df.fillna(0)

# Set the x-axis and y-axis tick marks and labels
# 多分、この説明だけだとわからないと思うので、F5クリックしてグラフ出せばわかると思う
plt.plot(df.index, df["cases"])
plt.xticks(rotation=45) # x軸のラベルを45度回転させる
plt.yticks([i*max(df["cases"])/10 for i in range(11)]) # y軸のラベルをdf["cases"]の最大値(=1329)の10分の1刻みで表示する

# Display the graph
plt.show()

# Close the database connection
# conn.close()は必ず入れよう。以下説明。
# conn.close() を呼び出さなかった場合、SQLite3データベースへの接続が閉じられず、プログラムが終了するまで接続が維持されます。これにより、データベースへの接続が開かれたままになり、他のプログラムが同じデータベースにアクセスしようとした場合に問題が発生する可能性があります。
#また、接続が開かれたままになると、データベースファイルがロックされたままになり、他のプログラムがデータベースファイルにアクセスできなくなる可能性があります。
# したがって、プログラムがデータベースにアクセスし終わったら、必ず conn.close() を呼び出して接続を閉じることが重要です。
conn.close()