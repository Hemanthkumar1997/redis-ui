## redis-ui
Simple Redis Key-value viewer application.

#### steps to run:
* install all requirements using "python3 -m pip install -r requirements.txt"
* run flask app using "python3 app.py"
* open http://0.0.0.0:8080/ 
* clicking on any key listed, it will show the pretty-printed json value in new tab.

#### Links
* `/getAllKeys`&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;-> Lists all keys</pre>
* `/getAllKeys`&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;-> Lists all keys</pre>
* `/getVal/<key>`&nbsp; &nbsp; &nbsp;-> Fetches value of supplied key
* `/purgeAll/`&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;-> Flushes everything in cache
* `/purge/<key>`&nbsp; &nbsp; &nbsp; &nbsp;-> Deletes data related to supplied key
