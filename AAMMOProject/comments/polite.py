
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
