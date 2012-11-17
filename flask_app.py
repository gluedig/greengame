'''
Created on Nov 17, 2012

@author: raber
'''

# A very simple Flask Hello World app for you to get started with...

from flask import Flask
import twitter
import collections

app = Flask(__name__)

main_hdr = '''
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="static/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
    <link rel="stylesheet" type="text/css" href="static/mystyle.css">
    <title>Green Game</title>
    </head>
    <body>
    <script src="https://platform.twitter.com/widgets.js" type="text/javascript"></script>
    <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>

    <div class="container-fluid">
        <div class="row-fluid">
            <div class="span12">
                <h2>Green Game</h2>
<!-- Begin MailChimp Signup Form -->
<link href="http://cdn-images.mailchimp.com/embedcode/slim-081711.css" rel="stylesheet" type="text/css">
<style type="text/css">
    #mc_embed_signup{background:#fff; clear:left; font:14px Helvetica,Arial,sans-serif; }
    /* Add your own MailChimp form style overrides in your site stylesheet or in this style block.
       We recommend moving this block and the preceding CSS link to the HEAD of your HTML file. */
</style>
<div id="mc_embed_signup">        
<form action="http://twitter.us6.list-manage.com/subscribe/post?u=c02b248faab3da7a19119c7bd&amp;id=28f614ae67" method="post" id="mc-embedded-subscribe-form" name="mc-embedded-subscribe-form" class="validate" target="_blank" novalidate>
    <label for="mce-EMAIL">Subscribe to our mailing list</label>
    <input type="email" value="" name="EMAIL" class="email" id="mce-EMAIL" placeholder="email address" required>
    <div class="clear"><input type="submit" value="Subscribe" name="subscribe" id="mc-embedded-subscribe" class="button"></div>
</form>
</div>

<!--End mc_embed_signup-->
            </div>
        </div>
        <div class="row-fluid">
            <div class="span4">
                <h4>Top contibutors</h4></br>'''
                
main_foot = '''
            </div>
            <div class="span4">
                <h4>Recent tweets<h4></br>
                <a class="twitter-timeline" href="https://twitter.com/search?q=%23greengame" data-widget-id="269808655258492930">Tweets about "#greengame"</a>
            </div>
        </div>
    </div>
    </body>
    </html>
'''


@app.route('/')
def main_route():
    twitter_search = twitter.Twitter(domain="search.twitter.com")
    res=twitter_search.search(q="#greengame")
    resp = main_hdr
    #shlv = shelve.open('greengame.shelve', writeback = True)
    shlv = dict()
    cnt = collections.Counter()
    
    resp += '<table class="table table-hover table-condensed"><tbody>'
    print(len(res))
    for x in res['results']:
        
        user_id = x['from_user_id_str'].__str__()
        #print(user_id)
        print(x)
        if user_id in shlv.keys():
            shlv[user_id]['count'] += 1
        else:
            shlv[user_id] = dict()
            shlv[user_id]['count'] = 1
            shlv[user_id]['user_name'] = x['from_user_name']
            shlv[user_id]['profile_url'] = x['profile_image_url']
            shlv[user_id]['user'] = x['from_user']
    
        cnt[user_id] = shlv[user_id]['count']
        shlv[user_id]['count'] = 0
    

    for user in cnt.most_common(10):
        user_id = str.format("{0}",user[0])

        resp += u"<tr><td><h4>{0}</h4></td><td><img src='{1}'/></td><td><h5><a href='http://twitter.com/{3}'>{2}</a></h5></td></tr></a>".format( 
                           unicode(user[1]), 
                           unicode(shlv[user_id]['profile_url']),
                           unicode(shlv[user_id]['user_name']),
                           unicode(shlv[user_id]['user']) )
  
    
    
    return resp+'</tbody></table>'+main_foot




if __name__ == '__main__':
    app.debug = True
    app.run()