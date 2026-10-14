layeredimage monika forward: #All definitions are for her facing forward.
    at Flatten
    always "assets/mpt/monika/monika_forward_facebase.png" #We always use the basic face.
    
    group outfit:
        
        attribute uniform default null
        attribute casual null

    # wry pairs a smiling mouth with annoyed eyes and brows.
    # Mood selects the default eye, mouth, and eyebrow parts.
    group mood:
        attribute neut default null #neutral
        attribute angr null #angry
        attribute anno null #annoyed
        attribute cry null  #crying
        attribute curi null #curious
        attribute dist null #distant
        attribute doub null #doubtful
        attribute flus null #flustered
        attribute happ null #happy
        attribute laug null #laughing
        attribute lsur null #surprised (lightly)
        attribute nerv null #nervous
        attribute pani null #panicked
        attribute pout null #pouting
        attribute sad null  #sad
        attribute sedu null #seductive
        attribute shoc null #shocked
        attribute vang null #VERY angry
        attribute vsur null #surprised (very)
        attribute worr null #worried
        attribute wry null  #wry -- the smile she keeps on while she is done with you
        attribute yand null #yandere

    group blush: #These are intentionally separate from mood; the idea being that these aren't consciously controlled by the character - rather, they're a result of their emotions making them blush/sweat/etc.
        attribute nobl default null #Default, no blush.
        attribute awkw null #awkward.  defaults for n
        attribute blus null #blushing.  defaults for n
        attribute blaw null #blushing and awkward.  defaults for n

    group left:
        anchor (0,0) subpixel (True)
        yoffset (-0.5)
        attribute ldown default if_any(["uniform"]):
            "assets/mpt/monika/monika_forward_uniform_left_down.png"
        attribute ldown default if_any(["casual"]):
            "assets/mpt/monika/monika_forward_casual_left_down.png"
        attribute lpoint if_any(["uniform"]):
            "assets/mpt/monika/monika_forward_uniform_left_point.png"
        attribute lpoint if_any(["casual"]):
            "assets/mpt/monika/monika_forward_casual_left_point.png"

    group right:
        anchor (0,0) subpixel (True)
        yoffset (-0.5)
        attribute rdown default if_any(["uniform"]):
            "assets/mpt/monika/monika_forward_uniform_right_down.png"
        attribute rdown default if_any(["casual"]):
            "assets/mpt/monika/monika_forward_casual_right_down.png"
        attribute rhip if_any(["uniform"]):
            "assets/mpt/monika/monika_forward_uniform_right_hip.png"
        attribute rhip if_any(["casual"]):
            "assets/mpt/monika/monika_forward_casual_right_hip.png"

    group nose:
        
        #Default nose/blush.
        attribute nose default if_any(["nobl"]):#default nose
            "assets/mpt/monika/monika_forward_nose_n1.png"
        attribute nose default if_any(["awkw"]):#default nose when "awkward"
            "assets/mpt/monika/monika_forward_nose_n2.png"
        attribute nose default if_any(["blus"]):#default nose when "blushing"
            "assets/mpt/monika/monika_forward_nose_n3.png"
        attribute nose default if_any(["blaw"]):#default nose when "blushing and awkward"
            "assets/mpt/monika/monika_forward_nose_n4.png"

        #All noses - truncated tags:
        attribute n1:
            "assets/mpt/monika/monika_forward_nose_n1.png"
        attribute n2:
            "assets/mpt/monika/monika_forward_nose_n2.png"
        attribute n3:
            "assets/mpt/monika/monika_forward_nose_n3.png"
        attribute n4:
            "assets/mpt/monika/monika_forward_nose_n4.png"

    group mouth:
        
        #Default Closed Mouths:
        attribute cm default if_any(["happ","nerv","wry"]):
            "assets/mpt/monika/monika_forward_mouth_ma.png"
        attribute cm default if_any(["neut","worr","anno","dist","doub"]):
            "assets/mpt/monika/monika_forward_mouth_md.png"
        attribute cm default if_any(["lsur","curi"]):
            "assets/mpt/monika/monika_forward_mouth_me.png"
        attribute cm default if_any(["vsur","pout"]):
            "assets/mpt/monika/monika_forward_mouth_mf.png"
        attribute cm default if_any(["shoc"]):
            "assets/mpt/monika/monika_forward_mouth_mi.png"
        attribute cm default if_any(["cry","sad","angr","flus"]):
            "assets/mpt/monika/monika_forward_mouth_mj.png"
        attribute cm default if_any(["vang","pani"]):
            "assets/mpt/monika/monika_forward_mouth_mm.png"
        attribute cm default if_any(["laug","sedu"]):
            "assets/mpt/monika/monika_forward_mouth_mn.png"
        attribute cm default if_any(["yand"]):
            "assets/mpt/monika/monika_forward_mouth_mo.png"
        
        #Open Mouths:
        attribute om if_any(["happ","sedu","wry"]):
            "assets/mpt/monika/monika_forward_mouth_mb.png"
        attribute om if_any(["nerv","yand","laug"]):
            "assets/mpt/monika/monika_forward_mouth_mc.png"
        attribute om if_any(["neut","dist"]):
            "assets/mpt/monika/monika_forward_mouth_me.png"
        attribute om if_any(["worr","vsur","pout"]):
            "assets/mpt/monika/monika_forward_mouth_mg.png"
        attribute om if_any(["anno","flus"]):
            "assets/mpt/monika/monika_forward_mouth_mh.png"
        attribute om if_any(["lsur","curi"]):
            "assets/mpt/monika/monika_forward_mouth_mi.png"
        attribute om if_any(["sad"]):
            "assets/mpt/monika/monika_forward_mouth_mk.png"
        attribute om if_any(["cry","shoc"]):
            "assets/mpt/monika/monika_forward_mouth_ml.png"
        attribute om if_any(["vang","angr","doub","pani"]):
            "assets/mpt/monika/monika_forward_mouth_mq.png"

        ###All mouths - truncated tags:
        attribute ma:
            "assets/mpt/monika/monika_forward_mouth_ma.png"
        attribute mb:
            "assets/mpt/monika/monika_forward_mouth_mb.png"
        attribute mc:
            "assets/mpt/monika/monika_forward_mouth_mc.png"
        attribute md:
            "assets/mpt/monika/monika_forward_mouth_md.png"
        attribute me:
            "assets/mpt/monika/monika_forward_mouth_me.png"
        attribute mf:
            "assets/mpt/monika/monika_forward_mouth_mf.png"
        attribute mg:
            "assets/mpt/monika/monika_forward_mouth_mg.png"
        attribute mh:
            "assets/mpt/monika/monika_forward_mouth_mh.png"
        attribute mi:
            "assets/mpt/monika/monika_forward_mouth_mi.png"
        attribute mj:
            "assets/mpt/monika/monika_forward_mouth_mj.png"
        attribute mk:
            "assets/mpt/monika/monika_forward_mouth_mk.png"
        attribute ml:
            "assets/mpt/monika/monika_forward_mouth_ml.png"
        attribute mm:
            "assets/mpt/monika/monika_forward_mouth_mm.png"
        attribute mn:
            "assets/mpt/monika/monika_forward_mouth_mn.png"
        attribute mo:
            "assets/mpt/monika/monika_forward_mouth_mo.png"
        attribute mp:
            "assets/mpt/monika/monika_forward_mouth_mp.png"
        attribute mq:
            "assets/mpt/monika/monika_forward_mouth_mq.png"
        attribute mr:
            "assets/mpt/monika/monika_forward_mouth_mr.png"

    group eyes:
        
        #Default Opened eyes:
        attribute oe default if_any(["neut","happ","laug","sad","pout","curi"]):
            "assets/mpt/monika/monika_forward_eyes_e1a.png"
        attribute oe default if_any(["worr","flus","dist"]):
            "assets/mpt/monika/monika_forward_eyes_e1b.png"
        attribute oe default if_any(["anno","angr","sedu","doub","wry"]):
            "assets/mpt/monika/monika_forward_eyes_e1d.png"
        attribute oe default if_any(["cry"]):
            "assets/mpt/monika/monika_forward_eyes_e1g.png"
        attribute oe default if_any(["vang","vsur","lsur"]):
            "assets/mpt/monika/monika_forward_eyes_e2a.png"
        attribute oe default if_any(["nerv"]):
            "assets/mpt/monika/monika_forward_eyes_e2b.png"
        attribute oe default if_any(["pani","shoc"]):
            "assets/mpt/monika/monika_forward_eyes_e2d.png"
        attribute oe default if_any(["yand"]):
            "assets/mpt/monika/monika_forward_eyes_e3a.png"
        
        #Default Closed eyes:
        attribute ce if_any(["neut","anno","vang","shoc","worr","sad","angr","lsur","vsur","pani","dist","worr"]):
            "assets/mpt/monika/monika_forward_eyes_e4a.png"#
        attribute ce if_any(["happ","laug","flus","yand","pout","sedu","nerv","curi","doub","wry"]):
            "assets/mpt/monika/monika_forward_eyes_e4b.png"#
        attribute ce if_any(["cry"]):
            "assets/mpt/monika/monika_forward_eyes_e4e.png"

        ###All eyes - truncated tags:
        attribute e1a:
            "assets/mpt/monika/monika_forward_eyes_e1a.png"
        attribute e1b:
            "assets/mpt/monika/monika_forward_eyes_e1b.png"
        attribute e1c:
            "assets/mpt/monika/monika_forward_eyes_e1c.png"
        attribute e1d:
            "assets/mpt/monika/monika_forward_eyes_e1d.png"
        attribute e1e:
            "assets/mpt/monika/monika_forward_eyes_e1e.png"
        attribute e1f:
            "assets/mpt/monika/monika_forward_eyes_e1f.png"
        attribute e1g:
            "assets/mpt/monika/monika_forward_eyes_e1g.png"
        attribute e1h:
            "assets/mpt/monika/monika_forward_eyes_e1h.png"
        attribute e2a:
            "assets/mpt/monika/monika_forward_eyes_e2a.png"
        attribute e2b:
            "assets/mpt/monika/monika_forward_eyes_e2b.png"
        attribute e2c:
            "assets/mpt/monika/monika_forward_eyes_e2c.png"
        attribute e2d:
            "assets/mpt/monika/monika_forward_eyes_e2d.png"
        attribute e3a:
            "assets/mpt/monika/monika_forward_eyes_e3a.png"
        attribute e3b:
            "assets/mpt/monika/monika_forward_eyes_e3b.png"
        attribute e4a:
            "assets/mpt/monika/monika_forward_eyes_e4a.png"
        attribute e4b:
            "assets/mpt/monika/monika_forward_eyes_e4b.png"
        attribute e4c:
            "assets/mpt/monika/monika_forward_eyes_e4c.png"
        attribute e4d:
            "assets/mpt/monika/monika_forward_eyes_e4d.png"
        attribute e4e:
            "assets/mpt/monika/monika_forward_eyes_e4e.png"
        attribute e0a:
            "assets/mpt/monika/monika_forward_eyes_e0a.png"
        attribute e0b:
            "assets/mpt/monika/monika_forward_eyes_e0b.png"

    group eyebrows:
        
        #Default Eyebrows:
        attribute brow default if_any(["neut","happ","yand"]):
            "assets/mpt/monika/monika_forward_eyebrows_b1a.png"#
        attribute brow default if_any(["cry","worr","shoc","laug","sad","flus","pani","worr","nerv"]):
            "assets/mpt/monika/monika_forward_eyebrows_b1b.png"#
        attribute brow default if_any(["anno","sedu","wry"]):
            "assets/mpt/monika/monika_forward_eyebrows_b1c.png"#
        attribute brow default if_any(["vang","angr"]):
            "assets/mpt/monika/monika_forward_eyebrows_b1e.png"#
        attribute brow default if_any(["lsur"]):
            "assets/mpt/monika/monika_forward_eyebrows_b2b.png"#
        attribute brow default if_any(["vsur"]):
            "assets/mpt/monika/monika_forward_eyebrows_b2a.png"#
        attribute brow default if_any(["dist","pout"]):
            "assets/mpt/monika/monika_forward_eyebrows_b1d.png"#
        attribute brow default if_any(["curi"]):
            "assets/mpt/monika/monika_forward_eyebrows_b1f.png"#
        
        #The following brows are for moods that differ between open and closed eyes:
        attribute brow default if_any(["doub"]) if_all(["oe"]) if_not(["ce"]):
            "assets/mpt/monika/monika_forward_eyebrows_b1f.png"#
        attribute brow default if_any(["doub"]) if_all(["ce"]) if_not(["oe"]):
            "assets/mpt/monika/monika_forward_eyebrows_b3b.png"#

        #All eyebrows - truncated tags:
        attribute b1a:
            "assets/mpt/monika/monika_forward_eyebrows_b1a.png"
        attribute b1b:
            "assets/mpt/monika/monika_forward_eyebrows_b1b.png"
        attribute b1c:
            "assets/mpt/monika/monika_forward_eyebrows_b1c.png"
        attribute b1d:
            "assets/mpt/monika/monika_forward_eyebrows_b1d.png"
        attribute b1e:
            "assets/mpt/monika/monika_forward_eyebrows_b1e.png"
        attribute b1f:
            "assets/mpt/monika/monika_forward_eyebrows_b1f.png"
        attribute b2a:
            "assets/mpt/monika/monika_forward_eyebrows_b2a.png"
        attribute b2b:
            "assets/mpt/monika/monika_forward_eyebrows_b2b.png"
        attribute b2c:
            "assets/mpt/monika/monika_forward_eyebrows_b2c.png"
        attribute b3a if_any(["e4a","e4b","e4c","e4d","e4e","ce"]):
            "assets/mpt/monika/monika_forward_eyebrows_b3a.png"
        attribute b3b if_any(["e4a","e4b","e4c","e4d","e4e","ce"]):
            "assets/mpt/monika/monika_forward_eyebrows_b3b.png"
        attribute b3c if_any(["e4a","e4b","e4c","e4d","e4e","ce"]):
            "assets/mpt/monika/monika_forward_eyebrows_b3c.png"

    #This group is intentionally last on this list, so it will render over top of every other thing on the face.
    group special:
    
        attribute s_scream:
            "assets/mpt/monika/monika_forward_special_scream.png"

layeredimage monika lean:
    at Flatten
    
    group outfit: #These attributes are here only to determine which set of "body" sprites to use later.  "null" is what lets us just use these attributes as logic and nothing else.
        
        attribute uniform default null
        attribute casual null

    group mood: #Mood determines what the defaults images are for the following attributes:
        #"oe", "ce", "om", "cm", "brow".
        #By changing what the "mood" attribute is, you can easily switch between premade sets of expressions that work well together, speeding up your workflow.
        #Additionally, you can add in any new ones as you like.
        attribute happ default null #happy
        attribute angr null #angry
        attribute anno null #annoyed
        attribute neut null #neutral

    group blush: #Have to separate these out, they can't share moods.
        attribute nobl default null #Default, no blush.
        attribute awkw null #awkward.  defaults for n
        attribute blus null #blushing.  defaults for n
        attribute blaw null #blushing and awkward.  defaults for n
        attribute bful null #attribute bful null #full face blush.

    group body:
        attribute body default if_any(["uniform"]):
            "assets/mpt/monika/monika_lean_uniform_bodybase.png"
        attribute body default if_any(["casual"]):
            "assets/mpt/monika/monika_lean_casual_bodybase.png"

    group head:
        attribute head default if_any(["uniform"]):
            "assets/mpt/monika/monika_lean_uniform_facebase.png"
        attribute head default if_any(["casual"]):
            "assets/mpt/monika/monika_lean_casual_facebase.png"

    group nose:
        
        #Default nose/blush.
        attribute nose default if_any(["nobl"]):#default nose
            "assets/mpt/monika/monika_lean_nose_n1.png"
        attribute nose default if_any(["awkw"]):#default nose when "awkward"
            "assets/mpt/monika/monika_lean_nose_n2.png"
        attribute nose default if_any(["blus"]):#default nose when "blushing"
            "assets/mpt/monika/monika_lean_nose_n3.png"
        attribute nose default if_any(["blaw"]):#default nose when both "blushing" and "awkward"
            "assets/mpt/monika/monika_lean_nose_n4.png"
        attribute nose default if_any(["bful"]):#full face blush, obscures eyes/eyebrows.
            "assets/mpt/monika/monika_lean_nose_n5.png"

        #All noses - truncated tags:
        attribute n1:
            "assets/mpt/monika/monika_lean_nose_n1.png"
        attribute n2:
            "assets/mpt/monika/monika_lean_nose_n2.png"
        attribute n3:
            "assets/mpt/monika/monika_lean_nose_n3.png"
        attribute n4:
            "assets/mpt/monika/monika_lean_nose_n4.png"
        attribute n5:
            "assets/mpt/monika/monika_lean_nose_n5.png"

    group mouth:
        
        #Default Closed Mouths:
        attribute cm default if_any(["happ"]):
            "assets/mpt/monika/monika_lean_mouth_m1.png"
        attribute cm default if_any(["neut","angr","anno"]):
            "assets/mpt/monika/monika_lean_mouth_m4.png"
        
        #Open Mouths:
        attribute om if_any(["neut","angr","anno"]):
            "assets/mpt/monika/monika_lean_mouth_m2.png"
        attribute om if_any(["happ"]):
            "assets/mpt/monika/monika_lean_mouth_m3.png"

        #All mouths - truncated tags:
        attribute m1:
            "assets/mpt/monika/monika_lean_mouth_m1.png"
        attribute m2:
            "assets/mpt/monika/monika_lean_mouth_m2.png"
        attribute m3:
            "assets/mpt/monika/monika_lean_mouth_m3.png"
        attribute m4:
            "assets/mpt/monika/monika_lean_mouth_m4.png"

    group eyes if_not(["n5","bful"]): #Cannot show if full-face blush is present.
        
        ##Default Opened eyes:
        attribute oe default if_any(["happ","neut"]):
            "assets/mpt/monika/monika_lean_eyes_e1.png"
        attribute oe default if_any(["anno"]):
            "assets/mpt/monika/monika_lean_eyes_e2.png"
        attribute oe default if_any(["angr"]):
            "assets/mpt/monika/monika_lean_eyes_e3.png"
        
        #Default Closed eyes:
        attribute ce if_any(["happ"]):
            "assets/mpt/monika/monika_lean_eyes_e4.png"
        attribute ce if_any(["neut","angr","anno"]):
            "assets/mpt/monika/monika_lean_eyes_e5.png"

        #All eyes - truncated tags:
        attribute e1:
            "assets/mpt/monika/monika_lean_eyes_e1.png"
        attribute e2:
            "assets/mpt/monika/monika_lean_eyes_e2.png"
        attribute e3:
            "assets/mpt/monika/monika_lean_eyes_e3.png"
        attribute e4:
            "assets/mpt/monika/monika_lean_eyes_e4.png"
        attribute e5:
            "assets/mpt/monika/monika_lean_eyes_e5.png"
        attribute e6:
            "assets/mpt/monika/monika_lean_eyes_e6.png"

    group eyebrows if_not(["n5","bful"]): #Cannot show if full-face blush is present.
        
        #Default Eyebrows:
        attribute brow default if_any(["happ","neut"]):
            "assets/mpt/monika/monika_lean_eyebrows_b1.png"
        attribute brow default if_any(["angr","anno"]):
            "assets/mpt/monika/monika_lean_eyebrows_b2.png"

        #All eyebrows - truncated tags:
        attribute b1:
            "assets/mpt/monika/monika_lean_eyebrows_b1.png"
        attribute b2:
            "assets/mpt/monika/monika_lean_eyebrows_b2.png"
        attribute b3:
            "assets/mpt/monika/monika_lean_eyebrows_b3.png"
