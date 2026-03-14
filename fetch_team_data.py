import requests
import pandas as pd
import os

# ==========================================================================
# 1. 基础设置与目录准备
# ==========================================================================
# 作用目的：动态获取当前脚本所在的目录，彻底废除 D 盘硬编码路径，适配云端 Linux 环境。
current_dir = os.path.dirname(os.path.abspath(__file__))

# 作用目的：定义最终生成的 CSV 文件名和完整路径（直接保存在脚本同级目录）
file_path = os.path.join(current_dir, "nba_30teams_data_2025_26.csv")

# ==========================================================================
# 2. 发送网络请求获取数据
# ==========================================================================
# 作用目的：抓取本赛季 30 支球队各项汇总数据的 API 接口
url = "https://api.pbpstats.com/get-totals/nba?Season=2025-26&SeasonType=Regular%2BSeason&StartType=All&Type=Team"

# 作用目的：模拟浏览器请求头，防止被服务器反爬机制拦截
headers = {'User-Agent': 'Mozilla/5.0'}

print("正在向 PBPStats 发送数据请求...")
# 作用目的：发送 GET 请求，设置 60 秒超时防止程序死锁
try:
    response = requests.get(url, headers=headers, timeout=60)

    # ==========================================================================
    # 3. 解析数据并导出
    # ==========================================================================
    # 作用目的：检查响应状态码，200 为正常响应
    if response.status_code == 200:
        json_data = response.json()
        
        # 作用目的：提取包含 30 支球队数据的核心列表
        teams_data = json_data.get("multi_row_table_data", [])
        
        if len(teams_data) > 0:
            # 作用目的：将列表转为 Pandas 数据框并保存为 CSV，不保存行索引，使用 utf-8-sig 防止中文乱码
            df = pd.DataFrame(teams_data)
            df.to_csv(file_path, index=False, encoding='utf-8-sig')
            print(f"抓取成功！共获取 {len(df)} 支球队的数据。")
            print(f"文件已保存至: {file_path}")
        else:
            print("解析失败：未能从返回的 JSON 中提取到 'multi_row_table_data' 节点。")
    else:
        print(f"请求失败：HTTP 状态码 {response.status_code}")
except Exception as e:
    print(f"发生网络请求错误: {e}")