$folder_path = "C:\Users\kaibr\Downloads\MatlabDan"
$matlabexe = "C:\Users\kaibr\Downloads\MatlabDan\export_cdt_as_csv.exe"
Echo dirname
$files = Get-ChildItem $folder_path
$subject_file_names = @()
foreach ($f in $files){
	$len = $f.Name.Length
	$extension = $f.Name.Substring($len-3)
	if ($extension -eq "cdt"){
		$subject_file_names += $f.Name.Substring(0,$len-4)
	}
	
	Echo $extension 
}
Echo $subject_file_names
$idx = 1
foreach ($subject in $subject_file_names){
	echo "$($idx) of $($subject_file_names.Length)"
	Start-Process $matlabexe -NoNewWindow -Wait "$($subject)"
	$idx += 1 
}