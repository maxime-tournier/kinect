# do this *before* importing nite2
import nite2_fixes

# actual script starts here
from primesense import openni2, nite2

PoseType = nite2.c_api.NitePoseType
SkeletonState = nite2.c_api.NiteSkeletonState

# if this fails, you need to symlink Redist/NiTE2 and
# Redist/libNiTE2.* in the current directory
nite2.initialize()

tracker = nite2.UserTracker(None)
    
pose_type = PoseType.NITE_POSE_CROSSED_HANDS

while True:
    frame = tracker.read_frame()
    timestamp = frame.timestamp

    for user in frame.users:
        print 'user:', user.id,

        if user.skeleton.state == SkeletonState.NITE_SKELETON_TRACKED:
            print 'calibrating'
        elif user.skeleton.state == SkeletonState.NITE_SKELETON_TRACKED:
            print 'tracked'
        elif user.skeleton.state == SkeletonState.NITE_SKELETON_NONE:
            print 'stopped tracking'
        else:
            print 'calibration error :-/'
 
        if user.is_new():
            print 'new user !'
            
            tracker.start_skeleton_tracking(user.id)
            tracker.start_pose_detection(user.id, pose_type)
            
        elif not user.is_lost():

            com = user.centerOfMass
            # print 'com:', com

            bbox = user.boundingBox
            # print 'bbox:', bbox

            if user.skeleton.state == SkeletonState.NITE_SKELETON_TRACKED:
                for j in user.skeleton.joints:

                    # god knows what this does
                    if j.positionConfidence > 0.5:
                        pass
                        # print j.jointType, j.position

        pose = user.get_pose(pose_type)

        if pose.is_entered(): print 'pose entered'
        elif pose.is_exited(): print 'pose exited'
        elif pose.is_held(): print 'pose held'
        
