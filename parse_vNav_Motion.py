import pydicom
import os
import numpy as np
import itertools
import glob
import argparse

def normalize(x):
  return x / np.sqrt(np.dot(x,x))

def readRotAndTrans(paths):
  files = itertools.chain.from_iterable([glob.glob(path) for path in paths])

  ds = sorted([pydicom.dcmread(x) for x in files], key=lambda dcm: dcm.AcquisitionNumber)

  head = [(np.array([1,0,0,0]),np.array([0,0,0]))]

  return list(itertools.chain.from_iterable([head, [(np.array(map(float, y[1:5])), map(float, y[6:9])) for y in [str.split(x.ImageComments) for x in ds[1:]]]]))

def angleAxisToQuaternion(a):
  w = np.cos(a[0] / 2.0)
  axisNorm = np.sqrt(np.dot(a[1:], a[1:]))

  if 0 == axisNorm :
    return np.array([1,0,0,0])

  axisScale = np.sin(a[0] / 2.0) / np.sqrt(np.dot(a[1:], a[1:]))
  tail = a[1:] * axisScale
  q = np.ndarray(shape=(4))
  q[0] = w
  q[1:] = tail
  return q

def quaternionToAxisAngle(q) :
  a = np.ndarray(shape=(4))
  a[0] = np.arccos(q[0]) * 2.0
  a[1:] = q[1:] / np.sqrt(np.dot(q[1:], q[1:]))
  return a

def quaternionToRotationMatrix(q):
  w = q[0];
  x = q[1];
  y = q[2];
  z = q[3];

  wSq = w * w;
  xSq = x * x;
  ySq = y * y;
  zSq = z * z;

  wx2 = w*x*2.0;
  wy2 = w*y*2.0;
  wz2 = w*z*2.0;

  xy2 = x*y*2.0;
  xz2 = x*z*2.0;

  yz2 = y*z*2.0;

  rotMatrix = np.ndarray(shape=(3,3))

  rotMatrix[0,0] = wSq + xSq - ySq - zSq;
  rotMatrix[0,1] = xy2 - wz2;
  rotMatrix[0,2] = xz2 + wy2;

  rotMatrix[1,0] = xy2 + wz2;
  rotMatrix[1,1] = wSq - xSq + ySq - zSq;
  rotMatrix[1,2] = yz2 - wx2;

  rotMatrix[2,0] = xz2 - wy2;
  rotMatrix[2,1] = yz2 + wx2;
  rotMatrix[2,2] = wSq - xSq - ySq + zSq;

  return rotMatrix

def rotationMatrixToQuaternion(m):
  ## Dylan Dec 19/12
  ## This algorithm taken from http://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToQuaternion/index.htm
  ##
  ## Also tried the algorithm in
  ##		Animating rotation with quaternion curves.
  ##		Ken Shoemake
  ##		Computer Graphics 19(3):245-254,  1985
  ##		http://portal.acm.org/citation.cfm?doid=325334.325242
  ## but you'll find that it's not numerically stable without some truncation epsilon.
  ## The algorithm we're using now doesn't require us to pick some arbitrary epsilon, so
  ## I like it better.

  tr = np.trace(m);

  if (tr > 0) :
    S = np.sqrt(tr+1.0) * 2; # S=4*qw
    SInv = 1.0 / S;
    w = 0.25 * S;
    x = (m[2,1] - m[1,2]) * SInv;
    y = (m[0,2] - m[2,0]) * SInv;
    z = (m[1,0] - m[0,1]) * SInv;
  elif ((m[0,0] > m[1,1]) and (m[0,0] > m[2,2])):
    S = np.sqrt(1.0 + m[0,0] - m[1,1] - m[2,2]) * 2; # S=4*qx
    SInv = 1.0 / S;
    w = (m[2,1] - m[1,2]) * SInv;
    x = 0.25 * S;
    y = (m[0,1] + m[1,0]) * SInv;
    z = (m[0,2] + m[2,0]) * SInv
  elif (m[1,1] > m[2,2]):
    S = np.sqrt(1.0 + m[1,1] - m[0,0] - m[2,2]) * 2; # S=4*qy
    SInv = 1.0 / S;
    w = (m[0,2] - m[2,0]) * SInv;
    x = (m[0,1] + m[1,0]) * SInv;
    y = 0.25 * S;
    z = (m[1,2] + m[2,1]) * SInv;
  else:
    S = np.sqrt(1.0 + m[2,2] - m[0,0] - m[1,1]) * 2; # S=4*qz
    SInv = 1.0 / S;
    w = (m[1,0] - m[0,1]) * SInv;
    x = (m[0,2] + m[2,0]) * SInv;
    y = (m[1,2] + m[2,1]) * SInv;
    z = 0.25 * S;

  return np.array([w, x, y, z])

def motionEntryToHomogeneousTransform(e) :
  t = np.ndarray(shape=(4,4))

  t[0:3,3] = e[1]
  t[0:3,0:3] = quaternionToRotationMatrix(angleAxisToQuaternion(e[0]))
  t[3,:] = [0,0,0,1]
  return np.matrix(t)

def diffTransformToMaxMotion(t, radius):
  angleAxis = quaternionToAxisAngle(rotationMatrixToQuaternion(t[0:3, 0:3]))
  angle = angleAxis[0]
  axis = angleAxis[1:]
  trans = t[0:3,3].flatten()
  t_rotmax = radius * np.sqrt(2.0 - 2.0 * np.cos(angle))
  return np.sqrt(
    (t_rotmax * t_rotmax) +
    (2.0 * t_rotmax) *
      np.linalg.norm(
        trans - (np.dot(trans, axis) * axis)) +
    (np.linalg.norm(trans) * np.linalg.norm(trans))
    )

def diffTransformToRMSMotion(t, radius):
  rotMatMinusIdentity = t[0:3,0:3] - np.array([[1,0,0],[0,1,0],[0,0,1]])
  trans = np.ravel(t[0:3,3])

  return np.sqrt(
    0.2 * radius * radius * np.trace(np.transpose(rotMatMinusIdentity) * rotMatMinusIdentity) +
    np.dot(trans, trans)
    )

parser = argparse.ArgumentParser(description='Parse DICOM files from a vNav series and convert them into different motion scores.')

parser.add_argument('--tr', required=True, type=float,
                    help='Repetition Time (TR) of the parent sequence (i.e., the MPRAGE) expressed in seconds.')
parser.add_argument('--input', nargs='+', required=True, type=os.path.abspath,
                    help='A list of DICOM files that make up the vNav series (in chronological order).')
parser.add_argument('--radius', nargs=1, required=True, type=float,
                    help='Assumed brain radius in millimeters for estimating rotation distance.')
output_type = parser.add_mutually_exclusive_group(required=True)
output_type.add_argument('--mean-rms', action='store_true', help='Print time-averaged root mean square (RMS) motion.')
output_type.add_argument('--mean-max', action='store_true', help='Print time-averaged max motion.')
output_type.add_argument('--rms-scores', action='store_true', help='Print root mean square (RMS) motion over time.')
output_type.add_argument('--max-scores', action='store_true', help='Print max motion over time.')

args = parser.parse_args()

# Transform creation and differences
transforms = [motionEntryToHomogeneousTransform(e) for e in readRotAndTrans(args.input)]
diffTransforms = [ts[1] * np.linalg.inv(ts[0]) for ts in zip(transforms[0:], transforms[1:])]

# Motion scores
rmsMotionScores = [diffTransformToRMSMotion(t, args.radius) for t in diffTransforms]
maxMotionScores = [diffTransformToMaxMotion(t, args.radius) for t in diffTransforms]

# Script output to STDOUT depending on "output_type"
if args.mean_rms :
  print np.mean(rmsMotionScores) * 60.0 / args.tr
elif args.mean_max :
  print np.mean(maxMotionScores) * 60.0 / args.tr
elif args.rms_scores :
  for score in rmsMotionScores:
    print score
elif args.max_scores :
  for score in maxMotionScores:
    print score
