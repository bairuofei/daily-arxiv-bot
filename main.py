import arxiv
import google.generativeai as genai
import os

# 从刚才设置的 GitHub Secrets 中读取 Key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def get_papers():
    client = arxiv.Client()
    # 搜索 AI 领域的最新 5 篇论文
    search = arxiv.Search(query="cs.AI", max_results=5, sort_by=arxiv.SortCriterion.SubmittedDate)
    results = list(client.results(search))
    
    content = "今日 arXiv AI 论文摘要：\n\n"
    for p in results:
        content += f"标题: {p.title}\n摘要: {p.summary}\n链接: {p.entry_id}\n\n"
    return content

def main():
    papers_text = get_papers()
    prompt = f"你是一个学术助手，请将以下论文摘要总结成一份中文简报，包含趋势分析和重点论文推荐：\n\n{papers_text}"
    
    response = model.generate_content(prompt)
    
    # 将结果写进一个文件，方便后续 Actions 读取并存入 README
    with open("summary.txt", "w", encoding="utf-8") as f:
        f.write(response.text)

if __name__ == "__main__":
    main()
