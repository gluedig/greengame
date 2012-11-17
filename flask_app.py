'''
Created on Nov 17, 2012

@author: raber
'''

# A very simple Flask Hello World app for you to get started with...

from flask import Flask
import twitter
import collections

app = Flask(__name__)

new_hdr = '''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Green Game</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">
    <link href="static/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
    <!-- Le styles -->
    <link href="static/bootstrap/css/bootstrap.css" rel="stylesheet">
    <style type="text/css">
      body {
        
        padding-bottom: 40px;
        
      }

      /* Custom container */
      .container-narrow {
        margin: 0 auto;
        max-width: 700px;
      }
      .container-narrow > hr {
        margin: 30px 0;
      }

      /* Main marketing message and sign up button */
      .jumbotron {
        padding: 60px 0;
        text-align: center;
      }
      .jumbotron h1 {
        font-size: 72px;
        line-height: 1;
      }
      .jumbotron .btn {
        font-size: 21px;
        padding: 14px 24px;
      }

      /* Supporting marketing content */
      .marketing {
        margin: 0px 0;
      }
      .marketing p + h4 {
        margin-top: 28px;
      }
    </style>
    <link href="static/bootstrap/css/bootstrap-responsive.css" rel="stylesheet">
    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
    <link href="http://cdn-images.mailchimp.com/embedcode/slim-081711.css" rel="stylesheet" type="text/css">
    <style type="text/css">
    #mc_embed_signup{background:rgb(156, 211, 57); clear:left; font:14px Helvetica,Arial,sans-serif; }
    /* Add your own MailChimp form style overrides in your site stylesheet or in this style block.
       We recommend moving this block and the preceding CSS link to the HEAD of your HTML file. */
    </style>
    <script src="https://platform.twitter.com/widgets.js" type="text/javascript"></script>
    <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src="//platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
  </head>
  <body style="background: rgb(156, 211, 57); background-image: url(static/img/bg.png); background-repeat: repeat-x;">
    <div class="container">
    <div class="masthead" >
        <img src="static/img/header.png">
      <div class="row-fluid" style="background: rgb(156, 211, 57); padding-top:50px;">

        <div class="span6" style="padding-left:20px;">
            <h2 style="color:white;">1. Take the challenge... <br> 2. Cut your bills... <br>3. Save the planet!</h2>
        </div>
        <div class="span6" style="padding-top:15px;">
            <em style="color:white; font-size:18px;">Play GreenGame, get challenged to change your behavior concerning energy usage. <br><br>Start competing right now on Twitter in a quest to share about your sustainable actions!</em>

        </div>


    </div>
    
    <div class="row">

        <div class="span12" style="padding-left:20px;">
            <br>
            
            <!-- Begin MailChimp Signup Form -->
<link href="http://cdn-images.mailchimp.com/embedcode/slim-081711.css" rel="stylesheet" type="text/css">
<style type="text/css">
     clear:left; font:14px Helvetica,Arial,sans-serif; }
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
        

    <div class="row-fluid marketing" style="background: rgb(156, 211, 57);">
            <div class="span1"></div>
            <div class="span4" >
                <h4>Top contributors</h4></br>
'''

new_foot = '''
            </div>
            <div class="span2"></div>
            <div class="span4">
                <h4>Recent tweets<h4></br>
                <a class="twitter-timeline" href="https://twitter.com/search?q=%23greengame" data-widget-id="269808655258492930">Tweets about "#greengame"</a>
            </div>
    </div>
    </div>
  </body>
</html>
'''

skip_those = ['GreenGameSW']

@app.route('/')
def main_route():
    twitter_search = twitter.Twitter(domain="search.twitter.com")
    res=twitter_search.search(q="#greengame")
    resp = new_hdr
    shlv = dict()
    cnt = collections.Counter()
    
    resp += '<table class="table table-hover table-condensed table-bordered" style="background: white;"><tbody>'

    for x in res['results']:
        user_id = x['from_user_id_str'].__str__()
        if x['from_user'] in skip_those:
            continue
        
        if not user_id in shlv.keys():
            shlv[user_id] = dict()
            shlv[user_id]['user_name'] = x['from_user_name']
            shlv[user_id]['profile_url'] = x['profile_image_url']
            shlv[user_id]['user'] = x['from_user']
    
        cnt[user_id] += 1
        shlv[user_id]['count'] = 0


    for user in cnt.most_common(10):
        user_id = str.format("{0}",user[0])

        resp += u"<tr><td><h4>{0}</h4></td><td><img src='{1}'/></td><td><h5><a href='http://twitter.com/{3}'>{2}</a></h5></td></tr></a>".format( 
                           unicode(user[1]), 
                           unicode(shlv[user_id]['profile_url']),
                           unicode(shlv[user_id]['user_name']),
                           unicode(shlv[user_id]['user']) )
  
    
    
    return resp+'</tbody></table>'+new_foot


if __name__ == '__main__':
    app.debug = True
    app.run()