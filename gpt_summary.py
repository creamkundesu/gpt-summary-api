from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# 環境変数からOpenAI APIキーを取得
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/summary", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        memo_text = data.get("memo", "")

        if not memo_text:
            return jsonify({"error": "No memo provided."}), 400

        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたはビジネスライターです。社員の日報を自然な日本語に整えて、100〜200文字で簡潔にまとめてください。"},
                {"role": "user", "content": memo_text}
            ]
        )
        summary = response['choices'][0]['message']['content']
        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render用にポートを環境変数から取る
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
