from django.http import JsonResponse
from django.views import View
from django.utils import timezone

from WmVoice.agent.openaiagent import OpenAIAgent
from WmVoice.agent import *

from WmVoice.constants import INGREDIENTS
from WmVoice.models import Item, ItemOrder, User

activeAgent = None


def getUser(request):
    try:
        return User.objects.get(id=request.session.get('user_id'))
    except Exception:
        return None


class ReceiveTranscriptView(View):

    def handleIngredientsResponse(self, response):

        # response has user friendly ingredients list
        # parsedResponse has list in python list format
        parsedResponse = parsingAgent.call(response)

        list_start_index = parsedResponse.find('[')
        list_end_index = parsedResponse.find(']')

        parsedResponse = parsedResponse[list_start_index+1:list_end_index]

        extras = {
            "mode": "Ingredients",
            "ingredients": parsedResponse,
        }

        return response, extras

    def handleAgentResponse(self, activeAgent, agentResponse):
        if '?' in agentResponse:
            # agent has not given final response, dont do anything
            return agentResponse, None

        if activeAgent.agent_name == 'ingredientsSearchAgent':
            return self.handleIngredientsResponse(agentResponse)

        else:
            return agentResponse, None

    def post(self, request):
        global activeAgent

        data = request.POST
        userInput = data.get('userInput')
        resetFlag = data.get('reset')
        inputExtras = data.get('inputExtras')
        extras = None

        user = getUser(request)

        if resetFlag.lower() == 'true' or activeAgent is None:
            # Classify Intent
            intentAgentResponse = intentClassifierAgent.call(userInput)
            activeAgent = None

            if 'ingredient' in intentAgentResponse.lower():
                activeAgent = ingredientsSearchAgent
                agentResponse = activeAgent.call(userInput)
                agentResponse, extras = self.handleAgentResponse(
                    activeAgent, agentResponse)

            elif 'return' in intentAgentResponse.lower():
                user = getUser(request)
                if user == None:
                    agentResponse = "Please login before returning an order"
                else:
                    returnableOrders = user.choice_ordered_items.filter(
                        return_valid_till__gte=timezone.now())
                    if len(returnableOrders) == 0:
                        agentResponse = "Sorry, I couldn't find any returnable order in your account"
                    else:
                        activeAgent = returnAgent
                        returnAgentInput = f"{userInput}\nOrders List: [{','.join([order.item.name for order in returnableOrders])}]"
                        agentResponse = activeAgent.call(returnAgentInput)
                        if "-1" in agentResponse:
                            agentResponse = "I could not find the item. Please try again?"
                        else:
                            extras = {
                                "mode": "Return",
                                "item_name": agentResponse,
                            }
                            agentResponse += " - Is this the item you want to return? Please reply with Yes or No"

            elif 'replace' in intentAgentResponse.lower():
                agentResponse = intentAgentResponse

            elif 'tell me more' in intentAgentResponse.lower():
                item_id = data.get('item_id')
                if item_id == None:
                    agentResponse = "I don't see any opened item here in the current browser page"
                else:
                    item = Item.objects.get(id=item_id)
                    activeAgent = detailsAgent
                    agent_input_text = f"Brief the item quality based on following user reviews : {item.getReviewsInLinedStrings()}"
                    agentResponse = activeAgent.call(agent_input_text)
                    agentResponse, extras = self.handleAgentResponse(
                        activeAgent, agentResponse)

            elif 'customer service' in intentAgentResponse.lower():
                agentResponse = " --> click here to call customer service"
                # call appropriate backend service

            elif 'self pickup' or 'self-pickup' in intentAgentResponse.lower():
                activeAgent = selfPickupAgent
                agentResponse = activeAgent.call(userInput)

            elif 'greeting' in intentAgentResponse.lower():
                # dont initialise any activeAgent in this, since we will redo the intent classification
                agentResponse = "calling greetingsAgent: " + \
                    greetingsAgent.call(userInput)

            elif 'something else' in intentAgentResponse.lower():
                # here possibilities could be walmart FAQ
                # dont initialise any activeAgent in this, since we will redo the intent classification
                agentResponse = "calling faqAgent: " + faqAgent.call(userInput)

            else:
                agentResponse = intentAgentResponse

        else:
            agentResponse = activeAgent.call(userInput)
            agentResponse, extras = self.handleAgentResponse(
                activeAgent, agentResponse)
            
            if activeAgent.agent_name == 'returnAgent':
                userInput = userInput.strip().lower()
                if "yes" in userInput:
                    itemOrders = ItemOrder.objects.filter(user=user, return_valid_till__gte=timezone.now())
                    for itemOrder in itemOrders:
                        if itemOrder.item.name.lower() == inputExtras.lower():
                            itemOrder.initiateReturn()
                            extras = {
                                "return_item_id": itemOrder.id,
                            }
                            break

        return JsonResponse({
            "reply": agentResponse,
            "extras": extras,
        })
