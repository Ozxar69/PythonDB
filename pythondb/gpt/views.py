import re

import markdown2
import openai
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ChatForm

from .models import Dialogue


openai.api_key = settings.OPENAI_API_KEY


def chat(request, fullscreen=False):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data['message']

            if request.user.is_authenticated:
                dialogues = request.user.dialogues.all().order_by('created_at')
                messages = []
                for dialogue in dialogues:
                    messages.append({"role": "user", "content": dialogue.user_message})
                    messages.append({"role": "assistant", "content": dialogue.bot_message})
            else:
                messages = []

            messages.append({"role": "user", "content": message})

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages
            )
            reply = response['choices'][0]['message']['content'].strip()
            reply = re.sub(
                    r"```(\w*)\s*(.*?)\s*```",
                    lambda match: f"<pre><code class='language-{match.group(1) or 'python'}'>{match.group(2).strip()}</code></pre>",
                    reply,
                    flags=re.DOTALL,
                )
            reply = re.sub(
                r"<(?!pre|code|/pre|/code).*?>",
                lambda match: f"&lt;{match.group(0)[1:-1]}&gt;",
                reply,
            )
            reply_html = markdown2.markdown(reply, extras=["fenced-code-blocks",
                                                           "code-friendly"])

            if request.user.is_authenticated:
                Dialogue.objects.create(
                    user=request.user,
                    user_message=message,
                    bot_message=reply_html
                )

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'reply': reply})

            return render(request, 'full_chat.html' if fullscreen else 'includes/chat.html', {
                'form': form,
                'reply': reply_html,
                'dialogues': request.user.dialogues.all() if request.user.is_authenticated else []
            })

    else:
        form = ChatForm()

    dialogues = request.user.dialogues.all() if request.user.is_authenticated else []
    return render(request, 'gpt/full_chat.html' if fullscreen else 'includes/chat.html', {
        'form': form,
        'dialogues': dialogues
    })

@login_required
def clean_chat(request):
    history = Dialogue.objects.filter(user=request.user)
    if request.method == 'POST':
        history.delete()
        return redirect(request.META.get("HTTP_REFERER", "/"))

def full_chat(request):
    return chat(request, fullscreen=True)
