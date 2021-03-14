import random
from telegram.ext import run_async, Filters
from telegram import Message, Chat, Update, Bot, MessageEntity
from miley import dispatcher
from miley.modules.disable import DisableAbleCommandHandler

ABUSE_STRINGS = (
    "`Owww ... Such a stupid idiot.`",
    "`Don't drink and type.`",
    "`Command not found. Just like your brain.`",
    "`Bot rule 544 section 9 prevents me from replying to stupid humans like you.`",
    "`Sorry, we do not sell brains.`",
    "`Believe me you are not normal.`",
    "`I bet your brain feels as good as new, seeing that you never use it.`",
    "`If I wanted to kill myself I'd climb your ego and jump to your IQ.`",
    "`You didn't evolve from apes, they evolved from you.`",
    "`What language are you speaking? Cause it sounds like bullshit.`",
    "`You are proof that evolution CAN go in reverse.`",
    "`I would ask you how old you are but I know you can't count that high.`",
    "`As an outsider, what do you think of the human race?`",
    "`Ordinarily people live and learn. You just live.`",
    "`Keep talking, someday you'll say something intelligent!.......(I doubt it though)`",
    "`Everyone has the right to be stupid but you are abusing the privilege.`",
    "`I'm sorry I hurt your feelings when I called you stupid. I thought you already knew that.`",
    "`You should try tasting cyanide.`",
    "`You should try sleeping forever.`",
    "`Pick up a gun and shoot yourself.`",
    "`Try bathing with Hydrochloric Acid instead of water.`",
    "`Go Green! Stop inhaling Oxygen.`",
    "`God was searching for you. You should leave to meet him.`",
    "`You should Volunteer for target in an firing range.`",
    "`Try playing catch and throw with RDX its fun.`",
    "`People like you are the reason we have middle fingers.`",
    "`When your mom dropped you off at the school, she got a ticket for littering.`",
    "`You’re so ugly that when you cry, the tears roll down the back of your head…just to a`",
    "`If you’re talking behind my back then you’re in a perfect position to kiss my a**!.`",
    "`Hey Remdi......Tell your giving rates.`"
 )


SONG_STRINGS = (
    "🎶 മിഴിയറിയാതെ വന്നു നീ മിഴിയൂഞ്ഞാലിൽ... കനവറിയാതെയേതോ കിനാവു പോലെ... 🎶.",
    "🎶 നിലാവിന്റെ നീലഭസ്മ കുറിയണിഞ്ഞവളേ... കാതിലോലക്കമ്മലിട്ടു കുണുങ്ങി നിന്നവളേ... 🎶",
    "🎶 എന്തിനു വേറൊരു സൂര്യോദയം... നീയെൻ പൊന്നുഷസ്സന്ധ്യയല്ലേ... 🎶", 
    "🎶 ശ്രീരാഗമോ തേടുന്നിതെൻ വീണതൻ പൊൻ തന്ത്രിയിൽ... 🎶", 
    "🎶 മഴത്തുള്ളികൾ പൊഴിഞ്ഞീടുമീ നാടൻ വഴി... നനഞ്ഞോടിയെൻ കുടക്കീഴിൽ നീ വന്ന നാൾ... 🎶", 
    "🎶 നീയൊരു പുഴയായ് തഴുകുമ്പോൾ ഞാൻ പ്രണയം വിടരും കരയാവും... 🎶", 
    "🎶 അല്ലിമലർ കാവിൽ പൂരം കാണാൻ... അന്നു നമ്മൾ പോയി രാവിൽ നിലാവിൽ... 🎶", 
    "🎶 നിലാവിന്റെ നീലഭസ്മ കുറിയണിഞ്ഞവളേ... കാതിലോലക്കമ്മലിട്ടു കുണുങ്ങി നിന്നവളേ... 🎶", 
    "🎶 ചന്ദനച്ചോലയിൽ മുങ്ങിനീരാടിയെൻ ഇളമാൻ കിടാവേ ഉറക്കമായോ... 🎶", 
    "🎶 അന്തിപ്പൊൻവെട്ടം കടലിൽ മെല്ലെത്താഴുമ്പോൾ... മാനത്തെ മുല്ലത്തറയില് മാണിക്യച്ചെപ്പ്... 🎶", 
    "🎶 താമരപ്പൂവിൽ വാഴും ദേവിയല്ലോ നീ... പൂനിലാക്കടവിൽ പൂക്കും പുണ്യമല്ലോ നീ... 🎶", 
    "🎶 കുന്നിമണിച്ചെപ്പു തുറന്നെണ്ണി നോക്കും നേരം, പിന്നിൽവന്നു കണ്ണു പൊത്തും കള്ളനെങ്ങു പോയി... 🎶", 
    "🎶 ശ്യാമാംബരം പുൽകുന്നൊരാ വെൺചന്ദ്രനായ് നിൻ പൂമുഖം... 🎶", 
    "🎶 പാടം പൂത്തകാലം പാടാൻ വന്നു നീയും... 🎶", 
    "🎶 കറുകവയൽ കുരുവീ... മുറിവാലൻ കുരുവീ... തളിർ വെറ്റിലയുണ്ടോ... വരദക്ഷിണ വെക്കാൻ... 🎶", 
    "🎶 പത്തുവെളുപ്പിന് മുറ്റത്തു നിക്കണ കസ്തൂരി മുല്ലയ്ക്ക് കാത്തുകുത്ത്... എന്റെ കസ്തൂരി മുല്ലയ്ക്ക് കാതു കുത്ത്.. 🎶", 
    "🎶 മഞ്ഞൾ പ്രസാദവും നെറ്റിയിൽ ചാർത്തി... മഞ്ഞക്കുറിമുണ്ടു ചുറ്റി... 🎶", 
    "🎶 കറുത്തപെണ്ണേ നിന്നെ കാണാഞ്ഞിട്ടൊരു നാളുണ്ടേ... 🎶"
 )

@run_async
def abuse(bot: Bot, update: Update):
    bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(ABUSE_STRINGS))
    else:
      message.reply_text(random.choice(ABUSE_STRINGS))

@run_async
def sing(bot: Bot, update: Update):
    bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(SONG_STRINGS))
    else:
      message.reply_text(random.choice(SONG_STRINGS))

__help__ = """
- /abuse : Insult someone.
- /sing : First lines of some random malayalam Songs.
"""

__mod_name__ = "Extras"

ABUSE_HANDLER = DisableAbleCommandHandler("abuse", abuse)
SING_HANDLER = DisableAbleCommandHandler("sing", sing)

dispatcher.add_handler(ABUSE_HANDLER)
dispatcher.add_handler(SING_HANDLER)
