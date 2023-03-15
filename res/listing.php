#!/bin/php
<?php
$path = $_POST['path'];
$lst = $_POST;

echo "<html><head></head><body>";
echo '<a href="..">..</a></br>';
echo '/'.$path."</br>";



foreach(array_slice($lst,2) as $value){
echo "<a href='".$value."'>".$value."</a></br>";
}

echo "</body></html>";
?>
