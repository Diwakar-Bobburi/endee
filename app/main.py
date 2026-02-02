from rag import generate_answer


def main():
    print("=" * 60)
    print("📄 RAG-based Document Question Answering System")
    print("🧠 Vector DB: Endee (Endee-style local store)")
    print("=" * 60)

    while True:
        question = input("\nAsk a question (or type 'exit' to quit): ")

        if question.lower() in ["exit", "quit"]:
            print("\n👋 Exiting application. Goodbye!")
            break

        answer = generate_answer(question)

        print("\n💡 Answer:\n")
        print(answer)
        print("\n" + "-" * 60)


if __name__ == "__main__":
    main()
