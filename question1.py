"""
設問1
監視ログファイルを読み込み、故障状態のサーバアドレスとそのサーバの故障期間を出力するプログラムを作成せよ。
出力フォーマットは任意でよい。
なお、pingがタイムアウトした場合を故障とみなし、最初にタイムアウトしたときから、次にpingの応答が返るまでを故障期間とする。
"""
import csv
import datetime
import math
from time import time


log_data = [] #監視ログデータ
server_timeout = [] #pingがタイムアウトしたサーバ情報
server_timeout_log = [] #サーバーがタイムアウトした時間と復旧した時間を格納
 
def failure(): #サーバーがタイムアウトした時間と復旧した時間を調べる
    duplicate = False

    for line in log_data:
        #pingがタイムアウトしたサーバアドレスと確認日時を取得
        if line[7] == '-':
            #前回のpingがタイムアウトしているサーバーである場合
            for line2 in server_timeout:
                if line[6] == line2[6]: 
                    #print(line[6],'サーバーはタイムアウト継続です')
                    duplicate = True
            if duplicate == False:
                #print('新たに',line[6],'サーバーがタイムアウトしました')
                server_timeout.append([line[0],line[1],line[2],line[3],line[4],line[5],line[6],line[7],'failure'])
            duplicate = False
        else:
            #サーバーが復旧した時間を調べる
            for line2 in server_timeout:
                if line[6] == line2[6]:
                    #print(line[6],'サーバーが復旧しました')
                    server_timeout_log.append([[line2[0],line[0]],[line2[1],line[1]],[line2[2],line[2]],[line2[3],line[3]],[line2[4],line[4]],[line2[5],line[5]],line[6],[line2[7],int(line[7])],'restoration'])
                    server_timeout.remove(line2)
                    


def failure_period():
    time_now = datetime.datetime.now() #現在の時刻の取得
    for line in server_timeout:
        #もしサーバーがすでに復旧している場合
        if line[8] == 'failure':
            #print(line[6],'サーバーは現在まで故障しています')
            server_timeout_log.append([[line[0],time_now.year],[line[1],time_now.month],[line[2],time_now.day],[line[3],time_now.hour],[line[4],time_now.minute],[line[5],time_now.second],line[6],[line[7],time_now.microsecond / 1000],'failure'])
    for line in server_timeout_log:
        period_calculation(line)
        
def period_calculation(server):
    
    #故障期間を出力

    #故障開始時刻
    failure_start = [server[0][0],server[1][0],server[2][0],server[3][0],server[4][0],server[5][0],0]
    #故障終了時刻
    failure_end = [server[0][1],server[1][1],server[2][1],server[3][1],server[4][1],server[5][1],server[7][1]]

    failure_year = 0
    failure_month = 0
    failure_day = 0
    failure_hour = 0 
    failure_minute = 0
    failure_second = 0
    failure_millisecond = 0

    failure_millisecond = server[7][1]
    #second
    if server[5][0] <= server[5][1]:
        failure_second = server[5][1]-server[5][0]
    
    else:
        failure_second =  60 + server[5][1]-server[5][0]
        if server[4][0] != 60-1:
            server[4][0] = server[4][0] + 1
        else:
            server[4][0] = 0

    #minute
    if server[4][0] <= server[4][1]:
        failure_minute = server[4][1]-server[4][0]
    else:
        failure_minute =  60 + server[4][1]-server[4][0]
        if server[3][0] != 24-1:
            server[3][0] = server[3][0] + 1
        else:
            server[3][0] = 0

    #hour
    if server[3][0] <= server[3][1]:
        failure_hour = server[3][1]-server[3][0]
    else:
        failure_hour =  24 + server[3][1]-server[3][0]
        if server[2][0] != month_day(server[0][0],server[1][0])-1:
            server[2][0] = server[2][0] + 1
        else:
            server[2][0] = 0

    #day
    if server[2][0] <= server[2][1]:
        failure_day = server[2][1]-server[2][0]
    else:
        failure_day = month_day(server[0][0],server[1][0]) + server[2][1]-server[2][0]

        if server[1][0] != 12:
            server[1][0] = server[1][0] + 1
        else:
            server[1][0] = 1

    #month（日換算する）
    if server[1][0] <= server[1][1]:
        while server[1][0] < server[1][1]:
            failure_month += month_day(server[0][0],server[1][0])
            server[1][0] += 1
    else:
        while server[1][0] < server[1][1] + 12:
            if server[1][0] <=12:
                failure_month += month_day(server[0][0],server[1][0])
            else:
                failure_month += month_day(server[0][0]+1,server[1][0])
            server[1][0] += 1
        server[0][0] = server[0][0] + 1
    #year（日換算する）
    while server[0][0] < server[0][1]:
        #閏年判定
        if month_day(server[0][0],2) == 29:
            failure_year += 366
        else:
            failure_year += 365
        server[0][0] += 1

    #故障期間

    #すでに復旧しているサーバー
    if server[8] == 'restoration':
        print('サーバアドレス',server[6],'は復旧済です。')
        print(failure_start[0],'年',end=' ')
        print(failure_start[1],'月',end=' ')
        print(failure_start[2],'日',end=' ')
        print(failure_start[3],'時',end=' ')
        print(failure_start[4],'分',end=' ')
        print(failure_start[5],'秒',end=' ')
        print(failure_start[6],'ミリ秒')
        print('から')
        print(failure_end[0],'年',end=' ')
        print(failure_end[1],'月',end=' ')
        print(failure_end[2],'日',end=' ')
        print(failure_end[3],'時',end=' ')
        print(failure_end[4],'分',end=' ')
        print(failure_end[5],'秒',end=' ')
        print(failure_end[6],'ミリ秒')
        print('まで故障していました。')
        print('故障期間は')
        print(failure_year+failure_month+failure_day,'日間と',end=' ')
        print(failure_hour,'時間と',end=' ')
        print(failure_minute,'分間と',end=' ')
        print(failure_second,'秒間と',end=' ')
        print(failure_millisecond,'ミリ秒間')
        print('でした。')
        print()
    elif server[8] == 'failure':
        print('サーバアドレス',server[6],'は現在も故障しています。')
        print(failure_start[0],'年',end=' ')
        print(failure_start[1],'月',end=' ')
        print(failure_start[2],'日',end=' ')
        print(failure_start[3],'時',end=' ')
        print(failure_start[4],'分',end=' ')
        print(failure_start[5],'秒',end=' ')
        print(failure_start[6],'ミリ秒')
        print('から')
        print(failure_year+failure_month+failure_day,'日間と',end=' ')
        print(failure_hour,'時間と',end=' ')
        print(failure_minute,'分間と',end=' ')
        print(failure_second,'秒間と',end=' ')
        print(failure_millisecond,'ミリ秒間')
        print("経過しています。")
        print()

def month_day(year,month):
    if (year % 4 == 0  and year % 100 != 0) or year % 400 == 0:
        #閏年
        month_d= [0,31,29,31,30,31,30,31,31,30,31,30,31,31,29,31,30,31,30,31,31,30,31,30,31] #各月の日数
    else:
        #閏年じゃない
        month_d = [0,31,28,31,30,31,30,31,31,30,31,30,31,31,28,31,30,31,30,31,31,30,31,30,31] #各月の日数

    return month_d[month]


    



def data():
     #監視ログファイル（CSVファイル）を開く
    with open('monitoringLog.csv','r') as f:  
        #データの読み込み
        data = csv.reader(f)
        #確認日時を「年、月、日、時、分、秒」に分割する、監視ログファイルのデータをlog_dataに入れる
        for line in data:
            log_data.append([int(line[0][:4]),int(line[0][4:6]),int(line[0][6:8]),int(line[0][8:10]),int(line[0][10:12]),int(line[0][12:14]),line[1],line[2]]) 


def main():
    data() #データ取得
    failure() #故障状態のサーバアドレス情報取得
    failure_period() #故障期間を出力
main()
