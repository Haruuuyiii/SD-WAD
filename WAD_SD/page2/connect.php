<?php

$host="localhost";
$username="root";
$password="";
$db="sd-wad-main";

$conn=new mysqli($host,$username,$password,$db);
if($conn->connect_error){
    die("Failed to Connect to Database: ".$conn->connect_error);
}
?>


