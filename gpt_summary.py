from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# 環境変数からOpenAI APIキーを取得
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    memo_text = data.get('memo', '')

    if not memo_text:
        return jsonify({"error": "memo is required"}), 400

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "あなたはビジネスライターです。社員の日報を、与えられたキーワードや短文をもとに、自然な日本語に整えてください。簡潔に100〜200文字程度でまとめてください。"},
            {"role": "user", "content": memo_text}
        ]
    )

    summary = response.choices[0].message.content
    return jsonify({"summary": summary})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

