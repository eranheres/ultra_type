from rich.console import Console
from rich.text import Text

console = Console()

hebrew_text = "אֶת־הַשָּׁמַיִם וְאֶת־הָאָרֶץ. וְהָאָרֶץ הָיְתָה תֹהוּ וָבֹהוּ וְחֹשֶׁךְ עַל־פְּנֵי תְהוֹם וְרוּחַ אֱלֹהִים מְרַחֶפֶת עַל־פְּנֵי הַמָּיִם. וַיֹּאמֶר אֱלֹהִים יְהִי אוֹר וַיְהִי־אוֹר. וַיַּרְא אֱלֹהִים אֶת־הָאוֹר כִּי־טוֹב וַיַּבְדֵּל אֱלֹהִים בֵּין הָאוֹר וּבֵין הַחֹשֶׁךְ. וַיִּקְרָא אֱלֹהִים לָאוֹר יוֹם וְלַחֹשֶׁךְ קָרָא לָיְלָה. וַי הִי עֶרֶב וַיְהִי בֹקֶר יוֹם אֶחָד."

# Create a Text object with the Hebrew text
text = Text(hebrew_text, justify="right")

# Print the text
console.print(text)

