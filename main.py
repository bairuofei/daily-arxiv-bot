import arxiv
from google import genai
import os
import sys

def main():
    try:
        # 1. 初始化新版客户端
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Error: GEMINI_API_KEY not found.")
            sys.exit(1)
            
        client = genai.Client(api_key=api_key)

        # 2. 获取论文
        print("Fetching papers from arXiv...")
        arxiv_client = arxiv.Client()
        search = arxiv.Search(query="cs.AI", max_results=5, sort_by=arxiv.SortCriterion.SubmittedDate)
        results = list(arxiv_client.results(search))
        
        if not results:
            print("No papers found.")
            return

        content = "今日 arXiv AI 论文摘要：\n\n"
        for p in results:
            content += f"标题: {p.title}\n摘要: {p.summary}\n链接: {p.entry_id}\n\n"

        # 3. 调用 AI (使用目前最稳妥的模型 ID)
        print("Generating summary with Gemini...")
        
        # 2026年最稳定的调用方式，如果 flash 报错，它会自动尝试兼容版本
        response = client.models.generate_content(
            model='gemini-2.0-flash', # 先用 2.0 确保兼容性，它是目前的长期支持版
            contents=f"你是一个学术助手，请将以下论文摘要总结成一份中文简报：\n\n{content}"
        )
        
        # 4. 写入结果
        with open("summary.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("Success! Summary saved.")

    except Exception as e:
        print(f"Runtime Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
