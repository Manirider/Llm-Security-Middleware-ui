from setuptools import setup, find_packages

setup(
    name="llm-security-middleware",
    version="1.0.0",
    description=(
        "Reusable security middleware for protecting LLM applications "
        "from prompt injection, jailbreaking, and adversarial attacks"
    ),
    author="Manikanta Suryasai",
    author_email="your-email@example.com",
    packages=find_packages(),
    install_requires=[
        "flask",
        "regex",
        "python-dotenv",
        "pydantic"
    ],
    python_requires=">=3.10",
)
