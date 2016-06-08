#!/home/kojima/cgi/bin/python
# CGI Test
import cgi
import slack_methods as sm

print "Content-Type: text/html\n\n"

print "<html><body>"

form = cgi.FieldStorage()
form_ok = 0
if form.has_key("post_text") and form.has_key("post_channel"):
    form_ok = 1
if form_ok == 0:
    print "<h1>ERROR</h1>"
else:
        print "<h2>Result</h2><hr><p>"
        post_text = form["post_text"].value
        post_channel = form["post_channel"].value
        print "<p><b>post_text: </b>", post_text
        print "<p><b>post_channel: </b>", post_channel
        sm.post_message(text=post_text, channel=post_channel)
        print "<p>"+sm.get_message(channel=post_channel)+"</p>"
print '<p><input type="button" onclick="location.href=\'slack_post.html\'" value="Back">'
print "</body></html>"
