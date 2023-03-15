#!/usr/bin/php
<?php
$x=0;
foreach(array_slice($argv,1) as $value){
    if($x==0){
        $val1 = $value;
        $x++;
    }
    else{
        $val2 = $value;
        $_POST[$val1] = $val2;
        $x=0;
    }
}

if ($argv[0]!=$_POST['dest']){
include($_POST['dest']);
}
else{
include("/home/newic/boa/errors/404.html");
}
?>


