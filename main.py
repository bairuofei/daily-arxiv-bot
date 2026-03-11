
import arxiv
import google.generativeai as genai
import os
import sys

def main():
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Error: GEMINI_API_KEY not found.")
            sys.exit(1)
            
        genai.configure(api_key=api_key)
        
        # 2026 年推荐使用 gemini-3-flash 或 gemini-2.0-flash
        # 如果依然报错 404，可以将下面的字符串改为 'gemini-2.0-flash'
        model = genai.GenerativeModel('gemini-3-flash')

        print("Fetching papers from arXiv...")
        client = arxiv.Client()
        search = arxiv.Search(query="cs.AI", max_results=5, sort_by=arxiv.SortCriterion.SubmittedDate)
        results = list(client.results(search))
        
        if not results:
            print("No papers found.")
            return

        content = "今日 arXiv AI 论文摘要：\n\n"
        for p in results:
            content += f"标题: {p.title}\n摘要: {p.summary}\n链接: {p.entry_id}\n\n"

        print("Generating summary with Gemini...")
        prompt = f"你是一个学术助手，请将以下论文摘要总结成一份中文简报，包含趋势分析和重点推荐：\n\n{content}"
        
        # 生成内容
        response = model.generate_content(prompt)
        
        with open("summary.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Success! Summary saved.")

    except Exception as e:
        print(f"Runtime Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
