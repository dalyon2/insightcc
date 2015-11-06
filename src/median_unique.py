import json, sys, codecs, re, time

#given a tweet, this function replaces all of the escape and html characters with their
#proper ascii equivalents

def remove_escapes(line):
    line=line.replace('\\\\','\\').replace('\\/','/').replace('\\\'','\'').replace('\\\"','\"').replace('\\t',' ').replace('\\n',' ')
    line=line.replace('&lt;','<').replace('&rt;','>')
    line=line.replace('&amp;','&')
    line=re.sub(r'\s+',' ',line)
    return line

#this function takes tweets from a file, cleans the text of unicode, and returns the cleaned tweets
#largely re-used from task 1

def extract_tweets(infile):
    tweets=[]
    
    with codecs.open(infile,'r','ascii') as f:
        for line in f:
            match=re.search('(\"text\":\")([^"]*)\",\"',line)
            if match:
                noesctext=remove_escapes(match.group(2))
                match2=re.search(r'\\u([0-9a-fA-F]{4})',noesctext)
                if match2:
                    if int(match2.group(1),16) > 127:
                        noesctext=re.sub(r'\\u[0-9a-fA-F]{4}','',noesctext)
                    else:   
                        noesctext=noesctext.decode('unicode-escape')
                tweet=json.loads(line)
# convert the time to a python readable format
                ts = time.strptime(tweet['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
                texttime = (noesctext, ts)
                tweets.append(texttime)
    f.close()
    return tweets

    
def build_graph(tweetlist,outfile):
    hashtaggraph={}
    timelimit=60
    g=open(outfile,'w')
    for tweet in tweetlist:
        numerator=0.0
        denominator=0.0
#convert the time to a float
        tweettime=time.mktime(tweet[1])
        checklinks=[]
#delete old links from the dictionary        
        for link1 in hashtaggraph:
            deletedlinks=[link2 for link2 in hashtaggraph[link1] if (tweettime-hashtaggraph[link1][link2])>timelimit ]
            for link2 in deletedlinks:
                del hashtaggraph[link1][link2]
                if link1 not in checklinks:
                    checklinks.append(link1)
        for link1 in checklinks:                
            if hashtaggraph[link1]=={}:
                del hashtaggraph[link1]
                    
#find new hashtags from the latest tweet
        hashes=re.findall(r'#[^\s]*',tweet[0])
        for i in xrange(len(hashes)):
            hashes[i]=str(hashes[i]).lower()
#add any new hashtag links to the dictionary, if they already exist refresh the timestamp
#the link dictionary contains both directions to make counting easier
        if len(hashes)>1:            
            for i in xrange(len(hashes)-1):
                for j in xrange(i+1,len(hashes)):
                    if len(hashes[i])>1 and len(hashes[j])>1:
                        if hashes[i] not in hashtaggraph:
                            hashtaggraph[hashes[i]]={}
                        hashtaggraph[hashes[i]][hashes[j]]=tweettime
                        if hashes[j] not in hashtaggraph:
                            hashtaggraph[hashes[j]]={}
                        hashtaggraph[hashes[j]][hashes[i]]=tweettime
        for link1 in hashtaggraph:
            denominator=denominator+1.0
            for link2 in hashtaggraph[link1]:
                numerator=numerator+1.0
#don't divide by 0!                
        if denominator>0:
            g.write(str(round(numerator/denominator,2))+'\n')
        else:
            g.write('0.00\n')
    g.close()
def main():
    args = sys.argv[1:]
    if len(args) != 2:
        print 'usage: infile outfile'
        sys.exit(1)

    texttweets=extract_tweets(args[0])
    build_graph(texttweets,args[1])

if __name__ == '__main__':
  main()

