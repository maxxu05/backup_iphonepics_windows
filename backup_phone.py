import os
from tqdm import tqdm
import time

start = time.time()

#################################################################
# Checks which iPhone Photos are not already in D:/Photos
#################################################################

os.chdir("D:/Photos")
filenames = set([f for (dirpath, dirnames, filenames) in os.walk(".") for f in filenames])
# import pdb; pdb.set_trace()

#################################################################


# https://stackoverflow.com/questions/27593315/how-can-i-iterate-across-the-photos-on-my-connected-iphone-from-windows-7-in-pyt
from win32com.shell import shell, shellcon
import pythoncom

# get the PIDL of source file and the ShellObject of the folder in which source file is
# and the PIDL of the folder

desktop = shell.SHGetDesktopFolder()

#################################################################
# Missing photos are copied to Destination Folder of "This PC\Data (D:)\Photos\temp"
#################################################################

for pidl in desktop:
    if desktop.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "This PC":
        pidl_dst = pidl
        break
dstFolder = desktop.BindToObject(pidl_dst, None, shell.IID_IShellFolder)
for pidl in dstFolder:
    if dstFolder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "DATA (D:)":
        pidl_dst = pidl
        break
dstFolder = dstFolder.BindToObject(pidl_dst, None, shell.IID_IShellFolder)
for pidl in dstFolder:
    if dstFolder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "Photos":
        pidl_dst = pidl
        break
dstFolder = dstFolder.BindToObject(pidl_dst, None, shell.IID_IShellFolder)
for pidl in dstFolder:
    if dstFolder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "temp":
        pidl_dst = pidl
        break
dstFolder = dstFolder.BindToObject(pidl_dst, None, shell.IID_IShellFolder)
didl = shell.SHGetIDListFromObject(dstFolder) #Grab the PIDL from the folder object
dst = shell.SHCreateItemFromIDList(didl)

#################################################################
# Constructing Source Folder of iPhone photos
#################################################################

# Source folder
for pidl in desktop:
    # print(desktop.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL))
    if desktop.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "This PC":
        pidl_get = pidl
        break
folder = desktop.BindToObject(pidl_get, None, shell.IID_IShellFolder)

for pidl in folder:
    # print(folder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL))
    if folder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "Apple iPhone":
        pidl_get = pidl
        break
folder = folder.BindToObject(pidl_get, None, shell.IID_IShellFolder)

for pidl in folder:
    if folder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "Internal Storage":
        pidl_get = pidl
        break
folder = folder.BindToObject(pidl_get, None, shell.IID_IShellFolder)

for pidl in folder:
    if folder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL) == "DCIM":
        pidl_get = pidl
        break
folder = folder.BindToObject(pidl_get, None, shell.IID_IShellFolder)

#################################################################
# Iterating Through Each iPhone photo folder and photo
#################################################################

newfiles = 0
for pidl in tqdm(folder, desc="Folder"): # for each folder inside DCIM
    # print(folder.GetDisplayNameOf(pidl, shellcon.SHGDN_NORMAL))
    pidl_get = pidl
    folderPIDL = pidl_get
    folder = folder.BindToObject(pidl_get, None, shell.IID_IShellFolder)

    for pidl_img in (pbar := tqdm(folder, desc="Files", leave=False)): 
        end = time.time()
        pbar.set_description(f"Total New Files {newfiles}, Min Elapsed {int((end-start)//60)}")

        imgPIDL = pidl_img
        filename = folder.GetDisplayNameOf(pidl_img, shellcon.SHGDN_NORMAL)

        if filename not in filenames:
            # import pdb; pdb.set_trace()
            newfiles += 1
            
            while not os.path.exists(f"D:/Photos/temp/{filename}"):
                fidl = shell.SHGetIDListFromObject(folder) #Grab the PIDL from the folder object
                
                si = shell.SHCreateShellItem(fidl, None, imgPIDL) #Create a ShellItem of the source file
                
                #Python IFileOperation
                pfo = pythoncom.CoCreateInstance(shell.CLSID_FileOperation,None,pythoncom.CLSCTX_ALL,shell.IID_IFileOperation)
                pfo.SetOperationFlags(shellcon.FOF_NOCONFIRMATION)
                pfo.CopyItem(si, dst, filename) # Schedule an operation to be performed

                success = pfo.PerformOperations() #perform operation

print(f"Total New Files {newfiles}, Min Elapsed {(end-start)//60}")