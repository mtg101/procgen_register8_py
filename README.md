I've got plans to make a procedurally generated C64 game: doing things like Elite did with names, properties, location, etc of systems all generated from seeds.

Trying to test the algorithms for this in assembler would spend too much time fighting assembler instead of focussing on the algorithm. 

What I need is a quick, interactive way of working on the algorithm without worrying about managing registers and fiddling with if/else in assembler.

So: Python sounds ideal. And I've never used Python before, so it's a good excuse to learn it!

Obviously as a high-level language Python doesnt have native register support, which is where assembler will be working. It has bitshifts, but no carry flags or ADC.

Doing that in any high-level language is simple enough, but it's busy work. So I got Claude AI to generate me the initial register8.py file. It works! According to both me and the unit tests Claude created ;)

So now I'm using that Register8 class to map out the procgen for Culture-64 game! Lots of LFSR deteministic pseudo RNGs, lots of seeds from names of systems/npcs/object, generating those things... 

All while learning how to use Python! And by use I mean not just learning how an if statement looks in Python - I include things like interactive mode, how tests work, the cool f-strings.

Update: so I've learned that when a Python function says it takes a string and returns an int... Python doesn't care if you pass a int and it returns a string. WTF? It's like it's designed to catch you out... Rust was too heavy for this task but Python is... well it's dangerous even as a scripting language! I'm sorry Java... despite your gargabe garbage collection, at least you have rules!
