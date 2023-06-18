# python_get_data
インターネットで公開されているいろいろなデータを取得するプログラム
を、試しにつくったものです

# プログラムの説明
## csv_to_sqlite.py
https://www.mhlw.go.jp/content/001060467.csv
のデータをインターネットから取得してこれをsqlite3に保存するプログラム

## retrieve_all_data_in_sqlite.py
sqlite3に格納させたデータを標準出力で出力させるプログラム

## create_line_graph.py
sqlite3に格納させたデータをmatlibplotを使って折れ線グラフ書いたもの。
日付指定がdate型を使わずに文字列で指定するのでちょっとびっくりしたので
参考のためにそのときのコードも残しておいた