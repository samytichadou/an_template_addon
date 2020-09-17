import bpy
import smtplib 
import os
import platform
import addon_utils

from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders


from .print_functions import print_and_report
from .json_functions import create_json_file
from .global_variables import submission_mail_subject
from .addon_prefs import get_addon_preferences
from .internet_functions import is_connected
from .op_create_manifest import generate_hash, get_separated_tags, get_global_k
from .lib_enc1 import dec_k
from .lib_enc2 import dec


# get AN version
def get_addon_version(addon_name):

    for addon in addon_utils.modules():

        if addon.bl_info['name'] == addon_name:
            addon_version = ""

            for n in addon.bl_info.get('version', (-1,-1,-1)):
                addon_version += str(n) + "."

            addon_version = addon_version[:-1]
            return addon_version

    return None


# get os
def get_os():
    return platform.system() + " " + platform.release()
   

# format message
def format_message_submission(context):

    properties_coll = context.window_manager.an_templates_properties

    body = ""
    body += "Nodetree Name :\n%s\n\n" % properties_coll.submission_nodetree
    body += "Nodetree Tags :\n%s\n\n" % properties_coll.submission_tags
    body += "Nodetree Category :\n%s\n\n" % properties_coll.submission_category
    body += "Nodetree Small Description :\n%s\n\n" % properties_coll.submission_small_description

    if properties_coll.submission_video_preview_url:
        body += "Nodetree Video URL :\n%s\n\n" % properties_coll.submission_video_preview_url

    body += "Author Name :\n%s\n\n" % properties_coll.submission_author_name
    body += "Author Mail :\n%s\n\n" % properties_coll.submission_author_mail
    body += "Blender Version:\n%s\n\n" % bpy.app.version_string

    an_version = get_addon_version("Animation Nodes")
    if an_version is not None:
        body += "Animation Nodes Version:\n%s\n\n" % an_version

    body += "Platform:\n%s\n\n" % get_os()

    if properties_coll.submission_side_notes:
        body += "Side Notes :\n%s\n\n" % properties_coll.submission_side_notes

    body += "\n"
    body += "Readme :\n\n"

    for l in properties_coll.submission_readme.lines:
        body += "%s\n" % l.body

    subject = submission_mail_subject + properties_coll.submission_nodetree + " - from " + properties_coll.submission_author_name
    
    return body, subject


# get screenshot
def get_screenshot(context):

    properties_coll = context.window_manager.an_templates_properties

    screenshot_filepath = os.path.join(get_addon_preferences().download_folder, properties_coll.submission_nodetree + "_preview.png")

    bpy.ops.screen.screenshot(filepath=screenshot_filepath, hide_props_region=True, check_existing=False, full=True)

    return screenshot_filepath


# create submission json
def create_submission_json(context):

    properties_coll = context.window_manager.an_templates_properties

    json_filepath = os.path.join(get_addon_preferences().download_folder, properties_coll.submission_nodetree + "_infos.json")

    # create dataset
    datas = {}

    datas["name"] =                 properties_coll.submission_nodetree
    datas["description"] =          properties_coll.submission_small_description
    datas["blender_version"] =      bpy.app.version_string
    datas["an_version"] =           get_addon_version("Animation Nodes")
    datas["tags"] =                 properties_coll.submission_tags
    datas["image_preview_url"] =    ""
    if properties_coll.submission_video_preview_url:
        video = properties_coll.submission_video_preview_url
    else:
        video = ""
    datas["video_preview_url"] =    video
    datas["file_url"] =             ""
    datas["readme_url"] =           ""
    datas["hash"] =                 generate_hash(10)

    print_and_report(None, "Creating Nodetree Info File", "INFO") #debug

    create_json_file(datas, json_filepath)

    print_and_report(None, "Nodetree Info File Successfully Created : %s" % json_filepath, "INFO") #debug

    return json_filepath


# send email
def send_email_submission(self, body, subject, filepath_list, author_mail):

    fromaddr = toaddr = "animationnodes.templates@gmail.com"
    
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
    
    # storing the senders email address   
    msg['From'] = fromaddr
    
    # storing the receivers email address  
    msg['To'] = toaddr

    # put author in copy
    msg['Cc'] = author_mail
    
    # storing the subject  
    msg['Subject'] = subject
    
    # string to store the body of the mail 
    #body = "this is a test2"
    
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 

    # attach list of files
    for filepath in filepath_list:
    
        # open the file to be sent  
        filename = os.path.basename(filepath)
        attachment = open(filepath, "rb")
        
        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 
        
        # To change the payload into encoded form 
        p.set_payload((attachment).read()) 
        
        # encode into base64 
        encoders.encode_base64(p) 
        
        p.add_header('Content-Disposition', "attachment", filename=filename) 
        
        # attach the instance 'p' to instance 'msg' 
        msg.attach(p) 
    
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security 
    s.starttls()
    
    # Authentication
    k, w, v = get_global_k()
    s.login(fromaddr, dec_k(dec(k), w))

    # Converts the Multipart msg into a string 
    text = msg.as_string() 
    
    # create mailing list
    addrs_list = [toaddr, author_mail]

    # sending the mail
    s.sendmail(fromaddr, addrs_list, text)
    
    # terminating the session 
    s.quit() 


# add category to submission tags
def add_category_to_submission_tags(context):

    properties_coll = context.window_manager.an_templates_properties

    if properties_coll.submission_category.lower() not in get_separated_tags(properties_coll.submission_tags):
        if not properties_coll.submission_tags.strip().endswith(","):
            properties_coll.submission_tags += ","
        properties_coll.submission_tags += properties_coll.submission_category.lower()


# check attachments size
def check_attachment_size(file_list):
    total_size = 0
    for f in file_list:
        total_size += os.path.getsize(f)

    if total_size > 25000000:
        return True

    else:
        return False


# Submission
class ANTEMPLATES_OT_submit_template(bpy.types.Operator):
    """Submit Opened Blend File as Template for the Library, File has to be Saved"""
    bl_idname = "antemplates.submit_template"
    bl_label = "Submit Template"
    bl_options = {'REGISTER', 'INTERNAL'}


    @classmethod
    def poll(cls, context):
        #return True
        if bpy.data.is_saved:
            if not get_addon_preferences().custom_library:
                properties_coll = context.window_manager.an_templates_properties
                if properties_coll.submission_nodetree != "CHOOSE_NODETREE":
                    if properties_coll.submission_readme:
                        if properties_coll.submission_tags:
                            if properties_coll.submission_category:
                                if properties_coll.submission_small_description:
                                    if properties_coll.submission_author_mail:
                                        if properties_coll.submission_author_name:
                                            return True


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):

        layout = self.layout

        layout.label(text="You are about to submit a new template.", icon="QUESTION")
        col = layout.column(align=True)
        col.label(text="This blend file will be saved.")
        col.label(text="A screenshot of blender may be taken for preview.")
        col.label(text="A copy of the submission will be sent to you by mail.")
        col.label(text="Please check all needed informations are complete.")
        layout.label(text="Continue ?")


    def execute(self, context):

        # check internet connection
        if not is_connected:
            print_and_report(self, "No Internet Connection", "WARNING") #debug
            return {"FINISHED"}

        # save
        print_and_report(None, "Saving Blend File", "INFO") #debug
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)

        # add category tag if needed
        add_category_to_submission_tags(context)

        # format body and get subject
        print_and_report(None, "Formatting Submission Text", "INFO") #debug
        body, subject = format_message_submission(context)

        print_and_report(None, "Creating Additional Submission Files", "INFO") #debug

        # screenshot
        properties_coll = context.window_manager.an_templates_properties
        if properties_coll.submission_image_preview_url:
            screenshot_filepath = bpy.path.abspath(properties_coll.submission_image_preview_url)
        else:
            screenshot_filepath = get_screenshot(context)

        # json
        json_filepath = create_submission_json(context)

        # check for size
        files_to_send = [bpy.data.filepath, screenshot_filepath, json_filepath]
        if check_attachment_size(files_to_send):
            # remove temporary files
            if not properties_coll.submission_image_preview_url:
                os.remove(screenshot_filepath)
            os.remove(json_filepath)

            print_and_report(self, "Attachment Files too Large for Submission, Please try to keep it under 25MB", "WARNING") #debug

            return {'FINISHED'}

        # send email
        print_and_report(None, "Sending Submission - Please Wait", "INFO") #debug
        send_email_submission(self, body, subject, files_to_send, context.window_manager.an_templates_properties.submission_author_mail)

        # remove temporary files
        print_and_report(None, "Removing Additional Submission Files", "INFO") #debug
        if not properties_coll.submission_image_preview_url:
            os.remove(screenshot_filepath)
        os.remove(json_filepath)

        print_and_report(self, "Submission Successfully Sent", "INFO") #debug

        return {'FINISHED'}