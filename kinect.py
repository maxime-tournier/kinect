
# do this *before* importing nite2
import nite2_fixes

# actual script starts here
from primesense import openni2, nite2

PoseType = nite2.c_api.NitePoseType
SkeletonState = nite2.c_api.NiteSkeletonState
JointType = nite2.c_api.NiteJointType

# if this fails, you need to symlink Redist/NiTE2 and
# Redist/libNiTE2.* in the current directory
nite2.initialize()

tracker = nite2.UserTracker(None)

# fixes memleak
from contextlib import contextmanager            
@contextmanager            
def read_frame():
    try:
        frame = tracker.read_frame()
        yield frame
    finally:
        nite2.c_api.niteUserTrackerFrameRelease(frame._user_tracker_handle,
                                                frame._handle)

def frames():
    while True:
        with read_frame() as f:
            yield f


def tracked(pose_type = None):
    for f in frames():
        res = {}
        
        for user in f.users:
            if user.is_new():
                tracker.start_skeleton_tracking(user.id)
                if pose_type: tracker.start_pose_detection(user.id, pose_type)
            elif not user.is_lost():
                if user.skeleton.state == SkeletonState.NITE_SKELETON_TRACKED:
                    res[user.id] = user

        yield res

def joints(user):
    for j in user.skeleton.joints:

        # god knows what this does
        if j.positionConfidence > 0.5:
            yield j.jointType, j.position


