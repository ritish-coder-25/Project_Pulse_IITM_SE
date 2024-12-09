from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
from flask import current_app
import os, json
from datetime import datetime
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.document_loaders import TextLoader


load_dotenv()

os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.environ.get("LANGCHAIN_API_KEY")


# llm = ChatGroq(
#     model="mixtral-8x7b-32768",
#     temperature=0.5,
#     max_retries=3,
#     # other params...
# )

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # api_key="...",  # if you prefer to pass api key in directly instaed of using env vars
    # base_url="...",
    # organization="...",
    # other params...
)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = InMemoryVectorStore(embeddings)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # chunk size (characters)
    chunk_overlap=200,  # chunk overlap (characters)
    add_start_index=True,  # track index in original document
)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def invoke_vectorstore_and_chain(docs):
    all_splits = text_splitter.split_documents(docs)
    document_ids = vector_store.add_documents(documents=all_splits)
    print(document_ids)
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 1, "fetch_k": 2, "lambda_mult": 0.5},
    )
    prompt = hub.pull("rlm/rag-prompt")
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    output = rag_chain.invoke(
        "You are a teacher with expertise in grading documentation. Your task is to assess the provided document, summarize its key points, and provide constructive feedback. Ensure your summary highlights the document's purpose, structure, and any notable strengths or weaknesses."
    )
    return output


def summarize_files(filenames):
    output_str = []
    for file in filenames:
        if file.endswith(".pdf"):

            loader = PyPDFLoader(file)
            docs = loader.load()
            print(docs[0].metadata)
            # content = format_docs(docs)
            output = invoke_vectorstore_and_chain(docs)
            output_str.append(output)
        else:
            loader = TextLoader(file)
            docs = loader.load()
            # content = format_docs(docs)
            output = invoke_vectorstore_and_chain(docs)
            output_str.append(output)
    return output_str


chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful code review assistant. Review the following code changes based on the following criteria:\n"
            "1. **Code Clarity (score 1-5)**: Is the code easy to read and understand? Are variable names, function names, and overall structure clear?\n"
            "2. **Functionality (score 1-5)**: Does the code achieve the intended functionality as described in the changes?\n"
            "3. **Efficiency (score 1-5)**: Is the code optimized for performance, and are there any areas where efficiency can be improved?\n"
            "4. **Maintainability (score 1-5)**: Is the code structured in a way that future modifications will be straightforward? Are there any potential issues that could hinder maintenance?\n"
            "5. **Documentation (score 1-5)**: Does the code include necessary comments, and is the logic explained adequately for other developers?\n"
            "After scoring, provide a brief overall review summarizing the strengths, any weaknesses, and any suggested improvements for each category. Additionally, give an overall summary of the code changes and their impact on the project.",
        ),
        (
            "human",
            "Based on the criteria provided, please provide a score for each category (1-5) and a brief review for each category. "
            "Afterward, summarize the overall strengths, weaknesses, and suggested improvements for the code changes."
            "Return a JSON object."
            "Here are the code changes I made: {changes}",
        ),
    ]
)

summary_chain = LLMChain(prompt=chat_prompt_template, llm=llm)


def summarize_code_changes(changes):
    chat_prompt = chat_prompt_template.invoke({"changes": changes})
    summary = summary_chain.run(chat_prompt)
    return summary


def load_changes_from_json(filename="commit_changes.json"):
    try:
        # Open the file and read the contents as a string
        with open(filename, "r") as json_file:
            # Read the contents of the file into a string
            file_contents = json_file.read()

            # Parse the string as JSON
            data = json.loads(file_contents)
        return data
    except Exception as e:
        print(f"Error loading data from JSON: {e}")
        return None


if __name__ == "__main__":
    # team_id = "Project_Pulse_IITM_SE"

    # with open("reports/Project_Pulse_IITM_SE_2024-11-10_17_output.json", "r") as file:
    #     changes_All = json.loads(file.read())

    # print(changes_All.keys())

    # changes = changes_All["Marmik Thaker"]["commit_details"][0]["file_changes"][0][
    #     "code_changes"
    # ]  # Limit to 1000 characters for testing(Getting error for more than 1000 characters)

    # def clean_code(code):
    #     # Remove leading/trailing whitespace and extra newlines
    #     cleaned_code = code.strip()
    #     # Replace multiple spaces with a single space
    #     cleaned_code = " ".join(cleaned_code.split())
    #     return cleaned_code

    # changes = clean_code(changes)  # Limit to 1000 characters for testing
    # result = summarize_code_changes(changes)
    # print(result)
    # with open(
    #     f"reports/{team_id}_{datetime.now().strftime('%Y-%m-%d_%H')}_summary.json", "w"
    # ) as file:
    #     file.write(json.dumps(result, indent=4))

    filenames = ["./uploads/dummy.txt", "./uploads/sample.pdf"]

    out = summarize_files(filenames)

    print(out)
