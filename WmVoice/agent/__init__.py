from .openaiagent import OpenAIAgent
from WmVoice.constants import COMMA_SEPARATOR, INTENTS


intentClassifierAgent = OpenAIAgent(
    f"Classify the following statement in one of these intents : [{COMMA_SEPARATOR.join(INTENTS)}]",
    agent_name='intentClassifierAgent',
    read_only=True
)

ingredientsSearchAgent = OpenAIAgent(
    "Return ingredients for this dish",
    agent_name='ingredientsSearchAgent',
    read_only=False
)

parsingAgent = OpenAIAgent(
    "Convert this input into a list of ingredients names. Response should be in python list format",
    agent_name='ingredientsSearchAgent',
    read_only=True
)

detailsAgent = OpenAIAgent(
    "You are a walmart buying helper, search walmart's website about the product I mention and tell me a brief summary about that product using product description, also tell me the user sentiments based on its reviews",
    agent_name='detailsAgent',
    read_only=False
)

greetingsAgent = OpenAIAgent(
    "You are a walmart customer service representative",
    agent_name='greetingsAgent',
    read_only=True
)


faqAgent = OpenAIAgent(
    "You are a walmart bot, answer the queries based on Walmarts FAQs and any other info provided by walmart in public domain",
    agent_name='faqAgent',
    read_only=False
)


returnAgent = OpenAIAgent(
    "Identify the product I am talking about from a list of products given. If product is found, reply with only it's name else reply with only -1",
    agent_name='returnAgent',
    read_only=False
)

selfPickupAgent = OpenAIAgent(
    "You are an agent which will ask user to give input date, time and place a schedule a self pickup for the user",
    agent_name='selfPickupAgent',
    read_only=False
)
