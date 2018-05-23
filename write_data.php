<?php
// the $_POST[] array will contain the passed in filename and filedata
// the directory "data" must be writable by the server
$filename = "/home/maddy/pinsoro/data/".$_POST['filename'];
$filedata = $_POST['filedata'];
// write the file to disk
file_put_contents($filename, $filedata);
?>
