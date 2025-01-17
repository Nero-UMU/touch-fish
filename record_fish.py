import datetime
import csv
import os

def record_fish(record_fish, generate_fish_record):
    if record_fish == "True":
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        csv_path = "fish-record.csv"
        html_path = "daily-fish.html"
        
        # 初始化或加载记录
        records = []
        if os.path.exists(csv_path):
            with open(csv_path, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append({
                        "Date": row["Date"],
                        "Count": int(row["Count"]),
                        "Time": row["Time"] if row["Time"] else ""
                    })
        
        # 检查今天的记录
        today_record = None
        for record in records:
            if record["Date"] == today:
                today_record = record
                break
                
        if today_record:
            # 增加今天的计数
            today_record["Count"] += 1
            # 添加新的时间记录
            if today_record["Time"]:
                today_record["Time"] += f" {current_time}"
            else:
                today_record["Time"] = current_time
        else:
            # 添加今天的新记录
            records.append({
                "Date": today,
                "Count": 1,
                "Time": current_time
            })
        
        # 写回CSV文件
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Date", "Count", "Time"])
            writer.writeheader()
            writer.writerows(records)

        # 生成HTML文件
        if generate_fish_record == "True":
            # 生成摸鱼记录
            today = datetime.datetime.now().date()
            week_start = today - datetime.timedelta(days=today.weekday())
            month_start = today.replace(day=1)
            
            # 统计各项数据
            today_count = 0 # 今日摸鱼次数
            morning_count = 0  # 今日上午摸鱼次数
            afternoon_count = 0  # 今日下午摸鱼次数
            week_count = 0  # 本周摸鱼次数
            month_count = 0 # 本月摸鱼次数
            total_count = 0 # 总摸鱼次数
            time_period = {i: 0 for i in range(24)}
            
            for record in records:
                record_date = datetime.datetime.strptime(record["Date"], "%Y-%m-%d").date()
                count = record["Count"]
                
                if record_date == today:
                    today_count = count
                    # 统计今天的上午/下午分布
                    if record["Time"]:
                        times = record["Time"].split()
                        for t in times:
                            hour = int(t.split(":")[0])
                            if hour < 12:
                                morning_count += 1
                            else:
                                afternoon_count += 1
                            
                if record_date >= week_start:
                    week_count += count
                if record_date >= month_start:
                    month_count += count
                total_count += count
                
                for time in record["Time"].split():
                    time_period[int(time.split(":")[0])] += 1
            max_time_period = max(time_period.items(), key=lambda x: x[1])
            
            time_period_sorted = sorted(time_period.items(), key=lambda x: x[1], reverse=False)
            
            period_ranking = {}
            for rank, (hour, count) in enumerate(time_period_sorted):
                period_ranking[hour] = "🐟" * (rank + 1)
            
            
            # 生成HTML内容
            html_content = f"""
            <html>
            <head>
                <meta charset="utf-8">
                <title>摸🐟统计</title>
                <style>
                    table {{
                        border-collapse: collapse;
                        width: 80%;
                        margin: 20px auto;
                    }}
                    th, td {{
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: center;
                    }}
                    th {{
                        background-color: #f2f2f2;
                    }}
                    h1 {{
                        text-align: center;
                    }}
                </style>
            </head>
            <body>
                <h1>摸🐟统计报告</h1>
                <table>
                    <tr>
                        <th>统计项目</th>
                        <th>次数</th>
                    </tr>
                    <tr>
                        <td>今日摸🐟次数</td>
                        <td>{today_count}</td>
                    </tr>
                    <tr>
                        <td>今日上午摸🐟次数</td>
                        <td>{morning_count}</td>
                    </tr>
                    <tr>
                        <td>今日下午摸🐟次数</td>
                        <td>{afternoon_count}</td>
                    </tr>
                    <tr>
                        <td>本周摸🐟次数</td>
                        <td>{week_count}</td>
                    </tr>
                    <tr>
                        <td>本月摸🐟次数</td>
                        <td>{month_count}</td>
                    </tr>
                    <tr>
                        <td>总摸🐟次数</td>
                        <td>{total_count}</td>
                    </tr>
                    <tr>
                        <td>最常摸🐟时段</td>
                        <td>{max_time_period[0]}:00-{max_time_period[0]}:59 ({max_time_period[1]}次)</td>
                    </tr>
                </table>
                
                <table>
                    <tr>
                        <th>时段</th>
                        <th>摸鱼时段排名</th>
                    </tr>
                    <tr>
                        <td>00:00-00:59</td>
                        <td style="text-align: left;">{period_ranking[0]}</td>
                    </tr>
                    <tr>
                        <td>01:00-01:59</td>
                        <td style="text-align: left;">{period_ranking[1]}</td>
                    </tr>
                    <tr>
                        <td>02:00-02:59</td>
                        <td style="text-align: left;">{period_ranking[2]}</td>
                    </tr>
                    <tr>
                        <td>03:00-03:59</td>
                        <td style="text-align: left;">{period_ranking[3]}</td>
                    </tr>
                    <tr>
                        <td>04:00-04:59</td>
                        <td style="text-align: left;">{period_ranking[4]}</td>
                    </tr>
                    <tr>
                        <td>05:00-05:59</td>
                        <td style="text-align: left;">{period_ranking[5]}</td>
                    </tr>
                    <tr>
                        <td>06:00-06:59</td>
                        <td style="text-align: left;">{period_ranking[6]}</td>
                    </tr>
                    <tr>
                        <td>07:00-07:59</td>
                        <td style="text-align: left;">{period_ranking[7]}</td>
                    </tr>
                    <tr>
                        <td>08:00-08:59</td>
                        <td style="text-align: left;">{period_ranking[8]}</td>
                    </tr>
                    <tr>
                        <td>09:00-09:59</td>
                        <td style="text-align: left;">{period_ranking[9]}</td>
                    </tr>
                    <tr>
                        <td>10:00-10:59</td>
                        <td style="text-align: left;">{period_ranking[10]}</td>
                    </tr>
                    <tr>
                        <td>11:00-11:59</td>
                        <td style="text-align: left;">{period_ranking[11]}</td>
                    </tr>
                    <tr>
                        <td>12:00-12:59</td>
                        <td style="text-align: left;">{period_ranking[12]}</td>
                    </tr>
                    <tr>
                        <td>13:00-13:59</td>
                        <td style="text-align: left;">{period_ranking[13]}</td>
                    </tr>
                    <tr>
                        <td>14:00-14:59</td>
                        <td style="text-align: left;">{period_ranking[14]}</td>
                    </tr>
                    <tr>
                        <td>15:00-15:59</td>
                        <td style="text-align: left;">{period_ranking[15]}</td>
                    </tr>
                    <tr>
                        <td>16:00-16:59</td>
                        <td style="text-align: left;">{period_ranking[16]}</td>
                    </tr>
                    <tr>
                        <td>17:00-17:59</td>
                        <td style="text-align: left;">{period_ranking[17]}</td>
                    </tr>
                    <tr>
                        <td>18:00-18:59</td>
                        <td style="text-align: left;">{period_ranking[18]}</td>
                    </tr>
                    <tr>
                        <td>19:00-19:59</td>
                        <td style="text-align: left;">{period_ranking[19]}</td>
                    </tr>
                    <tr>
                        <td>20:00-20:59</td>
                        <td style="text-align: left;">{period_ranking[20]}</td>
                    </tr>
                    <tr>
                        <td>21:00-21:59</td>
                        <td style="text-align: left;">{period_ranking[21]}</td>
                    </tr>
                    <tr>
                        <td>22:00-22:59</td>
                        <td style="text-align: left;">{period_ranking[22]}</td>
                    </tr>
                    <tr>
                        <td>23:00-23:59</td>
                        <td style="text-align: left;">{period_ranking[23]}</td>
                    </tr>
                </table>
                
                <p style="text-align: center;">统计时间: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </body>
            </html>
            """
            
            # 写入HTML文件
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(html_content)
