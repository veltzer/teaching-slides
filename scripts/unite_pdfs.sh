#!/bin/bash -e

if [[ $# -eq 2 ]]
then
	cp $2 $1
else
	pdfunite *.pdf $1
