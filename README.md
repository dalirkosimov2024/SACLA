# SACLA
Scripts for "Investigating material response to laser imprint" SACLA experiment

## How to use watcher.py

- watcher.py uses watchdog to monitor a directory, which I called "TESTFOLDER"
- Any modifications that occur in this directory will be copied to "NEW_PATH" folder
- "dev.log" logs all changes that occur

The setup should look something like this:
<pre>
 ___ src
    |___ watcher.py
    |___ dev.log
    |___ TESTFOLDER 
    |             |___ file1.txt
    |             |___ file2.txt
    |             
    |___ NEW_PATH
</pre>
