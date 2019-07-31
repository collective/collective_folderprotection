*** Settings ***

Library  Selenium2Library  timeout=5 seconds  implicit_wait=0.5 seconds
Resource  keywords.robot
Variables  plone/app/testing/interfaces.py

Suite Setup  Start browser
Suite Teardown  Close All Browsers

*** Variables ***

${BROWSER} =  headlessfirefox

*** Test Cases ***

Manager should be able to access the 'Assign password' view
    Go to homepage
    Log In As Site Owner
    Create Protected Folder  Protected
    Custom Log out
    Log In As Manager User
    Go to   ${protected_folder_url}
    Page Should Contain  Assign password
    Click Link  link=Assign password
    Page Should Contain  Choose a password to protect this object and, if it is a folder, its children.

Manager should be allowed to access protected folder
    Go to homepage
    Log In As Site Owner
    Create Protected Folder  Protected
    Click Link  link=Assign password
    Input Text  css=input#form-widgets-passw_hash  thepassword
    Click Button  Save
    Custom Log out
    Log In As Manager User
    Go to   ${protected_folder_url}
    Page Should Not Contain  This resource is password protected

Manager should not see the 'Assign password' view for a non protected folder
    Go to homepage
    Log In As Site Owner
    Create Not Protected Folder  Not-Protected
    Go to   ${not_protected_folder_url}
    Page Should Not Contain  Assign password
    Custom Log out
    Log In As Manager User
    Go to   ${not_protected_folder_url}
    Page Should Not Contain  Assign password

Manager should not be able to remove contents from protected folder
    Go to homepage
    Log In As Site Owner
    Create Protected Folder  Protected
    Go to   ${protected_folder_url}
    Create Page  A Page  This is an internal page
    Go to   ${internal_protected}
    Custom Remove Content
    Go to   ${internal_protected}
    Page Should Not Contain  This page does not seem to exist
    Custom Log out
    Log In As Manager User
    Go to   ${internal_protected}
    Custom Remove Content
    Go to   ${internal_protected}
    Page Should Not Contain  This page does not seem to exist
    
Manager should be able to remove not protected folder
    Go to homepage
    Log In As Site Owner
    Create Not Protected Folder  Not-Protected
    Go to   ${not_protected_folder_url}
    Create Page  A Page  This is an internal page
    Go to   ${internal_not_protected}
    Custom Remove Content
    Go to   ${internal_not_protected}
    Page Should Contain  This page does not seem to exist
    Go to   ${not_protected_folder_url}
    Create Page  A Page  This is an internal page
    Custom Log out
    Log In As Manager User
    Go to   ${internal_not_protected}
    Custom Remove Content
    Go to   ${internal_not_protected}
    Page Should Contain  This page does not seem to exist

Manager should not be able to rename content inside protected folder
    Go to homepage
    Log In As Site Owner
    Create Protected Folder  Protected
    Go to   ${protected_folder_url}
    Create Page  A Page  This is an internal page
    Go to   ${internal_protected}
    Rename Content  a-page  new-page  New Page
    Page Should Contain  Insufficient Privileges
    Custom Log out
    Log In As Manager User
    Go to   ${internal_protected}
    Rename Content  a-page  new-page  New Page
    Page Should Contain  Insufficient Privileges

Manager should be able to rename content inside not protected folder
    Go to homepage
    Log In As Site Owner
    Create Not Protected Folder  Not-Protected
    Go to   ${not_protected_folder_url}
    Create Page  A Page  This is an internal page
    Go to   ${internal_not_protected}
    Rename Content  a-page  new-page  New Page
    Go to   ${internal_not_protected}
    ${BASE}=  Get Element Attribute  tag=body   data-base-url
    Should Be Equal  ${BASE}  ${not_protected_folder_url}/new-page
    Page Should Contain  New Page
    Custom Log out
    Log In As Manager User
    Go to   ${not_protected_folder_url}/new-page
    Rename Content  new-page  a-page  A Page
    Go to   ${internal_not_protected}
    Page Should Not Contain  This page does not seem to exist
