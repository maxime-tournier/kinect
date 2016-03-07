import kinect


for users in kinect.tracked():
    for i, u in users.iteritems():
        print "user", i
        
        for t, j in kinect.joints(u):
            print '\t', t, j
            
