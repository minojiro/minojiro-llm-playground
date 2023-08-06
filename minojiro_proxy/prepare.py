import shared

collection = shared.get_chroma_collection()

with open("minojiro_info.txt") as f:
    for i, text in enumerate(f):
        if not text:
            continue
        # Vectorize the prepared information (Embedding)
        print(f"line: {i + 1}")
        embeddings = shared.get_embeddings(text)

        # store it in ChromaDB
        collection.add(
            ids=[f'id_{i}'],
            embeddings=embeddings,
            metadatas={"text": text},
        )

print("done!")
