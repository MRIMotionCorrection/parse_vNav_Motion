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

## Motion scores

The RMS motion score is based on:

- Jenkinson, Mark. “Measuring Transformation Error by RMS Deviation.” Technical Report. FMRIB Technical Report. Oxford: FMRIB, 1999. http://www.fmrib.ox.ac.uk/analysis/techrep/tr99mj1/tr99mj1.pdf.


Previous publications using this method include:

- Reuter, Martin, M. Dylan Tisdall, Abid Qureshi, Randy L. Buckner, André J. W. van der Kouwe, and Bruce Fischl. “Head Motion during MRI Acquisition Reduces Gray Matter Volume and Thickness Estimates.” NeuroImage 107 (February 15, 2015): 107–15. https://doi.org/10.1016/j.neuroimage.2014.12.006.
- Tisdall, M. Dylan, Martin Reuter, Abid Qureshi, Randy L. Buckner, Bruce Fischl, and André J. W. van der Kouwe. “Prospective Motion Correction with Volumetric Navigators (VNavs) Reduces the Bias and Variance in Brain Morphometry Induced by Subject Motion.” NeuroImage 127 (February 15, 2016): 11–22. https://doi.org/10.1016/j.neuroimage.2015.11.054.

which both used a radius of 64 mm and the --mean-rms option to compute motion scores for each scan.

Please be warned that an incorrect equation for the max motion score was previously presented in

- Tisdall, M. Dylan, Aaron T. Hess, Martin Reuter, Ernesta M. Meintjes, Bruce Fischl, and André J. W. van der Kouwe. “Volumetric Navigators for Prospective Motion Correction and Selective Reacquisition in Neuroanatomical MRI.” Magnetic Resonance in Medicine 68, no. 2 (2012): 389–99. https://doi.org/10.1002/mrm.23228.

A corrected equation for this measure is implemented in this python code and is now used in the vNavs sequences.

## Dependencies

The script assumes that you've got a version of pydicom installed. For directions on doing that, see https://github.com/pydicom/pydicom.

## Bugs and feature requests

If you find bugs, please report them in the issues section of https://github.com/MRIMotionCorrection/parse_vNav_Motion

If you want to add features, please make a pull request on GitHub as well. We'd love to see this expanded.
