from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import google.genai as genai
import re

# Import your finance utils
from portfolio.utils import get_risk_score, get_var, buy_stock, sell_stock

# Initialize Gemini Client
client = genai.Client(api_key="AIzaSyBY2STLvVnQUQM-Z-L-6QHdS2z5d6E8D9w")  # 🔹 Replace with your actual API key

# System instruction for accuracy
SYSTEM_PROMPT = """
You are an intelligent finance assistant.
- For finance and stock queries: provide accurate, detailed, and easy-to-understand answers.
- Always explain reasoning, not just one-line answers.
- If the user asks about stocks, give analysis with trends, risks, and opportunities.
- If the user asks something unrelated to finance, still answer politely and helpfully.
"""

def ask_chatbot(prompt):
    """Send prompt to Gemini AI and get better response"""
    response = client.models.generate_content(
        model="gemini-1.5-pro",   # More accurate than gemini-1.5
        contents=[SYSTEM_PROMPT, prompt]
    )
    return response.text.strip()

def process_user_query(user, message):
    """Handle queries related to stocks or AI"""
    message_lower = message.lower()
    
    user_id = getattr(user, "id", None)  # safe way to get id

    if "risk" in message_lower:
        if user_id:
            return f"Your current risk score is {get_risk_score(user_id)}."
        else:
            return "Login required to check risk score."
    elif "var" in message_lower:
        if user_id:
            return f"Your portfolio VaR is {get_var(user_id)}."
        else:
            return "Login required to check portfolio VaR."
    elif "buy" in message_lower:
        if user_id:
            return buy_stock(user_id, message)
        else:
            return "Login required to buy stocks."
    elif "sell" in message_lower:
        if user_id:
            return sell_stock(user_id, message)
        else:
            return "Login required to sell stocks."
    else:
        return ask_chatbot(message)



def chat_page(request):
    """Render chat interface"""
    return render(request, 'chatbot/chat.html')

@csrf_exempt
@csrf_exempt
def chat_api(request):
    try:
        if request.method != "POST":
            return JsonResponse({"error": "POST requests only"}, status=400)

        user = request.user if request.user.is_authenticated else None
        message = request.POST.get('message', '').strip()

        if not message:
            return JsonResponse({"error": "Message cannot be empty"}, status=400)

        reply = process_user_query(user, message)
        return JsonResponse({"reply": reply})
    
    except Exception as e:
        # Always return JSON even if error occurs
        return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)

