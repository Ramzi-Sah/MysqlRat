<?php
	session_start();
	include('../Config.php');
	/*----------------Set some vars--------------------------------*/
	if (!isset($_POST['USERNAME']) || !isset($_POST['PASSWORD'])){
		echo '<script>window.location.href = "..?error=1";</script>';
		die();
	}
	$USERNAME=$_POST['USERNAME'];
	$PASSWORD=$_POST['PASSWORD'];
	/*----------------Check forms-----------------*/
	if(preg_match("#\W#", $USERNAME, $false_char) || preg_match("#\W#", $PASSWORD, $false_char)){
		echo '<script>window.location.href = "..?error=1";</script>';
		die();
	}
	/*---------------- Connect to DB -----------------*/
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

	$reponse = $bdd->query('SELECT * FROM panel');

	while ($donnees = $reponse->fetch())
	{
		if($donnees['UserName'] != $USERNAME || $donnees['Password'] != $PASSWORD) {
			echo '<script>window.location.href = "..?error=1";</script>';
			die();
		}else{
			// set variables
			$_SESSION['Connected'] = True;
		}
	}

	$reponse->closeCursor(); // Termine le traitement de la requête

	echo '<script>window.location.href = "../Panel/Clients.php";</script>';
?>