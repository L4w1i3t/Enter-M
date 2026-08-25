# =============================================================================
# sayori_layeredimage.rpy  --  Sayori sprite, Monika Pose Toolkit (MPT)
# =============================================================================
#
# Third-party asset pack, used ONLY by the Mika lost record. The layer
# definitions and their original explanatory comments are kept verbatim so
# the pack can be re-synced from upstream; do not restyle them to match the
# rest of ENTER M.
#
# Art lives beside this file in MPT/sayori/.
# =============================================================================
layeredimage sayori turned: #turned definitions.
    
    always "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_facebase.png" #Always need this face.
    
    group outfit: #These attributes are here only to determine which set of "body" sprites to use later.  "null" is what lets us just use these attributes as logic and nothing else.
        attribute uniform default null
        attribute casual null
    
    
    
    group mood: #Mood determines what the defaults images are for the following attributes:
        #"oe", "ce", "om", "cm", "brow".
        #By changing what the "mood" attribute is, you can easily switch between premade sets of expressions that work well together, speeding up your workflow.
        #Additionally, you can add in any new ones as you like.
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
        attribute yand null #yandere
        #attribute xxxx null #xxxx #Do you want to define a new mood?  Here, have a template!
    
    
    
    group blush: #Have to separate these out, they can't share moods.
        attribute nobl null #No blush.
        attribute awkw null #awkward.  defaults for n
        attribute blus null #blushing.  defaults for n
        attribute blaw null #blushing and awkward.  defaults for n
    
    
    
    #Left arm variants
    group left if_any(["uniform"]):
        attribute ldown default:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_uniform_left_down.png"
        attribute lup:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_uniform_left_up.png"
    
    group left if_any(["casual"]):
        attribute ldown default:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_casual_left_down.png"
        attribute lup:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_casual_left_up.png"
    
    
    
    #Right arm variants
    group right if_any(["uniform"]):
        attribute rdown default:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_uniform_right_down.png"
        attribute rup:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_uniform_right_up.png"
    
    group right if_any(["casual"]):
        attribute rdown default:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_casual_right_down.png"
        attribute rup:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_casual_right_up.png"
    
    
    
    group nose:
        
        #Default nose/blush.
        attribute nose default if_any(["nobl"]):#default nose
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_nose_n1.png"
        attribute nose default if_any(["awkw"]):#default nose when "awkward"
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_nose_n2.png"
        attribute nose default if_any(["blus"]):#default nose when "blushing"
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_nose_n3.png"
        attribute nose default if_any(["blaw"]):#default nose when "blushing and awkward"
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_nose_n4.png"
        
        
        #All noses - truncated tags:
        attribute n1:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_nose_n1.png"
        attribute n2:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_nose_n2.png"
        attribute n3:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_nose_n3.png"
        attribute n4:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_nose_n4.png"
        attribute nl:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_nose_nl.png"
    
    
    
    group mouth:
        
        #Default Closed Mouths:
        attribute cm default if_any(["happ","sedu","nerv"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_ma.png"
        attribute cm default if_any(["neut","anno","worr","curi"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_md.png"
        attribute cm default if_any(["dist","flus"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_me.png"
        attribute cm default if_any(["lsur","shoc"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mf.png"
        attribute cm default if_any(["sad","angr","pout","doub"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mj.png"
        attribute cm default if_any(["cry","pani","vsur"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mk.png"
        attribute cm default if_any(["vang"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mm.png"
        attribute cm default if_any(["laug"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mn.png"
        attribute cm default if_any(["yand"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mo.png"
        
        #Open Mouths:
        attribute om if_any(["happ","laug"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mb.png"
        attribute om if_any(["yand","nerv"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mc.png"
        attribute om if_any(["pout","sedu"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mf.png"
        attribute om if_any(["sad","lsur","dist"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mg.png"
        attribute om if_any(["neut","anno","shoc","worr"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mh.png"
        attribute om if_any(["curi","doub"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mi.png"
        attribute om if_any(["flus"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mk.png"
        attribute om if_any(["cry","vsur"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_ml.png"
        attribute om if_any(["angr","pani","vang"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mq.png"
        
        
        ###All mouths - truncated tags:
        attribute ma:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_ma.png"
        attribute mb:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mb.png"
        attribute mc:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mc.png"
        attribute md:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_md.png"
        attribute me:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_me.png"
        attribute mf:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mf.png"
        attribute mg:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mg.png"
        attribute mh:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mh.png"
        attribute mi:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mi.png"
        attribute mj:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mj.png"
        attribute mk:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mk.png"
        attribute ml:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_ml.png"
        attribute mm:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mm.png"
        attribute mn:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mn.png"
        attribute mo:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mo.png"
        attribute mp:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mp.png"
        attribute mq:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mq.png"
        attribute mr:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_mouth_mr.png"
    
    
    
    group eyes:
        
        #Default Opened eyes:
        attribute oe default if_any(["neut","angr","happ","laug","sad"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e1a.png"
        attribute oe default if_any(["dist","worr","pout"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e1b.png"
        attribute oe default if_any(["anno","sedu","doub"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e1d.png"
        attribute oe default if_any(["cry"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e1g.png"
        attribute oe default if_any(["lsur","flus","vsur","curi"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e2a.png"
        attribute oe default if_any(["nerv"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e2b.png"
        attribute oe default if_any(["pani","vang","shoc"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e2d.png"
        attribute oe default if_any(["yand"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e3a.png"
        
        #Default Closed eyes:
        attribute ce if_any(["sad","anno","angr","dist","shoc","worr","nerv","curi","doub"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e4a.png"
        attribute ce if_any(["neut","happ","lsur","laug","vsur","yand","pout","sedu"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e4b.png"
        attribute ce if_any(["vang","flus","pani"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e4c.png"
        attribute ce if_any(["cry"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e4d.png"
        
        
        ###All eyes - truncated tags:
        attribute e1a:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e1a.png"
        attribute e1b:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e1b.png"
        attribute e1c:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e1c.png"
        attribute e1d:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e1d.png"
        attribute e1e:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e1e.png"
        attribute e1f:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e1f.png"
        attribute e1g:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e1g.png"
        attribute e1h:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e1h.png"
        attribute e2a:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e2a.png"
        attribute e2b:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e2b.png"
        attribute e2c:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e2c.png"
        attribute e2d:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e2d.png"
        attribute e3a:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e3a.png"
        attribute e3b:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e3b.png"
        attribute e4a:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e4a.png"
        attribute e4b:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e4b.png"
        attribute e4c:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e4c.png"
        attribute e4d:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e4d.png"
        attribute e4e:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e4e.png"
        attribute e0a:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e0a.png"
        attribute e0b:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyes_e0b.png"
    
    
    
    group eyebrows:
        
        #Default Eyebrows:
        attribute brow default if_any(["neut","happ","lsur","flus","shoc"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b1a.png"
        attribute brow default if_any(["sad","cry","pani","yand","nerv"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b1b.png"
        attribute brow default if_any(["laug","vsur","worr","sedu"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b1c.png"
        attribute brow default if_any(["anno","pout"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b1d.png"
        attribute brow default if_any(["angr","vang"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b1e.png"
        attribute brow default if_any(["curi","doub"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b1f.png"
        
        #The following brows are for moods that differ between open and closed eyes:
        attribute brow default if_any(["dist"]) if_all(["oe"]) if_not(["ce"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b2a.png"
        attribute brow default if_any(["dist"]) if_all(["ce"]) if_not(["oe"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b3c.png"
        
        
        ###All eyebrows - truncated tags:
        attribute b1a:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b1a.png"
        attribute b1b:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b1b.png"
        attribute b1c:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b1c.png"
        attribute b1d:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b1d.png"
        attribute b1e:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b1e.png"
        attribute b1f:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b1f.png"
        attribute b2a:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b2a.png"
        attribute b2b:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b2b.png"
        attribute b2c:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b2c.png"
        attribute b3a if_any(["e4a","e4b","e4c","e4d","e4e","ce"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b3a.png"
        attribute b3b if_any(["e4a","e4b","e4c","e4d","e4e","ce"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b3b.png"
        attribute b3c if_any(["e1d","e4a","e4b","e4c","e4d","e4e","ce"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_eyebrows_b3c.png"
    
    
    
    #This group is intentionally last on this list, so it will render over top of every other thing on the face.
    group special:
        
        attribute s_scream:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_turned_special_scream.png"



layeredimage sayori tap: #tapping definitions.
    
    group outfit:
        attribute uniform default:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_uniform_bodybase.png"
        attribute casual:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_casual_bodybase.png"
    
    always "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_facebase.png"
    
    
    
    group mood: #Mood determines what the defaults images are for the following attributes:
        #"oe", "ce", "om", "cm", "brow".
        #By changing what the "mood" attribute is, you can easily switch between premade sets of expressions that work well together, speeding up your workflow.
        #Additionally, you can add in any new ones as you like.
        attribute nerv default null #nervous
        attribute angr null #angry
        attribute dist null #distant
        attribute neut null #neutral
        attribute pout null #pouting
    
    
    
    group blush: #Have to separate these out, they can't share moods.
        attribute nobl default null #no blush applied.
        attribute awkw null #awkward.  defaults for n
        attribute blus null #blushing.  defaults for n
        attribute blaw null #blushing AND awkward.  defaults for n
        attribute bful null #full face blush.
    
    
    
    group nose:
        
        #Default nose/blush.
        attribute nose default if_any(["nobl"]):#default nose
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_nose_n1.png"
        attribute nose default if_any(["awkw"]):#default nose when "awkward"
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_nose_n2.png"
        attribute nose default if_any(["blus"]):#default nose when "blushing"
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_nose_n3.png"
        attribute nose default if_any(["blaw"]):#default nose when "blushing" and "awkward"
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_nose_n4.png"
        attribute nose default if_any(["bful"]):#default nose when "blushing" and "awkward"
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_nose_n5.png"
        
        #All noses - truncated tags:
        attribute n1:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_nose_n1.png"
        attribute n2:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_nose_n2.png"
        attribute n3:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_nose_n3.png"
        attribute n4:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_nose_n4.png"
        attribute n5:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_nose_n5.png"
    
    
    
    group mouth:
        
        #Default Closed Mouths:
        attribute cm default if_any(["pout"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_mouth_m2.png"
        attribute cm default if_any(["neut","nerv","angr","dist"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_mouth_m3.png"
        
        #Open Mouths:
        attribute om if_any(["nerv"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_mouth_m1.png"
        attribute om if_any(["neut","pout","angr","dist"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_mouth_m4.png"
        
        
        #All mouths - truncated tags:
        attribute m1:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_mouth_m1.png"
        attribute m2:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_mouth_m2.png"
        attribute m3:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_mouth_m3.png"
        attribute m4:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_mouth_m4.png"
    
    
    
    group eyes if_not(["n5","bful"]):
        
        #Default Opened eyes:
        attribute oe default if_any(["neut","nerv"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyes_e1.png"
        attribute oe default if_any(["pout","dist"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyes_e2.png"
        attribute oe default if_any(["angr"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyes_e5.png"
        
        #Default Closed eyes:
        attribute ce if_any(["neut","nerv","pout","angr","dist"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyes_e6.png"
        
        
        #All eyes - truncated tags:
        attribute e1:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyes_e1.png"
        attribute e2:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyes_e2.png"
        attribute e3:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyes_e3.png"
        attribute e4:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyes_e4.png"
        attribute e5:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyes_e5.png"
        attribute e6:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyes_e6.png"
    
    
    
    group eyebrows if_not(["n5","bful"]):
        
        #Default Eyebrows:
        attribute brow default if_any(["neut"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyebrows_b3.png"
        attribute brow default if_any(["nerv","dist"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyebrows_b1.png"
        attribute brow default if_any(["pout","angr"]):
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyebrows_b2.png"
        
        
        #All eyebrows - truncated tags:
        attribute b1:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyebrows_b1.png"
        attribute b2:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyebrows_b2.png"
        attribute b3:
            "lost_records/Mika/mod_assets/MPT/sayori/sayori_tapping_eyebrows_b3.png"



