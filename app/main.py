from app.rag import generate_answer


def main():
    query = input("Ask a question: ")
    answer = generate_answer(query)
    print("\nAnswer:\n")
    print(answer)


if __name__ == "__main__":
    main()
