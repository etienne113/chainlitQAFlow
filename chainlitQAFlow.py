from chainlit.input_widget import Select
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
import chainlit as cl
import os
import pinecone
import openai
from langchain.vectorstores.base import VectorStoreRetriever

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
openai.api_key = os.getenv('OPENAI_API_KEY')

load_dotenv()
os.environ["PINECONE_API_KEY"] = os.getenv('PINECONE_API_KEY')
os.environ["PINECONE_ENV"] = os.getenv('PINECONE_ENV')
embeddings = OpenAIEmbeddings()

welcome_message = """ Welcome to the Chainlit PDF QA demo! To get started:
  1. Upload one or more PDF or text files \n
  2. Ask questions about the files
  """


def sort_strings_alphabetically(input_list):
    sorted_list = sorted(input_list)
    return sorted_list


def get_doc_from_pinecone():
    pinecone.init(
        api_key=os.getenv("PINECONE_API_KEY"),
        environment=os.getenv("PINECONE_ENV"),
    )
    index_name = "test5"
    docsearch = Pinecone.from_existing_index(index_name=index_name, embedding=embeddings)

    return docsearch


@cl.on_chat_start
async def start():
    await cl.Message(content="Welcome to this space, you can use this to chat with your PDFs and text files").send()
    docsearch = await cl.make_async(get_doc_from_pinecone)()

    input_list = ["Software engineering", "DevOps", "Project management", "Data management", "Personal management"]
    departments_list = sort_strings_alphabetically(input_list=input_list)
    settings = await cl.ChatSettings(
        [
            Select(
                id="departments",
                label="Please select your department: ",
                values=["none"] + departments_list,
                initial_index=0,
            )
        ]
    ).send()
    value = settings["departments"]
    retrieverdb = docsearch.as_retriever()
    retrieverdb.search_type = "similarity"
    cl.user_session.set("retriever", retrieverdb)
    metadataFilter = {"departments": value}

    cl.user_session.set("filter", metadataFilter)


@cl.on_settings_update
async def handle_update(settings):
    selected_option = settings['departments']
    metadataFilter = {"departments": selected_option}
    retriever = cl.user_session.get("retriever")  # type: VectorStoreRetriever
    retriever.search_kwargs = {'k': 10, 'filter': metadataFilter}
    cl.user_session.set("filter", metadataFilter)


@cl.on_message
async def main(message):
    metadataFilter = cl.user_session.get("filter")
    retriever = cl.user_session.get("retriever")  # type: VectorStoreRetriever
    retriever.search_kwargs = {'k': 10, 'filter': metadataFilter}
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        ChatOpenAI(temperature=1, streaming=True),
        chain_type="stuff",  # from a small amount of docs  and "refine" for a larger number of docs
        retriever=retriever
    )

    res = await chain.acall(message)

    answer = res["answer"]
    await cl.Message(content=answer).send()
