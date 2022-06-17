import config


def logInfo(*msg, end="\n"):
	if config.log_level < 3:
		return
	print("\033[37m[info]%s\033[0m" % logMsg(*msg), end=end)


def logWarn(*msg, end="\n"):
	if config.log_level < 2:
		return
	print("\033[33m[warning]%s\033[0m" % logMsg(*msg), end=end)


def logError(*msg, end="\n"):
	if config.log_level < 1:
		return
	print("\033[31m[error]%s\033[0m" % logMsg(*msg), end=end)


def logMsg(*msg):
	allMsg = ""
	n = 1
	for m in msg:
		n += 1
		if allMsg != "":
			allMsg = allMsg + " "
		allMsg = allMsg + str(m)
	return allMsg