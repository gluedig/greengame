'''
Created on Nov 17, 2012

@author: raber
'''

# A very simple Flask Hello World app for you to get started with...

from flask import Flask
import twitter
import shelve
import collections

app = Flask(__name__)

main_hdr = '''
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="static/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
    <title>Bootstrap 101 Template</title>
    </head>
    <body>
    <script src="https://platform.twitter.com/widgets.js" type="text/javascript"></script>
    <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>

    <div class="container-fluid">
        <div class="row-fluid">
        Main
        </div>
        <div class="row-fluid">
            <div class="span2">

            </div>
            <div class="span10">
                <a class="twitter-timeline" href="https://twitter.com/search?q=%23greengame" data-widget-id="269808655258492930">Tweets about "#greengame"</a>
            </div>
        </div>
    </div>

    </body>
    </html>
'''

battle_hdr = '''
<!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="assets/css/bootstrap-responsive.css" rel="stylesheet">
    <title>Bootstrap 101 Template</title>
    </head>
    <body>
    <ul class="nav nav-pills nav-stacked">
    ...
    </ul>
    
    </body>
    </html>
'''

@app.route('/')
def main_route():
    return main_hdr


@app.route('/battle')
def battle_route():
    twitter_search = twitter.Twitter(domain="search.twitter.com")
    res=twitter_search.search(q="#greengame")
    resp = ''
    
    shlv = shelve.open('greengame.shelve', writeback = True)
    cnt = collections.Counter()
    
    print(len(res))
    for x in res['results']:
        
        user_id = x['from_user_id_str'].__str__()
        print(user_id)
        
        if user_id in shlv.keys():
            shlv[user_id]['count'] += 1
        else:
            shlv[user_id] = dict()
            shlv[user_id]['count'] = 1
            shlv[user_id]['user_name'] = x['from_user']
            shlv[user_id]['profile_url'] = x['profile_image_url_https']
    
        cnt[user_id] = shlv[user_id]['count']
        shlv[user_id]['count'] = 0
    

    for user in cnt.most_common():
        resp += str.format("{0} {1} </br>", user[0], user[1])
    
    shlv.close()
    
    
    
    return resp




if __name__ == '__main__':
    app.debug = True
    app.run()