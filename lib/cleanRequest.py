def cleanRequestTweet(tweetText):
	authorizedChar = "abcdefghijklmnopqrstuvwxyz+"
	cleanRequest = []
	for i in tweetText:
		if i in authorizedChar:
			cleanRequest.append(i)
		else:
			pass
	return ''.join(cleanRequest)