# you can write to stdout for debugging purposes, e.g.
# print "this is a debug message"

def solution(N):
    # write your code in Python 2.7
    nBinary = "{0:b}".format(N)
    print nBinary
    
    gapOpen, gapCnt, gapCountList = False, 0, []
    for char in nBinary:
        if char == '0':
            gapOpen = True ## only set this when gapOpen is False
            gapCnt =+ 1
        elif char == '1' and gapOpen:
            gapCountList.append(gapCnt)
            gapOpen = False
            gapCnt = 0
        else: ## the char is 1, but its already closed
            pass
           
    return get_max_gap_count(gapCountList)
        
def get_max_gap_count(gapCountList):
    print 'gapCountList: %s' % gapCountList
    mxLen = 0
    if len(gapCountList) > 0:
        mxLen = max(gapCountList)
    
    return mxLen
    



