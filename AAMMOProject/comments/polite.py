
"""
Function that check the politeness of text  
@param unchecked text 
@return checked text
"""
def check_politness(text):
	forbidden_words = ['fool','god','israel','hate','bad']
	for word in forbidden_words:
		text = text.replace(word,'****')
	return text

def check_emoticons_existance(text):
	emoticons = {':)':'/static/imgs/smile.gif',':P':'/static/imgs/tongue.gif','>:(':'/static/imgs/angry.gif',':O':'/static/imgs/shocked.gif'}
	for face in emoticons:
		text = text.replace(face,'<img src="' + emoticons[face]+'" width="60px" height="50px" />')
	return text

# "you are kind :)" is gonna be replaced with   -->   you are kind <img src="/static/imgs/smile.gif" width="60px" height="50px" />
