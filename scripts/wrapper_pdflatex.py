#!/usr/bin/env python

import sys
import os
import os.path
import subprocess

"""
This is a script that runs pdflatex for us.
Why do we need this script ?
- to remove the output before we run pdflatex so that we will be sure that we start clean.
if pdflatex finds a file it will * reprocess * it and we don't want that, do we ?
- we need to run pdflatex twice to create indexes and more.
- pdf latex is way too verbose - we want to remove that output and only show it if there is
an error.
- in case we fail we want to make sure we remove the output.

Maybe more reasons will follow...

Take note of the argument we pass to pdflatex:
- -interaction=nonstopmode - this means that latex will not stop and enter interactive
mode to ask the user what to do about an error (what is this behaviour anyway ?!?).
- -halt-on-error - this means that latex will stop on error.
- -output-directory - this tells pdflatex where the output folder is.

This python script is a rewrite of a similar script in perl.
"""

#parameters
# do you want debugging...
debug = 0
# remove the tmp file for output at the end of the run? (this should be yes
# unless you want junk files hanging around in /tmp...)
remove_tmp = 1
# how many times to run 'pdflatex(1)' ?
runs = 2
# do you want to run the 'qpdf' post processing stage?
qpdf = 1

# print to stdout a file content
# this function is adjusted for the ugly output that pdflatex produces and so it
# only prints the lines between lines starting with '!' (including the actual lines
# starting with '!'). Apparently this is how pdflatex shows errors. Ugrrr...
def printout(filename: str) {
    if debug:
        print(f"printing [{filename}]", file=sys.stderr)
    with open(filename):
        inerr = False
        for line in file:
            if inerr:
                print(line, file=sys.stderr)
                inerr = False
		    else
                if line.startswith("!"):
                    print(line, file=sys.stderr)
                    inerr = True

# this is a function that removes a file and can optionally die if there is a problem
def unlink_check(filename: str, check: bool, doit: bool):
    if doit:
        if debug:
			print(f"unlinking [{filename}]", file=sys.stderr)
        if check:
            os.unlink(filename)
        else:
            try:
                os.unlink(filename)
            except:
                pass

# this is a function that chmods a file and can optionally die if there is a problem
def chmod_check(filename:str, check: bool):
    if debug:
        print(f"chmodding [{filename}]", file=sys.stderr)
    if check:
	    os.chmod(filename, 0o444)
    else:
        try:
            os.chmod(filename, 0o444)
        except:
            pass

def my_call(args):
    if debug:
		print(f"my_call args are [{args}]", file=sys.stderr)
	res = subprocess.call(args)
    if debug:
		print(f"my_call res is [{res}]", file=sys.stderr)
	return res

# this is a function that renames a file and dies if there is a problem 
def rename(old_filename: str, new_filename: str, check: bool):
    if debug:
		print(f"my_rename [{old_filename, new_filename}]", file=sys.stderr)
    if check:
        os.rename(old_filename, new_filename)
    else:
        try:
            os.rename(old_filename, new_filename)
        except:
            pass

# here we go...
filename_input = sys.argv[1]
filename_output = sys.argv[2]
output_dir = os.path.basename(filename_output)
my($input)=shift(@ARGV)
my($output)=shift(@ARGV)
my($output_dir)=File::Basename::dirname($output)
# temporary file name to store errors...
my($volume,$directories,$myscript)=File::Spec->splitpath($0)
my($tmp_fname_out)='/tmp/'.$myscript.$$.'.out'
my($tmp_fname_err)='/tmp/'.$myscript.$$.'.err'
#my($tmp_output)='/tmp/'.$myscript.$$.'.pdf'
my($cmd)='pdflatex -interaction=nonstopmode -halt-on-error -output-directory '.$output_dir.' '.$input.' > '.$tmp_fname_out.' 2> '.$tmp_fname_err
if($debug) {
	print 'input is ['.$input.']'."\n"
	print 'output is ['.$output.']'."\n"
	print 'cmd is ['.$cmd.']'."\n"
}
# first remove the output (if it exists)
unlink_check($output,1,-f $output)
# we need to run the command twice!!! (to generate the index and more)
for(my($i)=0;$i<$runs;$i++) {
	my($res)=my_call($cmd)
	if($res) {
		# error path
		# print the errors
		printout($tmp_fname_out)
		printout($tmp_fname_err)
		# remove the tmp file for the errors
		unlink_check($tmp_fname_out,1,$remove_tmp)
		unlink_check($tmp_fname_err,1,$remove_tmp)
		# make sure to the remove the output (we are in the error path)
		unlink_check($output,1,-f $output)
		# exit with error code of the child...
		exit($res >> 8)
	} else {
		# everything is ok
		# remove the tmp file for the errors
		unlink_check($tmp_fname_out,1,$remove_tmp)
		unlink_check($tmp_fname_err,1,$remove_tmp)
		# change the output to be unchangble (but only in the final run!)
		if($i==$runs-1) {
			chmod_check($output,1)
			my($name,$path,$suffix)=File::Basename::fileparse($output, qw(.pdf))
			my($output_base)=File::Spec->catfile($path,$name)
			unlink_check($output_base.'.log',1,1)
			unlink_check($output_base.'.out',1,1)
			unlink_check($output_base.'.toc',1,1)
			unlink_check($output_base.'.aux',1,1)
		}
	}
}
if($qpdf) {
	# move the output to the new place
	my($tmp_output)=$output.'.pdf'
	my_rename($output,$tmp_output,1)
	# I also had '--force-version=1.5' but it is not needed since I use pdflatex and pdftex with the right version there...
	my($cmd4)='qpdf --deterministic-id --linearize '.$tmp_output.' '.$output.' > '.$tmp_fname_out.' 2> '.$tmp_fname_err
	my($res)=my_call($cmd4)
	if($res) {
		# error path
		# print the errors
		printout($tmp_fname_out)
		printout($tmp_fname_err)
		# remove the tmp file for the errors
		unlink_check($tmp_fname_out,1,$remove_tmp)
		unlink_check($tmp_fname_err,1,$remove_tmp)
		# remove the temporary file...
		unlink_check($tmp_output,1,1)
		# make sure to the remove the output (we are in the error path)
		unlink_check($output,1,-f $output)
		# exit with error code of the child...
		exit($res >> 8)
	} else {
		# everything is ok
		# remove the temporary file...
		unlink_check($tmp_output,1,1)
		# remove the tmp file for the errors
		unlink_check($tmp_fname_out,1,$remove_tmp)
		unlink_check($tmp_fname_err,1,$remove_tmp)
		# change the output to be unchangble (but only in the second time!)
		chmod_check($output,1)
	}
}
