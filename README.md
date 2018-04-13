### maestro
maestro is an attempt at a naive sensorimotor management. how far can we get without deep learning or other advanced ai techniques?



step 1a. get a state representation
          abd   ->  [0,1,3]
                    110100
step 1b. add on your last action and encode it into an SDR.

step 2. keep a running list of the last thing we've seen. pass that up.
          abc, abd  -> [111000110100]

step 3. keep track of what leads to what in SDR terms
          abc     ->  abd
          [0,1,2] ->  [0,1,3]  
          111000  ->  110100

step 4. get a goal from above, given where we are translate that into actions
          [0,1,7] ->  a b e
          110010  ->  ^ ^ ^-state
                      | |---state
                      |-----suggested action, if there is no other way to get
                            to be state then use the other action.
        consult where you are now
        110100  ->  111000 abc
        110100  ->  110010 abe  <-- our goal and our action is a to get there.
        110100  ->  010101 gbd


So the data hierarchy might look like this (each letter is a state (with acts))
  histories       | current moment    ->  goal
  o p n i m e b y | l u v e h i j k   ->  g o a l m e t o
          l u v e | h i j k               g o a l
              h i | j k                   g o
                j | k                     g

in the next time step...
  histories       | current moment    ->  goal
  p n i m e b y l | u v e h i j k g   ->  o a l m e t o g
                    u v e h i j k g       o a l g
                            i j k g       o a
                                k g       o
