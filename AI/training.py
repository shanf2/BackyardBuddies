#priority		feature
#first 			star
#second			time
#third			keyword

from keywordVal import *

def rankScore_keyword(keyword,positive_content,negative_content):
	top_pos,positive_keyword_val = importantWords(positive_content)
	top_neg,negative_keyword_val = importantWords(negative_content)

	keyword_val = {x: (keyword.get(x, 0) + positive_keyword_val.get(x, 0) - negative_keyword_val.get(x,0))/2
                    for x in set(set(keyword).union(positive_keyword_val)).union(negative_keyword_val)}

	return keyword_val
