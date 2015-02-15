def check_politeness(text):
	"""
	Function that check the politeness of text
	@param unchecked text
	@return checked text
	"""
	forbidden_words = ['fool', 'god', 'israel', 'hate', 'bad']
	for word in forbidden_words:
		text = text.replace(word, '****')
	return text


def check_emoticons_existence(text):
	"""
	This is a function that check is there is an emotion expression exist
	then it replace it with its gif icon
	@:param text with emot-expressions
	@:return text with emoticons
	"""

	emoticons = {
		':)': "'imgs/smile.gif'",
		':P': "'imgs/tongue.gif'",
		'>:(': "'imgs/angry.gif'",
		':O': "'imgs/shocked.gif'"
	}
	for face in emoticons:
		text = text.replace(face, '<img src="{% static ' + emoticons[face] + '%}" width="60px" height="50px" />')
	return text

# "you are kind :)" is gonna be replaced with   -==>   you are kind <img src="{% static imgs/smile.gif %}"
# width="60px" height="50px" />
