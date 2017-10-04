# parse_vNav_Motion.py

This is a small python script to parse the DICOM files from a vNavs series and convert them into an average RMS motion score. The script takes two arguments `--tr` which is the TR of the parent sequence (i.e., the MPRAGE) expressed in seconds (e.g., `--tr 2.4`) and `--input` which is the list of files DICOM files that makeup the vNavs series.

The script assumes that you've got a version of pydicom installed. For directions on doing that, see https://github.com/pydicom/pydicom
