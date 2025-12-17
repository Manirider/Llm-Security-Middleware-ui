from flask import Flask, request, jsonify
from llm_guard.middleware import LLMGuard

app = Flask(__name__)

# Choose security policy: "strict" or "balanced"
guard = LLMGuard(policy="balanced")


def fake_llm(prompt: str) -> str:
    """
    Mock LLM function (replace with real LLM API call)
    """
    return f"LLM Response: {prompt}"


@app.route("/chat", methods=["POST"])
def chat():
    """
    Secure chat endpoint protected by LLMGuard
    """
    data = request.get_json()

    if not data or "prompt" not in data:
        return jsonify({"error": "Prompt is required"}), 400

    prompt = data["prompt"]
    context = data.get("context")

    try:
        # 🔐 Secure input
        safe_prompt = guard.process_input(prompt, context=context)

        # 🤖 Call LLM
        raw_response = fake_llm(safe_prompt)

        # 🔐 Secure output
        safe_response = guard.process_output(raw_response)

        return jsonify({
            "status": "success",
            "response": safe_response
        })

    except ValueError as e:
        return jsonify({
            "status": "blocked",
            "reason": str(e)
        }), 403


if __name__ == "__main__":
    app.run(debug=True)
