# 招聘市场数据分析

## 项目简介
基于BOSS直聘10万+条招聘数据，分析数据类岗位的学历、薪资、经验及技能需求分布，为求职决策提供数据支撑。

## 技术栈
- Python、Pandas、Matplotlib
- MySQL、Streamlit

## 项目功能
- 筛选清洗数据类相关岗位
- 学历、薪资、经验要求多维度分析
- 技能需求频率统计
- Streamlit交互式仪表盘，支持按经验要求动态筛选

## 运行方式
```bash
# 安装依赖
pip install pandas matplotlib streamlit pymysql wordcloud jieba

# 运行仪表盘
streamlit run dashboard.py
```

## 数据来源
BOSS直聘公开招聘数据
