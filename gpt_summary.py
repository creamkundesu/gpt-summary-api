from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# OpenAI APIキーを環境変数から取得
client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

@app.route("/summary", methods=["POST"])
def summarize():
    try:
        data = request.get_json()
        memo_text = data.get("memo", "")

        if not memo_text:
            return jsonify({"error": "No memo provided."}), 400

        # OpenAI APIにリクエスト（v1.0.0 以降用）
        response = client.chat.completions.create(
            model="gpt-4o",  # 最新の高性能モデル
            messages=[
                {"role": "system", "content": "あなたはビジネスライターです。社員の日報を自然な日本語に整えて、100〜200文字で簡潔にまとめてください。"},
                {"role": "user", "content": memo_text}
            ]
        )

        # 結果の取り出し
        summary = response.choices[0].message.content
        return jsonify({"summary": summary})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # RenderではPORTが自動割り当てだから環境変数PORTを使う
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
