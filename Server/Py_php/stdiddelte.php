<?php

$server_dir = 'C:/Server/Apache24/htdocs/delete/';
$user_dir = $_POST['uname'];
$upload_dir = $server_dir.$user_dir;

function rmdirAll($dir) {
    $dirs = dir($dir);
    while(false !== ($entry = $dirs->read())) {
       if(($entry != '.') && ($entry != '..')) {
          if(is_dir($dir.'/'.$entry)) {
             rmdirAll($dir.'/'.$entry);
          } else {
             @unlink($dir.'/'.$entry);
          }
        }
     }
     $dirs->close();

     @rmdir($dir);
}

if(is_dir($upload_dir)){
    rmdirAll($upload_dir);	
}

?>