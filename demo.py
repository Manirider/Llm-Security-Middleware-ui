from llm_guard.middleware import LLMGuard

guard = LLMGuard(policy="strict")
print(guard.process_input("Hello world"))
