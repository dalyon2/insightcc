#!/user/bin/python
#Written in 2015 by David Lyon
#for the Insight Data Science coding challenge
import json, sys, codecs, re

#given a tweet, this function replaces all of the escape and html characters with their
#proper ascii equivalents

def remove_escapes(line):
    line=line.replace('\\\\','\\').replace('\\/','/').replace('\\\'','\'').replace('\\\"','\"').replace('\\t',' ').replace('\\n',' ')
    line=line.replace('&lt;','<').replace('&rt;','>')
    line=line.replace('&amp;','&')
    line=re.sub(r'\s+',' ',line)
    return line

#this function takes tweets from a file, extracts the text and created_at fields, and cleans the text
#of unicode and escape characters before writing the cleaned tweets to a file

def extract_tweets(infile,outfile):
    tweets=[]
    unicodetweets=0
    g=open(outfile,'w')
    with codecs.open(infile,'r','ascii') as f:
        for line in f:
# does the tweet have text? if so, remove escapes and html from it
            match=re.search('(\"text\":\")([^"]*)\",\"',line)
            if match:
                noesctext=remove_escapes(match.group(2))
# does the tweet have unicode characters? if so, remove or decode them (if they are secretly ascii)
# increment the counter only if we encountered real unicode
                match2=re.search(r'\\u([0-9a-fA-F]{4})',noesctext)
                if match2:
                    if int(match2.group(1),16) > 127:
                        noesctext=re.sub(r'\\u[0-9a-fA-F]{4}','',noesctext)
                        unicodetweets=unicodetweets+1
                    else:   
                        noesctext=noesctext.decode('unicode-escape')
                tweet=json.loads(line)
                g.write(noesctext + '(timestamp:' + tweet['created_at'] + ')\n')
    f.close()
    g.write('\n' + str(unicodetweets) + ' tweets contained unicode.')
    g.close()
    

def main():
    args = sys.argv[1:]
    if len(args) != 2:
        print 'usage: infile outfile'
        sys.exit(1)
    extract_tweets(args[0],args[1])
    
#    extract_tweets('../tweet_input/tweets.txt','../tweet_output/ft1.txt')


if __name__ == '__main__':
  main()
