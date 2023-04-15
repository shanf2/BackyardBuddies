import math
from keywordVal import *

#priority		feature
#first			time
#second			keyword
def postScore(post,keyword,cur_time,date_posted):
	time_val=0
	keyword_val=0

	#if post is within the first week(7 days) post, it is given priority
	time_val= 0.2*math.log(-(cur_time-date_posted),10)+0.831

	#if post contains keywords, it is given priority
	keyword_post,temp = importantWords(post)
	for key in keyword_post.keys():
		keyword_val= keyword_val + keyword.get(key,0)

	rank= time_val+keyword_val
	return rank
