# parse_vNav_Motion.py

This is a small python script to parse DICOM files from a vNav series and convert them into motion scores. The script takes four arguments.  The usage and help information below can be generated any time by calling it with the `-h` or `--help` flag.

```
usage: parse_vNav_Motion.py [-h] --tr TR --input INPUT [INPUT ...] --radius
                            RADIUS
                            (--mean-rms | --mean-max | --rms-scores | --max-scores)

Parse DICOM files from a vNav series and convert them into different motion
scores.

optional arguments:
  -h, --help            show this help message and exit
  --tr TR               Repetition Time (TR) of the parent sequence (i.e., the
                        MPRAGE) expressed in seconds.
  --input INPUT [INPUT ...]
                        A list of DICOM files that make up the vNav series (in
                        chronological order).
  --radius RADIUS       Assumed brain radius in millimeters for estimating
                        rotation distance.
  --mean-rms            Print time-averaged root mean square (RMS) motion.
  --mean-max            Print time-averaged max motion.
  --rms-scores          Print root mean square (RMS) motion over time.
  --max-scores          Print max motion over time.
```

The script assumes that you've got a version of pydicom installed. For directions on doing that, see https://github.com/pydicom/pydicom.

If you find bugs, please report them in the issues section of https://github.com/MRIMotionCorrection/parse_vNav_Motion

If you want to add features, please make a pull request on GitHub as well. We'd love to see this expanded.
