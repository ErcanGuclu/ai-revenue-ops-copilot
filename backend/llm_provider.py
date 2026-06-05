from google import genai

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    LLM_PROVIDER,
    OPENAI_API_KEY,
    OPENAI_MODEL,
)


def generate_text(prompt: str) -> str:
    if LLM_PROVIDER == "gemini":
        return _generate_text_with_gemini(prompt)

    if LLM_PROVIDER == "openai":
        return _generate_text_with_openai(prompt)

    raise ValueError(
        f"Desteklenmeyen LLM_PROVIDER değeri: {LLM_PROVIDER}. "
        "Desteklenen değerler: gemini, openai"
    )


def _generate_text_with_gemini(prompt: str) -> str:
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY bulunamadı. Proje ana klasöründe .env dosyası oluştur "
            "ve GEMINI_API_KEY değerini ekle."
        )

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    return response.text


def _generate_text_with_openai(prompt: str) -> str:
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY bulunamadı. OpenAI kullanmak için .env dosyasına "
            "OPENAI_API_KEY eklenmeli."
        )

    raise NotImplementedError(
        "OpenAI provider altyapısı config seviyesinde ayrıldı, "
        "ancak aktif entegrasyon bu sprintte Gemini ile yapılacaktır."
    )


def main() -> None:
    prompt = (
        "Write a short executive summary for a B2B revenue operations report. "
        "Keep it concise and business-oriented."
    )

    result = generate_text(prompt)
    print(result)


if __name__ == "__main__":
    main()