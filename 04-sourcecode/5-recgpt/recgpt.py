import os
import uuid
import yaml
import json
import urllib.parse
import requests
import logging
from langchain.agents.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.llms.openai import OpenAI

PREFIX = """RecGPT is designed to be able to assist with product recommend tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. RecGPT is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
RecGPT is able to process and understand human intent. As a language model, RecGPT can not give recommendation directly, but it has a list of tools to do recommend tasks. RecGPT can invoke different tools to meet human's intent, following the tool description.
Overall, RecGPT is a powerful and friendly recommend assistant tool that brings better experience to Human. 
TOOLS:
------

RecGPT  has access to the following tools:"""

FORMAT_INSTRUCTIONS = """To use a tool, please use the following format:
```
Thought: Do I need to use a tool? Yes
Action: the action to take, MUST should be one of [{tool_names}], DO NOT give extra words
Action Input: the input to the action, MUST axactly fit the input format and DO NOT give extra words
Observation: the result of the action
```
When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:
```
Thought: Do I need to use a tool? No
{ai_prefix}: [your response here]
```
If the tool gives you a list of products in json format, you should reorganize the information to a table.
In the table, each row contains one product and columns include index, product id, title, price, discount, store id and url.
When the tool fails to execute or return an invalid value, you should apologize to the Human.
"""

SUFFIX = """Let's Begin!
Previous conversation history:
{chat_history}
New input: {input}
Since RecGPT is a text language model, RecGPT must use tools to recommend products for Human.
The thoughts and observations are only visible for RecGPT, RecGPT should remember to repeat important information in the final response for Human. 
Thought: Do I need to use a tool? {agent_scratchpad} Let's think step by step.
"""

config = yaml.load(open('config.yaml'), Loader=yaml.FullLoader)
os.environ['OPENAI_API_KEY'] = config['openai_api_key']
proxy=config["proxy"]

def use_proxy(f):
    def wrap(*args, **kwargs):
        os.environ['http_proxy'] = proxy
        os.environ['https_proxy'] = proxy
        r = f(*args, **kwargs)
        os.environ.pop('http_proxy')
        os.environ.pop('https_proxy')
        return r
    return wrap


def ignore_proxy(f):
    def wrap(*args, **kwargs):
        if 'http_proxy' in os.environ and 'https_proxy' in os.environ:
            http_proxy = os.environ.pop('http_proxy')
            https_proxy = os.environ.pop('https_proxy')
            r = f(*args, **kwargs)
            os.environ['http_proxy'] = http_proxy
            os.environ['https_proxy'] = https_proxy
            return r
        else:
            return f(*args, **kwargs)
    return wrap


class BaseTool:
    def __init__(self, user_id, stream_id) -> None:
        self.stream_id = stream_id
        self.user_id = user_id

    def get_summary(self, rec_ids, max_num=5):
        rec_ids = rec_ids[:max_num]
        url = config['summary_url'].format(product_ids=','.join(rec_ids))
        res = self.url_get(url)
        item_list = json.loads(res)['summaryResponse']['summaryItemList']
        results = []
        for item in item_list.values():
            r = {
                    'product_id': item['productId'],
                    'title': item['fieldValueMap']['subject'],
                    'original_price': str(item['productPrice']['prices']['original_price']['minPrice']['cent']/100)+'USD',
                    'min_price': str(item['productPrice']['prices']['final_sale_price']['minPrice']['cent']/100)+'USD',
                    'discount': str(item['productPrice']['prices']['final_sale_price'].get('minPriceDiscount',0)),
                    'image': 'https://ae04.alicdn.com/kf/'+item['fieldValueMap']['image_names'].split(',')[0],
                    'store_id': item['fieldValueMap']['store_id'],
                    'url': f'https://www.aliexpress.com/item/{item["productId"]}.html'
                 }
            results.append(r)
        return results

    def get_rec_ids(self, url):
        res = self.url_get(url)
        return [str(x['itemId']) for x in json.loads(res)['result']]

    def get_rec_results(self, url):
        rec_ids = self.get_rec_ids(url)
        return self.get_summary(rec_ids)

    @ignore_proxy
    def url_get(self, url):
        logging.warning("get " + url)
        res = requests.get(url)
        return res.text

    def as_langchain_tool(self):
        return Tool(name=self.name, description=self.description, func=self.func)


class RecTool(BaseTool):
    name = "ProductRecommendTool"
    description = ("Useful when you want the system recommend some products for you. "
                  "No input needed for this tool. "
                  "The result is a list of products in json format.")
    def func(self, inputs):
        url = config['rec_url'].format(stream_id=self.stream_id, user_id=self.user_id)
        return self.get_rec_results(url)


class SimRecTool(BaseTool):
    name = "SimilarProductRecommendTool"
    description = ("Useful when you want the system recommend some products for you, thoese recommended products are similar to a product you provide. "
                  "One input is needed for this tool: a string of number, which represents the product id. "
                  "The result is a list of products in json format.")
    def func(self, inputs):
        product_id = inputs
        url = config['sim_rec_url'].format(stream_id=self.stream_id, user_id=self.user_id, product_id=product_id)
        return self.get_rec_results(url)


class StoreRecTool(BaseTool):
    name = "StoreProductRecommendTool"
    description = ("Useful when you want the system recommend some products for you, thoese recommended products are from a store you provide. "
                  "One input is needed for this tool: a string of number, which represents the store id. "
                  "The result is a list of products in json format.")
    def func(self, inputs):
        store_id = inputs
        url = config['store_rec_url'].format(stream_id=self.stream_id, user_id=self.user_id, store_id=store_id)
        return self.get_rec_results(url)


class SearchTool(BaseTool):
    name = "ProductSearchTool"
    description = ("Useful for search some products related to a query. "
                  "One input is needed for this tool: a string, which represents the query words. "
                  "The result is a list of products in json format.")
    def func(self, inputs):
        query = urllib.parse.quote(inputs, safe='/:?=&')
        url = config['search_url'].format(stream_id=self.stream_id, user_id=self.user_id, query=query)
        return self.get_search_results(url)

    def get_search_ids(self, url):
        res = self.url_get(url)
        return [str(x['productId']) for x in json.loads(res)['mods']['itemList']['content']]

    def get_search_results(self, url):
        rec_ids = self.get_search_ids(url)
        return self.get_summary(rec_ids)


class ChatBot:
    def __init__(self) -> None:
        self.stream_id = str(uuid.uuid1())
        self.user_id = config['user_id']
        self.tools = [
                        RecTool(self.user_id, self.stream_id).as_langchain_tool(),
                        SimRecTool(self.user_id, self.stream_id).as_langchain_tool(),
                        StoreRecTool(self.user_id, self.stream_id).as_langchain_tool(),
                        SearchTool(self.user_id, self.stream_id).as_langchain_tool()
                    ]
        self.llm = OpenAI(temperature=0.9, max_tokens=512)
        self.memory = ConversationBufferWindowMemory(memory_key="chat_history", output_key='output', k=5)
        self.agent = self.init_agtent()

    def init_agtent(self):
        return initialize_agent(
            tools=self.tools, 
            llm=self.llm, 
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, 
            memory=self.memory,
            agent_kwargs={'prefix': PREFIX, 'format_instructions': FORMAT_INSTRUCTIONS,
                          'suffix': SUFFIX},
            verbose=True
        )

    @use_proxy
    def run(self, text):
        res = self.agent({"input": text})
        return res


if __name__ == '__main__':
    import gradio as gr

    agent = ChatBot()

    with gr.Blocks() as demo:
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        send = gr.Button("Send")
        clear = gr.Button("Clear")

        def respond(message, chat_history):
            output = agent.run(message)['output']
            chat_history.append((message, output))
            return "", chat_history
        
        def clear_memory():
            agent.memory.clear()
            return None

        msg.submit(respond, [msg, chatbot], [msg, chatbot])
        send.click(respond, [msg, chatbot], [msg, chatbot])
        clear.click(clear_memory, None, chatbot, queue=False)

    demo.launch()
