import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

st.title('数据类岗位招聘市场分析')
st.write('数据来源：BOSS直聘 | 分析工具：Python · Pandas · Streamlit')

# 读取数据
df = pd.read_excel('data/BOSS_Zhipin_Sample_Data.xlsx')
keywords = ['数据', 'Python', 'python', '大数据', '数据分析', '数据开发']
exclude_keywords = ['标注', '训练师', '文员', '采集']
mask = df['职位名称'].str.contains('|'.join(keywords), na=False)
df_target = df[mask]
mask2 = ~df_target['职位名称'].str.contains('|'.join(exclude_keywords), na=False)
df_tech = df_target[mask2].copy()

# 侧边栏筛选
st.sidebar.header('筛选条件')
exp_options = ['全部'] + df_tech['经验要求'].dropna().unique().tolist()
selected_exp = st.sidebar.selectbox('经验要求', exp_options)

if selected_exp != '全部':
    df_tech = df_tech[df_tech['经验要求'] == selected_exp]

# 计算薪资均值（放在筛选之后）
import re
def parse_salary(s):
    s = s.split('·')[0]
    nums = re.findall(r'\d+', s)
    if len(nums) == 2:
        return (int(nums[0]) + int(nums[1])) / 2
    return None

df_tech['薪资_均值K'] = df_tech['薪资'].apply(parse_salary)
df_tech_clean = df_tech[df_tech['薪资_均值K'] < 200].copy()


# 学历分布饼图
st.subheader('学历要求分布')
edu_counts = df_tech['学历要求'].value_counts()
fig, ax = plt.subplots(figsize=(8, 6))
ax.pie(edu_counts, labels=edu_counts.index, autopct='%1.1f%%', startangle=90)
ax.set_title('数据类岗位学历要求分布')
st.pyplot(fig)

st.subheader('经验要求分布')
exp_counts = df_tech['经验要求'].value_counts()
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.bar(exp_counts.index, exp_counts.values, color='coral')
ax2.set_title('数据类岗位经验要求分布')
ax2.set_xlabel('经验要求')
ax2.set_ylabel('岗位数量')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig2)

# 薪资处理
import re
def parse_salary(s):
    s = s.split('·')[0]
    nums = re.findall(r'\d+', s)
    if len(nums) == 2:
        return (int(nums[0]) + int(nums[1])) / 2
    return None

df_tech['薪资_均值K'] = df_tech['薪资'].apply(parse_salary)
df_tech_clean = df_tech[df_tech['薪资_均值K'] < 200].copy()

# 薪资分布
st.subheader('薪资分布')
salary_counts = df_tech_clean['薪资'].value_counts().head(12)
fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.bar(salary_counts.index, salary_counts.values, color='steelblue')
ax3.set_title('数据类岗位薪资分布')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig3)

# 技能需求
st.subheader('技能需求频率')
skill_keywords = ['Python','SQL','MySQL','Hive','Hadoop','Spark',
                  'pandas','Excel','Tableau','ETL','Kafka','Flink',
                  '数据仓库','数据清洗','数据可视化','Linux']
skill_counts = {s: df_tech_clean['职位描述'].str.contains(s, case=False, na=False).sum()
                for s in skill_keywords}
skill_series = pd.Series(skill_counts).sort_values(ascending=False)
fig4, ax4 = plt.subplots(figsize=(12, 6))
ax4.bar(skill_series.index, skill_series.values, color='steelblue')
ax4.set_title('技能需求频率')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig4)
#
# # 词云
# import jieba
# from wordcloud import WordCloud
# stopwords = set(['的','和','与','等','及','或','对','在','中','有',
#                  '为','以','并','能','是','不','了','也','都','将',
#                  '负责','进行','相关','具有','具备','良好','优先','以上',
#                  '工作','能力','要求','岗位','职责','任职','参与','提供',
#                  '完成','管理','公司','团队','业务','技术','产品','系统',
#                  '开发','熟悉','了解','掌握','经验','年','者','如','可'])
# all_text = ' '.join(df_tech_clean['职位描述'].dropna().tolist())
# words_filtered = [w for w in jieba.cut(all_text) if w not in stopwords and len(w) > 1]
# wc = WordCloud(font_path='C:/Windows/Fonts/simhei.ttf',
#                width=800, height=400, background_color='white',
#                max_words=80).generate(' '.join(words_filtered))
# st.subheader('核心技能词云')
# fig5, ax5 = plt.subplots(figsize=(12, 6))
# ax5.imshow(wc, interpolation='bilinear')
# ax5.axis('off')
# st.pyplot(fig5)

