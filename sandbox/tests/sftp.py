import pysftp

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

with pysftp.Connection('sftp.hidrive.ionos.com', username='douglas', password='dFxcPVHj675faZR', cnopts=cnopts) as sftp:
    with sftp.cd('users/douglas/raspiImages'):             # temporarily chdir to public
        sftp.put('./uploads/testUploadFile.txt')  # upload file to public/ on remote
        sftp.put('./uploads/testPdf.pdf')  # upload file to public/ on remote