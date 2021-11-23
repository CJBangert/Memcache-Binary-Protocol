# Memcache-Binary-Protocol

## Installation
Used Python 3.8.10 on Ubuntu 20.04 (anything python 3 should work):  
```pip install -r requirements.txt ```

## To Run:
``` python app.py ```

*listens on 127.0.0.1:5000  
sample client code in client.py. To run:  

``` python client.py```

## Thoughts

Regarding performance, since this is just get/set it's pretty straighforward. I implemented the cache using a Python dictionary (Hash table),  
so lookups are O(1) and average case for setting a value is also constant time (worst case linear time if table is full).  

Concurrency issues I protected against were gets/sets running out of order (reading before value is set, etc). To protect against this, I put a lock on the memcache_process() function  
so only one thread can execute the code to deserialize and execute the request at a time. I did this for simplicity, but if I wanted to boost performance and maximize concurrency I could deserialize the requests concurrently and then execute the get/sets in the order that they arrived using a queue. 

Other limitations of my implementation to be improved on (to name a few) could be adding support for authorization, handling what happens when the cache fills up, and adding a persistent data layer  so all the data isn't wiped if the server crashes or somehow goes offline. I also could probably do a little better with naming (main.py is a bad name) and taking advantage of Python OOP


### The Flags

While developing this, the biggest issue I ran into was figuring out what the flags field (extras) was. The Memcache docs didnt really have much on it and I couldn't really find anything on  
the internet about it. The docs in one of the examples just had it as 0xdeadbeef (3735928559) so I was using that. However, that caused the client to try and decompress it during the deserialization step. To avoid it trying to do this and crashing I had to figure out how to not have that branch execute - where flags & (1 << 3) == 0 . To satisfy the condition for the correct branch to execute,  
the flag had to be divisible by 4: (flags & 1 << 4) !=0 . To get this value, I just made a for loop to print a bunch of values where flags & (1 << 3) == 0 and I just picked one that was divisible by 4. I chose 1765040 and it started working. Of course, this is not a good way to do this given that the flag value is not documented (but then again, nothing was :) ). 