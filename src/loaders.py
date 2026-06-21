from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


#------------------------------
#Load Documents ( knowledge Base )
#--------------------------
def load_documents(path="Data/Knowledge_base"):
    """
    Load all txt files from the knowledge base.
    """

    knowledge_base_path = Path(path)

    documents = []

    for file in knowledge_base_path.glob("*.txt"):
        loader = TextLoader(str(file), encoding="utf-8")
        docs = loader.load()
        documents.extend(docs)
    return documents

#--------------
# Chunk Documents
def chunk_documents(documents, chunk_size=500, chunk_overlap=100):
    """
    Split documents into chunks.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    return splitter.split_documents(documents)