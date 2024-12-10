
# folder with all mat lab files
$folder_path = ""

#path to matlab exe
$matlabexe = ""
Echo dirname

#getting a list of files
$files = Get-ChildItem $folder_path

# initialize array
$subject_file_names = @()

# get the base name for each file store in name e.g "sub_51.mat" - > "sub_51"
foreach ($f in $files){
	$len = $f.Name.Length
	$extension = $f.Name.Substring($len-3)
	if ($extension -eq "cdt"){
		$subject_file_names += $f.Name.Substring(0,$len-4)
	}
	
}
Echo $subject_file_names
$idx = 1

# run matlab exe with the base name as a parameter, spawn child process wait for it to resolve
foreach ($subject in $subject_file_names){
	echo "$($idx) of $($subject_file_names.Length)"
	Start-Process $matlabexe -NoNewWindow -Wait "$($subject)"
	$idx += 1 
}